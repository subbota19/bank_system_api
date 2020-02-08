from django.urls import path
from .views import *

urlpatterns = [
    path('create/', CreateAdmin.as_view(), name='create_account'),
    path('edit/', DetailAdmin.as_view(), name='delete_account'),
    path('account/', AccountAdmin.as_view(), name='account'),

]
