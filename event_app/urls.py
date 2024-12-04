from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('events/', views.event_list, name='event_list'),
    path('events/admin/', views.admin_event_list, name='admin_event_list'),
    path('department/', views.department_list, name='department_list'),
    path('department/edit-department/<str:department_id>/', views.edit_department, name='edit_department'),
    path('department/create/', views.create_department, name='create_department'),
    path('department/delete/<int:department_id>/', views.delete_department, name='delete_department'),
    path('events/create/', views.create_event, name='create_event'),
    path('events/event-types/', views.event_type_list, name='event_type_list'),
    path('events/event-types/delete/<str:event_type_id>/', views.delete_event_type, name='delete_event_type'),
    path('events/event-types/edit/<str:event_type_id>/', views.edit_event_type, name='edit_event_type'),
    path('events/event-types/create/', views.create_eventType, name='create_event_type'),
    path('events/<str:event_id>/', views.event_detail, name='event_detail'),
    path('events/admin/<str:event_id>/', views.admin_event_detail, name='admin_event_detail'),
    path('events/<str:event_id>/enroll/', views.enroll_in_event, name='enroll_in_event'),
    path('events/success/<str:msg>/', views.enroll_Success, name='enroll_success'),
    path('event/<str:event_id>/enrollments/', views.EventEnrollmentsView.as_view(), name='event_enrollments'),
    path('enrollment/<int:enrollment_id>/confirm/', views.ConfirmEnrollmentView.as_view(), name='confirm_enrollment'),
]
