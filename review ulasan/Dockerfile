# base image
FROM python:3.9

# Bikin WORKDIR
WORKDIR /app

# copy all files
COPY . /app

# install dependencies
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", 'review.py']