#!/usr/bin/env node
'use strict';

const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const crypto = require('node:crypto');
const {chromium} = require('playwright');

const sectionIds = ['hero', 'problems', 'solution', 'use-cases', 'process', 'final-cta'];
const outputDir = path.resolve(process.argv[2] || '');

if (!process.argv[2] || !fs.existsSync(outputDir)) {
  console.error('Usage: capture-lp.cjs OUTPUT_DIR');
  process.exit(2);
}

const sourceFontPath = path.resolve(process.env.LP_JAPANESE_FONT_PATH || '');
const sourceLicensePath = path.resolve(process.env.LP_JAPANESE_FONT_LICENSE_PATH || '');
if (!process.env.LP_JAPANESE_FONT_PATH || !fs.existsSync(sourceFontPath)) {
  console.error('LP_JAPANESE_FONT_PATH must point to the verified Noto Sans JP font.');
  process.exit(2);
}
if (!process.env.LP_JAPANESE_FONT_LICENSE_PATH || !fs.existsSync(sourceLicensePath)) {
  console.error('LP_JAPANESE_FONT_LICENSE_PATH must point to the font license.');
  process.exit(2);
}

const bundledFontRelative = 'assets/fonts/NotoSansJP-Variable.ttf';
const bundledLicenseRelative = 'assets/fonts/OFL.txt';
const bundledFontPath = path.join(outputDir, bundledFontRelative);
const bundledLicensePath = path.join(outputDir, bundledLicenseRelative);
const markerStart = '/* lp-factory:noto-sans-jp:start */';
const markerEnd = '/* lp-factory:noto-sans-jp:end */';

function fontCss(relativeUrl) {
  return `${markerStart}\n@font-face {\n  font-family: "LP Noto Sans JP";\n  src: url("${relativeUrl}") format("truetype");\n  font-style: normal;\n  font-weight: 100 900;\n  font-display: block;\n}\nhtml, body, button, input, textarea, select {\n  font-family: "LP Noto Sans JP", "Noto Sans JP", "Yu Gothic", Meiryo, sans-serif !important;\n}\n${markerEnd}`;
}

function upsertCssFile(relativePath, fontUrl) {
  const target = path.join(outputDir, relativePath);
  if (!fs.existsSync(target)) throw new Error(`Missing stylesheet required for font bundling: ${relativePath}`);
  let css = fs.readFileSync(target, 'utf8');
  const blockPattern = new RegExp(`${markerStart.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}[\\s\\S]*?${markerEnd.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\n?`, 'g');
  css = css.replace(blockPattern, '').trimStart();
  fs.writeFileSync(target, `${fontCss(fontUrl)}\n\n${css}`);
}

function upsertWireframeFont() {
  const relativePath = 'design/wireframe.html';
  const target = path.join(outputDir, relativePath);
  if (!fs.existsSync(target)) throw new Error(`Missing HTML required for font bundling: ${relativePath}`);
  let html = fs.readFileSync(target, 'utf8');
  const stylePattern = /<style data-lp-factory-japanese-font>[\s\S]*?<\/style>\s*/g;
  html = html.replace(stylePattern, '');
  const style = `<style data-lp-factory-japanese-font>\n${fontCss('../assets/fonts/NotoSansJP-Variable.ttf')}\n</style>\n`;
  html = html.includes('</head>') ? html.replace('</head>', `${style}</head>`) : `${style}${html}`;
  fs.writeFileSync(target, html);
}

function prepareJapaneseFont() {
  fs.mkdirSync(path.dirname(bundledFontPath), {recursive: true});
  fs.copyFileSync(sourceFontPath, bundledFontPath);
  fs.copyFileSync(sourceLicensePath, bundledLicensePath);
  upsertCssFile('styles.css', './assets/fonts/NotoSansJP-Variable.ttf');
  upsertCssFile('design/prototype/styles.css', '../../assets/fonts/NotoSansJP-Variable.ttf');
  upsertWireframeFont();
  return {
    path: bundledFontRelative,
    license: bundledLicenseRelative,
    bytes: fs.statSync(bundledFontPath).size,
    sha256: crypto.createHash('sha256').update(fs.readFileSync(bundledFontPath)).digest('hex'),
  };
}

