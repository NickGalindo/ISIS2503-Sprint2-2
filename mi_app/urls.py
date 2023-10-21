from django.contrib import admin
from django.urls import path
from . import views  

urlpatterns = [
    # Ruta para procesar imágenes
    path('admin/', admin.site.urls),
    path('procesar-imagen/', views.manejar_solicitud_imagen, name='procesar_imagen'),
    path('health-check/', views.healthCheck)
]
