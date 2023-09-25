# Usa una imagen base de Python
FROM memcached:latest

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el código fuente al contenedor

COPY . /app

EXPOSE 11211
# Instala las dependencias del proyecto
RUN apt-get update && apt-get install -y ketama
RUN pip install -r requirements.txt

CMD ["memcached"]