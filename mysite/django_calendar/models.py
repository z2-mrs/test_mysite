# coding: UTF-8
import datetime
from django.db import models
from django.utils import timezone


class Schedule(models.Model):
    """Schedule"""

    memo = models.TextField('Memo')
    date = models.DateField('Day')
    created_at = models.DateTimeField('StartDay', default=timezone.now)

    def __str__(self):
        return self.memo


class WithTimeSchedule(models.Model):
    """Schedule with time"""

    memo = models.TextField('Memo')
    start_time = models.TimeField('StartTime', default=datetime.time(7, 0, 0))
    end_time = models.TimeField('EndTime', default=datetime.time(7, 0, 0))
    date = models.DateField('Day')
    created_at = models.DateTimeField('StartDays', default=timezone.now)

    def __str__(self):
        return self.memo
