FROM python:3.8-slim as build

RUN DEBIAN_FRONTEND=noninteractive \
    apt-get update && apt-get install -y -q \
      build-essential python3-dev libffi-dev git && \
    python3 -m pip install --no-cache-dir --quiet -U pip && \
    python3 -m pip install --no-cache-dir --quiet poetry

ADD . /app

WORKDIR /app

RUN poetry build


FROM python:3.8-slim

COPY --from=build /app/dist/*.whl .

RUN DEBIAN_FRONTEND=noninteractive \
    apt-get update && apt-get install -y -q \
      build-essential python3-dev libffi-dev git && \
    python3 -m pip install --no-cache-dir --quiet -U pip && \
    python3 -m pip install --no-cache-dir --quiet *.whl && \
    rm -f *.whl && \
    apt remove -y --quiet build-essential python3-dev libffi-dev git && \
    apt autoremove -y --quiet

EXPOSE 5000

ENTRYPOINT ["python3", "-m", "shortner"]

CMD ["server", "run"]
