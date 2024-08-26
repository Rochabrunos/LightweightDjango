FROM python:latest

VOLUME django_data
# set work directory
WORKDIR /usr/src/app/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY docker-entrypoint.sh /

# copy project
COPY . .

RUN ["chmod", "+x", "/docker-entrypoint.sh"]

ENTRYPOINT  ["/docker-entrypoint.sh"]

EXPOSE 8000