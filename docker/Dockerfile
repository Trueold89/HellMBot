FROM python:3.12.3-alpine3.19 
ENV DB_PATH="/etc/hellmbot/database.sqlite"
RUN pip install --extra-index-url https://git.orudo.ru/api/packages/trueold89/pypi/simple/ HellMBot
WORKDIR /etc/hellmbot
ENTRYPOINT ["hellm"]
