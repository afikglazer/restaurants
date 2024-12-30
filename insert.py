from azure.cosmos import CosmosClient, PartitionKey
import os

# Your Cosmos DB connection details
url = "https://afik-cosmosdb-nosql.documents.azure.com:443/"
primary_key = os.getenv("LAB001-COSMOS")  # Replace with your actual primary key
database_name = "afik-cosmosdb-nosql-db-1"  # The name of your database
container_name = "afik-cosmosdb-nosql-container-1"  # The name of your container

# Initialize the Cosmos client
client = CosmosClient(url, credential=primary_key)

# Get the database and container
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

# Data to insert
restaurants = [
    {
        "id": "1",  # Add an id field for each document
        "TenantID": "tenant1",  # Partition key
        "name": "Pizza Hut",
        "style": "Italian",
        "address": "Wherever Street 99, Somewhere",
        "openHour": "09:00",
        "closeHour": "23:00",
        "vegetarian": "yes",
        "doesDeliveries": True
    },
    {
        "id": "2",  # Add an id field for each document
        "TenantID": "tenant1",  # Partition key
        "name": "Korean BBQ",
        "style": "Korean",
        "address": "Seoul Street 12, City",
        "openHour": "12:00",
        "closeHour": "22:00",
        "vegetarian": "no",
        "doesDeliveries": False
    },
    {
        "id": "3",  # Add an id field for each document
        "TenantID": "tenant1",  # Partition key
        "name": "Green Eatery",
        "style": "French",
        "address": "Paris Boulevard 5, Downtown",
        "openHour": "10:00",
        "closeHour": "21:00",
        "vegetarian": "yes",
        "doesDeliveries": True
    }
]

# Insert documents into the container
for restaurant in restaurants:
    container.upsert_item(restaurant)

print("Data inserted successfully!")
