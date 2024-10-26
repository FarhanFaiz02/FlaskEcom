import os
from flask import Flask, render_template, redirect, url_for, session, request, flash
from sqlalchemy import func
from extensions import db
from models import Product, ProductCategory, Order, OrderDetail
from factory import create_sample_data
from flask_bootstrap import Bootstrap4
from forms import CheckoutForm

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '#56B9ckFVYkN')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the db with the app
db.init_app(app)

bootstrap = Bootstrap4(app)

@app.route('/')
def index():
    products = Product.query.order_by(func.random()).limit(8).all()  # Fetch 10 random products
    categories = ProductCategory.query.all()
    return render_template('index.html', products=products, categories=categories)


@app.route('/search')
def search():
    query = request.args.get('search')  # Get the search query from the request
    if query:
        # Filter products based on the search query
        products = Product.query.filter(Product.name.ilike(f'%{query}%')).all()
    else:
        products = []  # If no query, return an empty list

    return render_template('search_results.html', products=products, query=query)


@app.route('/shop', defaults={'category_id': None})
@app.route('/shop/<int:category_id>')
def shop(category_id):
    if category_id:
        # Check if the category exists
        category = ProductCategory.query.get(category_id)
        if category:
            # Fetch products that belong to the given category
            products = Product.query.filter_by(category_id=category_id).all()
        else:
            # If category_id is invalid, flash a message and fetch all products
            flash('Invalid category selected.', 'danger')
            products = Product.query.all()
    else:
        # If no category_id is provided, fetch all products
        products = Product.query.all()

    categories = ProductCategory.query.all()  # Fetch all categories for filtering

    return render_template('shop.html', products=products, categories=categories, selected_category=category_id)


# Route to view individual product details
@app.route('/product/<int:product_id>')
def product(product_id):
    product = Product.query.get_or_404(product_id)  # Fetch the product or return 404 if not found
    return render_template('product.html', product=product)


@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])  # Retrieve cart from session, or an empty list if not set
    # Query products in the cart
    products = Product.query.filter(Product.id.in_(cart_items)).all()
    # Calculate the total price
    total_price = sum(product.price for product in products)
    # Pass products and total price to the template
    return render_template('cart.html', products=products, total_price=total_price)


@app.route('/cart/<int:product_id>')
def add_to_cart(product_id):
    # Example logic to add a product to the cart
    product = Product.query.get(product_id)
    if product:
        cart = session.get('cart', [])
        if product_id not in cart:
            cart.append(product_id)  # Add the product_id to the cart if it's not already there
            session['cart'] = cart  # Save the updated cart back to the session
            flash('Product added to cart!', 'success')
    else:
        flash('Product not found!', 'danger')

    return redirect(request.referrer or url_for('index'))


@app.route('/cart/remove/<int:product_id>')
def remove_from_cart(product_id):
    # Check if a cart exists in the session
    if 'cart' in session:
        cart = session['cart']
        # If the product is in the cart, remove it
        if product_id in cart:
            cart.remove(product_id)
            session['cart'] = cart  # Update the session with the new cart
            flash('Product removed from cart', 'success')
        else:
            flash('Product not found in cart', 'danger')
    else:
        flash('Cart is empty', 'info')

    # Redirect the user back to the cart page
    return redirect(url_for('cart'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():

    form = CheckoutForm()

    if request.method == 'POST':

        if form.validate_on_submit():
            # Calculate the total price of the cart
            cart_items = session.get('cart', [])
            products = Product.query.filter(Product.id.in_(cart_items)).all()

            # Calculate total price and organize cart items with quantities if needed
            total_price = 0
            cart_product_quantities = {}

            for product_id in cart_items:
                if product_id in cart_product_quantities:
                    cart_product_quantities[product_id] += 1
                else:
                    cart_product_quantities[product_id] = 1

            # Calculate the total price based on products and their quantities
            for product in products:
                total_price += product.price * cart_product_quantities[product.id]

            # Create a new order
            new_order = Order(
                customer_name=form.full_name.data,
                customer_email=form.email.data,
                customer_contact_number=form.contact_number.data,
                customer_address=form.address.data,
                total_price=total_price
            )

            # Add the order to the session but don’t commit yet
            db.session.add(new_order)
            db.session.flush()  # Get the order ID for order details before committing

            # Add each cart item to the OrderDetail table
            for product_id, quantity in cart_product_quantities.items():
                order_detail = OrderDetail(
                    order_id=new_order.id,
                    product_id=product_id,
                    quantity=quantity
                )
                db.session.add(order_detail)

            # Commit the order and order details to the database
            db.session.commit()

            # Clear the session cart after placing the order
            session.pop('cart', None)

            flash('Order placed successfully!', 'success')
            return redirect(url_for('index'))


        else:

            # Add this to see if the form has validation issues
            flash('Form validation failed', 'danger')
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')

    return render_template('checkout.html', form=form)


@app.route('/factory')
def factory():
    create_sample_data()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
