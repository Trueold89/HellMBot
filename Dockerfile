FROM python:3.12-alpine AS builder
RUN pip install -U pip setuptools
WORKDIR /tmp/build
COPY hellmbot /tmp/build/hellmbot
COPY setup.py /tmp/build/setup.py
RUN python setup.py sdist

FROM python:3.12-alpine as runtime
RUN pip install -U pip
COPY --from=builder /tmp/build/dist /dist
RUN pip install /dist/* && rm -rf /dist
WORKDIR /etc/hellmbot
ENTRYPOINT ["hellm"]
