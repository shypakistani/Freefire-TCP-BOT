# PakTcpBot Freefire  Bot

A Python-based automation tool and bot for Garena Free Fire utilizing TCP communication protocols. It handles requests, custom emotes, headers, and token caching.

## Features

- **TCP Network Controller:** Handles core TCP socket connections and requests tailored for Free Fire game servers.
- **Custom Headers Management:** Automatically processes authentication and game state headers through `xHeaders.py`.
- **Emote Automation:** Built-in automation patterns or triggers using `emotes.json`.
- **Session Cache:** Implements `status_cache.pkl` to locally store runtime session tokens and skip repeated sign-ins.

## Repository File Structure

- `main.py` - Core execution script initiating the TCP network connection and operational loops.
- `xC4.py` - Custom background processes or secondary algorithms.
- `xHeaders.py` - Manages metadata headers required for successful server handshakes.
- `emotes.json` - Map configurations containing action IDs for standard and custom in-game emotes.
- `token.json` - Safe container storing user authorization credentials and tokens.
- `status_cache.pkl` - Serialized pickle cache data handling fast state-recovers.
- `numbers.txt` / `MG24GAMER.txt` - Raw payload collections or targeting numbers list.
- `requirements.txt` - Python module dependencies needed for running the code.
- `runtime.txt` - Deployment constraints identifying supported Python runtimes.

## Prerequisites

- [Python 3.x](https://python.org) installed on your machine.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com
   cd Freefire-tcp
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Provide your session secrets inside `token.json`.
2. Configure parameters within the `emotes.json` file if you want to alter default in-game triggers.

## Usage

Run the primary automation sequence:
```bash
python main.py
```

## License

This project is open-source. Please review the repository owner's guidelines regarding contributions and updates.
