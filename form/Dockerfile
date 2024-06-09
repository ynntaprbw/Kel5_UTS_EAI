# Gunakan image node.js versi terbaru sebagai base image
FROM node:latest

# Set working directory di dalam container
WORKDIR /usr/src/app

# Menyalin package.json dan package-lock.json (jika ada) ke dalam container
COPY package*.json ./

# Menginstal dependensi proyek
RUN npm install

# Install pkg-config
RUN apt-get update && apt-get install -y pkg-config

# Menyalin seluruh proyek ke dalam container
COPY . .

# Expose port yang digunakan oleh aplikasi
EXPOSE 5002

# Command untuk menjalankan aplikasi
CMD ["node", "app.js"]