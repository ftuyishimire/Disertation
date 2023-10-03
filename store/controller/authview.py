from django.shortcuts import redirect, render
from django.contrib import messages

from store.forms import CustomUserForm  # Correct the form import

def register(request):
    form = CustomUserForm()  # Correct the form instantiation
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "successfully registered!, login 2 continue")
            return redirect('/login')
    context = {'form': form}
    return render(request, 'store/auth/register.html', context)


def loginpage(request):
    return render(request, "store/auth/login.html")