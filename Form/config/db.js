const mongoose = require('mongoose');

const connectDB = async () => {
    try {
        await mongoose.connect('mongodb://localhost:27017/Tubes', {
            useNewUrlParser: true,
            useUnifiedTopology: true
        });
        console.log('MongoDB connected to Tubes database');
    } catch (err) {
        console.error(err.message);
        process.exit(1);
    }
};

module.exports = connectDB;
