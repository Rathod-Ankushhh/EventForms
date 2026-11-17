
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db import transaction, IntegrityError
from django.db.models import F, Q, Count
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import Event, Registration, OrganizerProfile
from .forms import RegistrationForm, OrganizerSignupForm, EventForm


# Home page
@never_cache
def home(request):
    query = request.GET.get('q', '').strip()

    events = Event.objects.filter(
        date__gte=timezone.localdate(),
        status='approved'
    ).order_by('date')

    if query:
        events = events.filter(
            Q(name__icontains=query) |
            Q(venue__icontains=query)
        )

    paginator = Paginator(events, 6)
    page_number = request.GET.get('page')
    events = paginator.get_page(page_number)

    return render(
        request,
        'registrations/home.html',
        {'events': events}
    )


# Event details page
def event_detail(request, event_id):
    event = get_object_or_404(
        Event,
        id=event_id,
        status='approved'
    )

    return render(
        request,
        'registrations/event_detail.html',
        {'event': event}
    )


# Event registration
@transaction.atomic
def register_event(request, event_id):
    event = get_object_or_404(
        Event,
        id=event_id,
        status='approved'
    )

    if event.date < timezone.localdate():
        messages.error(
            request,
            'Registration for this event is closed.'
        )
        return redirect('event_detail', event_id=event_id)

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name'].strip()
            email = form.cleaned_data['email'].strip().lower()
            phone = form.cleaned_data['phone'].strip()
            college = form.cleaned_data['college'].strip()

            # Check duplicate registration
            if Registration.objects.filter(
                event=event,
                email=email
            ).exists():
                messages.error(
                    request,
                    'You have already registered for this Event!'
                )
                return redirect(
                    'register_event',
                    event_id=event.id
                )

            # Reduce available seats safely
            updated = Event.objects.filter(
                id=event_id,
                available_seats__gt=0
            ).update(
                available_seats=F('available_seats') - 1
            )

            if updated == 0:
                messages.error(
                    request,
                    'Sorry! No seats available.'
                )
                return redirect(
                    'register_event',
                    event_id=event.id
                )

            # Save registration and handle simultaneous duplicates
            try:
                with transaction.atomic():
                    Registration.objects.create(
                        event=event,
                        name=name,
                        email=email,
                        phone=phone,
                        college=college
                    )

            except IntegrityError:
                # Restore the seat if duplicate registration occurs
                Event.objects.filter(id=event_id).update(
                    available_seats=F('available_seats') + 1
                )

                messages.error(
                    request,
                    'You have already registered for this Event!'
                )

                return redirect(
                    'register_event',
                    event_id=event.id
                )

            return redirect('success')

    else:
        form = RegistrationForm()

    return render(
        request,
        'registrations/register.html',
        {
            'event': event,
            'form': form
        }
    )


# Registration success page
def success(request):
    return render(
        request,
        'registrations/success.html'
    )


# Organizer signup
def organizer_signup(request):
    if request.method == 'POST':
        form = OrganizerSignupForm(request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save()
                    OrganizerProfile.objects.create(user=user)

                login(request, user)

                return redirect('organizer_login')

            except IntegrityError:
                form.add_error(
                    'username',
                    'This username is already taken.'
                )

    else:
        form = OrganizerSignupForm()

    return render(
        request,
        'registrations/organizer_signup.html',
        {'form': form}
    )


# Organizer login
@never_cache
def organizer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and hasattr(
            user,
            'organizer_profile'
        ):
            login(request, user)
            return redirect('organizer_dashboard')

        messages.error(
            request,
            'Invalid username or password.'
        )

    return render(
        request,
        'registrations/organizer_login.html'
    )



# Organizer dashboard
@login_required(login_url='organizer_login')
@never_cache
def organizer_dashboard(request):
    events = Event.objects.filter(
        organizer=request.user
    ).annotate(
        registered_count=Count('registration')
    ).prefetch_related(
        'registration_set'
    ).order_by('-date')

    return render(
        request,
        'registrations/organizer_dashboard.html',
        {'events': events}
    )



# View event registrations
@login_required(login_url='organizer_login')
@never_cache
def event_registrations(request, event_id):
    event = get_object_or_404(
        Event,
        id=event_id,
        organizer=request.user
    )

    registrations = Registration.objects.filter(
        event=event
    ).order_by('name')

    return render(
        request,
        'registrations/event_registrations.html',
        {
            'event': event,
            'registrations': registrations,
            'registered_count': registrations.count(),
            'total_seats': event.available_seats + registrations.count(),
        }
    )



# Create event
@login_required(login_url='organizer_login')
@never_cache
def create_event(request):
    profile = get_object_or_404(
        OrganizerProfile,
        user=request.user
    )

    if request.method == 'POST':
        form = EventForm(request.POST)

        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user

            if profile.is_trusted:
                event.status = 'approved'
            else:
                event.status = 'pending'

            event.save()

            messages.success(
                request,
                'Event submitted successfully!'
            )

            return redirect('organizer_dashboard')

    else:
        form = EventForm()

    return render(
        request,
        'registrations/create_event.html',
        {'form': form}
    )


# Organizer logout
@login_required(login_url='organizer_login')
@never_cache
def organizer_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('organizer_login')

    return redirect('organizer_dashboard')
