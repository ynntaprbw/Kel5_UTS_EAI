const express = require('express');
const multer = require('multer');
const PaymentProof = require('../models/paymentproof');


const router = express.Router();

// Configure Multer storage
const storage = multer.memoryStorage();
const upload = multer({ storage });

// Upload endpoint
router.post('/', upload.single('file'), async (req, res) => {
  const { bookingId } = req.body;

  if (!req.file || !bookingId) {
    return res.status(400).send('No file uploaded or bookingId missing');
  }

  const newPaymentProof = new PaymentProof({
    bookingId: bookingId,
    img: {
      data: req.file.buffer,
      contentType: req.file.mimetype
    }
  });

  try {
    const savedPaymentProof = await newPaymentProof.save();
    res.status(201).send({
      message: 'File uploaded successfully',
      file: savedPaymentProof
    });
  } catch (error) {
    res.status(500).send('Error uploading file');
  }
});

module.exports = router;
