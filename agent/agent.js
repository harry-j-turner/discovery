import { createBot } from "mineflayer";
import express from "express";

const state = {
  lastChatMessage: { username: "", message: "" },
  weather: "clear",
  visibleBlocks: [],
  nearbyEntities: [],
};

const app = express();
app.use(express.json());

const minecraftServerPort = parseInt(process.argv[2], 10);

const bot = createBot({
  host: "localhost",
  port: minecraftServerPort,
  username: "bot",
});

function initializeBotListeners() {
  bot.on("chat", (username, message) => {
    state.lastChatMessage = { username, message };
  });
}

app.get("/sense", (req, res) => {
  res.json(state);
});

app.post("/act", (req, res) => {
  const { action, payload } = req.body;

  switch (action) {
    case "move":
      console.log(`Moving to location: ${JSON.stringify(payload.location)}`);
      break;
    case "speak":
      console.log(`Speaking message: ${payload.message}`);
      bot.chat(payload.message);
      break;
    default:
      res.status(400).send("Unknown action");
      return;
  }

  res.send("Action performed");
});

function startServer() {
  const port = 3000;
  app.listen(port, () => {
    console.log(`Agent server listening at http://localhost:${port}`);
  });

  initializeBotListeners();
}

startServer();
