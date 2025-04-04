const { chromium } = require('playwright');
const express = require('express');
const app = express();

app.use(express.json());

let browser, page;

// Debug information about the environment
console.log('Environment check:');
console.log(`DISPLAY=${process.env.DISPLAY}`);
console.log(`Current user: ${require('os').userInfo().username}`);

// Initialize browser function with better error handling
async function initBrowser() {
  try {
    console.log("Launching browser...");
    browser = await chromium.launch({ 
      headless: false,
      args: [
        '--no-sandbox', 
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage'
      ]
    });
    
    const context = await browser.newContext();
    page = await context.newPage();
    console.log("🚀 Browser is ready.");
    
    // Go to google.com
    await page.goto('https://www.google.com');
    console.log("Successfully navigated to Google");
    
    return true;
  } catch (error) {
    console.error("Browser initialization failed:", error);
    return false;
  }
}

// Try to initialize the browser on startup
(async () => {
  // Allow X server time to start (important in Docker environment)
  console.log("Waiting for X server to be ready...");
  await new Promise(resolve => setTimeout(resolve, 5000));
  
  const success = await initBrowser();
  if (!success) {
    console.log("Initial browser launch failed. Use /initialize endpoint to retry.");
  }
})();

// Endpoint: initialize browser
app.post('/initialize', async (req, res) => {
  try {
    // Close existing browser if it exists
    if (browser) {
      await browser.close();
    }
    
    const success = await initBrowser();
    if (success) {
      res.send("Browser initialized and ready.");
    } else {
      res.status(500).send("Failed to initialize browser. Check server logs.");
    }
  } catch (error) {
    res.status(500).send(`Failed to initialize browser: ${error.toString()}`);
  }
});

// Endpoint: navigate
app.post('/navigate', async (req, res) => {
  const { url } = req.body;
  try {
    if (!page) {
      return res.status(400).send("Browser not initialized. Call /initialize first.");
    }
    await page.goto(url);
    res.send(`Navigated to ${url}`);
  } catch (error) {
    res.status(500).send(`Navigation failed: ${error.toString()}`);
  }
});

// Endpoint: type query
app.post('/type', async (req, res) => {
  const { selector, text } = req.body;
  try {
    if (!page) {
      return res.status(400).send("Browser not initialized. Call /initialize first.");
    }
    await page.click(selector);
    await page.keyboard.type(text);
    res.send(`Typed "${text}" into ${selector}`);
  } catch (error) {
    res.status(500).send(`Type operation failed: ${error.toString()}`);
  }
});

// Additional endpoint: click an element
app.post('/click', async (req, res) => {
  const { selector } = req.body;
  try {
    if (!page) {
      return res.status(400).send("Browser not initialized. Call /initialize first.");
    }
    await page.click(selector);
    res.send(`Element ${selector} clicked`);
  } catch (error) {
    res.status(500).send(`Click operation failed: ${error.toString()}`);
  }
});

// Endpoint: key press
app.post('/press', async (req, res) => {
  const { key } = req.body;
  try {
    if (!page) {
      return res.status(400).send("Browser not initialized. Call /initialize first.");
    }
    await page.keyboard.press(key);
    res.send(`Key ${key} pressed`);
  } catch (error) {
    res.status(500).send(`Key press failed: ${error.toString()}`);
  }
});

// Endpoint: key press combination
app.post('/press-combination', async (req, res) => {
  const { key1, key2 } = req.body;
  try {
    if (!page) {
      return res.status(400).send("Browser not initialized. Call /initialize first.");
    }
    await page.keyboard.down(key1);
    await page.keyboard.down(key2);
    await page.keyboard.up(key2);
    await page.keyboard.up(key1);
    res.send(`Key combination ${key1}+${key2} pressed`);
  } catch (error) {
    res.status(500).send(`Key combination failed: ${error.toString()}`);
  }
});

// Endpoint: scroll the page
app.post('/scroll', async (req, res) => {
  const { x = 0, y = 0, behavior = 'auto' } = req.body; // Defaults to no scroll
  try {
    if (!page) {
      return res.status(400).send("Browser not initialized. Call /initialize first.");
    }
    await page.evaluate(({ x, y, behavior }) => {
      window.scrollBy({ top: y, left: x, behavior });
    }, { x, y, behavior });
    res.send(`Scrolled by x:${x}, y:${y}`);
  } catch (error) {
    res.status(500).send(`Scroll operation failed: ${error.toString()}`);
  }
});

// Endpoint: clear text from element
app.post('/clear', async (req, res) => {
  const { selector } = req.body;
  try {
    if (!page) {
      return res.status(400).send("Browser not initialized. Call /initialize first.");
    }
    await page.fill(selector, '');
    res.send(`Cleared text from ${selector}`);
  } catch (error) {
    res.status(500).send(`Clear operation failed: ${error.toString()}`);
  }
});

// Endpoint: Close popup
app.post('/close-popup', async (req, res) => {
  try {
    if (!page) {
      return res.status(400).send("Browser not initialized. Call /initialize first.");
    }
    const popup = await page.waitForEvent('popup');
    await popup.close();
    res.send("Popup closed");
  } catch (error) {
    res.status(500).send(`Close popup failed: ${error.toString()}`);
  }
});

// Health check endpoint
app.get('/health', async (req, res) => {
  try {
    if (browser && page) {
      res.send({ status: 'ok', browserRunning: true });
    } else {
      res.send({ status: 'ok', browserRunning: false, message: 'Browser not initialized' });
    }
  } catch (error) {
    res.status(500).send({ status: 'error', message: error.toString() });
  }
});

// Clean shutdown
process.on('SIGINT', async () => {
  console.log('Shutting down...');
  if (browser) {
    await browser.close();
  }
  process.exit(0);
});

// Start the server
app.listen(3000, '0.0.0.0', () => {
  console.log("🎯 Playwright controller listening on port 3000");
});