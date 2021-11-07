# Declaration of the Golang compiling version.

FROM golang:1.17rc2 AS build

FROM alpine:3.13.6

# Declaration of the project file system and username inside the development container.

ARG USERNAME=production
ARG WORKDIR=/home/$USERNAME

# Creating the user on ash and their home directory.

RUN adduser --home $WORKDIR --shell /bin/ash $USERNAME --disabled-password

# Changing the premises of the file system.

RUN chown -R $USERNAME $WORKDIR

RUN find "$WORKDIR/" -type d -exec chmod 755 {} \;
RUN find "$WORKDIR/" -type f -exec chmod 755 {} \;

RUN chmod 755 $WORKDIR

# Establishing the default user and the default work directory.

WORKDIR $WORKDIR
USER $USERNAME

# Copying the source code of the api.

COPY --from=build api_server $WORKDIR