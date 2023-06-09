from django.urls import path
from . import views

urlpatterns = [
    # "odkazy" na funkce vracející HTML soubory
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('load_details', views.load_details, name='load_details'),
    path('add_me', views.add_me, name='add_me'),
    path('remove_me', views.remove_me ,name='remove_me'),
    #Zpětná vazba
    path('feedback_site', views.feedback_site, name='feedback_site'),
    path('upload_feedback', views.upload_feedback, name='upload_feedback'),
    # funkce týkající se uživatele
    path('log_out', views.log_out, name="log_out"),
    path('register', views.register, name='register'),
    path('sign_in', views.sign_in, name='sign_in'),
]