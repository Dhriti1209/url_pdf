const puppeteer = require("puppeteer");

(async () => {
  const url = process.argv[2];
  const path = process.argv[3];

  if (!url || !path) {
    console.error("Missing URL or file path");
    process.exit(1);
  }

  const browser = await puppeteer.launch({
    args: ["--no-sandbox"],
    headless: true,
  });
  const page = await browser.newPage();
  await page.goto(url, { waitUntil: "networkidle2", timeout: 30000 });
  await page.pdf({ path, format: "A4" });
  await browser.close();
})();
