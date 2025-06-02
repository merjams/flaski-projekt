from flask import Flask, render_template, request
import requests
# Importime vajalikud matemaatilised funktsioonid: kraadide teisendamine radiaanideks (radians),
# siinus (sin), koosinus (cos), ruutjuur (sqrt) ja arkustangens (atan2), mida kasutatakse kauguse arvutamisel.
from math import radians, sin, cos, sqrt, atan2

app = Flask(__name__)

# Funktsioon geocode_address leiab kasutaja sisestatud aadressi geograafilised koordinaadid (laius ja pikkus).
def geocode_address(address):
    # Koostame URL-i päringuks OpenStreetMap Nominatim API-sse
    geo_url = f'https://nominatim.openstreetmap.org/search?q={address}&format=json'

    # Lisame kasutajaliidese päise, et API lubaks meil andmeid küsida
    headers = {
        'User-Agent': 'MinuFlaskRakendus/1.0 (merjamsepp@gmail.com)'  # API nõuab viisakat identifitseerimist
    }

    # Teeme HTTP GET-päringu
    response = requests.get(geo_url, headers=headers)

    # Kontrollime, kas vastus oli edukas (status_code 200 = OK)
    if response.status_code != 200:
        return None, None  # Kui mitte, tagastame tühjad väärtused

    # Püüame vastuse JSON-ina parsida
    try:
        geo_response = response.json()
    except ValueError:
        return None, None  # Kui JSON-parsimine ebaõnnestub

    # Kui otsing ei andnud tulemusi, tagastame tühjad väärtused
    if not geo_response:
        return None, None

    # Võtame esimese tulemuse ja tagastame selle laius- ja pikkuskraadi
    location = geo_response[0]
    return float(location['lat']), float(location['lon'])

