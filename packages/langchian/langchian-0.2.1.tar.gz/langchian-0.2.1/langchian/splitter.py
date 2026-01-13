from pathlib import Path

import time
from pathlib import Path

RAG_APP_CODE = r'''
import os, json, requests, pandas as pd, streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
API_URL = "{{URL}}"
DOC_FILE = "documents.txt"
MAX_TEXT_CHARS = 200_000

st.title("RAG Chat App")

st.session_state.setdefault("vector_db", None)
st.session_state.setdefault("ready", False)
st.session_state.setdefault("messages", [])

if st.sidebar.button("Create vector DB"):
    st.write("Preparing data...")
    full_text = ""

    if os.path.exists(DOC_FILE):
        with open(DOC_FILE, "r", encoding="utf-8") as f:
            full_text = f.read()
    else:
        response = requests.get(API_URL, timeout=60)
        response.raise_for_status()
        df = pd.DataFrame.from_dict(response.json(), orient="index").reset_index()

        for col in df.columns:
            df[col] = df[col].apply(lambda x: json.dumps(x) if isinstance(x, dict) else x)
            if df[col].dtype in ["int64", "float64"]:
                df[col] = df[col].fillna(df[col].median())
            else:
                df[col] = df[col].fillna("unknown").astype(str)

        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].str.lower().str.strip()

        for _, row in df.iterrows():
            full_text += " | ".join([f"{c}: {row[c]}" for c in df.columns]) + "\n"

        with open(DOC_FILE, "w", encoding="utf-8") as f:
            f.write(full_text)

    if len(full_text) > MAX_TEXT_CHARS:
        full_text = full_text[:MAX_TEXT_CHARS]

    splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    documents = splitter.create_documents([full_text])

    embeddings = OpenAIEmbeddings(api_key=API_KEY)
    st.session_state.vector_db = FAISS.from_documents(documents, embeddings)
    st.session_state.ready = True
    st.success("Vector database is ready. You can now chat.")

# History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("context"):
            with st.expander("Retrieved Context"):
                st.markdown(msg["context"])

# Chat
user_input = st.chat_input("Ask something about the data")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    retrieved_context = ""

    if not st.session_state.ready:
        bot_reply = "Please create the vector database first."
    else:
        llm = ChatOpenAI(model="gpt-4o-mini")
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a data analyst assistant.\nUse the provided context.\nDo NOT use external knowledge."),
            ("human", "Question: {question}\n\nContext:\n{context}")
        ])

        results = st.session_state.vector_db.similarity_search(user_input, k=1)
        if results:
            retrieved_context = results[0].page_content.strip()
            if retrieved_context == "..." or len(retrieved_context) < 10:
                retrieved_context = "Retrieved context was too short or invalid."
        else:
            retrieved_context = "No relevant context found."

        response = llm.invoke(prompt.format(question=user_input, context=retrieved_context))
        bot_reply = response.content

    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply,
        "context": retrieved_context
    })

    with st.chat_message("assistant"):
        st.markdown(bot_reply)
        if retrieved_context:
            with st.expander("Retrieved Context"):
                st.markdown(retrieved_context)

'''


def split_document(url, filename="app.py", delay=0.025):
    start_time=time.time()
    path = Path(filename)

    # Always overwrite if file exists
    final_code = RAG_APP_CODE.replace("{{URL}}", url)

    import re

    with path.open("w", encoding="utf-8") as f:
        tokens = re.findall(r'\S+|\s+', final_code)  # words + spaces/newlines

        for tok in tokens:
            if tok.isspace():
                f.write(tok)
                f.flush()
                time.sleep(delay * 0.8)

            else:
                for ch in tok:
                    f.write(ch)
                    f.flush()

                    # programmer-like pauses
                    if ch in "=:+-*/<>;,.(){}[]":
                        time.sleep(delay * 1.5)     # thinking symbols
                    elif ch.isdigit():
                        time.sleep(delay * 1.5)   # numbers
                    else:
                        time.sleep(delay)         # normal letters

