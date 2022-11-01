from django.urls import re_path, path 

from registration import views


urlpatterns = [
        path('validate', views.validate_registration , name='validate-registration'), 
        path('set-new-password', views.set_new_password, name='set-new-password')
        ]


