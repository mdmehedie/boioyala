from django.urls import path 
from .views import SetProfileView,ProfileUpdateView


urlpatterns=[
    path("set-profile/",SetProfileView.as_view(),name='set_profile'),
    path("update-profile/",ProfileUpdateView.as_view(),name="update_profile"),

]