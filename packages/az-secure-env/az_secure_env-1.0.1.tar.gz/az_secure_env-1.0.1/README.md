# 🔐 az-secure-env

A simple and powerful CLI tool to secure your Azure App Services and Function Apps by managing environment variables safely with Azure Key Vault.

## 🎯 What Does This Tool Do?

If you're using Azure App Services or Function Apps, you might be storing sensitive information like API keys, database passwords, and connection strings directly in your app's environment variables. **This is not secure!** 

This tool helps you:
- **Scan** your apps to find insecure plain-text settings
- **Migrate** sensitive settings to Azure Key Vault (a secure storage for secrets)
- **Automatically fix** permission issues so your app can read from Key Vault
- **Add new** secure environment variables directly to Key Vault

## ✨ Key Features

- 🔍 **Smart Scanning** - Identifies plain-text secrets and Key Vault references
- 🚀 **One-Click Migration** - Move secrets to Key Vault with a single command
- 🔧 **Auto-Fix Permissions** - Automatically configures managed identity and Key Vault access
- ➕ **Easy Secret Management** - Add new secrets through an interactive menu
- 🎨 **Beautiful Interface** - Clean, colorful output that's easy to understand
- ⚡ **No Manual Setup** - Handles identity creation, permissions, and app restarts

## 📦 Installation

### Install from PyPI (Recommended)
```bash
pip install az-secure-env
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Azure account with active subscription
- You must be logged in to Azure CLI:
  ```bash
  az login
  ```

### Basic Usage

#### 1. Scan Your App for Security Issues
```bash
az-secure-env scan \
  --subscription "your-subscription-id" \
  --resource-group "your-rg-name" \
  --app-name "your-app-name"
```

This shows you:
- App information (name, type, location, identity status)
- All environment variables and their security status
- Which settings are secure (using Key Vault) vs plain-text

#### 2. Scan + Auto-Fix Permissions
```bash
az-secure-env scan \
  --subscription "your-subscription-id" \
  --resource-group "your-rg-name" \
  --app-name "your-app-name" \
  --fix
```

The `--fix` flag automatically:
- Enables managed identity if not present
- Grants Key Vault access permissions
- Syncs Key Vault references
- Restarts your app to apply changes

#### 3. Migrate Secrets to Key Vault
```bash
az-secure-env migrate \
  --subscription "your-subscription-id" \
  --resource-group "your-rg-name" \
  --app-name "your-app-name" \
  --vault-name "your-keyvault-name"
```

This interactive command:
- Shows all plain-text environment variables
- Lets you select which ones to migrate
- Creates secrets in Key Vault
- Updates app settings to use Key Vault references
- Handles all permissions automatically

#### 4. Add New Secret to Key Vault
```bash
az-secure-env add-env \
  --subscription "your-subscription-id" \
  --resource-group "your-rg-name" \
  --app-name "your-app-name"
```

Interactive menu to add a new environment variable securely:
- Choose to add to existing Key Vault or create new one
- Enter variable name and value
- Automatically creates Key Vault reference in your app
- Handles all setup and permissions

## 📖 Detailed Examples

### Example 1: Complete Security Audit and Fix
```bash
# First, scan to see what needs fixing
az-secure-env scan --subscription "abc123" --resource-group "my-rg" --app-name "my-webapp"

# Then auto-fix any Key Vault permission issues
az-secure-env scan --subscription "abc123" --resource-group "my-rg" --app-name "my-webapp" --fix
```

### Example 2: Migrate All Secrets at Once
```bash
az-secure-env migrate \
  --subscription "abc123" \
  --resource-group "my-rg" \
  --app-name "my-webapp" \
  --vault-name "my-keyvault"

# When prompted, type "all" to migrate all plain-text settings
```

### Example 3: Selective Migration
```bash
az-secure-env migrate \
  --subscription "abc123" \
  --resource-group "my-rg" \
  --app-name "my-webapp" \
  --vault-name "my-keyvault"

# When prompted, type "1,3,5" to migrate only settings #1, #3, and #5
```

## 🔐 How It Works

### Security Model
1. **Managed Identity**: Your app gets a system-assigned managed identity (like a special Azure account for your app)
2. **Key Vault**: Secrets are stored in Azure Key Vault (like a secure safe)
3. **References**: Your app settings point to Key Vault, not the actual secret
4. **Automatic Access**: The tool grants your app's identity permission to read from Key Vault

### What Happens Behind the Scenes

When you migrate a setting like `API_KEY=super-secret-123`:
1. Creates a secret in Key Vault named `API-KEY` with value `super-secret-123`
2. Updates your app setting to: `API_KEY=@Microsoft.KeyVault(SecretUri=https://your-vault.vault.azure.net/secrets/API-KEY)`
3. Your app automatically reads the real value from Key Vault at runtime

## 🛠️ Commands Reference

### `scan`
Scan an app for settings and security status

**Options:**
- `--subscription` (required) - Azure subscription ID
- `--resource-group` (required) - Resource group name
- `--app-name` (required) - App Service or Function App name
- `--fix` (optional) - Automatically fix Key Vault permissions

### `migrate`
Migrate plain-text settings to Key Vault

**Options:**
- `--subscription` (required) - Azure subscription ID
- `--resource-group` (required) - Resource group name
- `--app-name` (required) - App Service or Function App name
- `--vault-name` (required) - Key Vault name

### `add-env`
Add a new environment variable securely

**Options:**
- `--subscription` (required) - Azure subscription ID
- `--resource-group` (required) - Resource group name
- `--app-name` (required) - App Service or Function App name

## ⚙️ Configuration

### Azure Authentication
The tool uses Azure CLI authentication. Make sure you're logged in:
```bash
az login
```

To use a specific account:
```bash
az account set --subscription "your-subscription-id"
```

### Required Azure Permissions
Your Azure account needs these permissions:
- Read/Write access to App Service/Function App
- Ability to grant Key Vault access policies
- Create/Read/Write access to Key Vault secrets

Typically, you need the **Contributor** role or these specific roles:
- `Website Contributor` (for App Services)
- `Key Vault Administrator` or `Key Vault Secrets Officer` (for Key Vault)

## 🤔 FAQ

**Q: Will this break my app?**  
A: No! The tool creates backups and only modifies settings you select. Your app is restarted automatically to apply changes.

**Q: What if I don't have a Key Vault?**  
A: The `add-env` command can create one for you, or you can create one manually first.

**Q: Can I use this with Azure Functions?**  
A: Yes! It works with both App Services and Function Apps.

**Q: What happens to my old plain-text settings?**  
A: They are replaced with Key Vault references. The actual values are stored securely in Key Vault.

**Q: Can I migrate back to plain-text?**  
A: Yes, you can manually update the app settings in Azure Portal, but we don't recommend it for security reasons.

## 🐛 Troubleshooting

### "No module named 'az_secure_env'"
Make sure you've installed the package: `pip install az-secure-env`

### "Authentication failed"
Run `az login` to authenticate with Azure.

### "Key Vault not found"
Ensure the Key Vault name is correct and exists in your subscription.

### "Permission denied"
Your Azure account needs sufficient permissions. Contact your Azure administrator.

## 👨‍💻 Author

Created by Aakash Shah to make Azure security easier for everyone.

## 🔗 Useful Links

- [Azure Key Vault Documentation](https://docs.microsoft.com/azure/key-vault/)
- [Azure App Service Documentation](https://docs.microsoft.com/azure/app-service/)
- [Managed Identities Documentation](https://docs.microsoft.com/azure/active-directory/managed-identities-azure-resources/)

---

**⭐ If this tool helped you, please consider giving it a star on GitHub!**