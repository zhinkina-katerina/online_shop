import uuid
from django.conf import settings

Redis = settings.REDIS


class CartManager:
    @staticmethod
    def get_or_create_cart(request):
        if not request.COOKIES.get('cart_hex'):
            cart_hex = uuid.uuid4().hex
            return cart_hex, None
        cart_hex = request.COOKIES.get('cart_hex')
        return cart_hex, Redis.hgetall(cart_hex)

    @staticmethod
    def update_cart(cart_hex, cart, item):
        if cart:
            if item['product'] in cart.keys():
                Redis.hincrby(cart_hex, item['product'], int(item['quantity']))
                return
        Redis.hset(cart_hex, item['product'], item['quantity'])

    @staticmethod
    def remove_product_from_cart(cart_hex, product_id):
        Redis.hdel(cart_hex, product_id)




