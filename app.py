from flask import Flask, request, render_template_string, session, redirect, url_for
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAI, OpenAIEmbeddings
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize Flask
app = Flask(__name__)
app.secret_key = "your-secret-key"  # Needed for session

# Load or build vector store
VECTOR_DB = "faiss_index"
if os.path.exists(f"{VECTOR_DB}.faiss"):
    vector_store = FAISS.load_local(VECTOR_DB, OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY))
else:
    loader = PyPDFLoader(os.path.abspath("BG.pdf"))  # Replace with your PDF path
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(VECTOR_DB)

llm = OpenAI(api_key=OPENAI_API_KEY)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Param</title>
  <link rel="icon" href="https://i.postimg.cc/CxXVSLXj/peacock.png" type="image/png">
    <style>
        body {
            font-family: Georgia, serif;
            background: #1c1c1c url('https://i.postimg.cc/Y90Q85md/kurukshetra.jpg') no-repeat center center fixed;
            background-size: cover;
            margin: 0; padding: 0;
            display: flex; justify-content: center; align-items: center; height: 100vh;
            color: #f0e6d2;
        }
        .chat-container {
            background: rgba(0, 0, 0, 0.7);
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(255,140,0,0.3);
            padding: 20px;
            width: 500px;
        }
        h2 {
            text-align: center;
            color: #ffa500;
        }
        .messages {
            max-height: 300px;
            overflow-y: auto;
            margin-bottom: 10px;
            padding: 10px;
            background: rgba(255, 140, 0, 0.1);
            border-radius: 5px;
        }
        .bot { color: #ffa500; margin-bottom: 5px; }
        .user { color: #f0e6d2; text-align: right; margin-bottom: 5px; }
        form { display: flex; }
        input[type="text"] {
            flex: 1;
            padding: 10px;
            font-size: 16px;
            border: 1px solid #444;
            border-radius: 5px 0 0 5px;
            background: #333;
            color: #f0e6d2;
        }
        button {
            background: #ff8c00;
            color: white;
            border: none;
            padding: 0 20px;
            border-radius: 0 5px 5px 0;
            font-size: 18px;
            cursor: pointer;
        }
        button.clear {
            background: #444;
            margin-top: 10px;
            width: 100%;
            border-radius: 5px;
        }
        .loading { display: none; text-align: center; color: #bbb; font-style: italic; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="chat-container">
        <h2>Hare Krishna 🙏🦚</h2>
        <div class="messages">
            {{ messages|safe }}
        </div>
        <form method="post" action="/" id="chatForm">
            <input type="text" name="question" placeholder="Ask about Bhagavad Gita..." required autofocus>
            <button type="submit">&#10148;</button>
        </form>
        <form method="post" action="/clear">
            <button type="submit" class="clear">Clear Chat</button>
        </form>
        <div class="loading" id="loading">Loading...</div>
    </div>
    <script>
        const form = document.getElementById('chatForm');
        const loading = document.getElementById('loading');
        form.addEventListener('submit', function() {
            loading.style.display = 'block';
        });
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def chat():
    if "history" not in session:
        session["history"] = ""

    if request.method == "POST":
        question = request.form.get("question")
        if question:
            session["history"] += f'<div class="user"><strong>You:</strong> {question}</div>'
            try:
                docs = vector_store.similarity_search(question, k=3)
                context = "\n\n".join([doc.page_content for doc in docs])
                prompt = f"""You are an AI assistant answering questions about the Bhagavad Gita.
Use the context to help answer accurately.

Context:
{context}

Question: {question}
Answer:"""
                answer = llm.invoke(prompt)
            except Exception as e:
                answer = f"An error occurred: {str(e)}"

            session["history"] += f'<div class="bot"><strong>Bot:</strong> {answer}</div>'

    return render_template_string(HTML_TEMPLATE, messages=session.get("history", ""))

@app.route("/clear", methods=["POST"])
def clear():
    session["history"] = ""
    return redirect(url_for("chat"))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)