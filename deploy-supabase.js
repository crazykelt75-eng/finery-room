/**
 * Finery Room — Supabase Storage Static Deployment Script
 * Deploys index.html, style.css, script.js, and assets to a public Supabase Storage bucket.
 * 
 * Usage:
 *   node deploy-supabase.js
 * 
 * Requirements:
 *   Set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY environment variables,
 *   or fill them into the config object below.
 */

const fs = require('fs');
const path = require('path');

// Try requiring @supabase/supabase-js
let createClient;
try {
  createClient = require('@supabase/supabase-js').createClient;
} catch (err) {
  console.log('To run this deployment script, please install @supabase/supabase-js:');
  console.log('  npm install @supabase/supabase-js');
  console.log('Then run: node deploy-supabase.js');
  process.exit(0);
}

const SUPABASE_URL = process.env.SUPABASE_URL || 'YOUR_SUPABASE_URL';
const SUPABASE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY || 'YOUR_SUPABASE_SERVICE_ROLE_KEY';
const BUCKET_NAME = process.env.SUPABASE_BUCKET || 'finery-room-site';

if (SUPABASE_URL === 'YOUR_SUPABASE_URL' || SUPABASE_KEY === 'YOUR_SUPABASE_SERVICE_ROLE_KEY') {
  console.error('\n⚠️ Missing Supabase Credentials!');
  console.error('Please configure your SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY.');
  console.error('Example:');
  console.error('  set SUPABASE_URL=https://xyzcompany.supabase.co');
  console.error('  set SUPABASE_SERVICE_ROLE_KEY=eyJh...');
  console.error('  node deploy-supabase.js\n');
  process.exit(1);
}

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

function getMimeType(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  const map = {
    '.html': 'text/html; charset=UTF-8',
    '.css': 'text/css; charset=UTF-8',
    '.js': 'application/javascript; charset=UTF-8',
    '.json': 'application/json',
    '.svg': 'image/svg+xml',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png': 'image/png',
    '.webp': 'image/webp'
  };
  return map[ext] || 'application/octet-stream';
}

function getAllFiles(dirPath, arrayOfFiles = []) {
  const files = fs.readdirSync(dirPath);
  files.forEach(file => {
    const fullPath = path.join(dirPath, file);
    if (fs.statSync(fullPath).isDirectory()) {
      if (file !== 'node_modules' && file !== '.git') {
        getAllFiles(fullPath, arrayOfFiles);
      }
    } else {
      arrayOfFiles.push(fullPath);
    }
  });
  return arrayOfFiles;
}

async function deploy() {
  console.log(`\n💎 Starting Finery Room deployment to Supabase Storage [${BUCKET_NAME}]...`);
  
  // 1. Ensure bucket exists
  const { data: buckets, error: listErr } = await supabase.storage.listBuckets();
  if (listErr) {
    console.error('Error listing buckets:', listErr.message);
    process.exit(1);
  }

  const bucketExists = buckets.some(b => b.name === BUCKET_NAME);
  if (!bucketExists) {
    console.log(`Creating public bucket: ${BUCKET_NAME}...`);
    const { error: createErr } = await supabase.storage.createBucket(BUCKET_NAME, {
      public: true
    });
    if (createErr) {
      console.error('Error creating bucket:', createErr.message);
      process.exit(1);
    }
  }

  // 2. Upload files
  const rootDir = __dirname;
  const filesToUpload = [
    path.join(rootDir, 'index.html'),
    path.join(rootDir, 'style.css'),
    path.join(rootDir, 'script.js'),
    ...getAllFiles(path.join(rootDir, 'assets'))
  ];

  for (const filePath of filesToUpload) {
    if (!fs.existsSync(filePath)) continue;
    const relPath = path.relative(rootDir, filePath).replace(/\\/g, '/');
    const fileBody = fs.readFileSync(filePath);
    const contentType = getMimeType(filePath);

    console.log(`Uploading: ${relPath} (${contentType})...`);
    const { error: uploadErr } = await supabase.storage
      .from(BUCKET_NAME)
      .upload(relPath, fileBody, {
        contentType,
        upsert: true
      });

    if (uploadErr) {
      console.error(`Failed to upload ${relPath}:`, uploadErr.message);
    }
  }

  const { data: publicUrlData } = supabase.storage
    .from(BUCKET_NAME)
    .getPublicUrl('index.html');

  console.log('\n✨ Deployment Complete!');
  console.log(`Public Website URL: ${publicUrlData.publicUrl}\n`);
}

deploy();
