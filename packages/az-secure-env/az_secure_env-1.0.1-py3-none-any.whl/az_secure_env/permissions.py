from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.mgmt.keyvault.models import AccessPolicyEntry, Permissions, SecretPermissions
from azure.mgmt.authorization import AuthorizationManagementClient
from azure.mgmt.authorization.models import RoleAssignmentCreateParameters
from az_secure_env.azure_auth import get_credential
import uuid


def find_keyvault(vault_name, subscription_id):
    """Find a Key Vault by name in the subscription"""
    credential = get_credential()
    kv_client = KeyVaultManagementClient(credential, subscription_id)
    
    for vault in kv_client.vaults.list_by_subscription():
        if vault.name.lower() == vault_name.lower():
            return vault
    
    return None


def grant_keyvault_access(vault_name, principal_id, subscription_id, app_name):
    """Grant the app's managed identity access to the Key Vault
    
    Returns: (success, message)
    """
    credential = get_credential()
    
    # Find the vault
    vault = find_keyvault(vault_name, subscription_id)
    if not vault:
        return False, f"Key Vault '{vault_name}' not found in subscription"
    
    # Extract resource group from vault ID
    # Format: /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.KeyVault/vaults/{name}
    vault_parts = vault.id.split('/')
    resource_group = vault_parts[4]
    
    kv_client = KeyVaultManagementClient(credential, subscription_id)
    
    # Check if RBAC is enabled
    if vault.properties.enable_rbac_authorization:
        # Use RBAC - assign "Key Vault Secrets User" role
        return _grant_rbac_access(vault, principal_id, subscription_id, app_name)
    else:
        # Use Access Policies
        return _grant_access_policy(vault, principal_id, resource_group, subscription_id, kv_client, app_name)


def _grant_rbac_access(vault, principal_id, subscription_id, app_name):
    """Grant RBAC access to Key Vault"""
    credential = get_credential()
    auth_client = AuthorizationManagementClient(credential, subscription_id)
    
    # Key Vault Secrets User role ID (built-in Azure role)
    role_id = "4633458b-17de-408a-b874-0445c86b69e6"
    role_definition_id = f"{vault.id}/providers/Microsoft.Authorization/roleDefinitions/{role_id}"
    
    # Check if assignment already exists
    for assignment in auth_client.role_assignments.list_for_scope(vault.id):
        if assignment.principal_id == principal_id:
            role_def_id = assignment.role_definition_id.split('/')[-1]
            if role_def_id == role_id:
                return True, f"✓ '{app_name}' already has 'Key Vault Secrets User' role on '{vault.name}'"
    
    # Create the role assignment
    try:
        assignment_name = str(uuid.uuid4())
        parameters = RoleAssignmentCreateParameters(
            role_definition_id=role_definition_id,
            principal_id=principal_id,
            principal_type="ServicePrincipal"  # Managed identity is a ServicePrincipal
        )
        
        auth_client.role_assignments.create(
            scope=vault.id,
            role_assignment_name=assignment_name,
            parameters=parameters
        )
        
        return True, f"✓ Granted 'Key Vault Secrets User' role to '{app_name}' on Key Vault '{vault.name}'"
    
    except Exception as e:
        error_msg = str(e)
        if "already exists" in error_msg.lower():
            return True, f"✓ '{app_name}' already has access to '{vault.name}'"
        return False, f"Failed to grant RBAC access: {error_msg}"


def _grant_access_policy(vault, principal_id, resource_group, subscription_id, kv_client, app_name):
    """Grant access policy to Key Vault"""
    
    # Check if access policy already exists
    if vault.properties.access_policies:
        for policy in vault.properties.access_policies:
            if policy.object_id == principal_id:
                if policy.permissions and policy.permissions.secrets:
                    if 'get' in [p.lower() for p in policy.permissions.secrets]:
                        return True, f"✓ '{app_name}' already has access policy on '{vault.name}'"
    
    # Create new access policy
    try:
        new_policy = AccessPolicyEntry(
            tenant_id=vault.properties.tenant_id,
            object_id=principal_id,
            permissions=Permissions(
                secrets=[SecretPermissions.GET, SecretPermissions.LIST]
            )
        )
        
        # Get existing policies
        existing_policies = list(vault.properties.access_policies) if vault.properties.access_policies else []
        existing_policies.append(new_policy)
        
        # Update the vault with new policies
        from azure.mgmt.keyvault.models import VaultAccessPolicyParameters, VaultAccessPolicyProperties
        
        parameters = VaultAccessPolicyParameters(
            properties=VaultAccessPolicyProperties(
                access_policies=existing_policies
            )
        )
        
        kv_client.vaults.update_access_policy(
            resource_group_name=resource_group,
            vault_name=vault.name,
            operation_kind='add',
            parameters=parameters
        )
        
        return True, f"✓ Granted access policy (Get, List secrets) to '{app_name}' on Key Vault '{vault.name}'"
    
    except Exception as e:
        return False, f"Failed to grant access policy: {str(e)}"


def fix_all_keyvault_references(settings, principal_id, subscription_id, app_name):
    """Fix all Key Vault references by granting necessary permissions
    
    Returns: list of (vault_name, success, message) tuples
    """
    from az_secure_env.keyvault import parse_keyvault_reference
    
    results = []
    processed_vaults = set()
    
    for key, value in settings.items():
        if value and "@Microsoft.KeyVault" in value:
            vault_name, secret_name = parse_keyvault_reference(value)
            
            if vault_name and vault_name not in processed_vaults:
                processed_vaults.add(vault_name)
                success, message = grant_keyvault_access(vault_name, principal_id, subscription_id, app_name)
                results.append((vault_name, success, message))
    
    return results
