variable "subscription_id" {
  description = "The Azure subscription ID"
  type        = string
  sensitive   = true
  default = "2a43cdb3-2031-4411-8951-551e7e525852"
}

# variable "cosmosdb_secret" {
#   description = "The Cosmos DB secret"
#   type        = string
#   sensitive   = true
#   default = "your-secret-value"
# }

variable "resource_group_name" {
  description = "The name of the resource group"
  type        = string
  default     = "azme_afik_glazer_rg"
}

variable "resource_group_name2" {
  description = "The name of the resource group"
  type        = string
  default     = "afik-container-app-rg"
}

variable "location" {
  description = "The Azure region to deploy the resources"
  type        = string
  default     = "Central US"
}

variable "revision_mode" {
  description = "The Azure region to deploy the resources"
  type        = string
  default     = "Single"
}

variable "throughput" {
  description = "thoughput property"
  type = number
  default = 400
}