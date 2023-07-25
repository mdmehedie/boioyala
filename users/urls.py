from django.urls import path 
from .views import SetProfileView


urlpatterns=[
    path("set-profile/",SetProfileView.as_view(),name='set_profile')

]