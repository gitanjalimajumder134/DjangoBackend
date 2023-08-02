from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .models import User

# admin.site.register(User, UserAdmin)

admin.site.register(Answer)

admin.site.register(Question)

admin.site.register(Quizzes)

admin.site.register(Category)