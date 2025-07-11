# Cohere API Client

Simple Python client for using the Cohere API with secure API key management. Includes both a command-line script and a Streamlit web application for text summarization.

## Installation

1. Clone the project
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file at the project root:

```
COHERE_API_KEY=your_api_key_here
```

2. Replace `your_api_key_here` with your Cohere API key

## Usage

### Command Line Script
```bash
python main.py
```

### Streamlit Web App
```bash
streamlit run app.py
```

## Project Structure

```
project/
├── .env                # Environment variables
├── .env.example        # Environment variables template
├── requirements.txt    # Python dependencies
├── main.py            # Main command-line script
├── app.py             # Streamlit web application
├── README.md          # Documentation
└── .gitignore         # Files to ignore by Git
```

## Features

### Command Line Script (main.py)
- Simple "Hello World" example using Cohere API
- Demonstrates basic API integration

### Streamlit Web App (app.py)
- Interactive text summarization interface
- Real-time text processing with Cohere's command-r-plus model
- User-friendly web interface with loading indicators and error handling

## API Key Setup

1. Sign up for a Cohere account at [cohere.com](https://cohere.com)
2. Get your API key from the Cohere dashboard
3. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
4. Edit `.env` and replace `your_cohere_api_key_here` with your actual API key

## Security

* The `.env` file contains sensitive information
* Make sure it's in `.gitignore`
* Never commit API keys to version control
* Use `.env.example` to share required environment variables structure

## Dependencies

* `cohere`: Official Cohere client
* `python-dotenv`: Environment variables management
* `streamlit`: Web application framework