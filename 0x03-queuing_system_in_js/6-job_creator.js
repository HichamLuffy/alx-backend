import redis from 'redis';
import { promisify } from 'util';
import express from 'express';
import kue from 'kue';

const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

const app = express();
const queue = kue.createQueue();

const availableSeats = 50;
client.set('available_seats', availableSeats);
client.set('reservationEnabled', true);

async function reserveSeat(number) {
  await setAsync('available_seats', number);
}

async function getCurrentAvailableSeats() {
  const seats = await getAsync('available_seats');
  return seats;
}

app.get('/available_seats', async (req, res) => {
  const seats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: seats });
});

app.get('/reserve_seat', (req, res) => {
  const job = queue.create('reserve_seat').save((err) => {
    if (!err) res.json({ status: 'Reservation in process' });
    else res.json({ status: 'Reservation failed' });
  });

  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', () => {
    console.log(`Seat reservation job ${job.id} failed`);
  });
});

app.get('/process', (req, res) => {
  queue.process('reserve_seat', async (job, done) => {
    const seats = await getCurrentAvailableSeats();
    if (seats > 0) {
      await reserveSeat(seats - 1);
      done();
    } else {
      done(new Error('Not enough seats available'));
    }
  });
  res.json({ status: 'Queue processing' });
});

app.listen(1245, () => {
  console.log('Server running on port 1245');
});
