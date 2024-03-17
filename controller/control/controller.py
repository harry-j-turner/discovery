import requests
import logging
import pydantic
import json

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from control.settings import settings
from control.base_models import (
    SenseData,
    Action,
    ActionType,
    ChatAction,
    MoveAction,
    NullAction,
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING)


class Controller:
    def __init__(self) -> None:

        self.base_url = f"{settings.agent_origin}:{settings.agent_port}"

        model = ChatOpenAI()
        parser = StrOutputParser()

        # TODO: Load prompt from file.
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a minecraft bot. The user will provide two bits of information, a datastructure of information about the world called Sense Data. The second is a list of valid actions you can take represented in JSON Schema. You must choose exactly one action to perform and respond with JSON in the correct form for the chosen action's schema.",
                ),
                ("user", "{input}"),
            ]
        )

        self.llm = prompt | model | parser

    def sense(self) -> None:
        """Get the current state of the agent and environment."""

        try:
            response = requests.get(f"{self.base_url}/sense")
            response.raise_for_status()
            data = response.json()
            return SenseData(**data)

        # Network Issues
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect to agent: {e}, is the agent running?")
            return None

        # Invalid Data
        except pydantic.ValidationError as e:
            logger.error(f"Invalid data received from agent: {e}, check compatibility.")
            return None

    def think(self, sense_data: SenseData) -> None:

        actions = [ChatAction, MoveAction, NullAction]
        action_schemas = [action.model_json_schema() for action in actions]

        message = f"# Sense Data\n{sense_data.serialise()}\n\n# Actions\n"
        message += json.dumps(action_schemas, indent=2)

        response = self.llm.invoke({"input": message})

        try:
            parsed_response = json.loads(response)
            return ActionType.validate_python(parsed_response)

        # Bad JSON
        except json.JSONDecodeError as e:
            logger.error(f"LLM did not return valid JSON: {e}")
            logger.error(f"LLM response: {response}")
            return None

        # Invalid Action
        except pydantic.ValidationError as e:
            logger.error(f"LLM did not return a valid action: {e}")
            logger.error(f"LLM response: {response}")
            return None

    def act(self, action: Action) -> None:
        """Dispatch an action to the agent."""

        try:
            # Action should be a valid action, see base_models.py.
            validated_action = ActionType.validate_python(action)
        except pydantic.ValidationError as e:
            logger.error(f"Invalid action: {e}")
            return

        try:
            response = requests.post(f"{self.base_url}/act", json=validated_action.model_dump())
            response.raise_for_status()

        # Network Issues
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect to agent: {e}, is the agent running?")
            return
