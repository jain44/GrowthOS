require('dotenv').config();
const { PrismaClient } = require('@prisma/client');
const p = new PrismaClient({ datasources: { db: { url: process.env.DIRECT_URL } } });

p.user.count()
  .then(c => console.log('Count:', c))
  .catch(e => console.error('Direct error:', e.message))
  .finally(() => p.$disconnect());
