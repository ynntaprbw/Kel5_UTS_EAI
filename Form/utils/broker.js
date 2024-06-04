const amqp = require('amqplib/callback_api');

let channel = null;

// Connect to RabbitMQ
function connect() {
  amqp.connect('amqp://localhost', (err, connection) => {
    if (err) {
      console.error('Failed to connect to RabbitMQ', err);
      return;
    }
    console.log('Connected to RabbitMQ');
    connection.createChannel((err, ch) => {
      if (err) {
        console.error('Failed to create channel', err);
        return;
      }
      channel = ch;
      console.log('Channel created');
    });
  });
}

function sendToQueue(queue, msg) {
  if (channel) {
    channel.assertQueue(queue, { durable: false });
    channel.sendToQueue(queue, Buffer.from(msg));
    console.log(`Sent message to ${queue}: ${msg}`);
  } else {
    console.error('Channel is not initialized');
  }
}

function consumeFromQueue(queue, callback) {
  if (channel) {
    channel.assertQueue(queue, { durable: false });
    channel.consume(queue, (msg) => {
      if (msg !== null) {
        callback(msg.content.toString());
        channel.ack(msg);
      }
    });
  } else {
    console.error('Channel is not initialized');
  }
}

module.exports = {
  connect,
  sendToQueue,
  consumeFromQueue,
};
