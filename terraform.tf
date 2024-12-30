provider "azurerm" {
  features {}

  subscription_id = "2a43cdb3-2031-4411-8951-551e7e525852"
}

# Create the resource group
resource "azurerm_resource_group" "example" {
  name     = "example-resources"
  location = "East US"
}

# Create the storage account
resource "azurerm_storage_account" "example" {
  name                     = "examplestorageacct"
  resource_group_name       = azurerm_resource_group.example.name
  location                 = azurerm_resource_group.example.location
  account_tier              = "Standard"
  account_replication_type = "LRS"
}

# Create the table storage
resource "azurerm_storage_table" "example" {
  name                 = "exampletable"
  storage_account_name = azurerm_storage_account.example.name
}

# Output the connection string
output "storage_account_connection_string" {
  value = azurerm_storage_account.example.primary_connection_string
}
