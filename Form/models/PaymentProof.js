const mongoose = require('mongoose');

const paymentProofSchema = new mongoose.Schema({
  bookingId: { type: mongoose.Schema.Types.ObjectId, ref: 'Booking', required: true },
  img: {
    data: Buffer,
    contentType: String
  },
  uploadedAt: { type: Date, default: Date.now }
});

const PaymentProof = mongoose.model('PaymentProof', paymentProofSchema);

module.exports = PaymentProof;

