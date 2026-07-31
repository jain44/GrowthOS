const net = require('net');

const client = net.connect({ host: 'aws-0-ap-southeast-2.pooler.supabase.com', port: 6543 }, () => {
  console.log('CONNECTED TO 6543');
  client.end();
});

client.on('error', (err) => {
  console.error('CONNECT ERROR:', err.message);
});
