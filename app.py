from flask import Flask, render_template, request
import requests
from math import radians, sin, cos, sqrt, atan2

app = Flask(__name__)

def geocode_address(address):
    geo_url = f'https://nominatim.openstreetmap.org/search?q={address}&format=json'
    headers = {
        'User-Agent': 'MinuFlaskRakendus/1.0 (merjamsepp@gmail.com)' 
    }
    response = requests.get(geo_url, headers=headers)

    if response.status_code != 200:
        return None, None

    try:
        geo_response = response.json()
    except ValueError:
        return None, None

    if not geo_response:
        return None, None

    location = geo_response[0]
    return float(location['lat']), float(location['lon'])

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

@app.route('/')
def home():
        return render_template('index.html')

@app.route('/soovitus', methods=['POST'])
def soovitus():
    address = request.form['address']
    budget = int(request.form['budget'])
    preference = request.form['preference']

    results = filter_restaurants(address, budget, preference)
    return render_template('results.html', restaurants=results)

def filter_restaurants(address, budget, preference):
    data = [
        {'name': 'Peetri Pizza', 'address': 'Roosikrantsi 23', 'budget': 10, 'type': 'pitsa','lat': 59.430121, 'lon': 24.7441, 'image_url': 'https://imageproxy.wolt.com/assets/67332fa5c59f3326de543155'},
        {'name': 'Burger King', 'address': 'Viru 23', 'budget': 5, 'type': 'burger', 'lat': 59.436703, 'lon': 24.750,'image_url': 'https://imageproxy.wolt.com/assets/67321464a5d40829eea5e217'},
        {'name': 'MySushi', 'address': 'Viru väljak 4-6', 'budget': 10, 'type': 'sushi', 'lat': 59.436236, 'lon': 24.754592, 'image_url': 'https://virukeskus.com/wp/wp-content/uploads/2024/03/mysushi-pilt-3-767x512.jpeg' },
        {'name': 'Vapiano', 'address': 'Estonia pst 9', 'budget': 15, 'type': 'pasta', 'lat': 59.436211, 'lon': 24.754601,'image_url': 'https://www.paevapraad.ee/admin/upload/Failid/Kalender/1701424800/17017751391713.webp'},
    ]

    address = address.strip().lower()
    preference = preference.strip().lower()
    budget=int(budget)
    
    user_lat, user_lon = geocode_address(address)
    if user_lat is None or user_lon is None:
        return [{"name": "Aadressi ei leitud", "address": "", "budget": 0, "type": "", "image_url": "", "distance": 0}]

    filtered = []
    for koht in data:
        if (koht['budget'] <= budget and preference == koht['type'].lower()):
            # Arvuta kaugus
            distance = calculate_distance(user_lat, user_lon, koht['lat'], koht['lon'])
            koht_copy = koht.copy()
            koht_copy['distance'] = round(distance, 2)
            filtered.append(koht_copy)
    
    filtered.sort(key=lambda x: x['distance'])
    return filtered

   

if __name__ == '__main__':
    app.run(debug=True)
