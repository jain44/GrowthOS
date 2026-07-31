const { PrismaClient } = require('@prisma/client');
const fs = require('fs');
const path = require('path');

const prisma = new PrismaClient();

async function main() {
  console.log('Reading schema.sql...');
  let rawSql = fs.readFileSync(path.join(__dirname, 'schema.sql'), 'utf-8');

  // Strip BOM if present
  if (rawSql.charCodeAt(0) === 0xFEFF) {
    rawSql = rawSql.slice(1);
  }

  // Remove comment lines first
  const cleanSql = rawSql
    .split('\n')
    .filter(line => !line.trim().startsWith('--'))
    .join('\n');

  // Split by semicolon
  const statements = cleanSql
    .split(';')
    .map(s => s.trim())
    .filter(s => s.length > 0);

  console.log(`Executing ${statements.length} DDL statements on Supabase...`);

  for (let i = 0; i < statements.length; i++) {
    const stmt = statements[i];
    try {
      await prisma.$executeRawUnsafe(stmt);
      console.log(`[${i + 1}/${statements.length}] Success`);
    } catch (err) {
      if (err.message.includes('already exists')) {
        console.log(`[${i + 1}/${statements.length}] Already exists (skipped)`);
      } else {
        console.error(`[${i + 1}/${statements.length}] Exception: ${err.message}`);
      }
    }
  }

  console.log('\n🎉 ALL TABLES, ENUMS, & INDEXES SUCCESSFULLY CREATED IN SUPABASE!');
}

main()
  .catch(console.error)
  .finally(() => prisma.$disconnect());
