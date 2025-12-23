# 🎀 Wonderland Toy Store

A full-featured e-commerce web application built with Flask and SQLAlchemy. This project demonstrates a complete toy store platform with user authentication, product management, shopping cart functionality, order processing, and administrative dashboard.

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-GPL2-blue.svg)](LICENSE)

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Docker Setup](#docker-setup)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Database Models](#database-models)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### User Features
- **User Authentication**: Registration, login, and logout functionality
- **Product Browsing**: Browse products by category with detailed product information
- **Shopping Cart**: Add/remove items, update quantities, persistent cart management
- **Wishlist**: Save favorite products for later purchase
- **Order Management**: View order history, track orders, and manage order status
- **User Dashboard**: Personal dashboard with profile information and order history
- **Password Recovery**: Forgot password and reset password functionality
- **Profile Management**: Update user information and preferences

### Admin Features
- **Admin Dashboard**: Comprehensive dashboard with analytics and statistics
- **Product Management**: Create, edit, and delete products with image uploads
- **Order Management**: View and manage all customer orders
- **User Management**: Manage customer accounts and permissions
- **Category Management**: Create and organize product categories
- **Inventory Management**: Track product stock and availability

### Additional Features
- **Responsive Design**: Mobile-friendly interface using modern CSS
- **Image Upload**: Support for product image uploads with validation
- **Database Seeding**: Automated database initialization with sample data
- **Session Management**: Secure user session handling
- **Error Handling**: Comprehensive error handling and validation

## 🛠️ Tech Stack

- **Backend**: [Flask](https://flask.palletsprojects.com/) 2.3.3
- **Database**: SQLAlchemy 2.0.23 with SQLite/PostgreSQL support
- **Authentication**: Flask-Login 0.6.3
- **Frontend**: HTML5, CSS3, JavaScript
- **Server**: Gunicorn (production)
- **Containerization**: Docker & Docker Compose
- **Python**: 3.8+

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher**: [Download Python](https://www.python.org/downloads/)
- **pip**: Python package manager (comes with Python)
- **Git**: For version control
- **Docker** (optional): [Install Docker](https://www.docker.com/products/docker-desktop)

Verify your installation:
```bash
python --version
pip --version
```

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/hasanzafzal/Wonderland-Toy-Store.git
cd Wonderland-Toy-Store
```

### 2. Create a Virtual Environment

**On macOS and Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs all required packages including:
- Flask 2.3.3
- Flask-SQLAlchemy 3.0.5
- Flask-Login 0.6.3
- SQLAlchemy 2.0.23
- Gunicorn 20.1.0+

### 4. Initialize the Database

The database will be automatically initialized when you run the application. The `start.sh` script handles database seeding with sample data.

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root (optional):

```bash
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///instance/wonderland.db
MAX_FILE_SIZE=5242880
```

### Database Configuration

The application uses SQLite by default. To use PostgreSQL, update the database URL in your configuration:

```python
DATABASE_URL=postgresql://username:password@localhost:5432/wonderland_db
```

## 🏃 Running the Application

### Standard Execution

1. Activate the virtual environment (if not already activated)
2. Run the application:

```bash
python run.py
```

The application will start on `http://localhost:5000`

### Using the Startup Script

```bash
chmod +x start.sh
./start.sh
```

This script automatically:
- Seeds the database with sample data
- Starts the Flask development server

### Production Deployment

For production, use Gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## 🐳 Docker Setup

### Build and Run with Docker

1. **Build the Docker image:**

```bash
docker build -t wonderland-toy-store .
```

2. **Run the container:**

```bash
docker run -p 5000:5000 -v $(pwd)/instance:/app/instance wonderland-toy-store
```

### Docker Compose

For a complete setup with services, use Docker Compose:

```bash
docker-compose up -d
```

Access the application at `http://localhost:5000`

To stop the containers:

```bash
docker-compose down
```

## 📁 Project Structure

```
Wonderland-Toy-Store/
├── app/                          # Main application package
│   ├── __init__.py              # Flask app initialization
│   ├── app.py                   # Application configuration
│   ├── models.py                # Database models
│   ├── routes.py                # API routes and views
│   ├── static/                  # Static files
│   │   ├── css/
│   │   │   └── style.css        # Main stylesheet
│   │   ├── images/
│   │   │   └── products/        # Product images directory
│   │   └── js/
│   │       └── script.js        # Frontend JavaScript
│   └── templates/               # HTML templates
│       ├── base.html            # Base template
│       ├── index.html           # Homepage
│       ├── products.html        # Product listing
│       ├── cart.html            # Shopping cart
│       ├── checkout.html        # Checkout page
│       ├── login.html           # Login page
│       ├── register.html        # Registration page
│       ├── dashboard.html       # User dashboard
│       ├── orders.html          # Order history
│       ├── wishlist.html        # Wishlist page
│       ├── admin/               # Admin templates
│       │   ├── dashboard.html   # Admin dashboard
│       │   ├── products.html    # Product management
│       │   ├── orders.html      # Order management
│       │   └── users.html       # User management
│       └── ...                  # Other templates
├── instance/                    # Instance folder (database, config)
├── run.py                       # Application entry point
├── seed_data.py                 # Database seeding script
├── start.sh                     # Startup script
├── requirements.txt             # Python dependencies
├── pyproject.toml              # Project metadata
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose configuration
└── README.md                   # This file
```

## 🔌 API Endpoints

### Authentication
- `GET/POST /register` - User registration
- `GET/POST /login` - User login
- `GET /logout` - User logout
- `GET/POST /forgot_password` - Password recovery request
- `GET/POST /reset_password/<token>` - Reset password with token

### Products
- `GET /products` - List all products
- `GET /products/<product_id>` - Get product details
- `GET /category/<category_id>` - Products by category
- `GET/POST /products/search` - Search products

### Shopping Cart
- `GET /cart` - View shopping cart
- `POST /cart/add/<product_id>` - Add item to cart
- `POST /cart/update/<item_id>` - Update cart item quantity
- `POST /cart/remove/<item_id>` - Remove item from cart

### Orders
- `GET /orders` - View user orders
- `GET /orders/<order_id>` - Order details
- `GET/POST /checkout` - Checkout page and process payment

### Wishlist
- `GET /wishlist` - View wishlist
- `POST /wishlist/add/<product_id>` - Add to wishlist
- `POST /wishlist/remove/<product_id>` - Remove from wishlist

### Admin
- `GET /admin/dashboard` - Admin dashboard
- `GET/POST /admin/products` - Manage products
- `GET /admin/orders` - Manage orders
- `GET /admin/users` - Manage users

## 💾 Database Models

### User
```python
- id: Integer (Primary Key)
- username: String (Unique)
- email: String (Unique)
- password_hash: String
- created_at: DateTime
- updated_at: DateTime
- is_admin: Boolean
```

### Product
```python
- id: Integer (Primary Key)
- name: String
- description: Text
- price: Float
- stock: Integer
- category_id: Integer (Foreign Key)
- image_filename: String
- is_featured: Boolean
- created_at: DateTime
```

### Category
```python
- id: Integer (Primary Key)
- name: String (Unique)
- description: Text
- created_at: DateTime
```

### Order
```python
- id: Integer (Primary Key)
- user_id: Integer (Foreign Key)
- total_price: Float
- status: String
- created_at: DateTime
- updated_at: DateTime
```

### Cart & CartItem
```python
- Cart: id, user_id, created_at
- CartItem: id, cart_id, product_id, quantity
```

### Wishlist
```python
- id: Integer (Primary Key)
- user_id: Integer (Foreign Key)
- product_id: Integer (Foreign Key)
- created_at: DateTime
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the Repository**
   ```bash
   git clone https://github.com/hasanzafzal/Wonderland-Toy-Store.git
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make Your Changes**
   - Write clean, readable code
   - Follow PEP 8 style guidelines
   - Add comments for complex logic

4. **Commit Your Changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```

5. **Push to the Branch**
   ```bash
   git push origin feature/amazing-feature
   ```

6. **Open a Pull Request**
   - Describe your changes clearly
   - Reference any related issues

## 📝 License

This project is licensed under the GNU General Public License v2.0 - see the [LICENSE](LICENSE) file for details.

## 🙋 Support

If you encounter any issues or have questions:

1. Check the [GitHub Issues](https://github.com/hasanzafzal/Wonderland-Toy-Store/issues)
2. Create a new issue with a detailed description
3. Include steps to reproduce the problem

## 📧 Contact

For inquiries and feedback, please reach out to:
- **Email**: your-email@example.com
- **GitHub**: [@hasanzafzal](https://github.com/hasanzafzal)

---

**Happy coding! 🚀** Built with ❤️ for e-commerce lovers
