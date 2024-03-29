import random
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from store.models import Cart, Order, OrderItem, Product, Profile
from django.contrib.auth.models import User


@login_required(login_url='login')
def index(request):
    rawcart = Cart.objects.filter(user=request.user)
    for item in rawcart:
        if item.product_qty > item.product.quantity:
            Cart.objects.filter(id=item.id).delete()

    cartitems = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cartitems:
        total_price = total_price + item.product.selling_price * item.product_qty

        userprofile= Profile.objects.filter(user=request.user).first()

    context = {'cartitems': cartitems, 'total_price': total_price, 'userprofile':userprofile}
    return render(request, "store/checkout.html", context)

@login_required(login_url='login')
def placeorder(request):
    if request.method == 'POST':
        #autofill the details for the user in the form during checkout the products.
        currentuser = User.objects.filter(id=request.user.id).first()

        if not currentuser.first_name:
            currentuser.first_name = request.POST.get('fname')
            currentuser.last_name = request.POST.get('lname')
            currentuser.save()
        
        if not Profile.objects.filter(user=request.user):
            userprofile = Profile()
            userprofile.user = request.user
            userprofile.phone = request.POST.get('phone')
            userprofile.address = request.POST.get('address')
            userprofile.city = request.POST.get('city')
            userprofile.state = request.POST.get('state')
            userprofile.country = request.POST.get('country')
            userprofile.pincode = request.POST.get('pincode')
            userprofile.save()

        neworder = Order()
        neworder.user = request.user
        neworder.fname = request.POST.get('fname')
        neworder.lname = request.POST.get('lname')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('phone')
        neworder.address = request.POST.get('address')
        neworder.city = request.POST.get('city')
        neworder.state = request.POST.get('state')
        neworder.country = request.POST.get('country')
        neworder.pincode = request.POST.get('pincode')

        neworder.payment_mode = request.POST.get('payment_mode')
        neworder.payment_id = request.POST.get('payment_id')


        cart = Cart.objects.filter(user=request.user)
        cart_total_price = 0
        for item in cart:
            cart_total_price = cart_total_price + item.product.selling_price * item.product_qty

        neworder.total_price = cart_total_price

        # Generate a unique tracking number
        while True:
            track_no = 'Chezbs' + str(random.randint(1111111, 9999999))
            if not Order.objects.filter(tracking_no=track_no).exists():
                break

        neworder.tracking_no = track_no
        neworder.save()

        neworderitems = Cart.objects.filter(user=request.user)
        for item in neworderitems:
            OrderItem.objects.create(
                order=neworder,
                product=item.product,
                price=item.product.selling_price,
                quantity=item.product_qty
            )
            # Decreasing product quantity from the stock
            orderproduct = Product.objects.filter(id=item.product_id).first()
            orderproduct.quantity = orderproduct.quantity - item.product_qty
            orderproduct.save()

        # Clear the user's cart
        Cart.objects.filter(user=request.user).delete()
        messages.success(request, "Your order has been placed successfully")

        payMode = request.POST.get('payment_mode')
        if (payMode == "Paid by PayPal"):
            return JsonResponse({'status': "Your orders has been placed"})
        else:
            messages.success(request, "Your order has been placed successfull")
    return redirect('/')
    






@login_required(login_url='login')
def paypalcheckout(request):
    cart = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cart:
        total_price += item.product.selling_price * item.product_qty

    return JsonResponse({
        "total_price": total_price
    })


def orders(request):
    return HttpResponse("My-orders Page")


