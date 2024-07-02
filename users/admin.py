from django.contrib import admin
from .models import User, Token

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'is_verified', 'is_admin')

@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token')
