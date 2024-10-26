from extensions import db

# ProductCategory model to store product categories
class ProductCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)  # Category name


# Updated Product model with category relationship
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('product_category.id'), nullable=False)
    image_url = db.Column(db.String(255), nullable=True)  # New field for storing image URL

    # Relationship to access the category of the product
    category = db.relationship('ProductCategory', backref=db.backref('products', lazy=True))


# Order model for customer orders
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(100), nullable=False)
    customer_contact_number = db.Column(db.String(100), nullable=False)
    customer_address = db.Column(db.String(200), nullable=False)
    total_price = db.Column(db.Float, nullable=False)


# OrderDetail model to store individual items within an order
class OrderDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Foreign keys for order and product references
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    # Quantity of the product in the order
    quantity = db.Column(db.Integer, nullable=False)

    # Relationships to access the order and product details
    order = db.relationship('Order', backref=db.backref('order_details', lazy=True))
    product = db.relationship('Product', backref=db.backref('order_details', lazy=True))