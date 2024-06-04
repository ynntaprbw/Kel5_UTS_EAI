const mongoose = require('mongoose');

const paymentProofSchema = new mongoose.Schema({
    bookingId: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Ticket'
    },
    amount: Number,
    status: {
        type: String,
        default: 'Pending'
    },
    createdAt: {
        type: Date,
        default: Date.now
    },
    updatedAt: Date
});

const PaymentProof = mongoose.model('PaymentProof', paymentProofSchema);

module.exports = PaymentProof;
