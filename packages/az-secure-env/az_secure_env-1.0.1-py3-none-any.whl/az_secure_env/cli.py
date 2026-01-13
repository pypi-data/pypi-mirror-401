import typer
from az_secure_env.appservice import fetch_app_settings, get_app_info, enable_managed_identity, restart_app, sync_keyvault_references
from az_secure_env.keyvault import check_keyvault_reference
from az_secure_env.permissions import fix_all_keyvault_references
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table
import time

app = typer.Typer(help="Secure App Service & Function App settings")
console = Console()

@app.command()
def scan(
    subscription: str = typer.Option(..., help="Azure subscription ID"),
    resource_group: str = typer.Option(..., help="Resource group name"),
    app_name: str = typer.Option(..., help="App Service or Function App name"),
    fix: bool = typer.Option(False, "--fix", help="Automatically grant Key Vault access permissions")
):
    """Scan an App Service or Function App for settings"""
    
    # Get app info to determine type
    app_info = None
    try:
        app_info = get_app_info(subscription, resource_group, app_name)
        typer.echo(f"\n{'='*60}")
        typer.echo(f"App Name:     {app_info['name']}")
        typer.echo(f"Type:         {app_info['type']}")
        typer.echo(f"Location:     {app_info['location']}")
        if app_info.get('principal_id'):
            typer.echo(f"Identity:     Enabled (Principal ID: {app_info['principal_id'][:8]}...)")
        else:
            console.print(f"Identity:     [yellow]⚠ No managed identity configured[/yellow]")
        typer.echo(f"{'='*60}\n")
    except Exception as e:
        typer.echo(f"Error getting app info: {e}", err=True)
        typer.echo(f"\nProceeding with settings scan...\n")
    
    # Fetch settings
    settings = fetch_app_settings(subscription, resource_group, app_name)
    
    if not settings:
        typer.echo("No application settings found.")
        return
    
    principal_id = app_info.get('principal_id') if app_info else None
    permissions_granted = False
    
    # If --fix flag is set, grant permissions first
    if fix:
        # Enable managed identity if not present
        if not principal_id:
            console.print("[bold cyan]Enabling system-assigned managed identity...[/bold cyan]\n")
            success, new_principal_id, message = enable_managed_identity(subscription, resource_group, app_name)
            
            if success:
                console.print(f"  [green]{message}[/green]")
                principal_id = new_principal_id
                # Update app_info
                if app_info:
                    app_info['principal_id'] = principal_id
                    console.print(f"  [green]Principal ID: {principal_id[:8]}...[/green]\n")
                # Wait a moment for identity propagation
                console.print("  [dim]Waiting for identity to propagate...[/dim]")
                time.sleep(10)
                typer.echo()
            else:
                console.print(f"  [red]✗ {message}[/red]\n")
                console.print("[red]Cannot proceed with fixing Key Vault permissions without managed identity[/red]\n")
                # Still show the scan results
                principal_id = None
        
        if principal_id:
            console.print("[bold cyan]Fixing Key Vault permissions...[/bold cyan]\n")
            results = fix_all_keyvault_references(settings, principal_id, subscription, app_info['name'])
            
            if results:
                for vault_name, success, message in results:
                    if success:
                        console.print(f"  [green]{message}[/green]")
                        permissions_granted = True
                    else:
                        console.print(f"  [red]✗ {message}[/red]")
                typer.echo()
            else:
                typer.echo("  No Key Vault references found.\n")
            
            # Sync and restart app if permissions were granted
            if permissions_granted:
                console.print("[bold cyan]Syncing Key Vault references...[/bold cyan]\n")
                success, message = sync_keyvault_references(subscription, resource_group, app_name)
                if success:
                    console.print(f"  [green]{message}[/green]\n")
                else:
                    console.print(f"  [yellow]⚠ {message}[/yellow]\n")
                
                console.print("[bold cyan]Restarting app to apply changes...[/bold cyan]\n")
                success, message = restart_app(subscription, resource_group, app_name)
                if success:
                    console.print(f"  [green]{message}[/green]\n")
                else:
                    console.print(f"  [yellow]⚠ {message}[/yellow]\n")
    
    typer.echo(f"Application Settings ({len(settings)} total):\n")
    
    for k, v in settings.items():
        # Check if it's a Key Vault reference
        if v and "@Microsoft.KeyVault" in v:
            is_secure, is_validated, error_msg = check_keyvault_reference(v, principal_id, subscription)
            
            if is_validated:
                console.print(f"  {k:40} [green]{v}[/green] [green bold]✓ SECURE & VALIDATED[/green bold]")
            else:
                status_msg = f"⚠ SECURE BUT NOT VALIDATED"
                if error_msg:
                    status_msg += f" ({error_msg})"
                console.print(f"  {k:40} [yellow]{v}[/yellow] [yellow bold]{status_msg}[/yellow bold]")
        else:
            masked = "********" if v else ""
            typer.echo(f"  {k:40} {masked}")
    
    typer.echo()
    
    if permissions_granted:
        console.print("[green bold]✓ All fixes applied successfully! Key Vault references synced and app restarted.[/green bold]")
        console.print("[dim]Note: It may take a few moments for the app to fully restart and pull the Key Vault references.[/dim]\n")


