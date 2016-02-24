FROM daocloud.io/python:3.4.3

ADD app.py app.py
EXPOSE 8080
CMD ["python", "./app.py"]
