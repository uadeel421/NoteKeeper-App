#!/bin/bash

# You're using a service principal for Terraform authentication, not Azure CLI login.
# This script sets the necessary environment variables for Terraform to authenticate with Azure using a service principal.
# This is typical for CI/CD pipelines or shared environments.
# load-terraform-creds.sh

# Default Key Vault Name
KEY_VAULT_NAME="kpkeysvault"

# You can optionally pass the Key Vault Name as an argument
if [ -n "$1" ]; then
    KEY_VAULT_NAME="$1"
fi

echo "Fetching Azure credentials from Key Vault: $KEY_VAULT_NAME"

# Fetch Azure credentials from Key Vault
# Using `$(...)` for command substitution and `xargs` to trim whitespace (optional but good practice)
ARM_CLIENT_ID=$(az keyvault secret show --vault-name "$KEY_VAULT_NAME" --name "ARM-CLIENT-ID" --query value -o tsv | tr -d '\r')
ARM_CLIENT_SECRET=$(az keyvault secret show --vault-name "$KEY_VAULT_NAME" --name "ARM-CLIENT-SECRET" --query value -o tsv | tr -d '\r')
ARM_SUBSCRIPTION_ID=$(az keyvault secret show --vault-name "$KEY_VAULT_NAME" --name "ARM-SUBSCRIPTION-ID" --query value -o tsv | tr -d '\r')
ARM_TENANT_ID=$(az keyvault secret show --vault-name "$KEY_VAULT_NAME" --name "ARM-TENANT-ID" --query value -o tsv | tr -d '\r')

# Check if any variables are empty (meaning the secret wasn't found or an error occurred)
if [ -z "$ARM_CLIENT_ID" ] || [ -z "$ARM_CLIENT_SECRET" ] || [ -z "$ARM_SUBSCRIPTION_ID" ] || [ -z "$ARM_TENANT_ID" ]; then
    echo "Error: One or more Azure credentials could not be fetched from Key Vault. Please ensure the secrets exist and your Azure CLI is authenticated and has access to the Key Vault."
    exit 1
fi

# Set Azure provider environment variables for Terraform
export ARM_CLIENT_ID
export ARM_CLIENT_SECRET
export ARM_SUBSCRIPTION_ID
export ARM_TENANT_ID

echo -e "\nTerraform Azure credentials loaded into environment variables.\n"

# Optional: Verify variables are set (for debugging, remove in production)
# echo "ARM_CLIENT_ID: $ARM_CLIENT_ID"
# echo "ARM_SUBSCRIPTION_ID: $ARM_SUBSCRIPTION_ID"
# echo "ARM_TENANT_ID: $ARM_TENANT_ID"
# echo "ARM_CLIENT_SECRET: (hidden)"