@app.command()
def migrate(
    subscription: str = typer.Option(..., help="Azure subscription ID"),
    resource_group: str = typer.Option(..., help="Resource group name"),
    app_name: str = typer.Option(..., help="App Service or Function App name"),
    vault_name: str = typer.Option(None, help="Key Vault name (will prompt if not provided)")
):
    """Migrate environment variables to Key Vault references"""
    
    console.print("\n[bold cyan]═══ Environment Variable Migration to Key Vault ═══[/bold cyan]\n")
    
    # Get app info
    try:
        app_info = get_app_info(subscription, resource_group, app_name)
        console.print(f"[bold]App:[/bold] {app_info['name']} ({app_info['type']})")
        console.print(f"[bold]Location:[/bold] {app_info['location']}\n")
    except Exception as e:
        console.print(f"[red]Error getting app info: {e}[/red]")
        raise typer.Exit(1)
    
    # Fetch current settings
    settings = fetch_app_settings(subscription, resource_group, app_name)
    
    if not settings:
        console.print("[yellow]No application settings found.[/yellow]")
        raise typer.Exit(0)
    
    # Filter out settings that are already Key Vault references
    plain_settings = {k: v for k, v in settings.items() if v and "@Microsoft.KeyVault" not in v}
    
    if not plain_settings:
        console.print("[yellow]All settings are already using Key Vault references.[/yellow]")
        raise typer.Exit(0)
    
    # Display current settings in a table
    table = Table(title="Current Environment Variables (Plain Text)")
    table.add_column("No.", style="cyan", width=4)
    table.add_column("Setting Name", style="magenta")
    table.add_column("Value (Masked)", style="dim")
    
    setting_list = list(plain_settings.items())
    for idx, (key, value) in enumerate(setting_list, 1):
        table.add_row(str(idx), key, "********" if value else "")
    
    console.print(table)
    console.print()
    
    # Ask which settings to migrate
    console.print("[bold]Select settings to migrate to Key Vault:[/bold]")
    console.print("Enter numbers separated by commas (e.g., 1,3,4) or 'all' for all settings")
    selection = Prompt.ask("Selection", default="all")
    
    if selection.lower() == "all":
        selected_settings = plain_settings
    else:
        try:
            indices = [int(x.strip()) for x in selection.split(",")]
            selected_settings = {setting_list[i-1][0]: setting_list[i-1][1] for i in indices if 1 <= i <= len(setting_list)}
        except (ValueError, IndexError):
            console.print("[red]Invalid selection. Please try again.[/red]")
            raise typer.Exit(1)
    
    if not selected_settings:
        console.print("[yellow]No settings selected.[/yellow]")
        raise typer.Exit(0)
    
    console.print(f"\n[green]Selected {len(selected_settings)} setting(s) for migration:[/green]")
    for key in selected_settings.keys():
        console.print(f"  • {key}")
    console.print()
    
    # Ask for Key Vault name if not provided
    if not vault_name:
        vault_name = Prompt.ask("Enter Key Vault name")
    
    # Confirm migration
    if not Confirm.ask(f"\n[bold]Proceed with migrating {len(selected_settings)} setting(s) to Key Vault '{vault_name}'?[/bold]"):
        console.print("[yellow]Migration cancelled.[/yellow]")
        raise typer.Exit(0)
    
    console.print("\n[bold cyan]Starting migration...[/bold cyan]\n")
    
    # Import migration module (we'll create this)
    from az_secure_env.migrate import migrate_settings_to_keyvault
    
    success, results = migrate_settings_to_keyvault(
        selected_settings,
        vault_name,
        subscription,
        resource_group,
        app_name,
        app_info
    )
    
    # Display results
    console.print()
    for result in results:
        if result['success']:
            console.print(f"  [green]✓ {result['message']}[/green]")
        else:
            console.print(f"  [red]✗ {result['message']}[/red]")
    
    if success:
        console.print("\n[green bold]✓ Migration completed successfully![/green bold]\n")
    else:
        console.print("\n[yellow]⚠ Migration completed with some errors.[/yellow]\n")


