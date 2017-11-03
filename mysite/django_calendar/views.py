import datetime
from collections import defaultdict
from django.utils.safestring import mark_safe
from django.views import generic
from django.shortcuts import render

from .calendarlib import (
    SimpleCalendarBS4, WithTimeCalendarBS4,
    TimeScheduleBS4
)
from .forms import ScheduleForm, WithTimeScheduleForm
from .models import Schedule, WithTimeSchedule


class CalendarView(generic.TemplateView):
    """View for Calendar"""

    template_name = 'django_calendar/calendar.html'

    def get_calendar(self, *args, **kwagrs):
        return SimpleCalendarBS4(*args, **kwagrs)

    def get_model(self):
        return Schedule

    def get_context_data(self, *args, **kwargs):
        """Add Calendar Obeject to Content"""
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')

        # /In Access Case
        if year is None and month is None:
            date = datetime.datetime.now()

        # with year month
        elif year and month:
            date = datetime.datetime(
                year=int(year), month=int(month), day=1
            )

        # mkdir like {1:3, 31:5}
        schedule_counter = defaultdict(int)
        queryset = self.get_model().objects.filter(
            date__year=date.year, date__month=date.month
        )
        for schedule in queryset:
            schedule_counter[schedule.date.day] += 1

        month_calendar = self.get_calendar(date, schedule_counter)
        month_calendar_html = month_calendar.formatmonth()
        context = super(CalendarView,self).get_context_data(*args, **kwargs)


        context['calendar'] = mark_safe(month_calendar_html)
        context['date'] = date
        return context


class WeekCalendarView(generic.TemplateView):
    """Weelkly calendar View."""

    template_name = 'django_calendar/week_calendar.html'

    def get_calendar(self, *args, **kwagrs):
        return SimpleCalendarBS4(*args, **kwagrs)

    def get_context_data(self, *args, **kwargs):
        week = self.kwargs.get('week')
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        date = datetime.datetime(
            year=int(year), month=int(month), day=1
        )
        calendar = self.get_calendar(date)
        html = calendar.formatweek_table(int(week))

        context = super().get_context_data(*args, **kwargs)
        context['calendar'] = mark_safe(html)
        context['date'] = date
        return context


class ScheduleCreateView(generic.CreateView):
    """View for make schedule"""

    model = Schedule
    form_class = ScheduleForm

    def form_valid(self, form):
        """"""
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        date = datetime.datetime(
            year=int(year), month=int(month), day=int(day))
        schedule = form.save(commit=False)
        schedule.date = date
        schedule.save()
        return render(self.request, 'django_calendar/close.html')


class ScheduleListView(generic.ListView):
    """view for schedule list"""

    model = Schedule

    def get_queryset(self):
        """return schedule"""
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        date = datetime.datetime(
            year=int(year), month=int(month), day=int(day)
        )
        queryset = self.model.objects.filter(
            date=date
        )
        return queryset


class WithTimeCalendarView(CalendarView):
    """view for monthly schedule with time and day"""

    template_name = 'django_calendar/withtime_calendar.html'

    def get_calendar(self, *args, **kwagrs):
        return WithTimeCalendarBS4(*args, **kwagrs)

    def get_model(self):
        return WithTimeSchedule


class WithTimeWeekCalendarView(WeekCalendarView):
    """View for Weelkly schedule with time"""

    template_name = 'django_calendar/withtime_week_calendar.html'

    def get_calendar(self, *args, **kwagrs):
        return WithTimeCalendarBS4(*args, **kwagrs)

    def get_model(self):
        return WithTimeSchedule


class WithTimeScheduleCreateView(ScheduleCreateView):
    """view for make schedules with time."""

    model = WithTimeSchedule
    form_class = WithTimeScheduleForm
    template_name = 'django_calendar/schedule_form.html'


class WithTimeScheduleListView(ScheduleListView):
    """view for schedules"""

    model = WithTimeSchedule

    def get_context_data(self, *args, **kwargs):
        schedules = self.get_queryset().order_by('start_time')
        # 6 to 5
        hours = []
        for x in range(24):
            hour = x + 6
            if hour >= 24:
                hour -= 24
            hours.append(hour)
        time_schedule = TimeScheduleBS4(hours=hours, step=10)
        context = super().get_context_data(*args, **kwargs)
        context['time_schedule'] = mark_safe(
            time_schedule.format_schedule(schedules)
        )
        return context
