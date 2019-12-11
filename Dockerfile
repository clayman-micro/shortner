FROM python:3.7-alpine3.10 as build

RUN apk add --update --no-cache --quiet \
        make libc-dev python3-dev libffi-dev linux-headers gcc g++ git \
        postgresql-dev && \
    python3 -m pip install --no-cache-dir --quiet -U pip && \
    python3 -m pip install --no-cache-dir --quiet pipenv

ADD . /app

WORKDIR /app

RUN pipenv install --dev && \
    pipenv lock -r > requirements.txt && \
    pipenv run python setup.py bdist_wheel


FROM python:3.7-alpine3.10

COPY --from=build /app/dist/*.whl .

RUN apk add --update --no-cache --quiet \
        make libc-dev python3-dev libffi-dev linux-headers gcc g++ git \
        postgresql-client && \
    python3 -m pip install --no-cache-dir --quiet -U pip && \
    python3 -m pip install --no-cache-dir --quiet *.whl && \
    # mkdir -p /usr/share/wallet && \
    # cp /usr/local/lib/python3.7/site-packages/wallet/storage/sql/* /usr/share/wallet && \
    rm -f *.whl && \
    apk del --quiet make libc-dev python3-dev libffi-dev linux-headers gcc g++ git

EXPOSE 5000

CMD ["pipenv", "run", "python3", "-m", "shortner", "server", "run", "--host=0.0.0.0"]