@app.command()
def add(
    subscription: str = typer.Option(..., help="Azure subscription ID"),
    resource_group: str = typer.Option(..., help="Resource group name"),
    app_name: str = typer.Option(..., help="App Service or Function App name"),
    name: str = typer.Option(None, "--name", help="Environment variable name"),
    value: str = typer.Option(None, "--value", help="Environment variable value"),
    secure: bool = typer.Option(None, "--secure/--plain", help="Store in Key Vault (secure) or plain text"),
    vault_name: str = typer.Option(None, "--vault-name", help="Key Vault name (required if --secure)")
):
    """Add a new environment variable to the app"""
    
    console.print("\n[bold cyan]═══ Add Environment Variable ═══[/bold cyan]\n")
    
    # Get app info
    try:
        app_info = get_app_info(subscription, resource_group, app_name)
        console.print(f"[bold]App:[/bold] {app_info['name']} ({app_info['type']})")
        console.print(f"[bold]Location:[/bold] {app_info['location']}\n")
    except Exception as e:
        console.print(f"[red]Error getting app info: {e}[/red]")
        raise typer.Exit(1)
    
    # Prompt for name if not provided
    if not name:
        name = Prompt.ask("Enter environment variable name")
    
    # Prompt for value if not provided
    if not value:
        value = Prompt.ask("Enter environment variable value", password=True)
    
    # Prompt for secure storage if not specified
    if secure is None:
        secure = Confirm.ask("Store securely in Key Vault?", default=True)
    
    # If secure, need vault name
    if secure and not vault_name:
        vault_name = Prompt.ask("Enter Key Vault name")
    
    console.print(f"\n[bold]Summary:[/bold]")
    console.print(f"  Variable: {name}")
    console.print(f"  Storage:  {'Key Vault (' + vault_name + ')' if secure else 'Plain text'}")
    
    if not Confirm.ask("\n[bold]Proceed with adding this variable?[/bold]"):
        console.print("[yellow]Operation cancelled.[/yellow]")
        raise typer.Exit(0)
    
    console.print("\n[bold cyan]Adding environment variable...[/bold cyan]\n")
    
    from az_secure_env.add_env import add_environment_variable
    
    success, results = add_environment_variable(
        name,
        value,
        secure,
        vault_name,
        subscription,
        resource_group,
        app_name,
        app_info
    )
    
    # Display results
    console.print()
    for result in results:
        if result['success']:
            console.print(f"  [green]✓ {result['message']}[/green]")
        else:
            console.print(f"  [red]✗ {result['message']}[/red]")
    
    if success:
        console.print("\n[green bold]✓ Environment variable added successfully![/green bold]\n")
    else:
        console.print("\n[red]✗ Failed to add environment variable.[/red]\n")


