FROM alpine:latest
RUN apk update && apk add python3 py3-pip
ENV DB_PATH="/etc/hellmbot/database.sqlite"
RUN pip install --extra-index-url https://git.orudo.ru/api/packages/trueold89/pypi/simple/ HellMBot --break-system-packages
WORKDIR /etc/hellmbot
ENTRYPOINT ["hellm"]