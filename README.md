# Cyber AI Block40 Lab

## Installation

### 1. Install UV
Visit [Astral's UV](https://docs.astral.sh/uv/getting-started/installation/) and follow the installation instructions for your OS.

### 2. Sync Dependencies
Change into the created directory and run the following command to install project dependencies:

```
cd cyber-ai-block40-lab
uv sync
```

### 3. Configure OpenAI API Key
Create a `.env` file in the project root and add your OpenAI API key (you can copy the .env.sample file):

```
cp .env.sample .env
```

## Running the Script

Execute the script using:

```bash
uv run block_40_script.py
```

