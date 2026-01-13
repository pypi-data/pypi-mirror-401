# discordbotlist.py
Easy to use API wrapper for DiscordBotList in Python

## Installation

> [!WARNING]
> You need to install an optional package either discordbotlist-py[pycord] or discordbotlist-py[discord]

```bash
# For discord.py
pip install discordbotlist-py[discord]

# For py-cord
pip install discordbotlist-py[pycord]
```

## Usage

### discord.py usage
```python
import discord
from discordbotlist import DblClient
from discord import Intents, Client
from discord import app_commands

class MyClient(Client):
    def __init__(self, *, intents: Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

bot = MyClient(intents=Intents.all())

# Initialize the DBL client with your API token
dbl = DblClient("your_dbl_token_here", bot)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    
    # Start auto-posting stats every hour (3600 seconds)
    dbl.start_posting(interval=3600)
    
    # Post commands to DiscordBotList
    commands = await bot.tree.fetch_commands()
    command_list = [
        {
            "name": cmd.name,
            "description": cmd.description,
            "type": cmd.type.value
        }
        for cmd in commands
    ]
    await dbl.post_command(command_list)
    print(f"Posted {len(command_list)} commands to DiscordBotList.")

# Listen for DBL stats updates
@dbl.event
async def on_dbl_updated(payload):
    print(f"DiscordBotList stats updated: {payload}")

# Listen for DBL commands updates
@dbl.event
async def on_dbl_commands_updated(commands):
    print(f"DiscordBotList commands updated: {commands}")

bot.run("your_bot_token_here")
```

### py-cord usage
### discord.py usage
```python
import discord
from discordbotlist import DblClient, AppCommandPayload
from discord import Intents, Bot

bot = Bot(intents=Intents.all())

# Initialize the DBL client with your API token
dbl = DblClient("your_dbl_token_here", bot)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    
    # Start auto-posting stats every hour (3600 seconds)
    dbl.start_posting(interval=3600)
    
    # Post commands to DiscordBotList
    commands = bot.application_commands
    command_list = [
        AppCommandPayload(
            name=cmd.name, description=cmd.description, type=1
        )
        for cmd in commands
    ]

    await dbl.post_command(command_list)
    print(f"Posted {len(command_list)} commands to DiscordBotList.")

# Listen for DBL stats updates
@dbl.event
async def on_dbl_updated(payload):
    print(f"DiscordBotList stats updated: {payload}")

# Listen for DBL commands updates
@dbl.event
async def on_dbl_commands_updated(commands):
    print(f"DiscordBotList commands updated: {commands}")

bot.run("your_bot_token_here")
```

### Manual Stats Posting

```python
# Manually post stats
await dbl.post_status()
```

### Stop Auto-posting

```python
# Stop the auto-posting loop
await dbl.stop_posting()
```
