const mongoose = require('mongoose');
const PaymentProof = require('./PaymentProof');

const ticketSchema = new mongoose.Schema({
    nama: {
        type: String,
        required: true
    },
    email: {
        type: String,
        required: true,
        match: /\S+@\S+\.\S+/
    },
    jml_tiket: {
        type: Number,
        required: true,
        min: 1
    },
    tgl_berangkat: {
        type: Date,
        required: true
    },
    no_hp: {
        type: String,
        required: true,
        match: /^\d{10,14}$/
    },
    harga: {
        type: Number,
        required: true
    },
    total_harga: {
        type: Number,
        required: true
    },
    paymentProof: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'PaymentProof'
    }
}, { timestamps: true, collection: 'Ticket' });

// otomatis delete paymentProof
ticketSchema.pre('remove', async function(next) {
    try {
        await PaymentProof.findByIdAndRemove(this.paymentProof);
        next();
    } catch (err) {
        next(err);
    }
});

const Ticket = mongoose.model('Ticket', ticketSchema);

module.exports = Ticket;
