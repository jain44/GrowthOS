const { Client } = require('pg');

const client = new Client({
  connectionString: 'postgresql://postgres.qufbsilxitduuydtklwq:Jainamjain%2312@aws-0-ap-southeast-2.pooler.supabase.com:6543/postgres?sslmode=require',
});

client.connect()
  .then(() => {
    console.log('SUCCESSFULLY AUTHENTICATED TO SUPABASE POSTGRES!');
    return client.query('SELECT current_database(), current_user;');
  })
  .then((res) => {
    console.log('QUERY RESULT:', res.rows);
    return client.end();
  })
  .catch((err) => {
    console.error('AUTH ERROR:', err.message);
    client.end();
  });