@app.command()
def menu(
    subscription: str = typer.Option(..., help="Azure subscription ID")
):
    """Interactive menu to scan, migrate, or add environment variables"""
    
    from az_secure_env.menu_helpers import (
        list_resource_groups,
        list_apps_in_resource_group,
        display_resource_groups,
        display_apps
    )
    
    console.print("\n[bold cyan]═══ Azure Secure Environment - Interactive Menu ═══[/bold cyan]\n")
    
    # Step 1: Select action
    console.print("[bold]What would you like to do?[/bold]")
    console.print("  1. Scan - Audit app settings and validate Key Vault references")
    console.print("  2. Migrate - Move plain-text env vars to Key Vault")
    console.print("  3. Add - Add a new environment variable")
    console.print()
    
    action_choice = Prompt.ask("Select action", choices=["1", "2", "3"], default="1")
    
    action_map = {
        "1": "scan",
        "2": "migrate",
        "3": "add"
    }
    selected_action = action_map[action_choice]
    
    console.print(f"\n[green]Selected: {selected_action.upper()}[/green]\n")
    
    # Step 2: List and select resource group
    console.print("[dim]Fetching resource groups...[/dim]")
    resource_groups = list_resource_groups(subscription)
    
    if not resource_groups:
        console.print("[red]No resource groups found in subscription.[/red]")
        raise typer.Exit(1)
    
    console.print()
    rg_table = display_resource_groups(resource_groups)
    console.print(rg_table)
    console.print()
    
    rg_choice = Prompt.ask("Select resource group number", default="1")
    
    try:
        rg_index = int(rg_choice) - 1
        if rg_index < 0 or rg_index >= len(resource_groups):
            console.print("[red]Invalid selection.[/red]")
            raise typer.Exit(1)
        selected_rg = resource_groups[rg_index]
    except ValueError:
        console.print("[red]Invalid input.[/red]")
        raise typer.Exit(1)
    
    console.print(f"\n[green]Selected Resource Group: {selected_rg}[/green]\n")
    
    # Step 3: List and select app
    console.print("[dim]Fetching apps in resource group...[/dim]")
    apps = list_apps_in_resource_group(subscription, selected_rg)
    
    if not apps:
        console.print(f"[yellow]No App Services or Function Apps found in resource group '{selected_rg}'.[/yellow]")
        raise typer.Exit(0)
    
    console.print()
    app_table = display_apps(apps)
    console.print(app_table)
    console.print()
    
    app_choice = Prompt.ask("Select app number", default="1")
    
    try:
        app_index = int(app_choice) - 1
        if app_index < 0 or app_index >= len(apps):
            console.print("[red]Invalid selection.[/red]")
            raise typer.Exit(1)
        selected_app = apps[app_index]
    except ValueError:
        console.print("[red]Invalid input.[/red]")
        raise typer.Exit(1)
    
    console.print(f"\n[green]Selected App: {selected_app['name']} ({selected_app['type']})[/green]\n")
    
    # Step 4: Execute the selected action by calling the function directly
    if selected_action == "scan":
        fix = Confirm.ask("Do you want to automatically fix Key Vault permission issues?", default=False)
        console.print()
        
        # Call scan function directly
        _execute_scan(subscription, selected_rg, selected_app['name'], fix)
    
    elif selected_action == "migrate":
        # Call migrate function directly
        _execute_migrate(subscription, selected_rg, selected_app['name'], None)
    
    elif selected_action == "add":
        # Call add function directly
        _execute_add(subscription, selected_rg, selected_app['name'], None, None, None, None)


