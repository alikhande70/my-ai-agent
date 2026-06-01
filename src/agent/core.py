import os
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()

class AIAgent:
    def __init__(self):
        self.name = os.getenv('AGENT_NAME', 'MyAI-Agent')
        self.console = Console()
    
    def run(self, task: str):
        self.console.print(f"[bold green]Executing task:[/bold green] {task}")
        return f"Task completed: {task}"

if __name__ == "__main__":
    agent = AIAgent()
    result = agent.run("Test task")
    print(result)