const jobs = [
  {name: 'wireframe', input: 'design/wireframe.html', output: 'design/wireframe.png', width: 1440, height: 1000},
  {name: 'design-desktop', input: 'design/prototype/index.html', output: 'design/desktop.png', width: 1440, height: 1000},
  {name: 'design-mobile', input: 'design/prototype/index.html', output: 'design/mobile.png', width: 390, height: 844},
  {name: 'implementation-desktop', input: 'index.html', output: 'implementation/screenshots/desktop.png', width: 1440, height: 1000},
  {name: 'implementation-mobile', input: 'index.html', output: 'implementation/screenshots/mobile.png', width: 390, height: 844},
];

async function capture(browser, job) {
  const inputPath = path.join(outputDir, job.input);
  const outputPath = path.join(outputDir, job.output);
  if (!fs.existsSync(inputPath)) {
    throw new Error(`${job.name}: missing input ${job.input}`);
  }
  fs.mkdirSync(path.dirname(outputPath), {recursive: true});

  const context = await browser.newContext({
    viewport: {width: job.width, height: job.height},
    deviceScaleFactor: 1,
    reducedMotion: 'reduce',
  });
  const page = await context.newPage();
  const consoleErrors = [];
  const pageErrors = [];
  const failedRequests = [];

  page.on('console', (message) => {
    if (message.type() === 'error') consoleErrors.push(message.text());
  });
  page.on('pageerror', (error) => pageErrors.push(String(error)));
  page.on('requestfailed', (request) => {
    failedRequests.push({url: request.url(), error: request.failure()?.errorText || 'unknown'});
  });

  await page.goto(pathToFileURL(inputPath).href, {waitUntil: 'load'});
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(250);

  const dom = await page.evaluate((expectedIds) => {
    const positions = expectedIds.map((id) => {
      const element = document.getElementById(id);
      return element ? {id, top: element.getBoundingClientRect().top + window.scrollY} : {id, top: null};
    });
    return {
      innerWidth: window.innerWidth,
      scrollWidth: document.documentElement.scrollWidth,
      scrollHeight: document.documentElement.scrollHeight,
      positions,
      missing: positions.filter((item) => item.top === null).map((item) => item.id),
      ordered: positions.every((item, index) => index === 0 || item.top === null || positions[index - 1].top === null || item.top >= positions[index - 1].top),
      japaneseFontReady: document.fonts.check('16px "LP Noto Sans JP"', '日本語表示確認'),
      bodyFontFamily: getComputedStyle(document.body).fontFamily,
    };
  }, sectionIds);

  await page.screenshot({path: outputPath, fullPage: true, animations: 'disabled'});
  await context.close();

  return {
    ...job,
    input: job.input,
    output: job.output,
    pngBytes: fs.statSync(outputPath).size,
    dom,
    consoleErrors,
    pageErrors,
    failedRequests,
    pass: dom.missing.length === 0 && dom.ordered && dom.scrollWidth <= dom.innerWidth + 1 && dom.japaneseFontReady && dom.bodyFontFamily.includes('LP Noto Sans JP') && consoleErrors.length === 0 && pageErrors.length === 0 && failedRequests.length === 0,
  };
}

(async () => {
  const japaneseFont = prepareJapaneseFont();
  const browser = await chromium.launch({headless: true});
  const results = [];
  try {
    for (const job of jobs) results.push(await capture(browser, job));
  } finally {
    await browser.close();
  }

  const evidence = {
    generatedAt: new Date().toISOString(),
    renderer: {
      node: process.version,
      playwright: require('playwright/package.json').version,
      chromium: chromium.executablePath(),
      japaneseFont,
    },
    sectionIds,
    results,
    pass: results.every((result) => result.pass),
  };
  const evidencePath = path.join(outputDir, 'implementation/render-evidence.json');
  fs.mkdirSync(path.dirname(evidencePath), {recursive: true});
  fs.writeFileSync(evidencePath, JSON.stringify(evidence, null, 2) + '\n');
  console.log(JSON.stringify({pass: evidence.pass, evidence: evidencePath, captures: results.map((r) => r.output)}));
  if (!evidence.pass) process.exit(1);
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
