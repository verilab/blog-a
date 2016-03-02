FROM python:3.4.3

ADD posts posts
ADD static static
ADD templates templates
ADD app.py app.py
ADD config.py config.py
ADD handler.py handler.py
ADD util.py util.py
ADD requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8080
CMD ["python", "./app.py"]
