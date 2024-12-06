from django.contrib import admin
from django.urls import path, include  # Certifique-se de importar 'include'
from main import views  # type: ignore

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('', include('main.urls')),  # Incluindo as URLs do aplicativo 'main'
]
