FROM python:3.10

ENV PYTHONUNBUFFERED=1

ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /storage_service

COPY ./storage_service/requirements /storage_service/requirements

RUN pip install --no-cache-dir --upgrade -r /storage_service/requirements/local.txt

COPY ./compose/storage_service/start /storage_service_start
RUN sed -i 's/\r//' /storage_service_start
RUN chmod +x /storage_service_start

COPY ./config ./

COPY ./storage_service ./
