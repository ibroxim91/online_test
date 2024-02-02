from django.urls import path
from .views import HomeView,TestView ,TestSaveView


urlpatterns = [
    path("" , HomeView.as_view() , name="home"),
    path("test/<int:id>" , TestView.as_view() , name="test"),
    path("test_save" , TestSaveView.as_view() , name="test_save"),

]