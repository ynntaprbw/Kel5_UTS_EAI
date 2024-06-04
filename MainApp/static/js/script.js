document.addEventListener('DOMContentLoaded', function() {
    var selectElement = document.querySelector('.custom-select');
    
    selectElement.addEventListener('change', function() {
        if (this.value === "") {
            this.style.color = '#999';
        } else {
            this.style.color = '#000';
        }
    });
    
    // Set the initial color
    if (selectElement.value === "") {
        selectElement.style.color = '#999';
    } else {
        selectElement.style.color = '#000';
    }
});

document.getElementById('contactForm').addEventListener('submit', function(event) {
    event.preventDefault();

    let formData = {
        nama: document.querySelector('input[name="nama"]').value,
        email: document.querySelector('input[name="email"]').value,
        jml_tiket: document.querySelector('input[name="jml_tiket"]').value,
        no_hp: document.querySelector('input[name="no_hp"]').value,
        harga: document.querySelector('select[name="harga"]').value
    };

    fetch('/post-beli', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            document.getElementById('popup-message').textContent = data.message;
            document.getElementById('popup').style.display = 'block';
        }
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('paymentForm').addEventListener('submit', function(event) {
    event.preventDefault();

    let formData = new FormData();
    formData.append('paymentProof', document.querySelector('input[name="paymentProof"]').files[0]);

    fetch('/upload_payment_proof', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            document.getElementById('popup').style.display = 'none';
            document.getElementById('successPopup').style.display = 'block';
        }
    })
    .catch(error => console.error('Error:', error));
});

document.querySelectorAll('.close2').forEach(element => {
    element.addEventListener('click', function() {
        element.parentElement.parentElement.style.display = 'none';
    });
});


document.addEventListener("DOMContentLoaded", function() {
    // Mendapatkan element p yang akan menampilkan tanggal
    var dateElement = document.getElementById("formatted-date");
    
    // Mendapatkan tanggal dari server dalam format ISO 8601
    var timestamp = "{{ beli.timestamp }}";
    
    // Mengubah format tanggal menjadi "YYYY-MM-DD"
    var formattedDate = new Date(timestamp).toISOString().split('T')[0];
    
    // Menampilkan tanggal yang diformat di element p
    dateElement.textContent = formattedDate;
});

// Fungsi untuk membuka popup ulasan dan mengisi nilai dalam form
function openPopupUlasan(button) {
    // Mendapatkan ID ulasan dari atribut data-id pada tombol
    var id = button.getAttribute('data-id');
    document.getElementById("popupulasan").style.display="block";
    var url = `/review/${id}`;

    // Mengirim permintaan GET ke API
    fetch(url)
    .then(response => response.json())
    .then(data => {
        // Mengisi nilai dalam form popup dengan data ulasan
        document.getElementById('tour').value = data.tour;
        document.getElementById('nama').value = data.nama;
        document.getElementById('rating').value = data.rating;
        document.getElementById('date_go').value = data.date_go;
        document.getElementById('go_with').value = data.go_with;
        document.getElementById('review').value = data.review;
        document.getElementById('title_review').value = data.title_review;

        // Menampilkan popup
        document.getElementById('popupulasan').style.display = 'block';
    })
    .catch(error => console.error('Error:', error));
}

// Function to close popup
function closePopupUlasan() {
    document.getElementById("popupulasan").style.display="none";
}

// Function to delete ulasan
function deleteUlasan(button) {
    var id = button.getAttribute("data-id");
    // Lakukan delete request ke server
    fetch(`/delete-ulasan/${id}`, { method: 'DELETE' })
        .then(response => {
            if (response.ok) {
                // Hapus elemen ulasan dari DOM
                button.closest('.ulasan-box').remove();
            }
        });
}

document.getElementById("updateUlasan").addEventListener("submit", function(event){
    event.preventDefault(); // Menghentikan form dari pengiriman default

    // Ambil nilai dari input field
    var tour = document.getElementById("tour").value;
    var nama = document.getElementById("nama").value;
    var rating = document.querySelector('input[name="rating"]:checked').value;
    var date_go = document.getElementById("date_go").value;
    var go_with = document.getElementById("go_with").value;
    var review = document.getElementById("review").value;
    var title_review = document.getElementById("title_review").value;

    // Lakukan pengiriman data form ke backend atau lakukan update sesuai kebutuhan
    console.log("tour:", tour);
    console.log("nama:", nama);
    console.log("rating:", rating);
    console.log("date_go:", date_go);
    console.log("go_with:", go_with);
    console.log("review:", review);
    console.log("title_review:", title_review);

    // Setelah update berhasil, tutup pop-up
    closePopupUlasan();
});

// Fungsi untuk membuka popup ulasan dan mengisi nilai dalam form
function openPopupPembelian(button) {
    // Mendapatkan ID ulasan dari atribut data-id pada tombol
    var id = button.getAttribute('data-id');
    document.getElementById("popuppembelian").style.display="block";
    var url = `/update-booking/${id}`;

    // Mengirim permintaan GET ke API
    fetch(url)
    .then(response => response.json())
    .then(data => {
        // Mengisi nilai dalam form popup dengan data ulasan
        document.getElementById('nama').value = data.nama;
        document.getElementById('email').value = data.email;
        document.getElementById('jml_tiket').value = data.jml_tiket;
        document.getElementById('no_hp').value = data.no_hp;
        document.getElementById('harga').value = data.harga;

        // Menampilkan popup
        document.getElementById('popuppembelian').style.display = 'block';
    })
    .catch(error => console.error('Error:', error));
}

document.getElementById("updatePembelian").addEventListener("submit", function(event){
    event.preventDefault(); // Menghentikan form dari pengiriman default

    // Ambil nilai dari input field
    var nama = document.getElementById("nama").value;
    var email = document.getElementById("email").value;
    var jml_tiket = document.getElementById("jml_tiket").value;
    var no_hp = document.getElementById("no_hp").value;
    var harga = document.getElementById("harga").value;

    // Buat object data untuk dikirim ke server
    var data = {
        nama: nama,
        email: email,
        jml_tiket: jml_tiket,
        no_hp: no_hp,
        harga: harga
    };

    // Kirim data menggunakan fetch
    fetch('http://localhost:5002/api/bookings', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Lakukan sesuatu jika update berhasil
            console.log('Success:', data);
            // Tutup popup setelah update berhasil
            closePopupPembelian();
        } else {
            // Tangani kesalahan dari server
            console.error('Error:', data.message);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});

// Function to close popup
function closePopupPembelian() {
    document.getElementById("popuppembelian").style.display="none";
}

// Function to delete ulasan
function deletePembelian(button) {
    var id = button.getAttribute("data-id");
    // Lakukan delete request ke server
    fetch(`/delete-pembelian/${id}`, { method: 'DELETE' })
}
