const https = require('https');

const token = process.env.SUPABASE_ACCESS_TOKEN || process.env.SUPABASE_TOKEN;
const projectRef = process.env.SUPABASE_PROJECT_REF || 'hqnwxckuptagvsizanho';

if (!token) {
  console.error('Missing SUPABASE_ACCESS_TOKEN. Please set the environment variable.');
  process.exit(1);
}

const denoCode = `const STORAGE_URL = "https://hqnwxckuptagvsizanho.supabase.co/storage/v1/object/public/finery-room";

const MIME_MAP: Record<string, string> = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "application/javascript; charset=utf-8",
  ".svg": "image/svg+xml",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".png": "image/png",
  ".json": "application/json"
};

Deno.serve(async (req: Request) => {
  const url = new URL(req.url);
  let path = url.pathname.replace(/^\\/functions\\/v1\\/finery-room/, "").replace(/^\\/finery-room/, "");
  if (!path || path === "/" || path === "") {
    path = "/index.html";
  }

  const ext = "." + (path.split(".").pop() || "").toLowerCase();
  const contentType = MIME_MAP[ext] || "text/plain";

  const targetUrl = STORAGE_URL + path;
  const resp = await fetch(targetUrl);

  if (!resp.ok) {
    return new Response("Not Found: " + path, { status: 404 });
  }

  const data = await resp.arrayBuffer();

  return new Response(data, {
    status: 200,
    headers: {
      "Content-Type": contentType,
      "Access-Control-Allow-Origin": "*",
      "Cache-Control": "public, max-age=600"
    }
  });
});
`;

const postData = JSON.stringify({
  verify_jwt: false,
  body: denoCode
});

const req = https.request({
  hostname: 'api.supabase.com',
  path: `/v1/projects/${projectRef}/functions/finery-room`,
  method: 'PATCH',
  headers: {
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(postData)
  }
}, (res) => {
  let b = '';
  res.on('data', c => b += c);
  res.on('end', () => {
    console.log('Update Status:', res.statusCode);
    console.log('Response:', b);
  });
});

req.on('error', e => console.error(e));
req.write(postData);
req.end();
