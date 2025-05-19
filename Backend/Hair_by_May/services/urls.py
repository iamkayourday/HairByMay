from django.urls import path
from .views import (
    ServiceCreateView, ServiceUpdateView, ServiceDeleteView,
    ServiceListView, ServiceDetailView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    CategoryListView, CategoryDetailView, AppointmentOptionCreateView, AppointmentOptionUpdateView, AppointmentOptionDeleteView,
    AppointmentOptionListView, AppointmentOptionDetailView, BookingCreateView, BookingUpdateView,
    BookingListView, BookingDetailView, BookingUserListView, BookingCancelView, ContactCreateView, ContactListView, BookingPaymentView
)

urlpatterns = [
    # SERVICES URLS
    path('services/', ServiceListView.as_view(), name='service-list'),
    path('services/<uuid:pk>/', ServiceDetailView.as_view(), name='service-detail'),
    path('services/create/', ServiceCreateView.as_view(), name='service-create'),
    path('services/update/<uuid:pk>/', ServiceUpdateView.as_view(), name='service-update'),
    path('services/delete/<uuid:pk>/', ServiceDeleteView.as_view(), name='service-delete'),

    # CATEGORIES URLS
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<uuid:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('categories/create/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/update/<uuid:pk>/', CategoryUpdateView.as_view(), name='category-update'),
    path('categories/delete/<uuid:pk>/', CategoryDeleteView.as_view(), name='category-delete'),

    # APPOINTMENT OPTIONS URLS
    path('appointment-options/', AppointmentOptionListView.as_view(), name='appointment-option-list'),
    path('appointment-options/<uuid:pk>/', AppointmentOptionDetailView.as_view(), name='appointment-option-detail'),
    path('appointment-options/create/', AppointmentOptionCreateView.as_view(), name='appointment-option-create'),
    path('appointment-options/update/<uuid:pk>/', AppointmentOptionUpdateView.as_view(), name='appointment-option-update'),
    path('appointment-options/delete/<uuid:pk>/', AppointmentOptionDeleteView.as_view(), name='appointment-option-delete'),
    
    # BOOKINGS URLS
    path('bookings/', BookingListView.as_view(), name='booking-list'),
    path('bookings/<uuid:pk>/', BookingDetailView.as_view(), name='booking-detail'),
    path('bookings/create/', BookingCreateView.as_view(), name='booking-create'),
    path('bookings/update/<uuid:pk>/', BookingUpdateView.as_view(), name='booking-update'),
    path('bookings/user/', BookingUserListView.as_view(), name='booking-user-list'),
    path('bookings/cancel/<uuid:pk>/', BookingCancelView.as_view(), name='booking-cancel'),
    path('contact/', ContactCreateView.as_view(), name='contact-submission'),
    path('contact/list/', ContactListView.as_view(), name='contact-list'),
    path('bookings/<uuid:booking_id>/pay/', BookingPaymentView.as_view()),
]

