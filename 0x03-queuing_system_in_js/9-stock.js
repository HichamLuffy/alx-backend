import express from 'express';
import { createClient } from 'redis';
import { promisify } from 'util';

const listProducts = [
  { id: 1, name: 'Suitcase 250', price: 50, stock: 4 },
  { id: 2, name: 'Suitcase 450', price: 100, stock: 10 },
  { id: 3, name: 'Suitcase 650', price: 350, stock: 2 },
  { id: 4, name: 'Suitcase 1050', price: 550, stock: 5 }
];

const app = express();
const port = 1245;

const client = createClient();
const getAsync = promisify(client.get).bind(client);

function getItemById(id) {
  return listProducts.find(product => product.id === id);
}

function reserveStockById(itemId, stock) {
  client.set(`item.${itemId}`, stock);
}

async function getCurrentReservedStockById(itemId) {
  const stock = await getAsync(`item.${itemId}`);
  return stock ? parseInt(stock, 10) : null;
}

app.get('/list_products', (req, res) => {
  res.json(listProducts.map(product => ({
    itemId: product.id,
    itemName: product.name,
    price: product.price,
    initialAvailableQuantity: product.stock
  })));
});

app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const product = getItemById(itemId);

  if (!product) {
    return res.json({ status: 'Product not found' });
  }

  const currentStock = await getCurrentReservedStockById(itemId);
  res.json({
    itemId: product.id,
    itemName: product.name,
    price: product.price,
    initialAvailableQuantity: product.stock,
    currentQuantity: currentStock !== null ? currentStock : product.stock
  });
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const product = getItemById(itemId);

  if (!product) {
    return res.json({ status: 'Product not found' });
  }

  const currentStock = await getCurrentReservedStockById(itemId);

  if (currentStock === null) {
    reserveStockById(itemId, product.stock - 1);
    return res.json({ status: 'Reservation confirmed', itemId });
  }

  if (currentStock <= 0) {
    return res.json({ status: 'Not enough stock available', itemId });
  }

  reserveStockById(itemId, currentStock - 1);
  res.json({ status: 'Reservation confirmed', itemId });
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
