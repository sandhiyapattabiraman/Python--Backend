from .model_wishlist import WishlistDAO

class WishlistService:
    def get_items(user_id):
        return WishlistDAO.get_user_wishlist(user_id)
    
    def add_item(user_id, product_id):
        return WishlistDAO.add_item(user_id, product_id)
    
    def remove_item(user_id, product_id):
        return WishlistDAO.remove_item(user_id, product_id)