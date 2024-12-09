FROM python:3.9-alpine
WORKDIR /app

# install required packages for psycopg2
RUN apk update && apk add postgresql-dev gcc musl-dev

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 80
CMD ["fastapi", "run", "main.py", "--port", "80"]
