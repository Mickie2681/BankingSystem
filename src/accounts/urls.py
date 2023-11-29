from django.urls import re_path


from .views import (
    login_view,
    register_view,
    logout_view
)

app_name = 'accounts'

urlpatterns = [
    re_path(r'^login/$', login_view, name='login'),
    re_path(r'^register/$', register_view, name='register'),
    re_path(r'^logout/$', logout_view, name='logout'),
]
