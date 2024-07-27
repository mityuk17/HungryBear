FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt
COPY ./.env /code/.env

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./app /code/app

