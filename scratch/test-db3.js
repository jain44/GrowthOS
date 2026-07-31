const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function main() {
  try {
    const users = await prisma.user.findMany();
    console.log('PRISMA CONNECTED SUCCESSFULLY! User count:', users.length);
  } catch (e) {
    console.error('PRISMA ERROR:', e.message);
  } finally {
    await prisma.$disconnect();
  }
}

main();
