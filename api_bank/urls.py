from django.contrib import admin
from django.urls import path, include
from client.token import CustomAuthToken
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls'), name='login_in_system'),
    path('api_admin/', include('bank_admin.urls'), name='bank_admin_urls'),
    path('generate_token/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('bank/', include('bank.urls'), name='bank_urls'),
    path('operation/', include('operation.urls'), name='operation_urls'),
    path('client/', include('client.urls'), name='client_urls'),
]
