from datetime import datetime
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from .models import Department, Event, Enrollment, EventImage, EventType, Notification
from .forms import DepartmentForm, EventForm, EventTypeForm, UserRegistrationForm, EnrollmentForm, EnrollmentConfirmationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('event_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff:
                return redirect('admin_event_list')
            return redirect('event_list')
        else:
            print("Form errors:", form.errors)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')

def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def create_event(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.save()
            images = request.FILES.getlist('images')
            for image in images:
                EventImage.objects.create(event=event, image=image)

            return redirect('admin_event_detail', event_id=event.event_id)
    else:
        form = EventForm()
    return render(request, 'myadmin/create_event.html', {'form': form, 'notifications': notifications})

@login_required
def event_detail(request, event_id):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    now = timezone.now() 
    event = Event.objects.get(event_id=event_id)
    return render(request, 'event_detail.html', {
        'event': event,
        'now': now,
        'notifications': notifications
    })

@login_required
def admin_event_detail(request, event_id):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    now = timezone.now() 
    event = Event.objects.get(event_id=event_id)
    return render(request, 'myadmin/event_detail.html', {
        'event': event,
        'notifications': notifications
    })

@login_required
def enroll_in_event(request, event_id):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    event = get_object_or_404(Event, event_id=event_id)
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, event=event)
    if created:
        message = f"You have enrolled in {event.name}. Waiting for confirmation."
    else:
        message = f"You already enrolled in {event.name}."
    Notification.objects.create(user=request.user, message=message)
    return redirect('enroll_success', msg=message)

@login_required
def enroll_Success(request, msg):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'success.html', {"msg":msg, 'notifications': notifications})

@login_required
@user_passes_test(is_admin)
def confirm_enrollment(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    if request.method == 'POST':
        form = EnrollmentConfirmationForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            if enrollment.is_confirmed:
                message = f"Your enrollment in {enrollment.event.name} has been confirmed."
            else:
                message = f"Your enrollment in {enrollment.event.name} has been rejected."
            Notification.objects.create(user=enrollment.user, message=message)
            return redirect('event_detail', event_id=enrollment.event.event_id)
    else:
        form = EnrollmentConfirmationForm(instance=enrollment)
    return render(request, 'myadmin/confirm_enrollment.html', {'form': form})

@login_required
def event_list(request):
    now = datetime.now()
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    # Categorize events
    upcoming_events = Event.objects.filter(start_date__gt=now).order_by('start_date')
    ongoing_events = Event.objects.filter(start_date__lte=now, end_date__gte=now).order_by('start_date')
    completed_events = Event.objects.filter(end_date__lt=now).order_by('-end_date')

    return render(request, 'event_list.html', {
        'upcoming_events': upcoming_events,
        'ongoing_events': ongoing_events,
        'completed_events': completed_events,
        'notifications': notifications
    })

@login_required
@user_passes_test(is_admin)
def admin_event_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    now = datetime.now()
    
    # Categorize events
    upcoming_events = Event.objects.filter(start_date__gt=now).order_by('start_date')
    ongoing_events = Event.objects.filter(start_date__lte=now, end_date__gte=now).order_by('start_date')
    completed_events = Event.objects.filter(end_date__lt=now).order_by('-end_date')

    return render(request, 'myadmin/event_list.html', {
        'upcoming_events': upcoming_events,
        'ongoing_events': ongoing_events,
        'completed_events': completed_events,
        'notifications': notifications
    })

@login_required
@user_passes_test(is_admin)
def event_type_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    event_types = EventType.objects.all()
    return render(request, 'myadmin/event_type_list.html', {'event_types': event_types,'notifications': notifications})

@login_required
@user_passes_test(is_admin)
def department_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    department_list = Department.objects.all()
    return render(request, 'myadmin/department_list.html', {'department_list': department_list, 'notifications': notifications})


@login_required
@user_passes_test(is_admin)
def create_eventType(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    if request.method == 'POST':
        form = EventTypeForm(request.POST)
        if form.is_valid():
            event_type = form.save(commit=False)
            event_type.save()
            return redirect('event_type_list')
    else:
        form = EventTypeForm()
    return render(request, 'myadmin/create_event_type.html', {'form': form, 'notifications': notifications})

@login_required
@user_passes_test(is_admin)
def create_department(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            dept = form.save(commit=False)
            dept.save()
            return redirect('department_list')
    else:
        form = EventTypeForm()
    return render(request, 'myadmin/department_create.html', {'form': form, 'notifications': notifications})

@login_required
@user_passes_test(is_admin)
def edit_department(request, department_id):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    department = get_object_or_404(Department, id=department_id)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    
    return render(request, 'myadmin/dept_edit.html', {'form': form, 'title': 'Edit Department', 'notifications': notifications})

@login_required
@user_passes_test(is_admin)
def edit_event_type(request, event_type_id):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    event_type = get_object_or_404(EventType, id=event_type_id)
    if request.method == 'POST':
        form = EventTypeForm(request.POST, instance=event_type)
        if form.is_valid():
            form.save()
            return redirect('event_type_list')
    else:
        form = EventTypeForm(instance=event_type)
    
    return render(request, 'myadmin/event_type_edit.html', {'form': form, 'title': 'Edit Event Type', 'notifications': notifications})


@login_required
def delete_department(request, department_id):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    department = get_object_or_404(Department, id=department_id)
    
    if request.method == 'POST':
        department.delete()
        return redirect('department_list')
    
    return render(request, 'myadmin/delete_dept.html', {'department': department, 'notifications': notifications})

@login_required
def delete_event_type(request, event_type_id):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    event_type = get_object_or_404(EventType, id=event_type_id)
    if request.method == 'POST':
        event_type.delete()
        return redirect('event_type_list')
    
    return render(request, 'admin/delete_event_type.html', {'event_type': event_type, 'notifications': notifications})

class EventEnrollmentsView(View):
    def get(self, request, event_id):
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        event = get_object_or_404(Event, event_id=event_id)
        enrollments = Enrollment.objects.filter(event=event)
        context = {
            'event': event,
            'enrollments': enrollments,
            'notifications': notifications
        }
        return render(request, 'myadmin/event_enrollments.html', context)

class ConfirmEnrollmentView(View):
    def post(self, request, enrollment_id):
        enrollment = get_object_or_404(Enrollment, id=enrollment_id)
        enrollment.is_confirmed = True
        enrollment.save()

        # Notify the user
        notification_message = f"Your enrollment for the event '{enrollment.event.name}' has been confirmed."
        Notification.objects.create(user=enrollment.user, message=notification_message)

        return redirect('event_enrollments', event_id=enrollment.event.event_id)
    
def index(request):
    return render(request, 'index.html')