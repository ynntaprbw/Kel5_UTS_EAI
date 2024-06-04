const express = require('express');
const router = express.Router();
const PaymentProof = require('../models/paymentproof');

// Route to get all payment proofs
router.get('/', async (req, res) => {
  try {
    const paymentProofs = await PaymentProof.find();
    res.status(200).json(paymentProofs);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error retrieving payment proofs' });
  }
});

module.exports = router;
