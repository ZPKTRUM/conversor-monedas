from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
API_KEY = '237542de277150060d4457c4'
API_URL = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    base = data['base']
    target = data['target']
    amount = float(data['amount'])

    response = requests.get(API_URL + base)
    if response.status_code != 200:
        return jsonify({'error': 'API request failed'}), 500

    rates = response.json().get('conversion_rates')
    if not rates or target not in rates:
        return jsonify({'error': 'Invalid target currency'}), 400

    converted_amount = amount * rates[target]
    return jsonify({'result': round(converted_amount, 2)})

if __name__ == '__main__':
    app.run(debug=True)