from azure.cosmos import CosmosClient, PartitionKey
import os

# Your Cosmos DB connection details
url = "https://afik-cosmosdb-nosql-account.documents.azure.com:443/"
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
        "id": "1",
        "name": "Pizza Hut",
        "style": "Italian",
        "address": "Wherever Street 99, Somewhere",
        "openHour": "09:00",
        "closeHour": "23:00",
        "vegetarian": "yes",
        "doesDeliveries": True
    },
    {
        "id": "2",
        "name": "Korean BBQ",
        "style": "Korean",
        "address": "Seoul Street 12, City",
        "openHour": "12:00",
        "closeHour": "22:00",
        "vegetarian": "no",
        "doesDeliveries": False
    },
    {
        "id": "3",
        "name": "Green Eatery",
        "style": "French",
        "address": "Paris Boulevard 5, Downtown",
        "openHour": "10:00",
        "closeHour": "21:00",
        "vegetarian": "yes",
        "doesDeliveries": True
    },
    {
        "id": "4",
        "name": "Taco Fiesta",
        "style": "Mexican",
        "address": "Cactus Street 45, Sunset District",
        "openHour": "11:00",
        "closeHour": "23:00",
        "vegetarian": "yes",
        "doesDeliveries": True
    },
    {
        "id": "5",
        "name": "Sushi Haven",
        "style": "Japanese",
        "address": "Shibuya Avenue 28, Metro City",
        "openHour": "12:00",
        "closeHour": "22:30",
        "vegetarian": "no",
        "doesDeliveries": True
    },
    {
        "id": "6",
        "name": "Vegan Delights",
        "style": "Vegan",
        "address": "Green Street 14, Earth Village",
        "openHour": "09:00",
        "closeHour": "20:00",
        "vegetarian": "yes",
        "doesDeliveries": True
    },
    {
        "id": "7",
        "name": "Spice Symphony",
        "style": "Indian",
        "address": "Bangalore Road 17, Global City",
        "openHour": "13:00",
        "closeHour": "23:00",
        "vegetarian": "yes",
        "doesDeliveries": False
    },
    {
        "id": "8",
        "name": "Burgers & Fries",
        "style": "American",
        "address": "Main Street 88, Uptown",
        "openHour": "10:00",
        "closeHour": "21:00",
        "vegetarian": "no",
        "doesDeliveries": True
    },
    {
        "id": "9",
        "name": "Pasta Paradiso",
        "style": "Italian",
        "address": "Roma Lane 22, Old Town",
        "openHour": "11:00",
        "closeHour": "22:00",
        "vegetarian": "yes",
        "doesDeliveries": False
    },
    {
        "id": "10",
        "name": "Cafe Cozy",
        "style": "Cafe",
        "address": "Riverfront Road 13, Lakeside",
        "openHour": "07:00",
        "closeHour": "19:00",
        "vegetarian": "yes",
        "doesDeliveries": True
    },
    {
        "id": "11",
        "name": "Banh Mi Delight",
        "style": "Vietnamese",
        "address": "Saigon Street 5, Central Park",
        "openHour": "10:00",
        "closeHour": "21:00",
        "vegetarian": "yes",
        "doesDeliveries": True
    },
    {
        "id": "12",
        "name": "BBQ Pitstop",
        "style": "American",
        "address": "Smokey Alley 40, Downtown",
        "openHour": "12:00",
        "closeHour": "23:00",
        "vegetarian": "no",
        "doesDeliveries": True
    },
    {
        "id": "13",
        "name": "The Sushi Box",
        "style": "Japanese",
        "address": "Tokyo Lane 9, Metro",
        "openHour": "11:30",
        "closeHour": "22:30",
        "vegetarian": "no",
        "doesDeliveries": True
    },
    {
        "id": "14",
        "name": "Curry Corner",
        "style": "Indian",
        "address": "Spice Street 12, Old Market",
        "openHour": "10:00",
        "closeHour": "22:00",
        "vegetarian": "yes",
        "doesDeliveries": False
    },
    {
        "id": "15",
        "name": "Trattoria Bella",
        "style": "Italian",
        "address": "Florence Road 15, City Center",
        "openHour": "12:00",
        "closeHour": "23:00",
        "vegetarian": "yes",
        "doesDeliveries": True
    },
    {
        "id": "16",
        "name": "Dim Sum Dynasty",
        "style": "Chinese",
        "address": "Chinatown Street 20, Downtown",
        "openHour": "10:00",
        "closeHour": "22:30",
        "vegetarian": "yes",
        "doesDeliveries": True
    },
    {
        "id": "17",
        "name": "Fiery Grill",
        "style": "American",
        "address": "Heatwave Avenue 33, Uptown",
        "openHour": "12:00",
        "closeHour": "23:00",
        "vegetarian": "no",
        "doesDeliveries": False
    },
    {
        "id": "18",
        "name": "Pho & More",
        "style": "Vietnamese",
        "address": "Hanoi Road 8, Downtown",
        "openHour": "11:00",
        "closeHour": "21:00",
        "vegetarian": "yes",
        "doesDeliveries": True
    },
    {
        "id": "19",
        "name": "The Wok",
        "style": "Chinese",
        "address": "Dragon Street 5, Central District",
        "openHour": "12:00",
        "closeHour": "22:00",
        "vegetarian": "yes",
        "doesDeliveries": True
    },
    {
        "id": "20",
        "name": "Bistro Parisien",
        "style": "French",
        "address": "Champs-Elysées 4, City Center",
        "openHour": "08:00",
        "closeHour": "22:00",
        "vegetarian": "yes",
        "doesDeliveries": False
    },
    {
        "id": "21",
        "name": "La Taqueria",
        "style": "Mexican",
        "address": "Puebla Street 33, South Side",
        "openHour": "12:00",
        "closeHour": "23:00",
        "vegetarian": "yes",
        "doesDeliveries": True
    },
    {
        "id": "22",
        "name": "Pasta Fresca",
        "style": "Italian",
        "address": "Napoli Boulevard 5, Downtown",
        "openHour": "10:00",
        "closeHour": "21:00",
        "vegetarian": "yes",
        "doesDeliveries": True
    },
    {
        "id": "23",
        "name": "Cafe au Lait",
        "style": "French",
        "address": "Rue de Paris 10, Main Square",
        "openHour": "07:00",
        "closeHour": "18:00",
        "vegetarian": "yes",
        "doesDeliveries": False
    },
    {
        "id": "24",
        "name": "Brunch Haven",
        "style": "Cafe",
        "address": "Sunny Plaza 5, Old Town",
        "openHour": "08:00",
        "closeHour": "16:00",
        "vegetarian": "yes",
        "doesDeliveries": True
    },
    {
        "id": "25",
        "name": "Peking Palace",
        "style": "Chinese",
        "address": "Imperial Avenue 7, Chinatown",
        "openHour": "11:00",
        "closeHour": "22:00",
        "vegetarian": "no",
        "doesDeliveries": True
    },
    {
        "id": "26",
        "name": "Sushi Samurai",
        "style": "Japanese",
        "address": "Kyoto Road 16, Bay Area",
        "openHour": "11:30",
        "closeHour": "23:00",
        "vegetarian": "no",
        "doesDeliveries": False
    },
    {
        "id": "27",
        "name": "Steakhouse Grill",
        "style": "American",
        "address": "Steak Lane 22, Downtown",
        "openHour": "12:00",
        "closeHour": "23:00",
        "vegetarian": "no",
        "doesDeliveries": True
    },
    {
        "id": "28",
        "name": "Mediterranean Breeze",
        "style": "Mediterranean",
        "address": "Sahara Street 11, Beachfront",
        "openHour": "11:00",
        "closeHour": "22:00",
        "vegetarian": "yes",
        "doesDeliveries": True
    },
    {
        "id": "29",
        "name": "Urban Bistro",
        "style": "Modern American",
        "address": "Highway 70, City Center",
        "openHour": "10:00",
        "closeHour": "22:00",
        "vegetarian": "yes",
        "doesDeliveries": False
    },
    {
        "id": "30",
        "name": "The Pasta House",
        "style": "Italian",
        "address": "Pasta Street 8, Uptown",
        "openHour": "11:00",
        "closeHour": "23:00",
        "vegetarian": "yes",
        "doesDeliveries": True
    }
]

# Insert documents into the container
for restaurant in restaurants:
    container.upsert_item(restaurant)

print("Data inserted successfully!")
