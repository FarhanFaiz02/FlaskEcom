import random
from faker import Faker
from extensions import db
from models import ProductCategory, Product, Order, OrderDetail

fake = Faker()

# Function to create 10 products and 5 orders with random order items
def create_sample_data():
    # Drop and recreate all tables
    db.drop_all()
    db.create_all()

    # Step 1: Create Product Categories
    categories = ['Electronics', 'Clothing', 'Furniture', 'Toys', 'Sports', 'Beauty', 'Pet Supplies']
    for category_name in categories:
        category = ProductCategory(name=category_name)
        db.session.add(category)

    db.session.commit()

    # Step 2: Create 10 Products
    products = []
    for i in range(10):
        category = random.choice(ProductCategory.query.all())  # Randomly select a category

        # Generate a random image URL (you can replace this with actual URLs)
        image_url = f"https://picsum.photos/250/250?random={i}"

        product = Product(
            name=fake.word(),
            description=fake.sentence(),
            price=round(random.uniform(10, 1000), 2),  # Random price between 10 and 1000
            category_id=category.id,
            image_url=image_url  # Add the new image_url field
        )
        products.append(product)
        db.session.add(product)

    db.session.commit()

    # Step 3: Create 5 Orders
    for i in range(5):
        order = Order(
            customer_name=fake.name(),
            customer_email=fake.email(),
            customer_contact_number=fake.phone_number(),
            customer_address=fake.address(),
            total_price=0  # To be calculated later
        )
        db.session.add(order)
        db.session.commit()

        # Step 4: Create random order details for each order
        total_price = 0
        for j in range(random.randint(1, 5)):  # Each order has between 1 to 5 products
            product = random.choice(products)
            quantity = random.randint(1, 5)  # Random quantity between 1 and 5
            order_detail = OrderDetail(
                order_id=order.id,
                product_id=product.id,
                quantity=quantity
            )
            db.session.add(order_detail)
            total_price += product.price * quantity

        # Update the order's total price after adding all the products
        order.total_price = round(total_price, 2)
        db.session.commit()

    return "Sample data created successfully!"


if __name__ == '__main__':
    create_sample_data()
