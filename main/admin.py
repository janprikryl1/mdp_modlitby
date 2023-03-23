from django.contrib import admin
from .models import Politician, Feedback

admin.site.site_header = "Správce"
admin.site.site_title = "Správce stránky Modlete se!"
admin.site.index_title = "Správa uživatelů a veškerých dat v databázi"

# Register your models here.
admin.site.register(Politician)
admin.site.register(Feedback)