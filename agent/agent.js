import { createBot } from "mineflayer";
import pathfinder from "mineflayer-pathfinder";
import express from "express";

// TODO: Split this into separate files.

const state = {
  last_message: null
};

const app = express();
app.use(express.json());

const minecraftServerPort = parseInt(process.argv[2], 10);

const bot = createBot({
  host: "localhost",
  port: minecraftServerPort,
  username: "bot",
});

bot.loadPlugin(pathfinder.pathfinder);

function initializeBotListeners() {
  bot.on("chat", (username, message) => {

    // Ignore messages from self.
    if (username === bot.username) {
      return;
    }
    
    state.last_message = {
      username,
      message
    };

    // Why? Try and reflect that conversation is transient.
    // Let the controller decide whether to remember conversation.
    setTimeout(() => {
      state.last_message = null;
    }, 10000);
  });
}

function getNearbyEntities(bot, distance = 16) {

  const allEntities = Object.keys(bot.entities).map((id) => {
    const entity = bot.entities[id];
    return {
      entityID: id,
      type: entity.name,
      position: entity.position
    }
  });

  // Delete the bot's own entity from the list.
  const otherEntities = allEntities.filter((entity) => {
    return entity.entityID !== bot.entity.id.toString();
  });

  // Nearby entities
  const nearbyEntities = otherEntities.filter((entity) => {
    return bot.entity.position.distanceTo(entity.position) < distance;
  });

  // Strip out the position.
  nearbyEntities.forEach((entity) => {
    delete entity.position;
  });

  return nearbyEntities;
}

app.get("/sense", (req, res) => {
  const fullState = {
    ...state,
    is_raining: bot.isRaining,
    is_day: bot.time.isDay,
    entities: getNearbyEntities(bot, 16) 
  };

  res.json(fullState);
});

app.post("/act", (req, res) => {
  const { action } = req.body;
  console.log("Performing action '" + action);

  let entityID;
  let entity;

  switch(action) {
    case "chat":
      bot.chat(req.body.message);
      break;
    case "move":
      entityID = req.body.entityID;
      entity = bot.entities[entityID];
      if (!entity) {
        console.error("Entity not found with ID", entityID);
        break;
      }
      const goal = new pathfinder.goals.GoalFollow(entity, 1);
      bot.pathfinder.setGoal(goal);
      break;   
    case 'null':
      // Do nothing.
      break;
    default:
      console.error("Unknown action", action);
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
