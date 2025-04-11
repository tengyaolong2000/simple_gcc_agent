import { Stagehand, Page, BrowserContext } from "@browserbasehq/stagehand";
import StagehandConfig from "./stagehand.config.js";
import { drawObserveOverlay, clearOverlays, actWithCache } from "./utils.js";

import express from 'express';
import { Request, Response } from 'express';

const app = express();
const port = 4000;


app.use(express.json());

let page: Page;
let context: BrowserContext;



async function init_browser() {
  try {
    const stagehand = new Stagehand({
      ...StagehandConfig,
    });
    await stagehand.init();

    page = stagehand.page;
    context = stagehand.context;
  } catch (error) {
    console.error("Error initializing browser:", error);
    throw new Error("Failed to initialize the browser");
  }
}

//try to initialize the browser on startup
(async () => {
  try {
    await init_browser();
    console.log("Stagehand browser initialized successfully");
  } catch (error) {
    console.error("Error initializing Stagehand browser:", error);
  }
})();


app.post('/initialize', async (req: Request, res: Response) => {
  try {
    await init_browser();
    res.status(200).send({ message: "Browser initialized successfully" });
  } catch (error) {
    console.error("Error initializing browser:", error);
    res.status(500).send({ error: "Failed to initialize browser" });
  }
});

async function do_action(action: string) {
  try {
    // Use act() to take actions on the page
    await page.act(action);
  } catch (error) {
    console.error("Error performing action:", error);
    throw new Error("Failed to perform the action");
  }
}

app.post('/action', async (req: Request, res: Response) => {

  const { action } = req.body;
  if (!action) {
    res.status(400).send({ error: "Action is required" });
    return;
  }

  try {
    await do_action(action);
    res.status(200).send({ message: "Action performed successfully" });
  } catch (error) {
    console.error("Error performing action:", error);
    res.status(500).send({ error: "Failed to perform the action" });
  }
});

async function navigate_to_url(url: string) {
  try {
    // Ensure the browser is initialized
    await page.goto(url);
  } catch (error) {
    console.error("Error navigating to URL:", error);
    throw new Error("Failed to navigate to the URL");
  }
}

app.post('/navigate', async (req: Request, res: Response) => {

  const { url } = req.body;
  if (!url) {
    res.status(400).send({ error: "URL is required" });
    return;
  }

  try {
    await navigate_to_url(url);
    res.status(200).send({ message: "Navigation successful" });
    return;
  } catch (error) {
    console.error("Error navigating to URL:", error);
    res.status(500).send({ error: "Failed to navigate to the URL" });
    return
  }
});

async function observe_action(instruction: string) {
  // Use observe() to plan an action before doing it
  const [action] = await page.observe(instruction);
  await drawObserveOverlay(page, [action]); // Highlight the search box
  await page.waitForTimeout(1000);
  //print the action
  console.log(action);
  await page.act(action)
}

async function test_run() {
  // Initialize browser
  await init_browser();
  // Navigate to a URL
  await navigate_to_url("https://www.chess.com/learn-how-to-play-chess");
  await observe_action("get the latest news");
  //await do_action("get the top players");
}

// test_run();

// Health check endpoint
app.get('/health', async (req, res) => {
  try {
    if (page && context) {
      res.send({ status: 'ok', browserRunning: true });
    } else {
      res.send({ status: 'ok', browserRunning: false, message: 'Browser not initialized' });
    }
  } catch (error) {
    res.status(500).send({ status: 'error', message: error instanceof Error ? error.toString() : String(error) });
  }
});


// Start the server
app.listen(4000, '0.0.0.0', () => {
  console.log("🎯 Stagehand controller listening on port 4000");
});