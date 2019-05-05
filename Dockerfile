FROM python:3-onbuild

#EXPOSE 8888
EXPOSE $PORT

CMD ["python", "./socket_server.py"]
