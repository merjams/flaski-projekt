from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
        return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    address = request.form['address']
    budget = int(request.form['budget'])
    preference = request.form['preference']

    results = filter_restaurants(address, budget, preference)
    return render_template('results.html', restaurants=results)

def filter_restaurants(address, budget, preference):
    data = [
        {'name': 'Peetri Pizza', 'address': 'Tallinn', 'budget': 10, 'type': 'pizza', 'image_url': 'https://imageproxy.wolt.com/assets/67332fa5c59f3326de543155'},
        {'name': 'Burger King', 'address': 'Tartu', 'budget': 5, 'type': 'burger', 'image_url': 'https://imageproxy.wolt.com/assets/67321464a5d40829eea5e217'},
        {'name': 'MySushi', 'address': 'Tallinn', 'budget': 10, 'type': 'sushi', 'image_url': 'https://virukeskus.com/wp/wp-content/uploads/2024/03/mysushi-pilt-3-767x512.jpeg' },
        {'name': 'Vapiano', 'address': 'Tallinn', 'budget': 15, 'type': 'pasta', 'image_url': 'https://www.paevapraad.ee/admin/upload/Failid/Kalender/1701424800/17017751391713.webp'},
    ]

    address = address.strip().lower()
    preference = preference.strip().lower()
    budget=int(budget)

    filtered = []
    for place in data:
        if (address in place['address'].lower() and
            place['budget'] <= budget and
            preference == place['type'].lower()):
            filtered.append(place)

    return filtered

if __name__ == '__main__':
    app.run(debug=True)
