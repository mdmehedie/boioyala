from django.urls import path 
from .views import*
from .middleware import auth_middleware
urlpatterns=[
    path("",HomeView.as_view(),name="home"),
    path("dashboard/",auth_middleware(DashboardView.as_view()),name="dashboard"),
    path("book/",BookView.as_view(),name="books"),
    path("book/<slug:slug>/",BookView.as_view(),name="book_detail"),
    path("profiles/",ProfileView.as_view(),name="profiles"),
    path("profile/<slug:url>/",ProfileView.as_view(),name="profile_detail"),

    path("create-book/",DonateBookView.as_view(),name="create_book"),

    path("post-status/<slug:slug>/",post_status_view,name="post_status"),
    path("request-for-book/<slug:slug>/",request_for_book,name="request_for_book"),
    



    #users
    path("login/",LoginView.as_view(),name="login"),
    path("sign-up/",SignUpView.as_view(),name="signup"),
    path("logout/",logout_view,name="logout"),
]