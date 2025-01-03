data "azurerm_key_vault" "afik-keyvault" {
  name                = "afik-keyvault"
  resource_group_name = var.resource_group_name
}

# Fetch the secret and retrieve its ID
data "azurerm_key_vault_secret" "example" {
  name         = "cosmosdb-sk"  # Replace with the name of the secret you want
  key_vault_id = data.azurerm_key_vault.afik-keyvault.id
}

data "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
}

resource "azurerm_log_analytics_workspace" "log_analytics" {
  name                = "afik-log-analytics"
  location            = var.location
  resource_group_name = data.azurerm_resource_group.rg.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_container_app_environment" "env" {
  name                = "afik-container-app-env"
  location            = var.location
  resource_group_name = data.azurerm_resource_group.rg.name

  log_analytics_workspace_id = azurerm_log_analytics_workspace.log_analytics.id
}

resource "azurerm_container_app" "app" {
  name                           = "afik-container-app"
  container_app_environment_id   = azurerm_container_app_environment.env.id
  resource_group_name            = data.azurerm_resource_group.rg.name
  revision_mode                  = var.revision_mode

  template {
    container {
      name   = "afik-container"
      image  = "afik23/flask:latest"
      cpu    = "0.25"
      memory = "0.5Gi"
      env {
        name        = "LAB001-COSMOS"
        secret_name = "cas-cosmosdb-sk" # Secret reference
      }
    }
  }

  ingress {
    external_enabled           = true
    allow_insecure_connections = true
    target_port                = 5000

    traffic_weight {
      latest_revision = true    # Specifies the traffic should go to the latest revision
      percentage      = 100     # Assign 100% of the traffic to the latest revision
    }
  }

  secret {
    name  = "cas-cosmosdb-sk"
    value = data.azurerm_key_vault_secret.example.value # Import/Get secret value from Key Vault
  }
}

resource "azurerm_cosmosdb_account" "afik-cosmosdb-nosql-account" {
  name                = "afik-cosmosdb-nosql-account"
  location            = var.location
  resource_group_name = data.azurerm_resource_group.rg.name

  offer_type = "Standard"
  kind       = "GlobalDocumentDB"

  consistency_policy {
    consistency_level       = "Session"
    max_interval_in_seconds = 5
    max_staleness_prefix    = 100
  }

  geo_location {
    location          = var.location
    failover_priority = 0
    zone_redundant    = false
  }

  public_network_access_enabled = true
  analytical_storage_enabled = false
  free_tier_enabled          = true

  capacity {
    total_throughput_limit = var.throughput * 4
  }
}

resource "azurerm_cosmosdb_sql_database" "afik-cosmosdb-nosql-db-1" {
  name                = "afik-cosmosdb-nosql-db-1"
  resource_group_name = data.azurerm_resource_group.rg.name
  account_name        = azurerm_cosmosdb_account.afik-cosmosdb-nosql-account.name
  throughput          = var.throughput
}

resource "azurerm_cosmosdb_sql_container" "afik-cosmosdb-nosql-container-1" {
  name                = "afik-cosmosdb-nosql-container-1"
  resource_group_name = data.azurerm_resource_group.rg.name
  account_name        = azurerm_cosmosdb_account.afik-cosmosdb-nosql-account.name
  database_name       = azurerm_cosmosdb_sql_database.afik-cosmosdb-nosql-db-1.name
  throughput          = var.throughput

  partition_key_paths   = ["/id"]
  partition_key_version    = 1
}


resource "azurerm_cosmosdb_sql_database" "container-requests-db" {
  name                = "container-requests-db"
  resource_group_name = data.azurerm_resource_group.rg.name
  account_name        = azurerm_cosmosdb_account.afik-cosmosdb-nosql-account.name
  throughput          = var.throughput
}

resource "azurerm_cosmosdb_sql_container" "container-requests" {
  name                = "container-requests"
  resource_group_name = data.azurerm_resource_group.rg.name
  account_name        = azurerm_cosmosdb_account.afik-cosmosdb-nosql-account.name
  database_name       = azurerm_cosmosdb_sql_database.container-requests-db.name
  throughput          = var.throughput

  partition_key_paths   = ["/id"]
  partition_key_version    = 1
}