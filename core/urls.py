from django.urls import re_path
from .views import home, about


app_name = 'core'

urlpatterns = [
    # url(r'^$', home_view, name='home'),
    re_path(r'^$', home, name='home'),
    re_path(r'^about/$', about, name='about'),
]