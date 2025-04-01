from .model_product import ProductDAO , Product


class ProductService:
    def get_products():
        return ProductDAO.get_products()
    
    def post_products(create_product):
        new_product = Product(**create_product.model_dump(),)
        return ProductDAO.create_product(new_product)