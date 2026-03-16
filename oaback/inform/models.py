from django.conf import settings
from django.db import models


class Inform(models.Model):
    title = models.CharField(max_length=200, verbose_name='Title')
    content = models.TextField(verbose_name='Content')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='informs',
        verbose_name='Author'
    )
    departments = models.ManyToManyField(
        'staff.Department',
        blank=True,
        related_name='informs',
        verbose_name='Visible Departments'
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    is_top = models.BooleanField(default=False, verbose_name='Is Top')

    class Meta:
        verbose_name = 'Announcement'
        verbose_name_plural = verbose_name
        ordering = ['-is_top', '-create_time']

    def __str__(self):
        return self.title


class InformRead(models.Model):
    inform = models.ForeignKey(
        Inform,
        on_delete=models.CASCADE,
        related_name='read_records',
        verbose_name='Announcement'
    )
    reader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='read_informs',
        verbose_name='Reader'
    )
    read_time = models.DateTimeField(auto_now_add=True, verbose_name='Read At')

    class Meta:
        verbose_name = 'Read Record'
        verbose_name_plural = verbose_name
        unique_together = ('inform', 'reader')

    def __str__(self):
        return f'{self.reader} read {self.inform}'
