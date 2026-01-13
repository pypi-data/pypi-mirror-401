from azure.keyvault.secrets import SecretClient
from azure.mgmt.web import WebSiteManagementClient
from azure.mgmt.web.models import StringDictionary
from az_secure_env.azure_auth import get_credential
from az_secure_env.permissions import find_keyvault, grant_keyvault_access
from az_secure_env.appservice import enable_managed_identity, sync_keyvault_references, restart_app
from az_secure_env.migrate import sanitize_secret_name
from rich.console import Console
import time

console = Console()


def add_environment_variable(name, value, secure, vault_name, subscription, resource_group, app_name, app_info):
    """Add a new environment variable to the app
    
    Args:
        name: Variable name
        value: Variable value
        secure: True to store in Key Vault, False for plain text
        vault_name: Key Vault name (required if secure=True)
        subscription: Azure subscription ID
        resource_group: Resource group name
        app_name: App Service/Function App name
        app_info: App information dict
    
    Returns: (overall_success, list_of_results)
    """
    results = []
    credential = get_credential()
    client = WebSiteManagementClient(credential, subscription)
    
    # Get current settings
    console.print(f"[dim]Fetching current settings...[/dim]")
    current_settings = client.web_apps.list_application_settings(resource_group, app_name)
    
    # Check if setting already exists
    if name in current_settings.properties:
        results.append({
            'success': False,
            'message': f"Environment variable '{name}' already exists. Use a different name or update it manually."
        })
        return False, results
    
    new_value = value
    
    if secure:
        # Store in Key Vault
        console.print(f"[dim]Storing '{name}' in Key Vault...[/dim]")
        
        # Step 1: Verify Key Vault exists
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
        
        # Step 3: Grant Key Vault access
        console.print(f"[dim]Ensuring Key Vault access for '{app_name}'...[/dim]")
        success, message = grant_keyvault_access(vault_name, principal_id, subscription, app_name)
        results.append({'success': success, 'message': message})
        
        if not success:
            return False, results
        
        # Wait for permissions to propagate
        time.sleep(3)
        
        # Step 4: Create secret in Key Vault
        try:
            secret_client = SecretClient(vault_url=vault_url, credential=credential)
            
            # Sanitize components for secret name
            sanitized_app = sanitize_secret_name(app_name)
            sanitized_rg = sanitize_secret_name(resource_group)
            sanitized_name = sanitize_secret_name(name)
            
            # Create secret name in format: <appname>-<rgname>-<secretname>
            secret_name = f"{sanitized_app}-{sanitized_rg}-{sanitized_name}"
            
            # Create the secret
            secret_client.set_secret(secret_name, value)
            
            # Create Key Vault reference
            new_value = f"@Microsoft.KeyVault(SecretUri=https://{vault_name}.vault.azure.net/secrets/{secret_name})"
            
            results.append({
                'success': True,
                'message': f"Created secret '{secret_name}' in Key Vault"
            })
        except Exception as e:
            results.append({
                'success': False,
                'message': f"Failed to create secret in Key Vault: {str(e)}"
            })
            return False, results
    else:
        # Plain text storage
        results.append({
            'success': True,
            'message': f"Storing '{name}' as plain text"
        })
    
    # Step 5: Add the setting to app
    console.print(f"[dim]Adding '{name}' to app settings...[/dim]")
    try:
        updated_properties = dict(current_settings.properties)
        updated_properties[name] = new_value
        
        settings_dict = StringDictionary(properties=updated_properties)
        client.web_apps.update_application_settings(
            resource_group_name=resource_group,
            name=app_name,
            app_settings=settings_dict
        )
        
        results.append({
            'success': True,
            'message': f"Added environment variable '{name}' to app settings"
        })
    except Exception as e:
        results.append({
            'success': False,
            'message': f"Failed to update app settings: {str(e)}"
        })
        return False, results
    
    # Step 6: Sync and restart if it's a Key Vault reference
    if secure:
        console.print(f"[dim]Syncing Key Vault references...[/dim]")
        success, message = sync_keyvault_references(subscription, resource_group, app_name)
        results.append({'success': success, 'message': message})
        
        console.print(f"[dim]Restarting app...[/dim]")
        success, message = restart_app(subscription, resource_group, app_name)
        results.append({'success': success, 'message': message})
    
    return True, results
