FROM python:3.10

COPY ./process_service/requirements /process_service/requirements

RUN pip install --no-cache-dir --upgrade -r /process_service/requirements/local.txt

COPY ./compose/process_service/start /process_service_start
RUN sed -i 's/\r//' /process_service_start
RUN chmod +x /process_service_start

COPY ./process_service /process_service

COPY ./config /config

WORKDIR /process_service
