FROM mcr.microsoft.com/appsvc/python:3.9_20201229.1

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN apt-get --allow-releaseinfo-change update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev 

RUN pip install --no-cache-dir chromadb

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt --no-cache-dir
ADD . /code/
RUN chmod +x /code/init.sh

ENV PORT 80
EXPOSE 80

ENTRYPOINT ["/code/init.sh"]