from django.shortcuts import render
from .models import ShippingAddress, Order, OrderItem
from cart.cart import Cart
from django.http import JsonResponse


# Create your views here.
def checkout(request):

    if request.user.is_authenticated:

        try:
            # users with shipping address
            shipping = ShippingAddress.objects.get(user=request.user.id)
            context = {"shipping": shipping}
            return render(request, "payment/checkout.html", context)

        except:
            # authenticated users without shipping address
            return render(request, "payment/checkout.html")

    # guest user
    return render(request, "payment/checkout.html")


def complete_checkout(request):

    if request.POST.get("action") == "post":
        name = request.POST.get("name")
        email = request.POST.get("email")
        mobile_number = request.POST.get("mobile_number")
        address1 = request.POST.get("address1")
        address2 = request.POST.get("address2")
        city = request.POST.get("city")
        state = request.POST.get("state")
        zipcode = request.POST.get("zipcode")

        shipping_address = (
            address1 + "\n" + address2 + "\n" + city + "," + state + "\n" + zipcode
        )

        # shopping cart information
        cart = Cart(request)

        # total price of items
        total = cart.get_total()

        """
            order variations

            1) Create Order -> with or without shipping information
            2) Create order -> with guest users

        """

        # 1) Create Order -> with or without shipping information

        if request.user.is_authenticated:
            order = Order.objects.create(
                full_name=name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=total,
                user=request.user,
            )

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    quantity=item["qty"],
                    price=item["price"],
                    user=request.user,
                )

        # 2) Create order -> with guest users
        else:
            order = Order.objects.create(
                full_name=name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=total,
            )

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    quantity=item["qty"],
                    price=item["price"],
                )

        order_success = True
        response = JsonResponse({"success": order_success})
        return response


def payment_success(request):

    # clear cart data
    for key in list(request.session.keys()):
        if key == "session_key":
            del request.session[key]

    return render(request, "payment/payment-success.html")


def payment_failed(request):
    return render(request, "payment/payment-failure.html")
