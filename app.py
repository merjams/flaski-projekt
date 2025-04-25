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
        {'name': 'Pizza Mafia', 'address': 'Tallinn', 'budget': 10, 'type': 'pizza'},
        {'name': 'Burger King', 'address': 'Tartu', 'budget': 5, 'type': 'burger'},
        {'name': 'Sushiplaza', 'address': 'Tallinn', 'budget': 20, 'type': 'sushi'},
        {'name': 'Vegan Vibes', 'address': 'Tallinn', 'budget': 15, 'type': 'vegan'},
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
