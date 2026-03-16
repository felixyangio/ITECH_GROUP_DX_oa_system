from django.conf import settings
from django.db import models


class AbsentType(models.Model):
    name = models.CharField(max_length=50, verbose_name='Leave Type')

    class Meta:
        verbose_name = 'Leave Type'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Absent(models.Model):
    STATUS_PENDING = 1
    STATUS_APPROVED = 2
    STATUS_REJECTED = 0
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    title = models.CharField(max_length=100, default='', verbose_name='Title')
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='my_absents',
        verbose_name='Applicant'
    )
    responder = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sub_absents',
        verbose_name='Approver'
    )
    absent_type = models.ForeignKey(
        AbsentType,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Leave Type'
    )
    start_date = models.DateField(verbose_name='Start Date')
    end_date = models.DateField(verbose_name='End Date')
    request_content = models.TextField(blank=True, default='', verbose_name='Leave Reason')
    status = models.SmallIntegerField(
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        verbose_name='Status'
    )
    response_content = models.TextField(blank=True, default='', verbose_name='Response')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Created At')

    class Meta:
        verbose_name = 'Leave Application'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']

    def __str__(self):
        return f'{self.applicant} - {self.absent_type}'
