# 🤖 GenAI Question Answering Application

An interactive AI-powered question-answering application using Google's FLAN-T5-base model with local execution via Streamlit, built with **LangChain** for LLM orchestration and **Transformers** for Hugging Face model integration.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This application demonstrates how to build a local AI question-answering system using Google's FLAN-T5-base model. The project evolved from initial attempts with Hugging Face's remote inference API to a robust local implementation using HuggingFacePipeline, providing better reliability and control over the model execution.

The application includes both a simple command-line interface (`main.py`) and a full-featured Streamlit web application (`app.py`) for interactive conversations.

## 🔧 Prerequisites

- Python 3.8+
- pip (Python package manager)
- **8GB RAM minimum** (for FLAN-T5-base model)
- **5GB free disk space** (for model storage)
- Internet connection for initial model download

## 🚀 Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd huggingface_project
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

**Note**: The first run will download the FLAN-T5-base model (~1.2GB) which may take 5-15 minutes depending on your internet speed.

## ⚙️ Configuration

### 1. Environment Variables (Optional)

Create a `.env` file in the root directory:

```env
# Optional: For future Hugging Face API integrations
HUGGINGFACE_API_KEY=your_token_here
```

**Note**: The current implementation uses local model execution, so the API key is not required but can be added for future enhancements.

### 2. Model Configuration

The application uses these default settings:
- **Model**: `google/flan-t5-base`
- **Max Tokens**: 128 (Streamlit app) / 64 (CLI)
- **Temperature**: 0.1 (Streamlit app) / 0 (CLI)
- **Task**: `text2text-generation`

## 🎮 Usage

### Option 1: Streamlit Web Application (Recommended)

```bash
streamlit run app.py
```

Access the application at: `http://localhost:8501`

**Features:**
- Interactive chat interface
- Real-time parameter adjustment
- Conversation history
- Example question buttons
- Model performance metrics

### Option 2: Command Line Interface

```bash
python main.py
```

**Features:**
- Simple question-answer format
- Quick testing and debugging
- Direct model interaction

### Interface Guide

**Streamlit App:**
1. **Chat Input**: Type questions in the bottom input field
2. **Sidebar Controls**: 
   - Adjust max tokens (50-512)
   - Modify temperature (0.0-1.0)
   - Clear chat history
3. **Example Buttons**: Quick start with predefined questions
4. **Response Area**: AI responses with formatting

### Usage Examples

```text
👤 User: "What are the benefits of regular exercise?"
🤖 AI: "Regular exercise provides numerous benefits including improved cardiovascular health, stronger muscles and bones, better mental health..."

👤 User: "How do you make a basic pasta dish?"
🤖 AI: "To make basic pasta: 1) Boil salted water, 2) Add pasta and cook according to package directions..."

👤 User: "Explain photosynthesis simply"
🤖 AI: "Photosynthesis is the process where plants use sunlight, water, and carbon dioxide to create food and oxygen..."
```

## 📁 Project Structure

```
huggingface_project/
├── app.py                 # Streamlit web application
├── main.py               # Command-line interface
├── requirements.txt      # Python dependencies
├── .env                 # Environment variables (optional)
├── README.md            # Project documentation
├── venv/                # Virtual environment
└── .cache/              # Model cache (created automatically)
    └── huggingface/     # Downloaded models storage
```

## 🛠️ Technologies Used

- **[Streamlit](https://streamlit.io/)** v1.28+ - Interactive web application framework
- **[LangChain](https://langchain.com/)** - LLM orchestration and pipeline management
- **[LangChain Community](https://python.langchain.com/docs/integrations/platforms/)** - HuggingFacePipeline integration
- **[Transformers](https://huggingface.co/transformers/)** v4.35+ - Hugging Face model library
- **[PyTorch](https://pytorch.org/)** - Deep learning framework backend
- **[FLAN-T5-base](https://huggingface.co/google/flan-t5-base)** - Google's instruction-tuned language model
- **[python-dotenv](https://pypi.org/project/python-dotenv/)** - Environment variable management

## 🔍 Troubleshooting

### Common Issues

#### 1. Memory Issues
```bash
# Error: CUDA out of memory / RAM insufficient
# Solution: Use smaller model variant
# In app.py and main.py, change:
model_name = "google/flan-t5-small"  # Instead of "flan-t5-base"
```

#### 2. Model Download Failures
```bash
# Error: Connection timeout during model download
# Solution: Clear cache and retry
rm -rf ~/.cache/huggingface/
python app.py  # Will re-download model
```

#### 3. PyTorch Installation Issues
```bash
# For CUDA support (NVIDIA GPU)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# For CPU-only installation
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

#### 4. LangChain Deprecation Warnings
```bash
# These warnings are normal and don't affect functionality
# They indicate newer versions are available but current code works
```

#### 5. Streamlit Connection Issues
```bash
# If app doesn't open automatically
# Manually navigate to: http://localhost:8501
# Or try: streamlit run app.py --server.port 8502
```

### Performance Optimization

#### For Low-Resource Systems:
```python
# In app.py, reduce model parameters:
model_name = "google/flan-t5-small"  # Smaller model
max_new_tokens = 64                  # Fewer tokens
temperature = 0                      # Deterministic output
```

#### For High-Performance Systems:
```python
# Use larger model variants:
model_name = "google/flan-t5-large"  # Better quality
max_new_tokens = 256                 # Longer responses
```

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.INFO)
```


## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## 📧 Support

For questions or issues:

- **GitHub Issues**: [Open an issue](https://github.com/your-repo/issues)
- **Streamlit Docs**: https://docs.streamlit.io/
- **LangChain Docs**: https://python.langchain.com/
- **Transformers Docs**: https://huggingface.co/docs/transformers/

## 🙏 Acknowledgments

- **Google** for the FLAN-T5 model family
- **Hugging Face** for the Transformers library
- **LangChain** for LLM orchestration tools
- **Streamlit** for the amazing web app framework
