"""Database models for Wonderland Toy Store"""

class Product:
    """Product model"""
    def __init__(self, id, name, price, description):
        self.id = id
        self.name = name
        self.price = price
        self.description = description

class Order:
    """Order model"""
    def __init__(self, id, customer_name, total_price):
        self.id = id
        self.customer_name = customer_name
        self.total_price = total_price
