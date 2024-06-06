const express = require('express');
const router = express.Router();
const Booking = require('../models/Booking');
const sendMessage = require('../kafka/producer');
const validPrices = require('../utils/validPrices');
const moment = require('moment');
const nodemailer = require('nodemailer');

// Nodemailer transporter configuration
var transport = nodemailer.createTransport({
    host: "live.smtp.mailtrap.io",
    port: 587,
    auth: {
        user: "api",
        pass: "98778a64ffb9eb788f0acdebb0a55438"
    }
});

// fungsi buat send email testing pakai malitrap.io
const sendEmail = async (subject, text, to) => {
    const mailOptions = {
        from: 'mailtrap@demomailtrap.com',
        to: 'amiliaagataa@gmail.com',
        subject: subject,
        text: text
    };

    try {
        await transport.sendMail(mailOptions);
        console.log('Email sent');
    } catch (err) {
        console.error('Error sending email:', err.message);
    }
};

router.get('/', async (req, res) => {
    try {
        const lastBooking = await Ticket.findOne().sort({ createdAt: +1 });
        if (!lastBooking) return res.status(404).json({ message: 'Booking not found' });
        res.json(lastBooking);
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});


router.post('/', async (req, res) => {
    try {
        const { nama, email, jml_tiket, tgl_berangkat, no_hp, harga } = req.body;

        // Validate the received price
        const hargaValid = validPrices.some(price => price.harga === harga);
        if (!hargaValid) {
            return res.status(400).json({ message: 'Harga tidak valid' });
        }

        // Validate the number of tickets
        if (parseInt(jml_tiket) <= 0) {
            return res.status(400).json({ message: 'Jumlah tiket harus lebih besar dari 0' });
        }

        // Validate departure date
        if (!moment(tgl_berangkat, 'YYYY-MM-DD', true).isValid()) {
            return res.status(400).json({ message: 'Tanggal keberangkatan tidak valid' });
        }

        // Validate email format
        if (!/\S+@\S+\.\S+/.test(email)) {
            return res.status(400).json({ message: 'Format email tidak valid' });
        }

        // Validate phone number format
        if (!/^\d{10,14}$/.test(no_hp)) {
            return res.status(400).json({ message: 'Nomor HP harus terdiri dari 10-14 digit angka' });
        }

        // Calculate total price
        const total_harga = harga * parseInt(jml_tiket);

        // Save new booking data
        const newBooking = new Booking({ nama, email, jml_tiket, tgl_berangkat, no_hp, harga, total_harga });
        const booking = await newBooking.save();

        // Send message to Kafka
        sendMessage('miliaTubes', {
            action: 'create',
            booking
        });

        // Send confirmation email to the latest booking email address
        const subject = 'Booking Confirmation';
        const text = `Dear ${booking.nama},\n\nIni adalah pengingat bahwa keberangkatan anda ada pada tanggal: ${booking.tgl_berangkat}. Berikut merupakan detail pemesanan anda:\n\n
        Nama: ${booking.nama}\n
        Email: ${booking.email}\n
        Jumlah Tiket: ${booking.jml_tiket}\n
        Tanggal Keberangkatan: ${booking.tgl_berangkat}\n
        Nomor HP: ${booking.no_hp}\n
        Harga: ${booking.harga}\n
        Total Harga: ${booking.total_harga}\n\n
        Nb: Anda dapat melakukan perubahan dan pembatalan maksimal H+7 dari tanggal pemesanan.
        Terimakasih, Semoga Perjalanan anda menyenangkan!\n`;
        sendEmail(subject, text, booking.email);

        res.status(201).json(booking);
    } catch (err) {
        res.status(400).json({ message: err.message });
    }
});


// Route to update the last booking input
router.put('/', async (req, res) => {
    try {
        const { nama, email, jml_tiket, tgl_berangkat, no_hp, harga } = req.body;

        // Validate the received price
        const hargaValid = validPrices.some(price => price.harga === harga);
        if (!hargaValid) {
            return res.status(400).json({ message: 'Harga tidak valid' });
        }

        // Get the last booking
        const booking = await Booking.findOne().sort({ createdAt: -1 });
        if (!booking) {
            return res.status(404).json({ message: 'Booking not found' });
        }

        // Compare the current date with the booking createdAt
        const dateNow = moment();
        const bookingDate = moment(booking.createdAt);
        const diffInDays = dateNow.diff(bookingDate, 'days');

        // Maximum time limit for updating
        const maxDays = 7;

        if (diffInDays > maxDays) {
            return res.status(400).json({ message: `Masa waktu perubahan telah berakhir. Anda hanya dapat memperbarui booking dalam ${maxDays} hari setelah waktu pencatatan.` });
        }

        // Calculate total price
        const total_harga = harga * parseInt(jml_tiket);

        // Update booking data
        booking.nama = nama;
        booking.email = email;
        booking.jml_tiket = jml_tiket;
        booking.tgl_berangkat = tgl_berangkat;
        booking.no_hp = no_hp;
        booking.harga = harga;
        booking.total_harga = total_harga;

        // Save the updated booking
        await booking.save();

        // Send message to Kafka
        sendMessage('miliaTubes', {
            action: 'update',
            booking
        });

        // Send confirmation email to the latest booking email address
        const subject = 'Booking Update Confirmation';
        const text = `Dear ${booking.nama},\n\nPerubahan keberangkatan berhasil di update, keberangkatan anda ada pada tanggal: ${booking.tgl_berangkat}. Berikut merupakan detail pemesanan anda:\n\n
        Nama: ${booking.nama}\n
        Email: ${booking.email}\n
        Jumlah Tiket: ${booking.jml_tiket}\n
        Tanggal Keberangkatan: ${booking.tgl_berangkat}\n
        Nomor HP: ${booking.no_hp}\n
        Harga: ${booking.harga}\n
        Total Harga: ${booking.total_harga}\n\n
        Nb: Anda dapat melakukan perubahan dan pembatalan maksimal H+7 dari tanggal pemesanan.
        Terimakasih, Semoga Perjalanan anda menyenangkan!\n`;
        sendEmail(subject, text, booking.email);

        res.status(200).json(booking);
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});


// Route to delete the last booking input
router.delete('/', async (req, res) => {
    try {
        // Get the last booking
        const lastBooking = await Booking.findOne().sort({ createdAt: -1 });
        if (!lastBooking) {
            return res.status(404).json({ message: 'Booking not found' });
        }

        // Compare the current date with the booking createdAt
        const dateNow = moment();
        const bookingDate = moment(lastBooking.createdAt);
        const diffInDays = dateNow.diff(bookingDate, 'days');

        // Maximum time limit for deleting
        const maxDays = 7;

        if (diffInDays > maxDays) {
            return res.status(400).json({ message: `Masa waktu penghapusan telah berakhir. Anda hanya dapat menghapus booking dalam ${maxDays} hari setelah waktu pencatatan.` });
        }

        // Delete the last booking
        await Booking.deleteOne({ _id: lastBooking._id });

        // Send delete confirmation message to Kafka
        sendMessage('miliaTubes', {
            action: 'delete',
            bookingId: lastBooking._id
        });

        // Send confirmation email to the latest booking email address
        const subject = 'Booking Delete Confirmation';
        const text = `Dear ${lastBooking.nama},\n\nKeberangkatan anda ada pada tanggal: ${lastBooking.tgl_berangkat} Berhasil dihapus. Berikut merupakan detail pemesanan anda:\n\n
        Nama: ${lastBooking.nama}\n
        Email: ${lastBooking.email}\n
        Jumlah Tiket: ${lastBooking.jml_tiket}\n
        Tanggal Keberangkatan: ${lastBooking.tgl_berangkat}\n
        Nomor HP: ${lastBooking.no_hp}\n
        Harga: ${lastBooking.harga}\n
        Total Harga: ${lastBooking.total_harga}\n\n
        Terimakasih, Semoga anda puas dengan pelayanan kami!\n`;
        sendEmail(subject, text, lastBooking.email);

        res.status(200).json({ message: 'Booking deleted' });
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

module.exports = router;

