# Neeko Bot

A Discord bot split into two independent bots that share the same prefix (`.`):

- **LoL Bot** (`lol_bot/`) — League of Legends stats and profile management via the Riot API
- **Fun Bot** (`fun_bot/`) — Fun commands: images, translation, random answers, and more

---

## Setup

### Requirements

Install dependencies from the project root:

```bash
pip install -r requirements.txt
```

### Environment variables

Each bot reads its own `.env` file from its folder.

**`lol_bot/.env`**
```
DISCORD_TOKEN=your_discord_bot_token
RIOT_TOKEN=your_riot_api_key
```

**`fun_bot/.env`**
```
DISCORD_TOKEN=your_discord_bot_token
DEEPL_AUTH_KEY=your_deepl_api_key
OLLAMA_MODEL=llama3.2:1b
```

`OLLAMA_MODEL` is optional and defaults to `llama3.2:1b`. Ollama must be running locally (`ollama serve`) with the model pulled (`ollama pull llama3.2:1b`).

> **Raspberry Pi 5 setup**: `llama3.2:1b` runs fully on CPU and answers in ~5 seconds on RPi 5 with 8 GB RAM. For even faster responses, use `ollama pull tinyllama` and set `OLLAMA_MODEL=tinyllama`.

### Data files

Each bot stores its data in its own folder:

| Bot | File | Contents |
|-----|------|----------|
| lol_bot | `users.json` | Registered summoner profiles |
| lol_bot | `feedback.json` | Error reports |
| fun_bot | `gifs.json` | Blocus gif list |
| fun_bot | `feedback.json` | Error reports |

The bot creates these files automatically on first use.

The fun_bot also requires an `images/` folder inside `fun_bot/` for the `.image` and `.video` commands.

### Running

Run each bot from its own directory:

```bash
cd lol_bot && python main.py
cd fun_bot && python main.py
```

---

## LoL Bot — Commands

All commands use the prefix `.`. Arguments in `<>` are required, `[]` are optional.  
If `[Summoner#TAG]` is omitted, the bot uses your registered account.

### Profile

| Command | Description |
|---------|-------------|
| `.register <Summoner> <Tag>` | Link your Riot account to your Discord |
| `.unregister` | Remove your linked account |
| `.profile` | View your linked account |

### League of Legends

| Command | Description |
|---------|-------------|
| `.rank [Summoner#TAG]` | Show Solo/Duo and Flex rank with LP and winrate |
| `.lastgame [Summoner#TAG]` | Show the most recent game (champion, KDA, result) |
| `.history [count=5] [Summoner#TAG]` | Show last N games as a compact list (max 10) |
| `.played [Summoner#TAG]` | Show time played today and this week |
| `.streak [Summoner#TAG]` | Show current win or loss streak |
| `.mastery [Summoner#TAG]` | Show top 5 champion masteries with points |
| `.livegame [Summoner#TAG]` | Show current in-game status, champion, and duration |

### Other

| Command | Description |
|---------|-------------|
| `.hello` | Say hello to the bot |
| `.error <message>` | Report a bug or send feedback |
| `.help [category]` | Show commands — categories: `profile`, `lol`, `other` |

---

## Fun Bot — Commands

### Other

| Command | Description |
|---------|-------------|
| `.blocus` | Send a random motivational gif |
| `.blocus add <url>` | Add a gif/image URL to the blocus list |
| `.réussite` | Get your session success percentage |
| `.question <message>` | Ask the bot a yes/no question |
| `.image <name>` | Send a saved image by keyword |
| `.video <name>` | Send a saved video by keyword |
| `.search <query>` | Search and post an image from the web |
| `.trans <from> <to> <text>` | Translate text with DeepL (e.g. `.trans EN FR Hello`) |
| `.hello` | Say hello to the bot |
| `.error <message>` | Report a bug or send feedback |
| `.paypal` | Get the PayPal link |

### Help

| Command | Description |
|---------|-------------|
| `.help [category]` | Show commands — categories: `other` |

---

## Project structure

```
Neeko_bot/
├── lol_bot/
│   ├── main.py          # Bot entry point
│   ├── comm_bot.py      # Profile commands and help
│   ├── comm_lol.py      # LoL command handlers
│   ├── riot_lol.py      # Riot API wrapper (RiotProfile class)
│   └── utils.py         # Shared helpers and JSON loaders
├── fun_bot/
│   ├── main.py          # Bot entry point
│   ├── comm_bot.py      # hello/error/help commands
│   ├── comm_other.py    # Fun command handlers
│   └── utils.py         # Shared helpers and JSON loaders
└── README.md
```
