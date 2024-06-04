const mongoose = require('mongoose');

const bookingSchema = new mongoose.Schema({
    nama: { type: String, required: true },
    email: { type: String, required: true },
    jml_tiket: { type: Number, required: true },
    no_hp: { type: String, required: true },
    harga: { type: Number, required: true },
    total_harga: { type: Number, required: true },
    tanggal_berangkat: { type: Date, default: Date.now },
    timestamp: { type: Date, default: Date.now }
}, { collection: 'Ticket' });

module.exports = mongoose.model('Booking', bookingSchema);
