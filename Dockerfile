FROM python:3.7-alpine
COPY requirements.txt /
RUN pip install -r requirements.txt
EXPOSE 5000
COPY restapp.py /app/
WORKDIR /app
CMD python3.7 ./restapp.py
