from flask import Flask, render_template, jsonify, session, redirect, url_for, request
import json
import os

app = Flask(__name__)
# A secret key is required for Flask to use 'sessions' (to remember the user's cart)
app.secret_key = 'gunters_forge_secret'

# Route to serve the main blacksmith shop page
@app.route('/')
def home():
    return render_template('index.html')

# Route for the individual buy page
@app.route('/buy/<item_name>')
def buy_page(item_name):
    # Passes the name of the item to the HTML template so it knows what to display
    return render_template('buy.html', item_name=item_name)

# Route that secretly handles adding the item to the cart, then sends you to the cart page
@app.route('/add_to_cart/<item_name>', methods=['POST'])
def add_to_cart(item_name):
    # If the user doesn't have a cart yet, create an empty one
    if 'cart' not in session:
        session['cart'] = []
    
    # Add the item to the cart and save it back to the session
    cart = session['cart']
    cart.append(item_name)
    session['cart'] = cart
    
    # Send the user to the cart page to see their updated cart
    return redirect(url_for('view_cart'))

# Route to view everything in the cart
@app.route('/cart')
def view_cart():
    # Grab the cart from the session, or an empty list if it doesn't exist
    cart_items = session.get('cart', [])
    return render_template('cart.html', cart=cart_items)

# Optional: Sample backend route to read your orders.json file
@app.route('/api/orders', methods=['GET'])
def get_orders():
    data_path = os.path.join('data', 'orders.json')
    if os.path.exists(data_path):
        with open(data_path, 'r') as f:
            orders = json.load(f)
        return jsonify(orders)
    return jsonify([])

if __name__ == '__main__':
    app.run(port=3000, debug=True)