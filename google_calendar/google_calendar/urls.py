from django.urls import path
from .views import GoogleCalendarInitView, GoogleCalendarInitCallbackView

urlpatterns = [
    path('rest/v1/calendar/init/', GoogleCalendarInitView.as_view(),
         name='google-calendar-init'),
    path('rest/v1/calendar/init/redirect', GoogleCalendarInitCallbackView.as_view(),
         name='google-calendar-init-callback'),
]
