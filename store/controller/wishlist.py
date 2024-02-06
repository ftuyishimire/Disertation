from django.shortcuts import get_object_or_404
from django.core.exceptions import MultipleObjectsReturned
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from store.models import Wishlist, Product


@login_required(login_url='login')
def index(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    context = {'wishlist':wishlist}
    return render(request, 'store/wishlist.html', context)


def addtowishlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if(product_check):
                if(Wishlist.objects.filter(user=request.user, product_id=prod_id)):
                    return JsonResponse({'status':"Product is already on the wishlist"})
                else:
                    Wishlist.objects.create(user=request.user, product_id=prod_id)
                    return JsonResponse({'status': "Product wishlisted"})
            else:
                return JsonResponse({'status':"No such product found"})
        else:
            return JsonResponse({'status':"Login to proceed"})
    return redirect('/')

def deletewishlistitem(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))

            try:
                # Use filter to retrieve the Wishlist items for a specific product
                wishlist_items = Wishlist.objects.filter(user=request.user, product_id=prod_id)
                
                # If there are multiple items, delete each one individually
                for item in wishlist_items:
                    item.delete()
                
                # Return success response
                return JsonResponse({'status': 'Product removed from wishlist successfully'})
            
            except Wishlist.DoesNotExist:
                # If no items are found, return an error response
                return JsonResponse({'status': 'Product not found in wishlist'}, status=404)
            except MultipleObjectsReturned:
                # If multiple items are found, handle the situation as needed
                return JsonResponse({'status': 'Multiple items found for the product'}, status=500)
            except Exception as e:
                # Handle other exceptions
                return JsonResponse({'status': str(e)}, status=500)
        else:
            return JsonResponse({'status': "Login to continue"})

    return redirect('/')