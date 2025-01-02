provider "azurerm" {
  features {}

  subscription_id = var.subscription_id
  #subscription_id = "2a43cdb3-2031-4411-8951-551e7e525852"
}

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.70.0"
    }
  }
}

data "azurerm_key_vault" "existing" {
  name                = "afik-keyvault"
  resource_group_name = "azme_afik_glazer_rg"
}

# Fetch the secret and retrieve its ID
data "azurerm_key_vault_secret" "example" {
  name         = "cosmosdb-sk"  # Replace with the name of the secret you want
  key_vault_id = data.azurerm_key_vault.existing.id
}

# output "secret_id" {
#   value = data.azurerm_key_vault_secret.example.id
# }


resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location =  var.location
}

resource "azurerm_log_analytics_workspace" "log_analytics" {
  name                = "afik-log-analytics"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_container_app_environment" "env" {
  name                = "afik-container-app-env"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  log_analytics_workspace_id = azurerm_log_analytics_workspace.log_analytics.id
}

resource "azurerm_container_app" "app" {
  name                           = "afik-container-app"
  container_app_environment_id   = azurerm_container_app_environment.env.id
  resource_group_name            = azurerm_resource_group.rg.name
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
