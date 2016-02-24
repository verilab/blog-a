FROM daocloud.io/python:3.4.3

ADD posts posts
ADD static static
ADD templates templates
ADD app.py app.py
ADD config.py config.py
ADD handler.py handler.py

EXPOSE 8080
CMD ["python", "./app.py"]
