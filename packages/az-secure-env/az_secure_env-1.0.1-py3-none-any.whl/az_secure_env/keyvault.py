import re
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.mgmt.authorization import AuthorizationManagementClient
from az_secure_env.azure_auth import get_credential


def parse_keyvault_reference(reference):
    """Parse Key Vault reference to extract vault name and secret name
    
    Format: @Microsoft.KeyVault(SecretUri=https://vault-name.vault.azure.net/secrets/secret-name/version)
    or: @Microsoft.KeyVault(VaultName=vault-name;SecretName=secret-name)
    """
    if not reference or "@Microsoft.KeyVault" not in reference:
        return None, None
    
    # Try to extract from SecretUri format
    uri_match = re.search(r'SecretUri=https://([^.]+)\.vault\.azure\.net/secrets/([^/)]+)', reference)
    if uri_match:
        return uri_match.group(1), uri_match.group(2)
    
    # Try to extract from VaultName/SecretName format
    vault_match = re.search(r'VaultName=([^;)]+)', reference)
    secret_match = re.search(r'SecretName=([^;)]+)', reference)
    
    if vault_match and secret_match:
        return vault_match.group(1), secret_match.group(1)
    
    return None, None


def validate_keyvault_access(vault_name, secret_name, principal_id, subscription_id):
    """Validate if the app's managed identity can access the Key Vault secret
    
    Returns: (is_valid, error_message)
    """
    if not vault_name or not secret_name:
        return False, "Invalid Key Vault reference format"
    
    if not principal_id:
        return False, "No managed identity configured"
    
    try:
        credential = get_credential()
        
        # Get the Key Vault to find its resource group
        kv_client = KeyVaultManagementClient(credential, subscription_id)
        
        # List all vaults in subscription to find the one matching our name
        vault_resource_id = None
        vault_obj = None
        
        for vault in kv_client.vaults.list_by_subscription():
            if vault.name.lower() == vault_name.lower():
                vault_resource_id = vault.id
                vault_obj = vault
                break
        
        if not vault_resource_id:
            return False, f"Key Vault '{vault_name}' not found in subscription"
        
        # Check access policies (legacy)
        has_access = False
        if vault_obj.properties.access_policies:
            for policy in vault_obj.properties.access_policies:
                if policy.object_id == principal_id:
                    # Check if it has 'get' permission for secrets
                    if policy.permissions and policy.permissions.secrets:
                        if 'get' in [p.lower() for p in policy.permissions.secrets]:
                            has_access = True
                            break
        
        # Check RBAC assignments (modern approach)
        if not has_access and vault_obj.properties.enable_rbac_authorization:
            auth_client = AuthorizationManagementClient(credential, subscription_id)
            
            # Key Vault Secrets User role: 4633458b-17de-408a-b874-0445c86b69e6
            # Key Vault Reader role: 21090545-7ca7-4776-b22c-e363652d74d2
            required_roles = [
                '4633458b-17de-408a-b874-0445c86b69e6',  # Key Vault Secrets User
                '00482a5a-887f-4fb3-b8bf-3b45d0e1b7c4',  # Key Vault Secrets Officer
            ]
            
            # Check role assignments on the vault
            for assignment in auth_client.role_assignments.list_for_scope(vault_resource_id):
                if assignment.principal_id == principal_id:
                    # Extract role definition ID
                    role_def_id = assignment.role_definition_id.split('/')[-1]
                    if role_def_id in required_roles:
                        has_access = True
                        break
        
        if has_access:
            return True, None
        else:
            if vault_obj.properties.enable_rbac_authorization:
                return False, "App identity lacks RBAC role (needs 'Key Vault Secrets User')"
            else:
                return False, "App identity not in Key Vault access policies"
    
    except Exception as e:
        error_str = str(e)
        if "not found" in error_str.lower():
            return False, f"Key Vault '{vault_name}' not found"
        return False, f"Validation error: {error_str[:60]}"


def check_keyvault_reference(reference, principal_id, subscription_id):
    """Check if a Key Vault reference is valid and accessible
    
    Returns: (is_secure, is_validated, message)
    """
    vault_name, secret_name = parse_keyvault_reference(reference)
    
    if not vault_name or not secret_name:
        return True, False, "Invalid Key Vault reference format"
    
    is_valid, error_msg = validate_keyvault_access(vault_name, secret_name, principal_id, subscription_id)
    
    if is_valid:
        return True, True, None
    else:
        return True, False, error_msg
