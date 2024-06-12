import redis from 'redis';
import { promisify } from 'util';
import kue from 'kue';

const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);
const queue = kue.createQueue();

async function reserveSeat(number) {
  await setAsync('available_seats', number);
}

async function getCurrentAvailableSeats() {
  const seats = await getAsync('available_seats');
  return seats;
}

queue.process('reserve_seat', async (job, done) => {
  const seats = await getCurrentAvailableSeats();
  if (seats > 0) {
    await reserveSeat(seats - 1);
    done();
  } else {
    done(new Error('Not enough seats available'));
  }
});
