const mongoose = require('mongoose');

const paymentProofSchema = new mongoose.Schema({
    bookingId: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Ticket'
    },
    status: {
        type: String,
        default: 'Pending'
    },
    createdAt: {
        type: Date,
        default: Date.now
    },
    updatedAt: Date,
    paymentImage: {
        data: Buffer, 
        contentType: String 
    }
});

const PaymentProof = mongoose.model('PaymentProof', paymentProofSchema);

module.exports = PaymentProof;
