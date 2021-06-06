FROM node:16.3.0

COPY ["package.json", "/usr/src/"]

WORKDIR /usr/src

RUN npm install -g npm@latest
RUN npm install --production=false

ENV ACCESS_PORT=3000
EXPOSE $ACCESS_PORT