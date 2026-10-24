require('dotenv').config();
const { PrismaClient } = require('@prisma/client');

async function main() {
  console.log("DATABASE_URL:", process.env.DATABASE_URL?.replace(/:[^:@]+@/, ':***@'));
  console.log("DIRECT_URL:", process.env.DIRECT_URL?.replace(/:[^:@]+@/, ':***@'));
  
  console.log("\nAttempting $connect with DATABASE_URL...");
  const p1 = new PrismaClient({ datasources: { db: { url: process.env.DATABASE_URL } } });
  try {
    await p1.$connect();
    console.log("DATABASE_URL $connect SUCCESS!");
    const count = await p1.user.count();
    console.log("Users count:", count);
  } catch (err) {
    console.error("DATABASE_URL error:", err.message);
  } finally {
    await p1.$disconnect();
  }

  console.log("\nAttempting $connect with DIRECT_URL...");
  const p2 = new PrismaClient({ datasources: { db: { url: process.env.DIRECT_URL } } });
  try {
    await p2.$connect();
    console.log("DIRECT_URL $connect SUCCESS!");
    const count = await p2.user.count();
    console.log("Users count:", count);
  } catch (err) {
    console.error("DIRECT_URL error:", err.message);
  } finally {
    await p2.$disconnect();
  }
}

main();
