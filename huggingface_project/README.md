# GenAI LangChain & OpenAI/HuggingFace Streamlit Playground

A versatile playground for GenAI projects using **LangChain**, **OpenAI**, **HuggingFace**, and **Streamlit**. Includes a wide range of app templates:

* 💬 **Conversational AI (GPT-4.1-nano, OpenAI, Conversation Memory)**
* 🤖 **Agentic QA (OpenAI, Wikipedia, Tavily, Math Tool)**
* 🧠 **RAG (Retrieval-Augmented Generation): Multi-Document, PDF/DOCX/TXT**
* 🏷️ **Company Naming, Slogan, Prompt Chaining**
* ⚡ **Simple Sequential Chains, Prompt Templates**

Ready for demo, learning, and rapid prototyping with your own `.env` and custom models!

---

## 🚀 Quickstart

1. **Clone or download this repo**
2. *(Optional)* Create a Python venv and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # or .\venv\Scripts\activate on Windows
   ```
3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```
4. **Add your `.env` file with secrets:**

   ```env
   OPENAI_API_KEY=sk-...
   HUGGINGFACEHUB_API_TOKEN=hf_...
   ```
5. **Launch any Streamlit app:**

   ```bash
   streamlit run app.py                   # HF QA playground
   streamlit run app_chain.py             # Prompt chaining (HuggingFace)
   streamlit run app_agent.py             # OpenAI Wikipedia agent
   streamlit run app_agent_tavily.py      # OpenAI Plan & Execute agent (Tavily, Wikipedia, Math)
   streamlit run app_conversationelchain.py # OpenAI conversational chatbot
   streamlit run app_rag.py               # Retrieval-Augmented QA (multi-doc, PDF, docx, txt)
   streamlit run app_simple_seqential_chain.py # Simple sequential chain demo
   # ...or any main_*.py variant from terminal
   ```

---

## 📂 Main Files & Apps

| File                               | Description                                            |
| ---------------------------------- | ------------------------------------------------------ |
| `app.py`                           | QA with HuggingFace FLAN-T5-base (Streamlit)           |
| `app_chain.py`                     | Prompt chaining, product naming (HF)                   |
| `app_agent.py`                     | OpenAI Wikipedia React Agent (GPT-4.1-nano)            |
| `app_agent_tavily.py`              | Plan & Execute Agent (Tavily, Wikipedia, Math, OpenAI) |
| `app_conversationelchain.py`       | Conversational chatbot (OpenAI, memory)                |
| `app_rag.py`                       | Multi-doc RAG: TXT, PDF, DOCX                          |
| `app_simple_seqential_chain.py`    | Simple sequential chain demo (HF GPT2)                 |
| `main.py`                          | CLI QA with HF FLAN-T5-base                            |
| `main_agent.py`                    | CLI Wikipedia React Agent (OpenAI)                     |
| `main_agent_tavily.py`             | CLI Plan & Execute Agent                               |
| `main_chain.py`                    | CLI prompt chaining demo                               |
| `main_conversationelchain.py`      | CLI conversational chain (OpenAI)                      |
| `main_conversationhistory.py`      | CLI: Conversation with chat history loading            |
| `main_rag.py`                      | CLI: Simple Retrieval-Augmented Generation             |
| `managing-a-mobile-project-...txt` | Sample document for RAG                                |

---

## 🛠️ Features

* **OpenAI & HuggingFace LLMs**
* **Agents** (Wikipedia, Tavily, Math, Plan\&Execute)
* **Multi-format document QA** (TXT, PDF, DOCX)
* **Prompt chaining & templates**
* **Conversation memory & history**
* **Streamlit interactive UIs**
* **Configurable via .env and sidebar**
* **Quick switches between QA, agents, chatbots**

---

## 📝 Example .env

```env
OPENAI_API_KEY=sk-...
HUGGINGFACEHUB_API_TOKEN=hf_...
```

---

## 📦 Requirements

All main libraries in `requirements.txt`. Main dependencies:

* `langchain`
* `langchain_community`, `langchain-openai`, `langchain-huggingface`, `langchain-text-splitters`
* `python-dotenv`, `streamlit`, `chromadb`, `transformers`, `torch`
* `pdfplumber`, `unstructured`, `docx2txt`
* `tavily-python`, `wikipedia`, `numexpr`, `tiktoken`

---

## 🤖 Credits

* Powered by [LangChain](https://github.com/langchain-ai/langchain), [OpenAI](https://platform.openai.com/), [HuggingFace](https://huggingface.co/), [Streamlit](https://streamlit.io/)
* Example data: `managing-a-mobile-project-in-an-agile-environment.txt`
