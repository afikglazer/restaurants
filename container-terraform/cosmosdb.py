from azure.cosmos import CosmosClient, PartitionKey
import os

# Set up CosmosDB connection details
endpoint = "https://afik-cosmosdb-nosql.documents.azure.com:443/"
key = os.getenv("LAB001-COSMOS")
database_name = "afik-cosmosdb-nosql-db-1"
container_name = "afik-cosmosdb-nosql-container-1"

# Create CosmosClient and connect to the database and container
client = CosmosClient(endpoint, key)
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

# Query to retrieve only the specific fields from the objects
query = """
    SELECT c.name, c.style, c.address, c.openHour, c.closeHour, c.vegetarian, c.doesDeliveries
    FROM c
"""

# Execute the query
items = list(container.query_items(query=query, enable_cross_partition_query=True))

# Create a list to store the selected objects
selected_objects = []

# Process the retrieved data and add them to the list
for item in items:
    selected_objects.append(item)

# Now `selected_objects` contains the filtered objects
print(selected_objects)