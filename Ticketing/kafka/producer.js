const kafka = require('kafka-node');
const Producer = kafka.Producer;
const client = new kafka.KafkaClient({ kafkaHost: 'localhost:9092' });
const producer = new Producer(client);

producer.on('ready', () => {
    console.log('Kafka Producer is ready');
});

producer.on('error', (err) => {
    console.error('Error in Kafka Producer:', err);
});

const sendMessage = (topic, message) => {
    const payloads = [
        {
            topic: topic,
            messages: JSON.stringify(message),
        },
    ];

    producer.send(payloads, (err, data) => {
        if (err) {
            console.error('Error sending message to Kafka:', err);
        } else {
            console.log('Message sent to Kafka:', data);
        }
    });
};

module.exports = sendMessage;
