
variable "resource_group_name" {
  description = "The Name of the Azure Resource group"
  type        = string  
}

variable "location" {
    description = "Azure region"
    type        = string
}

variable "key_vault_name" {
  description = " The Name of the Key Vault"
  default = "kpkeysvault"
}

variable "mysql_server_name" {
  description = "Name of the Azure MySQL server"
  type        = string
}

variable "mysql_server_version" {
description = "Version of the MySQL server"
type        = string
}

variable "mysql_sku_name"{
description = "Name of the MySQL SKU"
type        = string
}

# Kubernetes Cluster Veriables

variable "aks_cluster_name" {
  description = "Name of the AKS cluster"
  type        = string
}

variable "kubernetes_version" {
description = "Version of the MySQL server"
type        = string
}

variable "default_node_pool_name" {
  description = "Name of the Default Node Pool Name"
  type        = string
}

variable "vm_size" {
  description = "VM size of the AKS nodes"
  type        = string
}

variable "os_sku" {
  description = "OS SKU for the nodes (e.g., AzureLinux, Ubuntu)"
  type        = string
}

variable "node_count" {
  description = "Node count"
  type        = number
}

variable "max_pods" {
  description = "Maximum number of pods per node"
  type        = number
}


variable "user_node_pool" {
  description = "Name of the User Node Pool Name"
  type        = string
}