def _execute_scan(subscription, resource_group, app_name, fix):
    """Execute scan command"""    # Implementation moved from scan command
    app_info = None
    try:
        app_info = get_app_info(subscription, resource_group, app_name)
        typer.echo(f"\n{'='*60}")
        typer.echo(f"App Name:     {app_info['name']}")
        typer.echo(f"Type:         {app_info['type']}")
        typer.echo(f"Location:     {app_info['location']}")
        if app_info.get('principal_id'):
            typer.echo(f"Identity:     Enabled (Principal ID: {app_info['principal_id'][:8]}...)")
        else:
            console.print(f"Identity:     [yellow]⚠ No managed identity configured[/yellow]")
        typer.echo(f"{'='*60}\n")
    except Exception as e:
        typer.echo(f"Error getting app info: {e}", err=True)
        typer.echo(f"\nProceeding with settings scan...\n")
    
    settings = fetch_app_settings(subscription, resource_group, app_name)
    if not settings:
        typer.echo("No application settings found.")
        return
    
    principal_id = app_info.get('principal_id') if app_info else None
    permissions_granted = False
    
    if fix:
        if not principal_id:
            console.print("[bold cyan]Enabling system-assigned managed identity...[/bold cyan]\n")
            success, new_principal_id, message = enable_managed_identity(subscription, resource_group, app_name)
            if success:
                console.print(f"  [green]{message}[/green]")
                principal_id = new_principal_id
                if app_info:
                    app_info['principal_id'] = principal_id
                    console.print(f"  [green]Principal ID: {principal_id[:8]}...[/green]\n")
                console.print("  [dim]Waiting for identity to propagate...[/dim]")
                time.sleep(10)
                typer.echo()
            else:
                console.print(f"  [red]✗ {message}[/red]\n")
                console.print("[red]Cannot proceed with fixing Key Vault permissions without managed identity[/red]\n")
                principal_id = None
        
        if principal_id:
            console.print("[bold cyan]Fixing Key Vault permissions...[/bold cyan]\n")
            results = fix_all_keyvault_references(settings, principal_id, subscription, app_info['name'])
            if results:
                for vault_name, success, message in results:
                    if success:
                        console.print(f"  [green]{message}[/green]")
                        permissions_granted = True
                    else:
                        console.print(f"  [red]✗ {message}[/red]")
                typer.echo()
            else:
                typer.echo("  No Key Vault references found.\n")
            
            if permissions_granted:
                console.print("[bold cyan]Syncing Key Vault references...[/bold cyan]\n")
                success, message = sync_keyvault_references(subscription, resource_group, app_name)
                if success:
                    console.print(f"  [green]{message}[/green]\n")
                else:
                    console.print(f"  [yellow]⚠ {message}[/yellow]\n")
                
                console.print("[bold cyan]Restarting app to apply changes...[/bold cyan]\n")
                success, message = restart_app(subscription, resource_group, app_name)
                if success:
                    console.print(f"  [green]{message}[/green]\n")
                else:
                    console.print(f"  [yellow]⚠ {message}[/yellow]\n")
    
    typer.echo(f"Application Settings ({len(settings)} total):\n")
    for k, v in settings.items():
        if v and "@Microsoft.KeyVault" in v:
            is_secure, is_validated, error_msg = check_keyvault_reference(v, principal_id, subscription)
            if is_validated:
                console.print(f"  {k:40} [green]{v}[/green] [green bold]✓ SECURE & VALIDATED[/green bold]")
            else:
                status_msg = f"⚠ SECURE BUT NOT VALIDATED"
                if error_msg:
                    status_msg += f" ({error_msg})"
                console.print(f"  {k:40} [yellow]{v}[/yellow] [yellow bold]{status_msg}[/yellow bold]")
        else:
            masked = "********" if v else ""
            typer.echo(f"  {k:40} {masked}")
    typer.echo()
    if permissions_granted:
        console.print("[green bold]✓ All fixes applied successfully! Key Vault references synced and app restarted.[/green bold]")
        console.print("[dim]Note: It may take a few moments for the app to fully restart and pull the Key Vault references.[/dim]\n")


