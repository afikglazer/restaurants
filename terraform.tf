provider "azurerm" {
  features {}

  subscription_id = "2a43cdb3-2031-4411-8951-551e7e525852"
}

# Create a Resource Group
resource "azurerm_resource_group" "example" {
  name     = "example-resources"
  location = "East US"
}

# Create a Cosmos DB Account with Geo-Location
resource "azurerm_cosmosdb_account" "example" {
  name                = "example-cosmosdb"  # Unique name for the Cosmos DB account
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  kind                = "GlobalDocumentDB"  # SQL API (supports JSON)
  offer_type          = "Standard"

  # Geo-location blocks for replication (at least one required)
  geo_location {
    location          = "East US"
    failover_priority = 0
  }

  capabilities {
    name = "EnableSQL"
  }

  consistency_policy {
    consistency_level = "Eventual"  # Other options: "Strong", "Session", etc.
  }
}

# Create a Cosmos DB SQL Database
resource "azurerm_cosmosdb_sql_database" "example" {
  name                = "example-database"
  resource_group_name = azurerm_resource_group.example.name
  account_name        = azurerm_cosmosdb_account.example.name  # Correct attribute
}

# Create a Cosmos DB SQL Container (to store JSON)
# resource "azurerm_cosmosdb_sql_container" "example" {
#   name                 = "example-container"
#   database_name        = azurerm_cosmosdb_sql_database.example.name
#   resource_group_name  = azurerm_resource_group.examp
