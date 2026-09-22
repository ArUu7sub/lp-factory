#!/usr/bin/env node
'use strict';

const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium} = require('playwright');

const sectionIds = ['hero', 'problems', 'solution', 'use-cases', 'process', 'final-cta'];
const outputDir = path.resolve(process.argv[2] || '');

if (!process.argv[2] || !fs.existsSync(outputDir)) {
  console.error('Usage: capture-lp.cjs OUTPUT_DIR');
  process.exit(2);
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
    pass: dom.missing.length === 0 && dom.ordered && dom.scrollWidth <= dom.innerWidth + 1 && consoleErrors.length === 0 && pageErrors.length === 0 && failedRequests.length === 0,
  };
}

(async () => {
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
