FROM python:3.10

COPY ./storage_service/requirements /requirements

RUN pip install --no-cache-dir --upgrade -r /requirements/local.txt

COPY ./compose/storage_service/start /storage_service_start
RUN sed -i 's/\r//' /storage_service_start
RUN chmod +x /storage_service_start

WORKDIR /storage_service
