from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from .models import Service
from .forms import BulkAddForm

# Register your models here.
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    change_list_template = 'admin/service_change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('bulk_add/', self.admin_site.admin_view(self.bulk_add))
        ]
        return custom_urls + urls

    def bulk_add(self, request):
        if request.method == 'POST':
            form = BulkAddForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data['data'].splitlines()
                for line in data:
                    name, price = line.split(',')
                    Service.objects.create(name=name.strip(), price=float(price.strip()))
                self.message_user(request, "Successfully added records.")
                return redirect('..')
        else:
            form = BulkAddForm()
        return render(request, 'admin/bulk_add_form.html', {'form': form})
