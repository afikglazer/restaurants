
provider "azurerm" {
  features {}

  subscription_id = "2a43cdb3-2031-4411-8951-551e7e525852"
}

# Reference an existing resource group
data "azurerm_resource_group" "afik-rg-name" {
    name = "azme_afik_glazer_rg"  # Replace with the name of your existing resource group
}

resource "azurerm_cosmosdb_account" "afik-cosmosdb-account-tf" {
    name                = "example-cosmosdb-account"
    location            = data.azurerm_resource_group.afik-rg-name.location
    resource_group_name = data.azurerm_resource_group.afik-rg-name.name
    offer_type          = "Standard"
    kind                = "GlobalDocumentDB"  # Specifies NoSQL API (SQL API is default for NoSQL)

    geo_location {
    location          = "Central US"  # US Central region
    failover_priority = 0  # Primary region
    }

    capabilities {
    name = "EnableGremlin"  # Optional if you want to enable additional capabilities like Gremlin (Graph) API.
    }

    consistency_policy {
    consistency_level = "Session"
    }

    tags = {
    name = "afik-cosmosdb-account-tf"
    }
}
