FROM ghcr.io/unoconv/unoserver-docker:0.4.1

ARG UID=worker
ARG GID=worker

USER ${UID}
WORKDIR /home/worker

RUN pip install --break-system-packages -U unoserver fastapi pydantic uvicorn gunicorn python-multipart

COPY --chown=${UID}:${GID} etc/converter-docker-entrypoint.sh /docker-entrypoint.sh
COPY --chown=${UID}:${GID} src/converter /home/worker/converter

ENTRYPOINT ["/docker-entrypoint.sh"]
