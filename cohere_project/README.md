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
├── .streamlit/         # Streamlit configuration
│   └── secrets.toml.example  # Secrets template for local testing
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
- Supports both local development and cloud deployment

## Security

### Local Development
* **main.py**: Uses `.env` file for API key management
* **app.py**: Uses `.streamlit/secrets.toml` file for API key management
* Both `.env` and `.streamlit/secrets.toml` contain sensitive information and are in `.gitignore`
* Never commit API keys to version control
* Use `.env.example` and `.streamlit/secrets.toml.example` to share required configuration structure

### Streamlit Cloud Deployment (app.py)
* API keys are stored securely in Streamlit Cloud's secrets management
* Secrets are encrypted and not visible in your repository
* Use the Streamlit Cloud dashboard to manage sensitive configuration

## Deployment Options

### Option 1: Streamlit Cloud (app.py only)
1. Push your code to GitHub (without API keys)
2. Connect your repository to [share.streamlit.io](https://share.streamlit.io)
3. Configure secrets through the Streamlit Cloud dashboard
4. Your web app will be deployed automatically with a public URL

### Option 2: Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment:
# For main.py (command line script)
cp .env.example .env
# Edit .env with your API key

# For app.py (Streamlit web app)
mkdir -p .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit .streamlit/secrets.toml with your API key

# Run applications
python main.py              # Command line script (uses .env)
streamlit run app.py        # Web app (uses .streamlit/secrets.toml)
```

**Note**: 
- `main.py` uses `.env` file for local development
- `app.py` uses `.streamlit/secrets.toml` for local development and Streamlit Cloud secrets for deployment

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