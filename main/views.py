from django.contrib.auth import logout, get_user_model, login
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from .models import Politician, Feedback


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        my_objects = Politician.objects.filter(intercessors__email=request.user.email)
        all_objects = Politician.objects.all()
        all_objects.order_by('intercessors')
        return render(request, "index.html", {"all": all_objects, "my": my_objects})
    all_objects = Politician.objects.all()
    all_objects.order_by('intercessors')
    return render(request, "index.html", {"all": all_objects})


def load_details(request):
    politican = Politician.objects.get(id=int(request.POST['id']))
    intercessors = list(politican.intercessors.values('first_name', 'last_name'))
    return JsonResponse({"name": politican.__str__(), "position": politican.position, "intercessors": intercessors})


def log_out(request):  # Odhlášení uživatele
    if request.user.is_authenticated:
        logout(request)
        return redirect('index')
    else:
        return redirect('index')


def add_me(request):
    politican = Politician.objects.get(id=int(request.POST['id']))
    if not politican.intercessors.contains(request.user):
        politican.intercessors.add(request.user)
        return JsonResponse({"name": politican.name, "surname": politican.surname, "position": politican.position})
    return JsonResponse({"yet": True})


def remove_me(request):
    politican = Politician.objects.get(id=int(request.POST['id']))
    if politican.intercessors.contains(request.user):
        politican.intercessors.remove(request.user)
    return HttpResponse()


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


# Zpětná vazba
def feedback_site(request):
    return render(request, "feedback.html")


def upload_feedback(request):  # Uložení zpětné vazby
    if request.user.is_authenticated:
        f = Feedback(e_mail=request.POST['email'], subject=request.POST['subject'], text=request.POST['message'],
                     user=request.user)  # Vytvoření modelu Feedback
    else:
        f = Feedback(e_mail=request.POST['email'], subject=request.POST['subject'],
                     text=request.POST['message'])  # Vytvoření modelu Feedback
    f.save()  # Uložení modelu
    return HttpResponse()


# Chyby stránky
def handler404(request, *args, **argv):  # Stránka nenalezena
    return render(request, "error.html", {'code': 404})


def handler500(request, *args, **argv):  # Jiná chyba
    return render(request, "error.html", {'code': 500})
