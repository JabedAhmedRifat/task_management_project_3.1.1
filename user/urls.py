from django.urls import path
from .views import *
from knox import views as knox_views


urlpatterns= [
    
    path('list-user/', ListUsersView),
    path('delete-user/<int:pk>/', deleteUser),
    
    path('user-detail/<int:pk>/', detailUsersView),
    
    path('user-update/<int:pk>/', updateUserView),
    
    path('register/', RegistrationAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('logout/',knox_views.LogoutView.as_view(), name='logout'),
    path('get-user/', UserAPI.as_view()),
    path('change-password/', changePasswordView),
    
    path('reset-password/', ResetPasswordAPI.as_view(), name='user-reset-password'),
    path('set-new-password/<str:uid>/<str:token>/', SetNewPasswordAPI.as_view(), name='user-set-new-password'),


    path('target-create/', createTarget),
    path('target-list/', listTarget),
    path('target-detail/<int:pk>/', detailTarget),
    path('target-update/<int:pk>/', updateTarget),
    path('target-delete/<int:pk>/', deleteTarget),
    
    path('target-filter/', searchUserOnTarget.as_view()),
    
    


    
]

