FROM node:16.3.0

ARG USERNAME=development
ARG WORKDIR=/home/$USERNAME

RUN useradd -ms /bin/bash $USERNAME

COPY ["package.json", "$WORKDIR/"]

WORKDIR $WORKDIR

RUN find "$WORKDIR/" -type d -exec chmod 755 {} \;
RUN find "$WORKDIR/" -type f -exec chmod 755 {} \;

ENV PATH="$WORKDIR/.local/bin:${PATH}"

RUN chown -R $USERNAME $WORKDIR
RUN chmod 755 $WORKDIR

RUN npm install -g npm@latest
RUN npm install --production=false

USER $USERNAME