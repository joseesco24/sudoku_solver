FROM gcc:9.4.0

RUN git clone https://github.com/Microsoft/vcpkg.git /opt/vcpkg

ARG VCPKG_DIR=/opt/vcpkg
WORKDIR $VCPKG_DIR

RUN ./bootstrap-vcpkg.sh
RUN ./vcpkg integrate bash
RUN ./vcpkg integrate install 

RUN echo 'alias vcpkg="$VCPKG_DIR/vcpkg"' >> ~/.bashrc

ENV PATH="$VCPKG_DIR:${PATH}"

ARG USERNAME=development
ARG WORKDIR=/home/$USERNAME

RUN useradd -ms /bin/bash $USERNAME

RUN find "$WORKDIR/" -type d -exec chmod 755 {} \;
RUN find "$WORKDIR/" -type f -exec chmod 755 {} \;

RUN chown -R $USERNAME $VCPKG_DIR
RUN chmod 755 $VCPKG_DIR

RUN chown -R $USERNAME $WORKDIR 
RUN chmod 755 $WORKDIR 

WORKDIR $WORKDIR
USER $USERNAME