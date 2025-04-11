from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
        return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    address = request.form['address']
    budget = request.form['budget']
    preference = request.form['preference']

    results = filter_restaurants(address, budget, preference)
    return render_template('results.html', restaurants=results)

def filter_restaurants(address, budget, preference):
    data = [
        {'name': 'Pizza Mafia', 'address': 'Tallinn', 'budget': '€', 'type': 'pizza'},
        {'name': 'Burger King', 'address': 'Tartu', 'budget': '€€', 'type': 'burger'},
        {'name': 'Sushiplaza', 'address': 'Tallinn', 'budget': '€€€', 'type': 'sushi'},
        {'name': 'Vegan Vibes', 'address': 'Tallinn', 'budget': '€', 'type': 'vegan'},
    ]

    address = address.strip().lower()
    budget = budget.strip()
    preference = preference.strip().lower()

    filtered = []
    for place in data:
        if (address in place['address'].lower() and
            place['budget'].startswith(budget) and
            preference == place['type'].lower()):
            filtered.append(place)

    return filtered

if __name__ == '__main__':
    app.run(debug=True)
