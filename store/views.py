from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Category, Product

# Create your views here.

def home(request):
    return render(request, 'store/index.html')


def collections(request):
    category = Category.objects.filter(status=0)
    context = {
        'category': category
    }
    return render(request, 'store/collections.html', context)

def collectionsview(request, slug):
    if(Category.objects.filter(slug=slug, status=0)):
        products = Product.objects.filter(category__slug=slug)
        category_name = Category.objects.filter(slug=slug).first()
        context = {
            'products': products,
            'category_name': category_name
        }
        return render(request, "store/products/index.html", context)
    else:
        messages.warning(request, "No such category found")
        return redirect('collections')
