from django.conf.urls import url
from django_calendar import views

app_name = 'django_calendar'

urlpatterns = [
    # Normal Calendar
    url(r'^$', views.CalendarView.as_view(), name='calendar'),
    url(r'^(?P<year>[0-9]+)/(?P<month>[0-9]+)/$',
        views.CalendarView.as_view(), name='calendar'),
    url(r'^week/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<week>[0-9]+)/$',
        views.WeekCalendarView.as_view(), name='week_calendar'),
    url(
        (
            r'^schedule_create/'
            r'(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$'
        ),
        views.ScheduleCreateView.as_view(),
        name='schedule_create'),
    url(
        (
            r'^schedule_list/'
            r'(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$'
        ),
        views.ScheduleListView.as_view(),
        name='schedule_list'),

    # Calendar with time
    url(r'^withtime/$',
        views.WithTimeCalendarView.as_view(), name='withtime_calendar'),
    url(r'^withtime/(?P<year>[0-9]+)/(?P<month>[0-9]+)/$',
        views.WithTimeCalendarView.as_view(),
        name='withtime_calendar'),
    url(
        (
            r'^withtime/week/'
            r'(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<week>[0-9]+)/$'
        ),
        views.WithTimeWeekCalendarView.as_view(),
        name='withtime_week_calendar'),
    url(
        (
            r'^withtime/schedule_create/'
            r'(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$'
        ),
        views.WithTimeScheduleCreateView.as_view(),
        name='withtime_schedule_create'),
    url(
        (
            r'^withtime/schedule_list/'
            r'(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$'
        ),
        views.WithTimeScheduleListView.as_view(),
        name='withtime_schedule_list'),
]
