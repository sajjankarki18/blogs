from django.urls import path
from .import views, auth_views

urlpatterns = [
    path('', views.home, name='home'),
    # CRUD functionality
    path('addBlogs/', views.addBlogs, name="addBlogs"),
    path("yourBlogs/<str:pk>/", views.yourBlogs, name="yourBlogs"),
    path('editBlogs/<str:pk>/', views.editBlogs, name="editBlogs"),
    path('deleteBlogs/<str:pk>/', views.deleteBlogs, name="deleteBlogs"),
    
    # global blogs -> Blogs of all globally active users
    path('blogFeed/', views.blogFeed, name="blogFeed"),
    
    # comments views
    path('addComment/<str:pk>/', views.addComment, name="addComment"),
    path('deleteComment/<str:pk>/', views.deleteComment, name="deleteComment"),
    
    # authentication paths
    path('userLogin/', auth_views.userLogin, name="userLogin"),
    path('userRegistration/', auth_views.userRegistration, name="userRegistration"),
    path('userLogout/', auth_views.userLogout, name="userLogout")
]
