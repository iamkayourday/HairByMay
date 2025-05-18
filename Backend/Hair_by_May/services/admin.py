from django.contrib import admin
from .models import Service, Category,AppointmentOption, Booking


# Register your models here.
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'duration', 'description')
    search_fields = ('title',)
    ordering = ('title',)
    list_per_page = 10

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name',)
    search_fields = ('name',)
    ordering = ('name',)
    list_per_page = 10

class AppointmentOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'extra_cost', 'extra_duration')
    search_fields = ('name',)
    ordering = ('name',)
    list_per_page = 10

class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'full_name', 'email', 'phone', 'preferred_date', 'preferred_time', 'status')
    search_fields = ('full_name', 'email', 'phone')
    list_filter = ('status',)
    ordering = ('-created_at',)
    list_per_page = 10

# Register your models here.
admin.site.register(Service, ServiceAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(AppointmentOption, AppointmentOptionAdmin)