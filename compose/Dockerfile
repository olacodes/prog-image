FROM python:3.10

COPY ./requirements /progImg/requirements
RUN pip install --no-cache-dir --upgrade -r /progImg/requirements/local.txt

COPY ./storage_service/requirements /progImg/storage_service/requirements
RUN pip install --no-cache-dir --upgrade -r /progImg/storage_service/requirements/local.txt


COPY ./compose/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./compose/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower

COPY ./config /progImg/config
COPY ./storage_service /progImg/storage_service
COPY ./process_service /progImg/process_service

WORKDIR /progImg