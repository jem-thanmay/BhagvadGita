### Bhagavad Gita Chatbot 🦚

This project is a Flask-based AI chatbot that answers questions about the Bhagavad Gita using vector embeddings powered by LangChain + OpenAI.

Features
- Chat interface with Hare Krishna theme
- Uses FAISS for fast vector search
- Queries the Bhagavad Gita text to provide meaningful answers
- Option to clear chat history

### Project Structure

```
BhagvadGita-Chatbot/
├── app.py              # Main Flask application
├── requirements.txt     # Python dependencies
├── faiss_index.*        # Vector store files (generated after first run)
└── README.md            # This file

```
### Setup 
### 1. Clone the Repo:
```
git clone https://github.com/your-username/BhagvadGita-Chatbot.git
cd BhagvadGita-Chatbot
```
### 2. Create Virtual Environment:
```
python3 -m venv .venv
source .venv/bin/activate
```
### 3. Install Requirements:
```
pip install -r requirements.txt
```
### 4. Create a .env file and add your OpenAI API key:
```
OPENAI_API_KEY="XXXXXXXXXXXXXXXXXXX"
```
### 5. Bhagvad Gita PDF link in the root directory:
https://prabhupadagita.com/wp-content/uploads/2013/10/bhagavad-gita-as-it-is.pdf

### 6. Update app.py:
```
loader = PyPDFLoader(os.path.abspath("Bhagavad-gita_As_It_Is.pdf"))
```
### 7. Run the app:
```
python3 app.py
```
### 8. Open the browser:
```
localhost:5000
```

### 9. Screenshots of Working App:
<img width="1468" alt="Screenshot 2025-06-18 at 15 03 13" src="https://github.com/user-attachments/assets/0d2dbe72-56cf-45a2-b6aa-6e3aaa095e9f" />

### 10. Built With:
- OpenAI for LLM & Embeddings
- LangChain for the framework
- Srila Prabhupada for Bhagvad Gita As It Is
