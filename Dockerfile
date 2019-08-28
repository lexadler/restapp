FROM python:3.7-alpine
COPY requirements.txt /
RUN pip install -r requirements.txt
EXPOSE 5000
COPY src/app.py /app/
WORKDIR /app
CMD python3.7 ./app.py
