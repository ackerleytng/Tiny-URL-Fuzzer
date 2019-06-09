var http = require('http');
var util = require('util');

const ip = "0.0.0.0";
const port = process.argv[2];

http.createServer(function (req, res) {
  const addr = req.connection.address();
  const url = addr.address + ':' + addr.port + req.url;

  console.log(util.format(
    "[%s] - http://%s - [%s]",
    req.connection.remoteAddress,
    url,
    req.headers['user-agent'] || ''
  ));

  res.writeHead(200, {'Content-Type': 'text/plain'});
  res.end(url + '\n');
}).listen(port, ip);

console.log("Server running at http://" + ip + ":" + port);
