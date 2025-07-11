# Cohere API Client

Simple Python client for using the Cohere API with secure API key management.

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

```bash
python main.py
```

## Project Structure

```
project/
├── .env                # Environment variables
├── requirements.txt    # Python dependencies
├── main.py            # Main script
├── README.md          # Documentation
└── .gitignore         # Files to ignore by Git
```

## Security

* The `.env` file contains sensitive information
* Make sure it's in `.gitignore`
* Never commit API keys

## Dependencies

* `cohere>=5.0.0`: Official Cohere client
* `python-dotenv>=1.0.0`: Environment variables management