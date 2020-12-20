from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path("registeruser", views.registerUser),
    path('quotes', views.home),
    path('login', views.login),
    path('logout', views.logout),
    path('myaccount/<int:idShow>', views.editAcc),
    path('updateuser/<int:idShow>', views.updateUser),
    path('addpost', views.addPost),
    path('user/<int:idShow>', views.userInfo),
    path('delete/<int:idShow>', views.deletePost),
    path('likeme/<int:idShow>', views.likePost),
    path('unlikeme/<int:idShow>', views.unlikePost),
]
