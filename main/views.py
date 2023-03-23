from django.contrib.auth import logout, get_user_model, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Politician

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        my_objects = Politician.objects.filter(intercessors__email=request.user.email)
        all_objects = Politician.objects.all()
        all_objects.order_by('intercessors')
        return render(request, "index.html", {"all":all_objects, "my":my_objects})
    all_objects = Politician.objects.all()
    all_objects.order_by('intercessors')
    return render(request, "index.html", {"all": all_objects})

def log_out(request):  # Odhlášení uživatele
    if request.user.is_authenticated:
        logout(request)
        return redirect('index')
    else:
        return redirect('index')

def register(request):  # Registrace uživatele
    mail = request.POST['email']
    for n in User.objects.all():
        if mail == n.email:
            return JsonResponse({"status": "email"})

    User.objects.create_user(username=mail, email=mail,
                             password=str(request.POST['password']),
                             first_name=request.POST['name'],
                             last_name=request.POST['surname'])
    return JsonResponse({"status": "ok"})

def authenticate_by_email(email, password):  # Přilášení probíhá pomocí emailu a hesla
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(email=email)
    except UserModel.DoesNotExist:
        return None
    else:
        if user.check_password(password):
            return user
    return None


def sign_in(request):  # Přihlášení uživatele
    user = authenticate_by_email(email=request.POST['email'], password=request.POST['password'])
    if user is not None:
        login(request, user)
        return JsonResponse({"status": "ok"})

    return JsonResponse({"status": "error"})

# Chyby stránky
def handler404(request, *args, **argv):  # Stránka nenalezena
    return render(request, "error.html", {'code': 404})


def handler500(request, *args, **argv):  # Jiná chyba
    return render(request, "error.html", {'code': 500})
