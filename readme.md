# FlaskEcom

## Project Overview

FlaskEcom is an e-commerce platform built with **HTML, CSS, Flask Bootstrap, Python, Flask, Jinja2 Flask-WTForm, Flask
SQLAlchemy**. This documentation provides the steps to set up, install, and run the project in a local environment.

Project Scopes

- Factory route to generate dummy data
- Product classification based on category
- Bootstrap based responsive basic frontend
- Homepage to showcase random products, products categories & banner
- Shop page to display products based on category
- Product details page to display product details along with related products
- Add to cart functionality with session-based cart storage
- Cart page to display cart items
- Checkout page to process order with WTForm based checkout form
- Product search functionality with dedicated search result page
- Random dummy image generation for product images

## Setup Instructions

### 1. Clone the Repository

Clone the FlaskEcom repository:

```bash
git clone https://github.com/FarhanFaiz02/FlaskEcom.git
cd FlaskEcom
```

### 2. Set Up a Virtual Environment

Create and activate a Python virtual environment:

```bash
python -m venv venv
```

Activate the environment:

- **Linux/macOS**: `source venv/bin/activate`
- **Windows**: `venv\Scripts\activate`

### 3. Install Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory and set up the necessary environment variables (example):

```dotenv
SECRET_KEY=MaBOhhsMUM7s5YdtomK5rmqQDJqWl1dy5
DATABASE_URL=mysql+pymysql://<username>:<password>@<host>/<database_name>
```

> **Note**: Replace `<username>`, `<password>`, `<host>`, and `<database_name>` with your actual MySQL database
> credentials.

### 5. Create the MySQL Database

Using your MySQL client or command line, create the database specified in your `.env` file:

```sql
CREATE DATABASE pythonEcommerce;
```

### 6. Initialize the Database with Tables and Dummy Data

Once the database is set up, start the Flask application:

```bash
flask run
```

Then navigate to the following URL in your browser:

```
http://127.0.0.1:5000/factory
```

This route will automatically create all tables based on the models and populate them with initial dummy data for
testing.

### 7. Run the Application

To access the application, navigate to:

```
http://127.0.0.1:5000
```

---

This setup ensures all necessary steps are in place for installing, configuring, and running the FlaskEcom project on a
local machine.

### Preapared by: Faizullah Farhan