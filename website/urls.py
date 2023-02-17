from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from .views import *
from . import views
app_name = "pages"
urlpatterns = [
    path('', index, name="index"),
    path('login', Login, name="login"),
    path('logout', Logout, name="logout"),
    path("restPassword/<str:uidb64>/<str:token>/",  RestPassword.as_view() , name="restPassword"),
    path('Teacherforms', Forms, name="forms"),
    path('CatForm', CatCoursesForm, name="CatForm"),
    path('Phone', Phone, name="Phone"),
    path('CatUpdate/<int:id>/', updateCatCoursesForm, name="Update"),
    path('TeacherUpdate/<int:id>/', updateTeacher, name="UpdateTeacher"),
    path('Video', VideoView, name="Video"),
    path('VideoUpdate/<int:id>/', updateVideo, name="UpdateVideo"),
    path('VideoDelete/<int:id>/', DeleteVideo, name="DeleteVideo"),
    path('TeacherDelete/<int:id>/', DeleteTeacher, name="DeleteTeacher"),
    path('CourseDelete/<int:id>/', DeleteCatCourse, name="DeleteCatCourse"),
    path('Puy/<int:id>/', bay, name="puy"),
    path('Bannarsforms', BannarView, name="Bannars"),
    path('BannarDelete/<int:id>/', DeleteBanars, name="DeleteBannars"),
    


] 
handler404 = 'website.views.page_not_found_view'
handler505 = 'website.views.page_not_found_view_505'
