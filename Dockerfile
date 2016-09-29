FROM python:3.5.1

COPY posts posts
COPY pages pages
COPY static static
COPY themes themes
COPY app.py app.py
COPY config.py config.py
COPY handler.py handler.py
COPY util.py util.py
COPY generator.py generator.py
COPY theme.py theme.py
COPY custom custom
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python app.py apply-theme

EXPOSE 8080
CMD ["python", "./app.py"]
