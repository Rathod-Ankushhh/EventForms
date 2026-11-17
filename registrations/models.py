
from django.db import models
from django.contrib.auth.models import User


class OrganizerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='organizer_profile'
    )
    is_trusted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Event(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    venue = models.CharField(max_length=200)
    available_seats = models.PositiveIntegerField()

    organizer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events'
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    def __str__(self):
        return self.name


class Registration(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    college = models.CharField(max_length=200)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['event', 'email'],
                name='unique_email_per_event'
            )
        ]

    def __str__(self):
        return self.name
