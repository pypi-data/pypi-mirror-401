from azure.mgmt.web import WebSiteManagementClient
from azure.mgmt.web.models import ManagedServiceIdentity, ManagedServiceIdentityType
from az_secure_env.azure_auth import get_credential

def fetch_app_settings(subscription, resource_group, app_name):
    client = WebSiteManagementClient(
        credential=get_credential(),
        subscription_id=subscription
    )

    settings = client.web_apps.list_application_settings(
        resource_group,
        app_name
    )

    return settings.properties or {}

def get_app_info(subscription, resource_group, app_name):
    """Get app information including type (Function App vs App Service)"""
    client = WebSiteManagementClient(
        credential=get_credential(),
        subscription_id=subscription
    )
    
    app = client.web_apps.get(resource_group, app_name)
    
    # Determine app type based on kind property
    app_kind = app.kind or ""
    if "functionapp" in app_kind.lower():
        app_type = "Function App"
    else:
        app_type = "App Service"
    
    # Get managed identity principal ID
    principal_id = None
    if app.identity and app.identity.principal_id:
        principal_id = app.identity.principal_id
    
    return {
        "name": app.name,
        "type": app_type,
        "location": app.location,
        "kind": app.kind,
        "principal_id": principal_id
    }

def enable_managed_identity(subscription, resource_group, app_name):
    """Enable system-assigned managed identity on the app
    
    Returns: (success, principal_id, message)
    """
    client = WebSiteManagementClient(
        credential=get_credential(),
        subscription_id=subscription
    )
    
    try:
        # Get current app
        app = client.web_apps.get(resource_group, app_name)
        
        # Check if already enabled
        if app.identity and app.identity.principal_id:
            return True, app.identity.principal_id, f"System-assigned identity already enabled"
        
        # Enable system-assigned managed identity
        identity = ManagedServiceIdentity(
            type=ManagedServiceIdentityType.SYSTEM_ASSIGNED
        )
        
        app.identity = identity
        
        # Update the app - use begin_create_or_update which returns a poller
        poller = client.web_apps.begin_create_or_update(
            resource_group_name=resource_group,
            name=app_name,
            site_envelope=app
        )
        
        # Wait for the operation to complete
        updated_app = poller.result()
        
        if updated_app.identity and updated_app.identity.principal_id:
            return True, updated_app.identity.principal_id, f"✓ Enabled system-assigned managed identity"
        else:
            return False, None, "Failed to enable managed identity"
    
    except Exception as e:
        return False, None, f"Error enabling managed identity: {str(e)}"

def restart_app(subscription, resource_group, app_name):
    """Restart the app to pull fresh Key Vault references
    
    Returns: (success, message)
    """
    client = WebSiteManagementClient(
        credential=get_credential(),
        subscription_id=subscription
    )
    
    try:
        client.web_apps.restart(resource_group, app_name)
        return True, f"✓ Restarted '{app_name}' to pull fresh Key Vault references"
    except Exception as e:
        return False, f"Failed to restart app: {str(e)}"

def sync_keyvault_references(subscription, resource_group, app_name):
    """Force sync of Key Vault references by updating app settings
    
    Returns: (success, message)
    """
    client = WebSiteManagementClient(
        credential=get_credential(),
        subscription_id=subscription
    )
    
    try:
        # Get current settings
        current_settings = client.web_apps.list_application_settings(resource_group, app_name)
        
        # Re-apply the same settings to trigger Key Vault reference refresh
        from azure.mgmt.web.models import StringDictionary
        
        settings_dict = StringDictionary(properties=current_settings.properties)
        client.web_apps.update_application_settings(
            resource_group_name=resource_group,
            name=app_name,
            app_settings=settings_dict
        )
        
        return True, f"✓ Synced Key Vault references for '{app_name}'"
    except Exception as e:
        return False, f"Failed to sync Key Vault references: {str(e)}"
