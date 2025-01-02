provider "azurerm" {
  features {}
  subscription_id = "2a43cdb3-2031-4411-8951-551e7e525852"
}

resource "azurerm_cosmosdb_account" "example" {
  name                = "afik-cosmosdb-nosql22"
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
    total_throughput_limit = 1000
  }

}
