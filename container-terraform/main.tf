provider "azurerm" {
  features {}

  subscription_id = "2a43cdb3-2031-4411-8951-551e7e525852"
}

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.70.0"
    }
  }
}

resource "azurerm_resource_group" "rg" {
  name     = "afik-container-app-rg"
  location = "East US"
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
  revision_mode                  = "Single"  # Choose "Single" or "Multiple"

  template {
    container {
      name   = "afik-container"
      image  = "afik23/flask:latest" # Replace with your container image
      cpu    = "0.25"    # Correct CPU format
      memory = "0.5Gi"   # Correct memory format
      env {
        name  = "AFIK"
        value = "12345"
      }
      env {
        name        = "LAB001-COSMOS"
        secret_name = "cas-cosmosdb-sk" # Use only the secret name without "secretref:"
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
    value = "your-secret-value" # Replace with the actual secret value
  }

}
