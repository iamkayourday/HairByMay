from django.db import models
from django.conf import settings
import uuid
# Create your models here.

# AppointmentOption model to define additional options for appointments
# This model is used to define additional options for appointments
class AppointmentOption(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    name = models.CharField(max_length=100, blank=True)
    extra_cost = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    extra_duration = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

# Service model to define the services offered
# This model is used to define the services offered by the salon
class Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    duration = models.CharField(max_length=100)
    description = models.TextField()
    appointment_options = models.ManyToManyField(AppointmentOption, blank=True)

    def __str__(self):
        return self.title
    
# Category model to group services
# This model is used to categorize services for better organization
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    name = models.CharField(max_length=100)
    services = models.ManyToManyField(Service, related_name="categories")

    def __str__(self):
        return self.name

# Booking model to handle appointments 
class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    selected_options = models.ManyToManyField(AppointmentOption, blank=True)  # Allow multiple choices
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    special_instructions = models.TextField(blank=True, null=True)
    payment_status = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=[
        ('pending', 'Pending'), ('confirmed', 'Confirmed'), ('canceled', 'Canceled'), ('completed', 'Completed')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking for {self.full_name} - {self.service.title}"
