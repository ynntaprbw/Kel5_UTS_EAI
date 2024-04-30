# base image
FROM php:8.2-cli

# working dir
WORKDIR /var/www/html

# copy all files
COPY . .

CMD ["php", "-S", "0.0.0.0:8000", "-t", "public"]
