FROM python:3.7.10
COPY ["requirements.txt","/usr/src/"]
WORKDIR /usr/src
RUN pip install --upgrade pip
RUN pip install -r requirements.txt