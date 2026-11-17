from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/<int:event_id>/register/', views.register_event, name='register_event'),
    path('success/', views.success, name='success'),
    path('organizer/signup/', views.organizer_signup, name='organizer_signup'),
    path('organizer/login/', views.organizer_login, name='organizer_login'),
    path('organizer/dashboard/', views.organizer_dashboard, name='organizer_dashboard'),
    path('organizer/create-event/', views.create_event, name='create_event'),
    path('organizer/logout/', views.organizer_logout, name='organizer_logout'),
    path('organizer/event/<int:event_id>/registrations/',views.event_registrations,name='event_registrations'),
]


