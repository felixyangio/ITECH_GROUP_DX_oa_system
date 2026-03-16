from django.conf import settings
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name='Department Name')
    intro = models.CharField(max_length=200, blank=True, default='', verbose_name='Description')

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Staff(models.Model):
    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 0
    STATUS_LOCKED = 3
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_INACTIVE, 'Inactive'),
        (STATUS_LOCKED, 'Locked'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='staff_profile',
        verbose_name='User'
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='staffs',
        verbose_name='Department'
    )
    status = models.SmallIntegerField(
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE,
        verbose_name='Status'
    )
    uid = models.CharField(max_length=20, blank=True, default='', verbose_name='Employee ID')
    join_date = models.DateField(null=True, blank=True, verbose_name='Join Date')

    class Meta:
        verbose_name = 'Staff'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.user)
