from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    path('', UserListView.as_view(), name='accounts'),
    path('/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    path('/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),

]