# Funktsioon calculate_distance arvutab kahe punkti vahemaa Maal, kasutades Haversine'i valemit.
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Maa raadius kilomeetrites

    # Teisendame kõik koordinaadid kraadidest radiaanideks
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Arvutame vahed laius- ja pikkuskraadides
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine'i valemi osa – sfäärilise kauguse arvutus
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Kaugus kilomeetrites
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
        {'name': 'Peetri Pizza', 'address': 'Roosikrantsi 23, Tallinn', 'budget': 10, 'type': 'pitsa', 'rating': '4.7/5', 'lat': 59.430121, 'lon': 24.7441, 'image_url': 'https://imageproxy.wolt.com/assets/67332fa5c59f3326de543155'},
        {'name': 'Burger King', 'address': 'Viru 23, Tallinn', 'budget': 5, 'type': 'burger', 'rating': '4.5/5', 'lat': 59.436703, 'lon': 24.750,'image_url': 'https://imageproxy.wolt.com/assets/67321464a5d40829eea5e217'},
        {'name': 'MySushi', 'address': 'Viru väljak 4-6, Tallinn', 'budget': 10, 'type': 'sushi', 'rating': '3.1/5', 'lat': 59.436236, 'lon': 24.754592, 'image_url': 'https://virukeskus.com/wp/wp-content/uploads/2024/03/mysushi-pilt-3-767x512.jpeg' },
        {'name': 'Vapiano', 'address': 'Estonia pst 9, Tallinn', 'budget': 15, 'type': 'pasta', 'rating': '3.7/5', 'lat': 59.436211, 'lon': 24.754601,'image_url': 'https://www.paevapraad.ee/admin/upload/Failid/Kalender/1701424800/17017751391713.webp'},
        {'name': 'Pizza Americana', 'address': 'Kaarli pst 2, Tallinn', 'budget': 12, 'type': 'pitsa', 'rating': '4.4/5', 'lat': 59.433225, 'lon':  24.741982, 'image_url':'https://imageproxy.wolt.com/menu/menu-images/5d0200594c6f3d9e5ea6ea32/e48fd118-dfd4-11eb-a1b3-862363ed7636_nr1.jpeg?w=1920'},
        {'name': 'Kaja Pizza', 'address': 'Õle 33, Tallinn', 'budget': 15, 'type': 'pitsa', 'rating': '4.8/5', 'lat': 59.439592, 'lon':  24.717254, 'image_url': 'https://imageproxy.wolt.com/assets/67332fc27296644b4f09782e'},
        {'name': 'Sushi Plaza', 'address': 'Narva mnt 6, Tallinn', 'budget': 15, 'type': 'sushi', 'rating': '4.4/5', 'lat':59.43744, 'lon': 24.762009, 'image_url': 'https://media-cdn.tripadvisor.com/media/photo-m/1280/2e/c1/9f/a5/sushi-plaza-serves-a.jpg'},
        {'name': 'Vegan restoran V', 'address': 'Rataskaevu tn 12, Tallinn', 'budget': 30, 'type': 'vegan', 'rating': '4.8/5', 'lat': 59.437183, 'lon': 24.742541,'image_url': 'https://file.visittallinn.ee/6ghbatj/detail-vegan-restoran-v-tallinn-visit-estonia.jpg'},
        {'name': 'Chakra', 'address':'Bremeni käik 1, Tallinn', 'budget': 25, 'type': 'india', 'rating': '4.6/5', 'lat':59.439381, 'lon': 24.749454, 'image_url':'https://file.visittallinn.ee/4x5jxm/detail-chakrav2.jpg'},
        {'name': 'Han restoran', 'address':'A. Lauteri tn 5, Tallinn', 'budget': 15, 'type': 'hiina', 'rating': '4.3/5', 'lat': 59.43149, 'lon': 24.757691, 'image_url': 'https://cdn-media.choiceqr.com/prod-eat-hansresto/tXBhMfa-BCdhMhD-DNqzfDg.jpeg'},
        {'name': 'Reval Cafe Müürivahe', 'address':'Müürivahe 14, Tallinn', 'budget': 12, 'type': 'kohvik', 'rating': '4.5/5', 'lat': 59.434932, 'lon': 24.745632, 'image_url': 'https://revalcafe.ee/wp-content/uploads/2021/04/marekmetslaid_MMP0089-3.jpg'},
        {'name': 'Gelato Ladies', 'address':'Uus tn 28, Tallinn', 'budget': 3, 'type': 'jäätis','rating': '4.7/5', 'lat': 59.440909, 'lon': 24.749807, 'image_url': 'https://images.happycow.net/venues/1024/13/58/hcmp135831_465849.jpeg'}
    
    ]

    address = address.strip().lower()
    preference = preference.strip().lower()
    budget=int(budget)
    
    
    user_lat, user_lon = geocode_address(address)
    if user_lat is None or user_lon is None:
        return [{"name": "Aadressi ei leitud", "address": "", "budget": 0, "type": "", "image_url": "", "distance": 0}]

    # Loome tühja nimekirja, kuhu lisame hiljem kõik kasutajale sobivad kohad
    filtered = []

    # Käime kõik andmed ükshaaval läbi
    for koht in data:
        # Kontrollime, kas:
        # - koha hind on väiksem või võrdne kasutaja eelarvega
        # - koha tüüp vastab kasutaja eelistusele (võrreldes väikeste tähtedega)
        if (koht['budget'] <= budget and preference == koht['type'].lower()):
            # Arvutame kauguse kasutaja asukohast selle koha asukohani
            distance = calculate_distance(user_lat, user_lon, koht['lat'], koht['lon'])
        
            # Teeme koha andmetest koopia, et mitte muuta originaalandmeid
            koht_copy = koht.copy()
        
            # Lisame koopiale juurde kauguse, ümardatuna kahe komakohani
            koht_copy['distance'] = round(distance, 2)
        
            # Lisame selle töödeldud ja kaugusega täiendatud koha sobivate nimekirja
            filtered.append(koht_copy)

# Sorteerime sobivate kohtade nimekirja kauguse järgi kasvavas järjekorras
filtered.sort(key=lambda x: x['distance'])

# Tagastame sorteeritud ja filtreeritud kohtade nimekirja
return filtered


   

if __name__ == '__main__':
    app.run(debug=True)
