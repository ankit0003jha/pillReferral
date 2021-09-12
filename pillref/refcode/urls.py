from django.db.models import indexes
from django.urls import path
from .views import ProfileAPIView, profileDetail
from . import views


urlpatterns = [

  path('', views.index, name='index'),
  path('signup/', views.signup_view ,name="signup_view"),
  path('login/', views.login_view, name="login_view"),
  path('logoutuser', views.logoutuser, name="logoutuser"),
  path('home', views.home, name="home"),
  path('history/', views.my_recommendations_view, name="my_recommendations_view"),
  path('referralcode/<str:ref_code>', views.profile, name="profile"),
  path('api/referral/code', views.Referral_code_API, name="Referral_code_API"),
   path('api/generate/code', views.generate_code, name="generate_code"),
  path('api/', ProfileAPIView.as_view()),
  path('api/<int:pk>/', profileDetail.as_view()),

]