const mongoose = require('mongoose');

const ticketSchema = new mongoose.Schema({
    nama: String,
    email: String,
    jml_tiket: Number,
    tgl_berangkat: Date,
    no_hp: String,
    harga: Number,
    total_harga: Number,
    paymentProof: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'PaymentProof'
    }
}, { timestamps: true, collection: 'Ticket' });

const Ticket = mongoose.model('Ticket', ticketSchema);

module.exports = Ticket;
