from django.urls import path
from django.views.decorators.cache import never_cache

from . import views

urlpatterns = [
    # "odkazy" na funkce vracející HTML soubory
    path('', views.index, name='index'),
    # funkce týkající se uživatele
    path('log_out', views.log_out, name="log_out"),
    path('register', views.register, name='register'),
    path('sign_in', views.sign_in, name='sign_in'),
]