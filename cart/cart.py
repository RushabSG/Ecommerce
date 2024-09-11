from decimal import Decimal
from store.models import Product

# session for cart


class Cart:

    def __init__(self, request):

        self.session = request.session

        # returning user - obtain his/her existing session
        cart = self.session.get("session_key")

        # New user - generate a session key
        if "session_key" not in request.session:
            cart = self.session["session_key"] = {}

        self.cart = cart

    def add(self, product, product_quantity):

        product_id = str(
            product.id
        )  # to not change the product details if it is already inside the cart

        if product_id in self.cart:
            self.cart[product_id]["qty"] = product_quantity

        else:
            self.cart[product_id] = {
                "price": str(product.price),
                "qty": product_quantity,
            }

        self.session.modified = True

    def delete(self, product):
        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

    def update(self, product, qty):
        product_id = str(product)
        product_quantity = qty

        if product_id in self.cart:
            self.cart[product_id]["qty"] = product_quantity

        self.session.modified = True

    def __len__(self):

        return sum(item["qty"] for item in self.cart.values())

    def __iter__(self):

        all_product_id = self.cart.keys()

        products = Product.objects.filter(id__in=all_product_id)

        cart = self.cart.copy()  # copy session data

        for product in products:
            cart[str(product.id)]["product"] = product

        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total"] = item["price"] * item["qty"]
            yield item

    def get_total(self):
        return sum(Decimal(item["price"]) * item["qty"] for item in self.cart.values())