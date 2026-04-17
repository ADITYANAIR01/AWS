const express = require('express');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

const APP_VERSION  = process.env.APP_VERSION  || '1.0.0';
const NODE_ENV     = process.env.NODE_ENV     || 'production';
const AWS_REGION   = process.env.AWS_REGION   || 'ap-south-1';
const DEPLOY_TIME  = process.env.DEPLOY_TIME  || new Date().toISOString();
const BUILD_ID     = process.env.BUILD_ID     || 'local';

app.get('/health', (req, res) => {
  res.json({ status: 'ok', version: APP_VERSION });
});

app.get('/', (req, res) => {
  let html = fs.readFileSync(path.join(__dirname, 'public', 'index.html'), 'utf8');
  html = html
    .replace(/{{APP_VERSION}}/g,  APP_VERSION)
    .replace(/{{NODE_ENV}}/g,     NODE_ENV)
    .replace(/{{AWS_REGION}}/g,   AWS_REGION)
    .replace(/{{DEPLOY_TIME}}/g,  DEPLOY_TIME)
    .replace(/{{BUILD_ID}}/g,     BUILD_ID);
  res.send(html);
});

app.listen(PORT, () => {
  console.log(`PipelineX running on port ${PORT}`);
  console.log(`Version: ${APP_VERSION} | Build: ${BUILD_ID} | Region: ${AWS_REGION}`);
});