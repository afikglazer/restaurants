provider "azurerm" {
  features {}
  subscription_id = "2a43cdb3-2031-4411-8951-551e7e525852"
}

resource "azurerm_cosmosdb_account" "afik-cosmosdb-nosql-account" {
  name                = "afik-cosmosdb-nosql-account"
  location            = "Central US"
  resource_group_name = "azme_afik_glazer_rg"

  offer_type = "Standard"
  kind       = "GlobalDocumentDB"

  consistency_policy {
    consistency_level       = "Session"
    max_interval_in_seconds = 5
    max_staleness_prefix    = 100
  }

  geo_location {
    location          = "Central US"
    failover_priority = 0
    zone_redundant    = false
  }

  public_network_access_enabled = true
  analytical_storage_enabled = false
  free_tier_enabled          = false

  tags = {
    defaultExperience    = "Core (SQL)"
    hidden-cosmos-mmspecial = ""
  }

  capacity {
    total_throughput_limit = 1600
  }
}

resource "azurerm_cosmosdb_sql_database" "afik-cosmosdb-nosql-db-1" {
  name                = "afik-cosmosdb-nosql-db-1"
  resource_group_name = "azme_afik_glazer_rg"
  account_name        = azurerm_cosmosdb_account.afik-cosmosdb-nosql-account.name
  throughput          = 400
}

resource "azurerm_cosmosdb_sql_container" "afik-cosmosdb-nosql-container-1" {
  name                = "afik-cosmosdb-nosql-container-1"
  resource_group_name = "azme_afik_glazer_rg"
  account_name        = azurerm_cosmosdb_account.afik-cosmosdb-nosql-account.name
  database_name       = azurerm_cosmosdb_sql_database.afik-cosmosdb-nosql-db-1.name
  throughput          = 400

  partition_key_paths   = ["/id"]
  partition_key_version    = 1
}


resource "azurerm_cosmosdb_sql_database" "container-requests-db" {
  name                = "container-requests-db"
  resource_group_name = "azme_afik_glazer_rg"
  account_name        = azurerm_cosmosdb_account.afik-cosmosdb-nosql-account.name
  throughput          = 400
}

resource "azurerm_cosmosdb_sql_container" "container-requests" {
  name                = "container-requests"
  resource_group_name = "azme_afik_glazer_rg"
  account_name        = azurerm_cosmosdb_account.afik-cosmosdb-nosql-account.name
  database_name       = azurerm_cosmosdb_sql_database.container-requests-db.name
  throughput          = 400

  partition_key_paths   = ["/id"]
  partition_key_version    = 1
}