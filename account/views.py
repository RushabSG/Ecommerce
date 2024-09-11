from django.shortcuts import render
from .forms import CreateUserForm, LoginForm, UpdateUserForm
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from .token import user_tokenizer_generate
from django.template.loader import render_to_string
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# PAYMENT APP
from payment.forms import ShippingForm
from payment.models import ShippingAddress, Order, OrderItem

# Create your views here.


def register(request):

    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            # email verification setup(template)
            current_site = get_current_site(request)
            subject = "Account verification email"
            message = render_to_string(
                "account/registration/email-verification.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": user_tokenizer_generate.make_token(user),
                },
            )

            user.email_user(subject, message)

            return redirect("email-verification-sent")

    context = {"form": form}

    return render(request, "account/registration/register.html", context)


def email_verification(request, uidb64, token):

    unique_id = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=unique_id)

    # Success
    if user and user_tokenizer_generate.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("email-verification-success")

    # Failed
    else:
        return redirect("email-verification-failed")


def email_verification_sent(request):
    return render(request, "account/registration/email-verification-sent.html")


def email_verification_failed(request):
    return render(request, "account/registration/email-verification-failed.html")


def email_verification_success(request):
    return render(request, "account/registration/email-verification-success.html")


# login
def my_login(request):

    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("dashboard")
        #     else:
        #         form.add_error(None, "Invalid username or password")

        # else:
        #     form.add_error(None, "Invalid username or password")

    context = {"form": form}
    return render(request, "account/my-login.html", context=context)


# logout
def user_logout(request):
    logout(request)
    messages.success(request, "Logout successful!")
    return redirect("store")


# dashboard
@login_required(login_url="login")
def dashboard(request):
    return render(request, "account/dashboard.html")


@login_required(login_url="login")
def profile_management(request):

    user_form = UpdateUserForm(instance=request.user)
    if request.method == "POST":
        user_form = UpdateUserForm(data=request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()

            return redirect("dashboard")

    context = {"user_form": user_form}
    return render(request, "account/profile-management.html", context=context)


@login_required(login_url="login")
def delete_account(request):

    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        user.delete()
        messages.error(request, "Account Deleted")
        return redirect("store")

    return render(request, "account/delete-account.html")


@login_required(login_url="login")
def manage_shipment(request):
    try:
        # get shipping details about the user
        shipping = ShippingAddress.objects.get(user=request.user.id)
    except ShippingAddress.DoesNotExist:
        shipping = None

    form = ShippingForm(instance=shipping)
    if request.method == "POST":
        form = ShippingForm(request.POST, instance=shipping)
        if form.is_valid():
            # assign the user FK on the object
            shipping_form = form.save(commit=False)
            shipping_form.user = request.user
            shipping_form.save()

            return redirect("dashboard")

    context = {"form": form}
    return render(request, "account/manage-shipping.html", context)


# order management
@login_required(login_url="login")
def track_order(request):
    try:
        orders = OrderItem.objects.filter(user=request.user)
        context = {"orders": orders}
        return render(request, "account/track-order.html", context)
    except:
        return render(request, "account/track-order.html")
