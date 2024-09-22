FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code

# Instala as bibl   iotecas necessárias
RUN apt-get update && apt-get install -y binutils libproj-dev gdal-bin
RUN apt-get update && apt-get install -y libgeos-dev

# Adiciona as variáveis de ambiente
ENV GDAL_LIBRARY_PATH=/usr/lib/libgdal.so
ENV GEOS_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/libgeos_c.so

# Instala as dependências Python
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copia o código da aplicação
COPY . /code/