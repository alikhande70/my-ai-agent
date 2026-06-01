#!/usr/bin/env python3
"""Main entry point for AI Agent"""

import sys
from typing import Optional

from src.core.agent import AIAgent
from src.core.config import Config
from src.core.logger import Logger
from src.core.exceptions import AIAgentException


def setup_agent() -> AIAgent:
    """Setup and initialize AI Agent"""
    try:
        config = Config()
        agent = AIAgent(config=config)
        return agent
    except Exception as e:
        Logger.critical(f"Failed to setup agent: {str(e)}")
        sys.exit(1)


def interactive_mode(agent: AIAgent) -> None:
    """Interactive conversation mode"""
    Logger.info("Entering interactive mode. Type 'exit' to quit.")
    print(f"\n{agent.config.agent_name} Ready!")
    print("Type 'exit' to quit, 'clear' to clear memory, or 'info' for system info.\n")

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() == "exit":
                Logger.info("Exiting interactive mode")
                print("Goodbye!")
                break

            if user_input.lower() == "clear":
                agent.clear_memory()
                print("Memory cleared.\n")
                continue

            if user_input.lower() == "info":
                info = agent.get_system_info()
                print(f"\n=== System Info ===")
                for key, value in info.items():
                    print(f"{key}: {value}")
                print()
                continue

            # Process user input
            response = agent.process(user_input)
            print(f"\nAgent: {response}\n")

        except KeyboardInterrupt:
            Logger.info("Interrupted by user")
            print("\n\nGoodbye!")
            break
        except AIAgentException as e:
            Logger.error(f"Agent error: {str(e)}")
            print(f"Error: {str(e)}\n")
        except Exception as e:
            Logger.error(f"Unexpected error: {str(e)}")
            print(f"An unexpected error occurred: {str(e)}\n")


def single_query_mode(agent: AIAgent, query: str) -> None:
    """Process a single query and exit"""
    try:
        response = agent.process(query)
        print(f"\nAgent Response:\n{response}")
    except AIAgentException as e:
        Logger.error(f"Agent error: {str(e)}")
        print(f"Error: {str(e)}")
        sys.exit(1)


def main():
    """Main function"""
    Logger.info("Starting AI Agent Application")

    # Setup agent
    agent = setup_agent()

    # Check for command line arguments
    if len(sys.argv) > 1:
        # Single query mode
        query = " ".join(sys.argv[1:])
        Logger.info(f"Processing query: {query}")
        single_query_mode(agent, query)
    else:
        # Interactive mode
        interactive_mode(agent)


if __name__ == "__main__":
    main()
