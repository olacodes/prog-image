FROM python:3.9

COPY ./requirements /app/requirements

RUN pip install --no-cache-dir --upgrade -r /app/requirements/local.txt

COPY ./compose/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

COPY ./compose/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./compose/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower

WORKDIR /app