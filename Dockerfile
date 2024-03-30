FROM python:3.10

WORKDIR /app 
COPY requirements.txt requirements.txt
RUN pip install  -r requirements.txt

ARG MAKERSUITE_API_KEY
ENV MAKERSUITE_API_KEY=$MAKERSUITE_API_KEY

COPY . .

EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]