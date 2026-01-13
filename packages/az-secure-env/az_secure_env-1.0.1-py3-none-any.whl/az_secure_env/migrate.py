from azure.keyvault.secrets import SecretClient
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.mgmt.web import WebSiteManagementClient
from azure.mgmt.web.models import StringDictionary
from az_secure_env.azure_auth import get_credential
from az_secure_env.permissions import find_keyvault, grant_keyvault_access
from az_secure_env.appservice import enable_managed_identity, sync_keyvault_references, restart_app
from rich.console import Console
import time
import re

console = Console()


def sanitize_secret_name(name):
    """Convert setting name to valid Key Vault secret name
    
    Key Vault secret names can only contain alphanumeric characters and hyphens
    """
    # Replace underscores and other characters with hyphens
    sanitized = re.sub(r'[^a-zA-Z0-9-]', '-', name)
    # Remove consecutive hyphens
    sanitized = re.sub(r'-+', '-', sanitized)
    # Remove leading/trailing hyphens
    sanitized = sanitized.strip('-')
    return sanitized


def migrate_settings_to_keyvault(selected_settings, vault_name, subscription, resource_group, app_name, app_info):
    """Migrate selected settings to Key Vault
    
    Returns: (overall_success, list_of_results)
    """
    results = []
    credential = get_credential()
    
    # Step 1: Verify Key Vault exists
    console.print(f"[dim]Verifying Key Vault '{vault_name}'...[/dim]")
    vault = find_keyvault(vault_name, subscription)
    
    if not vault:
        results.append({
            'success': False,
            'message': f"Key Vault '{vault_name}' not found in subscription"
        })
        return False, results
    
    vault_url = f"https://{vault_name}.vault.azure.net"
    results.append({
        'success': True,
        'message': f"Found Key Vault '{vault_name}'"
    })
    
    # Step 2: Ensure managed identity is enabled
    principal_id = app_info.get('principal_id')
    
    if not principal_id:
        console.print(f"[dim]Enabling managed identity on '{app_name}'...[/dim]")
        success, new_principal_id, message = enable_managed_identity(subscription, resource_group, app_name)
        
        if success:
            principal_id = new_principal_id
            results.append({'success': True, 'message': message})
            # Wait for identity propagation
            console.print("  [dim]Waiting for identity to propagate...[/dim]")
            time.sleep(10)
        else:
            results.append({'success': False, 'message': message})
            return False, results
    
    # Step 3: Grant Key Vault access to the app
    console.print(f"[dim]Granting Key Vault access to '{app_name}'...[/dim]")
    success, message = grant_keyvault_access(vault_name, principal_id, subscription, app_name)
    results.append({'success': success, 'message': message})
    
    if not success:
        return False, results
    
    # Wait a bit for permissions to propagate
    console.print("  [dim]Waiting for permissions to propagate...[/dim]")
    time.sleep(5)
    
    # Step 4: Create secrets in Key Vault
    console.print(f"[dim]Creating secrets in Key Vault...[/dim]")
    secret_client = SecretClient(vault_url=vault_url, credential=credential)
    
    secret_mappings = {}  # Maps original setting name to Key Vault reference
    
    for setting_name, setting_value in selected_settings.items():
        try:
            # Sanitize components
            sanitized_app = sanitize_secret_name(app_name)
            sanitized_rg = sanitize_secret_name(resource_group)
            sanitized_setting = sanitize_secret_name(setting_name)
            
            # Create secret name in format: <appname>-<rgname>-<secretname>
            secret_name = f"{sanitized_app}-{sanitized_rg}-{sanitized_setting}"
            
            # Create or update the secret
            secret_client.set_secret(secret_name, setting_value)
            
            # Create Key Vault reference
            kv_reference = f"@Microsoft.KeyVault(SecretUri=https://{vault_name}.vault.azure.net/secrets/{secret_name})"
            secret_mappings[setting_name] = kv_reference
            
            results.append({
                'success': True,
                'message': f"Created secret '{secret_name}' for setting '{setting_name}'"
            })
        except Exception as e:
            results.append({
                'success': False,
                'message': f"Failed to create secret for '{setting_name}': {str(e)}"
            })
    
    if not secret_mappings:
        results.append({
            'success': False,
            'message': "No secrets were created successfully"
        })
        return False, results
    
    # Step 5: Update app settings with Key Vault references
    console.print(f"[dim]Updating app settings with Key Vault references...[/dim]")
    
    try:
        client = WebSiteManagementClient(credential, subscription)
        
        # Get current settings
        current_settings = client.web_apps.list_application_settings(resource_group, app_name)
        
        # Update with Key Vault references
        updated_properties = dict(current_settings.properties)
        for setting_name, kv_reference in secret_mappings.items():
            updated_properties[setting_name] = kv_reference
        
        # Apply updated settings
        settings_dict = StringDictionary(properties=updated_properties)
        client.web_apps.update_application_settings(
            resource_group_name=resource_group,
            name=app_name,
            app_settings=settings_dict
        )
        
        results.append({
            'success': True,
            'message': f"Updated {len(secret_mappings)} app setting(s) with Key Vault references"
        })
    except Exception as e:
        results.append({
            'success': False,
            'message': f"Failed to update app settings: {str(e)}"
        })
        return False, results
    
    # Step 6: Sync Key Vault references
    console.print(f"[dim]Syncing Key Vault references...[/dim]")
    success, message = sync_keyvault_references(subscription, resource_group, app_name)
    results.append({'success': success, 'message': message})
    
    # Step 7: Restart the app
    console.print(f"[dim]Restarting app...[/dim]")
    success, message = restart_app(subscription, resource_group, app_name)
    results.append({'success': success, 'message': message})
    
    return True, results
