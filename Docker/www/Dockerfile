FROM alpine:3.8

RUN mkdir /root/app/
WORKDIR /root/app

RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

ADD ./backend/requirements.txt /root/app/requirements.txt

RUN pip3 install -r /root/app/requirements.txt

ADD ./backend/src /root/app/

ENV FLASK_ENV="development"
ENV FLASK_APP="__init__.py"

CMD ["flask", "run", "--host=0.0.0.0"]


EXPOSE 5000
