from django.http.response import JsonResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.contrib import messages

from store.models import Product, Cart

def addtocart(request):
    if request.method =='POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if(product_check):
                if(Cart.objects.filter(user=request.user.id, product_id=prod_id)):
                    return JsonResponse({'status': "Product already in cart"})
                else:
                    prod_qty = int(request.POST.get('product_qty'))

                    if product_check.quantity >= prod_qty:
                        Cart.objects.create(user=request.user, product_id=prod_id, product_qty=prod_qty)
                        return JsonResponse({'status': "Product added successfully"})
                    else:
                        return JsonResponse({'status': "Only" +str(product_check.quantity) + "quantity Available"})
            else:
                return JsonResponse({'status': "No such product found"})

        else:
            return JsonResponse({'status': "login to continue"})

    return redirect('/')



def viewcart(request):
    cart = Cart.objects.filter(user=request.user)
    context = {
        'cart': cart
    }
    return render(request, 'store/include/cart.html', context)


def updatecart(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if(Cart.objects.filter(user=request.user, product_id=prod_id)):
            prod_qty = int(request.POST.get('product_qty'))
            cart = Cart.objects.get(product_id=prod_id, user=request.user)
            cart.product_qty = prod_qty
            cart.save()
            return JsonResponse({'status': "updated successfully."})
    return redirect('/')


def deletecartitem(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        cartitems = Cart.objects.filter(user=request.user, product_id=prod_id)
        if cartitems.exists():
            cartitems.delete()
            return JsonResponse({'status': "Product is deleted from your cart."})
        else:
            return HttpResponseBadRequest('Cart item not found.')
    return redirect('/')
