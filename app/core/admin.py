from django.contrib import admin
from core import models
# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Movie)
admin.site.register(models.Rating)