FROM python:3.9 

WORKDIR /app
COPY . /app

# Run unit tests
RUN python -m unittest tests/*

# Run python script
ENTRYPOINT ["python", "./main.py"] 