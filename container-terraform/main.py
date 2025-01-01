from flask import Flask, request, jsonify
import time
from datetime import datetime  # Import only the `datetime` class
from azure.cosmos import CosmosClient, PartitionKey
import os

app = Flask(__name__)

def wrRecord(sentParams: dict):
    print("degel")
    endpoint = "https://afik-cosmosdb-nosql.documents.azure.com:443/"
    key = os.getenv("LAB001-COSMOS")
    database_name = "container-requests"
    container_name = "container-requests"
    client = CosmosClient(endpoint, key)
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)
    print(sentParams)
    print(sentParams)
    print(sentParams)
    print(sentParams)
    print(sentParams)
    record = {
        "id": str(int(time.time() * 1000)),  # UNIX timestamp in milliseconds
        "message": sentParams
    }
    print(record)

    
    try:
        container.upsert_item(record)
        print("Record inserted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

def getDocumentDataSet() -> list:
    endpoint = "https://afik-cosmosdb-nosql.documents.azure.com:443/"
    key = os.getenv("LAB001-COSMOS")
    database_name = "afik-cosmosdb-nosql-db-1"
    container_name = "afik-cosmosdb-nosql-container-1"
    client = CosmosClient(endpoint, key)
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)

    query = """
        SELECT c.name, c.style, c.address, c.openHour, c.closeHour, c.vegetarian, c.doesDeliveries
        FROM c
    """
    items = list(container.query_items(query=query, enable_cross_partition_query=True))
    return [item for item in items]

restaurants = getDocumentDataSet()

def is_open_now(open_hour, close_hour):
    now = datetime.now().time()
    open_time = datetime.strptime(open_hour, "%H:%M").time()
    close_time = datetime.strptime(close_hour, "%H:%M").time()
    return open_time <= now <= close_time

@app.route('/recommend', methods=['GET'])
def recommend_restaurant():
    query_params = request.args

    style = query_params.get('style')
    vegetarian = query_params.get('vegetarian')
    open_now = query_params.get('openNow', 'false').lower() == 'true'
    wrRecord(sentParams=query_params)

    for restaurant in restaurants:
        if style and restaurant['style'].lower() != style.lower():
            continue
        if vegetarian and restaurant['vegetarian'].lower() != vegetarian.lower():
            continue
        if open_now and not is_open_now(restaurant['openHour'], restaurant['closeHour']):
            continue

        return jsonify({
            "restaurantRecommendation": {
                "name": restaurant['name'],
                "style": restaurant['style'],
                "address": restaurant['address'],
                "openHour": restaurant['openHour'],
                "closeHour": restaurant['closeHour'],
                "vegetarian": restaurant['vegetarian'],
                "doesDeliveries": restaurant['doesDeliveries']
            },
            "requestTime": datetime.now().isoformat()
        })

    return jsonify({"message": "No restaurant matches the criteria."}), 404

if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=5000, debug=True)
