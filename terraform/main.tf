terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.26.0"
    }
  }
}

provider "azurerm" {
  features {}
}
# This fetches details about the currently authenticated Azure client (your Terraform identity, usually a service principal).
data "azurerm_client_config" "current" {}

data "azurerm_resource_group" "main" {
  name = var.resource_group_name
}

data "azurerm_key_vault" "main" {
  name                = var.key_vault_name
  resource_group_name = data.azurerm_resource_group.main.name
}

# Retrieve MySQL admin username from Key Vault
data "azurerm_key_vault_secret" "mysql_username" {
  name         = "mysql-admin-username"
  key_vault_id = data.azurerm_key_vault.main.id
}

# Retrieve MySQL admin password from Key Vault
data "azurerm_key_vault_secret" "mysql_password" {
  name         = "mysql-admin-password"
  key_vault_id = data.azurerm_key_vault.main.id
}

resource "azurerm_user_assigned_identity" "uai" {
  name                = "sql-identity"
  resource_group_name = data.azurerm_resource_group.main.name
  location            = data.azurerm_resource_group.main.location
}

resource "azurerm_mysql_flexible_server" "main" {
  name                   = var.mysql_server_name
  location               = data.azurerm_resource_group.main.location
  resource_group_name    = data.azurerm_resource_group.main.name
  administrator_login    = data.azurerm_key_vault_secret.mysql_username.value
  administrator_password = data.azurerm_key_vault_secret.mysql_password.value
  version                = var.mysql_server_version
  sku_name               = var.mysql_sku_name
  

  storage {
    size_gb = 20
  }

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.uai.id]
  }

  depends_on = [
    data.azurerm_key_vault.main
  ]
}

resource "azurerm_mysql_flexible_server_firewall_rule" "allow_all" {
  name                = "allow_all"
  resource_group_name = data.azurerm_resource_group.main.name
  server_name         = azurerm_mysql_flexible_server.main.name
  start_ip_address    = "0.0.0.0"
  end_ip_address      = "255.255.255.255"
}

# AKS Cluster Deployment

resource "azurerm_kubernetes_cluster" "aks" {
  name                = var.aks_cluster_name
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  dns_prefix          = "kp"
  kubernetes_version  =  var.kubernetes_version #Free-tier
  sku_tier            = "Free"

  default_node_pool {
    name                  = var.default_node_pool_name
    vm_size               = var.vm_size
    os_sku                = var.os_sku
    node_count            = var.node_count
    max_pods              = var.max_pods

  }

  identity{
    type = "SystemAssigned"
  }

 network_profile {
    network_plugin      = "azure"
    load_balancer_sku   = "standard"
 }
   tags = {
    Environment = "system"
   }   

}

# Additional User Node Pool
resource "azurerm_kubernetes_cluster_node_pool" "user_node_pool" {
  name                  = var.user_node_pool 
  kubernetes_cluster_id = azurerm_kubernetes_cluster.aks.id
  vm_size               = var.vm_size
  os_sku                = var.os_sku
  node_count            = var.node_count
  max_pods              = var.max_pods
  mode                  = "User"

node_labels = {
  "env" = "staging"
  }

}