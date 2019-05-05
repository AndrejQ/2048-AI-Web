FROM python:3-onbuild

EXPOSE 8888

CMD ["python", "./socket_server.py"]
