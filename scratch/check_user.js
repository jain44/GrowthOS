require('dotenv').config();
const { PrismaClient } = require('@prisma/client');
const bcrypt = require('bcryptjs');

const prisma = new PrismaClient();

async function check() {
  try {
    console.log("Checking database connection...");
    const userCount = await prisma.user.count();
    console.log("Total users in DB:", userCount);
    
    const user = await prisma.user.findUnique({
      where: { email: 'demo@growthos.ai' }
    });
    console.log("User query result:", user ? { id: user.id, email: user.email, name: user.name, hasPassword: !!user.password } : "Not found");
    
    if (user && user.password) {
      const match = await bcrypt.compare('Test@1234', user.password);
      console.log("Password compare with 'Test@1234':", match);
    }
  } catch (e) {
    console.error("DB error:", e);
  } finally {
    await prisma.$disconnect();
  }
}

check();
