from .model_order import OrderDAO


class OrderService:
    def get_address_id(user_id):
        return OrderDAO.get_address_id(user_id)
    
    def add_address(details):
        return OrderDAO.add_address(details)
    
    def place_order(new_order):
        return OrderDAO.place_order(new_order)
    
    def get_user_orders(user_id):
        return OrderDAO.get_orders_by_user(user_id)

    def clear_cart(user_id):
        return OrderDAO.clear_cart(user_id)
    
    def get_products():
        return OrderDAO.most_sold()