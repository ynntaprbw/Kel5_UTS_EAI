const { Kafka } = require('kafkajs');
const mongoose = require('mongoose');
const Ticket = require('../models/Booking');
const PaymentProof = require('../models/PaymentProof');

// Konfigurasi MongoDB
mongoose.connect('mongodb://localhost:27017/Tubes', {
    useNewUrlParser: true,
    useUnifiedTopology: true,

}).then(() => {
    console.log('Connected to MongoDB');
    runConsumer();
}).catch(err => {
    console.error('Error connecting to MongoDB:', err);
});

// Konfigurasi Kafka
const kafka = new Kafka({
    clientId: 'booking-consumer',
    brokers: ['localhost:9092']
});

const consumer = kafka.consumer({ groupId: 'booking-group' });

const runConsumer = async () => {
    await consumer.connect();
    await consumer.subscribe({ topic: 'miliaTubes', fromBeginning: true });

    await consumer.run({
        eachMessage: async ({ topic, partition, message }) => {
            try {
                const event = JSON.parse(message.value.toString());
                console.log(`Received message: ${event.action} booking with data: ${event.booking || event.bookingId}`);

                if (event.action === 'create') {
                    await handleCreateBooking(event.booking);
                } else if (event.action === 'update') {
                    await handleUpdateBooking(event.booking);
                } else if (event.action === 'delete') {
                    await handleDeleteBooking(event.bookingId);
                }
            } catch (err) {
                console.error('Error processing booking message:', err);
            }
        },
    });
};

const handleCreateBooking = async (booking) => {
    try {
        const newPaymentProof = new PaymentProof({
            bookingId: booking._id,
            amount: booking.total_harga,
            status: 'Pending',
            createdAt: new Date()
        });
        await newPaymentProof.save();
        console.log('Payment proof created:', newPaymentProof);
    } catch (err) {
        console.error('Error creating payment proof:', err);
    }
};

const handleUpdateBooking = async (booking) => {
    try {
        const paymentProof = await PaymentProof.findOne({ bookingId: booking._id });
        if (!paymentProof) {
            console.error('Payment proof not found for booking ID:', booking._id);
            return;
        }
        paymentProof.amount = booking.total_harga;
        paymentProof.updatedAt = new Date();
        await paymentProof.save();
        console.log('Payment proof updated:', paymentProof);
    } catch (err) {
        console.error('Error updating payment proof:', err);
    }
};

const handleDeleteBooking = async (bookingId) => {
    try {
        console.log('Deleting payment proof for booking ID:', bookingId);
        const paymentProof = await PaymentProof.findOne({ bookingId });
        if (paymentProof) {
            console.log('Found payment proof:', paymentProof);
            await PaymentProof.deleteOne({ bookingId });
            console.log('Payment proof deleted for booking ID:', bookingId);
        } else {
            console.log('No payment proof found for booking ID:', bookingId);
        }
    } catch (err) {
        console.error('Error deleting payment proof:', err);
    }
};

module.exports = { runConsumer };
