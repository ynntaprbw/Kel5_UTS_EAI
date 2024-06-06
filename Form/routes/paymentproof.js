const express = require('express');
const multer = require('multer');
const mongoose = require('mongoose');
const Ticket = require('../models/Booking');
const PaymentProof = require('../models/PaymentProof');
const router = express.Router();
const sendMessage = require('../kafka/producer');

// Configure Multer storage
const storage = multer.memoryStorage();
const upload = multer({ storage });

// Upload endpoint
router.post('/', upload.single('file'), async (req, res) => {
    const { bookingId } = req.body;

    if (!req.file || !bookingId) {
        return res.status(400).json({ message: 'No file uploaded or bookingId missing' });
    }

    try {
        // Find the booking by ID
        const booking = await Ticket.findById(bookingId);
        if (!booking) {
            return res.status(404).json({ message: 'Booking not found' });
        }

        const newPaymentProof = new PaymentProof({
            bookingId: bookingId,
            amount: amount,
            paymentImage: {
                data: req.file.buffer,
                contentType: req.file.mimetype
            }
        });

        const savedPaymentProof = await newPaymentProof.save();

        // Link the payment proof to the booking
        booking.paymentProof = savedPaymentProof._id;
        await booking.save();

            // Send message to Kafka
            sendMessage('miliaTubesPaymentProofs', {
                action: 'upload',
                bookingId: bookingId,
                paymentProof: savedPaymentProof
            });
    
            res.status(201).json({
                message: 'File uploaded successfully',
                file: savedPaymentProof
            });
        } catch (error) {
            console.error(error);
            res.status(500).json({ message: 'Error uploading file' });
        }
    });
    
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
    