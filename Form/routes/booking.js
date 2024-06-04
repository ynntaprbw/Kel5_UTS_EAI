const express = require('express');
const router = express.Router();
const Booking = require('../models/Booking');
const validPrices = require('./validPrices');
const moment = require('moment');


// Rute untuk pemesanan baru
router.post('/', async (req, res) => {
    try {
        const { nama, email, jml_tiket, no_hp, harga } = req.body;

        // Validasi harga yang diterima
        const validPrices = [100000, 200000, 300000];
        if (!validPrices.includes(harga)) {
            return res.status(400).json({ message: 'Harga tidak valid' });
        }

        // Validasi jumlah tiket
        if (parseInt(jml_tiket) <= 0) {
            return res.status(400).json({ message: 'Jumlah tiket harus lebih besar dari 0' });
        }

        // Validasi email
        if (!/\S+@\S+\.\S+/.test(email)) {
            return res.status(400).json({ message: 'Format email tidak valid' });
        }

        // Validasi nomor telepon
        if (!/^\d{10,14}$/.test(no_hp)) {
            return res.status(400).json({ message: 'Nomor HP harus terdiri dari 10-14 digit angka' });
        }

        // Hitung total harga
        const total_harga = harga * parseInt(jml_tiket);

        const newBooking = new Booking({ nama, email, jml_tiket, no_hp, harga, total_harga });
        const booking = await newBooking.save();
        res.status(201).json(booking);
    } catch (err) {
        res.status(400).json({ message: err.message });
    }
});


// Rute untuk mendapatkan pemesanan terakhir kali input form
router.get('/', async (req, res) => {
    try {
        const lastBooking = await Booking.findOne().sort({ timestamp: -1 });
        if (!lastBooking) return res.status(404).json({ message: 'Booking not found' });
        res.json(lastBooking);
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

// Rute untuk memperbarui pemesanan terakhir kali input form
router.put('/', async (req, res) => {
    try {
        const { nama, email, jml_tiket, no_hp, harga } = req.body;

        // Validasi harga yang diterima
        const hargaValid = validPrices.some(price => price.harga === harga);
        if (!hargaValid) {
            return res.status(400).json({ message: 'Harga tidak valid' });
        }

        // Ambil pemesanan terakhir
        const lastBooking = await Booking.findOne().sort({ timestamp: -1 });
        if (!lastBooking) {
            return res.status(404).json({ message: 'Booking not found' });
        }

        // Bandingkan tanggal sekarang dengan tanggal pencatatan booking
        const dateNow = moment();
        const bookingDate = moment(lastBooking.timestamp);
        const diffInDays = dateNow.diff(bookingDate, 'days');

        // Batas waktu maksimum untuk memperbarui
        const maxDays = 7;

        if (diffInDays > maxDays) {
            return res.status(400).json({ message: `Masa waktu perubahan telah berakhir. Anda hanya dapat memperbarui booking dalam ${maxDays} hari setelah waktu pencatatan.` });
        }

        // Hitung total harga
        const total_harga = harga * parseInt(jml_tiket);

        // Perbarui data booking
        lastBooking.nama = nama;
        lastBooking.email = email;
        lastBooking.jml_tiket = jml_tiket;
        lastBooking.no_hp = no_hp;
        lastBooking.harga = harga;
        lastBooking.total_harga = total_harga;

        await lastBooking.save();

        res.json(lastBooking);
    } catch (err) {
        res.status(400).json({ message: err.message });
    }
});

// Rute untuk menghapus pemesanan terakhir kali diinput
router.delete('/', async (req, res) => {
    try {
        // Dapatkan data booking terakhir kali diinput
        const lastBooking = await Booking.findOne().sort({ timestamp: -1 });
        if (!lastBooking) {
            return res.status(404).json({ message: 'Booking not found' });
        }

        // Bandingkan tanggal sekarang dengan tanggal pencatatan booking
        const dateNow = moment();
        const bookingDate = moment(lastBooking.timestamp);
        const diffInDays = dateNow.diff(bookingDate, 'days');

        // Batas waktu maksimum untuk menghapus
        const maxDays = 7;

        if (diffInDays > maxDays) {
            return res.status(400).json({ message: `Masa waktu penghapusan telah berakhir. Anda hanya dapat menghapus booking dalam ${maxDays} hari setelah waktu pencatatan.` });
        }

        // Hapus data booking terakhir kali diinput
        await Booking.deleteOne({ _id: lastBooking._id });
        res.json({ message: 'Booking deleted' });
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

module.exports = router;
