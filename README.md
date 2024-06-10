ALAMY TOUR API
Ini adalah repository untuk ALAMY TOUR API yang terdiri dari tiga layanan utama:

- MainApp API
- Layanan Form Pembelian
- Layanan Ulasan

1. Layanan Form Pembelian
Layanan Form Pembelian adalah API untuk mengelola pembelian tiket tour. Ini memungkinkan pengguna untuk membuat pesanan baru, mendapatkan detail pesanan terbaru, memperbarui pesanan terbaru, dan menghapus pesanan terbaru.
Endpoint yang tersedia : 

- POST /api/bookings: Membuat pesanan baru
- GET /api/bookings: Mendapatkan detail pesanan terbaru
- PUT /api/bookings: Memperbarui pesanan terbaru
- DELETE /api/bookings: Menghapus pesanan terbaru

Untuk informasi lebih lanjut tentang parameter input/output dan kode respons, silakan lihat file README.yaml yang relevan.

2. Layanan Ulasan
Layanan Ulasan adalah API untuk mengelola ulasan tour. Ini memungkinkan pengguna untuk mendapatkan semua ulasan, membuat ulasan baru, mendapatkan ulasan berdasarkan ID, memperbarui ulasan, dan menghapus ulasan.
Endpoint yang tersedia

- GET /reviews: Mendapatkan semua ulasan
- POST /reviews: Membuat ulasan baru
- GET /reviews/{review_id}: Mendapatkan ulasan berdasarkan ID
- PUT /reviews/{review_id}: Memperbarui ulasan
- DELETE /reviews/{review_id}: Menghapus ulasan

Untuk informasi lebih lanjut tentang parameter input/output dan kode respons, silakan lihat file README.yaml yang relevan.
