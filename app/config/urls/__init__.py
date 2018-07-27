from django.urls import path, include
from .. import views

urlpatterns = [

    path('', include('config.urls.views')),
    path('api/', include('config.urls.apis')),
]
