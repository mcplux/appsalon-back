from django.contrib import admin
from .models import User, Token

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_verified', 'is_staff')
    readonly_fields = ('password', 'last_login', 'date_joined')

@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token')
