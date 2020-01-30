from django.urls import path
from .views import CreateClient, AccountClient, DetailClient

urlpatterns = [
    path('create/', CreateClient.as_view(), name='create_account'),
    path('edit/', DetailClient.as_view(), name='edit_account'),
    path('account/', AccountClient.as_view(), name='account'),

]
