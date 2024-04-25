from django.contrib import admin
from .models import people
from .models import feedback

# Register your models here.
admin.site.register(people)
admin.site.register(feedback)