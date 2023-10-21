from django.shortcuts import render
from django.http import HttpResponse
from .models import ManejadorImagen
from django.conf import settings
from google.cloud import storage  # Importa la biblioteca de Google Cloud Storage
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from PIL import Image
from io import BytesIO
from django.http import HttpResponse

def healthCheck(request):
    return HttpResponse("ok")

def procesar_imagen(imagen_path, capacidad):
    try:
        # Inicializa el cliente de Google Cloud Storage
        storage_client = storage.Client()

        # Nombre del depósito de Google Cloud Storage
        bucket_name = 'almacenamiento-imagenes'

        # Cargar la imagen desde la ubicación especificada 
        fs = FileSystemStorage(location='mi_app\imagenes')
        with fs.open(imagen_path) as imagen_file:
            # Simulación de procesamiento de imagen (escalamiento)
            imagen = Image.open(imagen_file)
            imagen = imagen.resize((capacidad, capacidad))

            # Guardar la imagen procesada en GCS
            bucket = storage_client.get_bucket(bucket_name)
            nombre_archivo_procesado = 'medicamentos-genericos-1.jpg'
            blob = bucket.blob(nombre_archivo_procesado)
            buffer = BytesIO()
            imagen.save(buffer, format='JPEG')
            buffer.seek(0)
            blob.upload_from_file(buffer, content_type='image/jpeg')

            # Devolver la URL pública de la imagen procesada en GCS
            url_imagen_procesada = 'https://storage.googleapis.com/{}/{}'.format(bucket_name, nombre_archivo_procesado)

            return url_imagen_procesada

    except Exception as e:
        return str(e)

def manejar_solicitud_imagen(request):
    # Recuperar el objeto ManejadorImagen 
    manejador = ManejadorImagen.objects.first()

    if manejador:
        if manejador.esta_en_alta_demanda():
            # Estamos en horas de alta demanda, aumentar la capacidad
            capacidad = manejador.capacidad_alta_demanda
        else:
            # No estamos en horas de alta demanda, usar capacidad normal
            capacidad = manejador.capacidad_normal
    else:
        # Si no hay un objeto ManejadorImagen, usar capacidad normal como predeterminado
        capacidad = settings.CAPACIDAD_POR_DEFECTO  

    try:
        # Lógica para manejar la solicitud de imágenes con la capacidad adecuada
        # Simulación de procesamiento de imagen
        url_imagen_procesada = procesar_imagen('nombre_de_imagen.jpg', capacidad)
        resultado = "Imagen procesada exitosamente. Capacidad: {}. URL de imagen procesada: {}".format(capacidad, url_imagen_procesada)

    except Exception as e:
        # Manejar cualquier error que ocurra durante el procesamiento de la imagen
        resultado = "Ocurrió un error al procesar la imagen: {}".format(str(e))

    return HttpResponse(resultado)
