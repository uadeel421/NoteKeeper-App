resource_group_name  = "kprg"
location             = "France Central"

mysql_server_name    = "rwdbserver"
mysql_server_version = "8.0.21"
mysql_sku_name       = "B_Standard_B1ms"  

aks_cluster_name    = "kp-k8s-cluster"
kubernetes_version  = "1.32.3"
default_node_pool_name = "default"
user_node_pool         =  "stgpool"

vm_size                = "Standard_D2pls_v6"
os_sku                 = "AzureLinux"

node_count             = 1
max_pods               = 30

