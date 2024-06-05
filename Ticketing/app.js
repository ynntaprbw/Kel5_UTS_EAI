const express = require('express');
const mongoose = require('mongoose');
const bookingRouter = require('./routes/booking');
const paymentProofRouter = require('./routes/paymentproof');
const consumer = require('./kafka/consumer'); 

const app = express();

app.use(express.json());

// DB Connection
mongoose.connect('mongodb://localhost:27017/Tubes', { useNewUrlParser: true, useUnifiedTopology: true });
const db = mongoose.connection;
db.on('error', (err) => {
  console.error('MongoDB connection error:', err);
});
db.once('open', function () {
  console.log("Connected to MongoDB");
});

// Routes
app.use('/api/bookings', bookingRouter);
app.use('/api/paymentproofs', paymentProofRouter);

// Error handling
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send('Something broke!');
});

// Server
const port = 5001;
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});

module.exports = app;
