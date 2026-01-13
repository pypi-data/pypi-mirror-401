from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.web import WebSiteManagementClient
from az_secure_env.azure_auth import get_credential
from rich.console import Console
from rich.table import Table

console = Console()


def list_resource_groups(subscription):
    """List all resource groups in the subscription
    
    Returns: list of resource group names
    """
    credential = get_credential()
    resource_client = ResourceManagementClient(credential, subscription)
    
    resource_groups = []
    for rg in resource_client.resource_groups.list():
        resource_groups.append(rg.name)
    
    return sorted(resource_groups)


def list_apps_in_resource_group(subscription, resource_group):
    """List all App Services and Function Apps in a resource group
    
    Returns: list of dicts with 'name' and 'type' keys
    """
    credential = get_credential()
    web_client = WebSiteManagementClient(credential, subscription)
    
    apps = []
    
    try:
        for app in web_client.web_apps.list_by_resource_group(resource_group):
            app_kind = app.kind or ""
            if "functionapp" in app_kind.lower():
                app_type = "Function App"
            else:
                app_type = "App Service"
            
            apps.append({
                'name': app.name,
                'type': app_type,
                'kind': app.kind,
                'location': app.location
            })
    except Exception as e:
        console.print(f"[red]Error listing apps: {e}[/red]")
    
    return sorted(apps, key=lambda x: x['name'])


def display_resource_groups(resource_groups):
    """Display resource groups in a table
    
    Returns: Table object
    """
    table = Table(title="Resource Groups")
    table.add_column("No.", style="cyan", width=4)
    table.add_column("Resource Group Name", style="magenta")
    
    for idx, rg in enumerate(resource_groups, 1):
        table.add_row(str(idx), rg)
    
    return table


def display_apps(apps):
    """Display apps in a table
    
    Returns: Table object
    """
    table = Table(title="App Services & Function Apps")
    table.add_column("No.", style="cyan", width=4)
    table.add_column("Name", style="magenta")
    table.add_column("Type", style="green")
    table.add_column("Location", style="blue")
    
    for idx, app in enumerate(apps, 1):
        table.add_row(str(idx), app['name'], app['type'], app['location'])
    
    return table