def _execute_migrate(subscription, resource_group, app_name, vault_name):
    """Execute migrate command - calls migrate logic directly"""
    from az_secure_env.migrate import migrate_settings_to_keyvault
    console.print("\n[bold cyan]═══ Environment Variable Migration to Key Vault ═══[/bold cyan]\n")
    
    try:
        app_info = get_app_info(subscription, resource_group, app_name)
        console.print(f"[bold]App:[/bold] {app_info['name']} ({app_info['type']})")
        console.print(f"[bold]Location:[/bold] {app_info['location']}\n")
    except Exception as e:
        console.print(f"[red]Error getting app info: {e}[/red]")
        raise typer.Exit(1)
    
    settings = fetch_app_settings(subscription, resource_group, app_name)
    if not settings:
        console.print("[yellow]No application settings found.[/yellow]")
        raise typer.Exit(0)
    
    plain_settings = {k: v for k, v in settings.items() if v and "@Microsoft.KeyVault" not in v}
    if not plain_settings:
        console.print("[yellow]All settings are already using Key Vault references.[/yellow]")
        raise typer.Exit(0)
    
    table = Table(title="Current Environment Variables (Plain Text)")
    table.add_column("No.", style="cyan", width=4)
    table.add_column("Setting Name", style="magenta")
    table.add_column("Value (Masked)", style="dim")
    
    setting_list = list(plain_settings.items())
    for idx, (key, value) in enumerate(setting_list, 1):
        table.add_row(str(idx), key, "********" if value else "")
    console.print(table)
    console.print()
    
    console.print("[bold]Select settings to migrate to Key Vault:[/bold]")
    console.print("Enter numbers separated by commas (e.g., 1,3,4) or 'all' for all settings")
    selection = Prompt.ask("Selection", default="all")
    
    if selection.lower() == "all":
        selected_settings = plain_settings
    else:
        try:
            indices = [int(x.strip()) for x in selection.split(",")]
            selected_settings = {setting_list[i-1][0]: setting_list[i-1][1] for i in indices if 1 <= i <= len(setting_list)}
        except (ValueError, IndexError):
            console.print("[red]Invalid selection. Please try again.[/red]")
            raise typer.Exit(1)
    
    if not selected_settings:
        console.print("[yellow]No settings selected.[/yellow]")
        raise typer.Exit(0)
    
    console.print(f"\n[green]Selected {len(selected_settings)} setting(s) for migration:[/green]")
    for key in selected_settings.keys():
        console.print(f"  • {key}")
    console.print()
    
    if not vault_name:
        vault_name = Prompt.ask("Enter Key Vault name")
    
    if not Confirm.ask(f"\n[bold]Proceed with migrating {len(selected_settings)} setting(s) to Key Vault '{vault_name}'?[/bold]"):
        console.print("[yellow]Migration cancelled.[/yellow]")
        raise typer.Exit(0)
    
    console.print("\n[bold cyan]Starting migration...[/bold cyan]\n")
    success, results = migrate_settings_to_keyvault(selected_settings, vault_name, subscription, resource_group, app_name, app_info)
    
    console.print()
    for result in results:
        if result['success']:
            console.print(f"  [green]✓ {result['message']}[/green]")
        else:
            console.print(f"  [red]✗ {result['message']}[/red]")
    
    if success:
        console.print("\n[green bold]✓ Migration completed successfully![/green bold]\n")
    else:
        console.print("\n[yellow]⚠ Migration completed with some errors.[/yellow]\n")


def _execute_add(subscription, resource_group, app_name, name, value, secure, vault_name):
    """Execute add command - calls add logic directly"""
    from az_secure_env.add_env import add_environment_variable
    console.print("\n[bold cyan]═══ Add Environment Variable ═══[/bold cyan]\n")
    
    try:
        app_info = get_app_info(subscription, resource_group, app_name)
        console.print(f"[bold]App:[/bold] {app_info['name']} ({app_info['type']})")
        console.print(f"[bold]Location:[/bold] {app_info['location']}\n")
    except Exception as e:
        console.print(f"[red]Error getting app info: {e}[/red]")
        raise typer.Exit(1)
    
    if not name:
        name = Prompt.ask("Enter environment variable name")
    if not value:
        value = Prompt.ask("Enter environment variable value", password=True)
    if secure is None:
        secure = Confirm.ask("Store securely in Key Vault?", default=True)
    if secure and not vault_name:
        vault_name = Prompt.ask("Enter Key Vault name")
    
    console.print(f"\n[bold]Summary:[/bold]")
    console.print(f"  Variable: {name}")
    console.print(f"  Storage:  {'Key Vault (' + vault_name + ')' if secure else 'Plain text'}")
    
    if not Confirm.ask("\n[bold]Proceed with adding this variable?[/bold]"):
        console.print("[yellow]Operation cancelled.[/yellow]")
        raise typer.Exit(0)
    
    console.print("\n[bold cyan]Adding environment variable...[/bold cyan]\n")
    success, results = add_environment_variable(name, value, secure, vault_name, subscription, resource_group, app_name, app_info)
    
    console.print()
    for result in results:
        if result['success']:
            console.print(f"  [green]✓ {result['message']}[/green]")
        else:
            console.print(f"  [red]✗ {result['message']}[/red]")
    
    if success:
        console.print("\n[green bold]✓ Environment variable added successfully![/green bold]\n")
    else:
        console.print("\n[red]✗ Failed to add environment variable.[/red]\n")


if __name__ == "__main__":
    app()
