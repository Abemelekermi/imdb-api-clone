FROM python:3.13.5-alpine3.22
LABEL maintainer="Abemelek"

# For real time debugging buffered = 1
ENV PYTHONUNBUFFERED=1

COPY ./requirments.txt /tmp/requirments.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000


RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update postgresql-client jpeg-dev && \
    apk add --update --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev && \
    /py/bin/pip install -r /tmp/requirments.txt && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol

ENV PATH="/py/bin:$PATH"

USER django-user