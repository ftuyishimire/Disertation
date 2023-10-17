import random
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from store.models import Cart, Order, OrderItem, Product, Profile
from django.contrib.auth.models import User
from django.urls import reverse

@login_required(login_url='login')
def index(request):
    cartitems = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.selling_price * item.product_qty for item in cartitems)

    userprofile = Profile.objects.filter(user=request.user).first()

    context = {'cartitems': cartitems, 'total_price': total_price, 'userprofile': userprofile}
    return render(request, "store/checkout.html", context)

@login_required(login_url='login')
def placeorder(request):
    if request.method == 'POST':
        try:
            currentuser = User.objects.get(id=request.user.id)

            if not currentuser.first_name:
                currentuser.first_name = request.POST.get('fname')
                currentuser.last_name = request.POST.get('lname')
                currentuser.save()

            userprofile, created = Profile.objects.get_or_create(user=request.user)
            userprofile.phone = request.POST.get('phone')
            userprofile.address = request.POST.get('address')
            userprofile.city = request.POST.get('city')
            userprofile.state = request.POST.get('state')
            userprofile.country = request.POST.get('country')
            userprofile.pincode = request.POST.get('pincode')
            userprofile.save()

            neworder = Order(user=request.user, fname=request.POST.get('fname'), lname=request.POST.get('lname'), email=request.POST.get('email'),
                             phone=request.POST.get('phone'), address=request.POST.get('address'), city=request.POST.get('city'), state=request.POST.get('state'),
                             country=request.POST.get('country'), pincode=request.POST.get('pincode'), payment_mode=request.POST.get('payment_mode'))

            neworder.save()

            cart = Cart.objects.filter(user=request.user)
            cart_total_price = sum(item.product.selling_price * item.product_qty for item in cart)

            neworder.total_price = cart_total_price
            neworder.tracking_no = 'Chezbs' + str(random.randint(1111111, 9999999))
            neworder.save()

            for item in cart:
                OrderItem.objects.create(order=neworder, product=item.product, price=item.product.selling_price, quantity=item.product_qty)

                # Decrease product quantity from the stock
                orderproduct = Product.objects.get(id=item.product_id)
                orderproduct.quantity -= item.product_qty
                orderproduct.save()

            # Clear the user's cart
            cart.delete()
            messages.success(request, "Your order has been placed successfully")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    return redirect(reverse('index'))
