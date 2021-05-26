FROM python:3.7.10

ARG USERNAME=production
ARG WORKDIR=/home/$USERNAME

RUN useradd -ms /bin/bash $USERNAME

COPY [".","$WORKDIR"]

RUN find "$WORKDIR/" -type d -exec chmod 755 {} \;
RUN find "$WORKDIR/" -type f -exec chmod 755 {} \;

ENV PATH="$WORKDIR/.local/bin:${PATH}"

RUN chown -R $USERNAME $WORKDIR
RUN chmod 755 $WORKDIR

WORKDIR $WORKDIR
USER $USERNAME

RUN pip install --upgrade pip
RUN pip install -r requirements/commons.txt

ENV PORT=3000
EXPOSE $PORT

CMD ["python", "api_server.py"]