from django.urls import path
from .views import *

urlpatterns = [
    path('list/', OperationList.as_view(), name='all_operations'),
    path('create/', CreateOperation.as_view(), name='create_operation'),
    path('detail/<int:pk>/', DetailOperation.as_view(), name='edit_operation')
]
