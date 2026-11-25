// Oss! Squad hidden test build: tiny static server for Railway (no dependencies).
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.join(__dirname, 'public'), PORT = process.env.PORT || 8080;
const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.json': 'application/json',
  '.webmanifest': 'application/manifest+json', '.png': 'image/png', '.webp': 'image/webp', '.jpg': 'image/jpeg',
  '.svg': 'image/svg+xml', '.txt': 'text/plain', '.css': 'text/css', '.ico': 'image/x-icon' };
http.createServer((req, res) => {
  let p = decodeURIComponent((req.url || '/').split('?')[0]);
  if (p.endsWith('/')) p += 'index.html';
  let f = path.normalize(path.join(ROOT, p));
  if (!f.startsWith(ROOT)) { res.writeHead(403); return res.end(); }
  fs.stat(f, (err, st) => {
    if (err || !st.isFile()) f = path.join(ROOT, 'index.html');
    const ext = path.extname(f);
    res.writeHead(200, {
      'Content-Type': TYPES[ext] || 'application/octet-stream',
      'X-Robots-Tag': 'noindex, nofollow',          // hidden test build: keep it out of search
      'Cache-Control': ext === '.html' || f.endsWith('sw.js') ? 'no-cache' : 'public, max-age=86400'
    });
    fs.createReadStream(f).pipe(res);
  });
}).listen(PORT, () => console.log('Oss! Squad test build on port ' + PORT));
