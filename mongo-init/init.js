db = db.getSiblingDB('products_db');

db.createUser({
  user: 'products',
  pwd: 'apiProducts',
  roles: [{ role: 'readWrite', db: 'products_db' }],
});
