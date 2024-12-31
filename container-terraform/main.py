from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Sample restaurant database
restaurants = [
    {
        "name": "Pizza Hut",
        "style": "Italian",
        "address": "Wherever Street 99, Somewhere",
        "openHour": "09:00",
        "closeHour": "23:00",
        "vegetarian": "yes",
        "doesDeliveries": True
    },
    {
        "name": "Korean BBQ",
        "style": "Korean",
        "address": "Seoul Street 12, City",
        "openHour": "12:00",
        "closeHour": "22:00",
        "vegetarian": "no",
        "doesDeliveries": False
    },
    {
        "name": "Green Eatery",
        "style": "French",
        "address": "Paris Boulevard 5, Downtown",
        "openHour": "10:00",
        "closeHour": "21:00",
        "vegetarian": "yes",
        "doesDeliveries": True
    }
]

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
