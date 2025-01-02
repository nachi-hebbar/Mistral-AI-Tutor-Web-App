import streamlit as st
from mistralai.client import MistralClient
import numpy as np
import faiss
from mistralai import Mistral

# Initialize the Mistral client

api_key = st.secrets["MISTRAL_API_KEY"]  # Use Streamlit secrets for API key management
cli = Mistral(api_key=api_key)


# Function to get text embeddings
def get_text_embedding(input_text: str):
    embeddings_response = cli.embeddings.create(
        model="mistral-embed",
        inputs=[input_text]
    )
    return embeddings_response.data[0].embedding


# Function to retrieve relevant document chunks
def rag_pdf(documents: list, question: str) -> str:
    chunk_size = 4096
    chunks = []
    for doc in documents:
        chunks += [doc[i:i + chunk_size] for i in range(0, len(doc), chunk_size)]

    text_embeddings = np.array([get_text_embedding(chunk) for chunk in chunks])
    d = text_embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(text_embeddings)

    question_embeddings = np.array([get_text_embedding(question)])
    D, I = index.search(question_embeddings, k=4)
    retrieved_chunks = [chunks[i] for i in I[0]]
    return "\n\n".join(retrieved_chunks)


# Function to ask Mistral
def ask_mistral(messages: list, documents: list):

    concise_instruction = "Please provide a concise response to the following question based on the context provided:\n\n"
    if documents:
        retrieved_text = rag_pdf(documents, messages[-1]["content"])
        messages[-1]["content"] = retrieved_text + "\n\n" + concise_instruction + messages[-1]["content"]

    response = cli.chat.complete(
        model="pixtral-12b-2409",
        messages=messages,
        max_tokens=2000,
    )
    return response.choices[0].message.content


# Main page
st.title("📄 Ask Your Document Anything")
st.markdown("Ask questions about your uploaded documents and get AI-powered answers!")

# Ensure documents are available in session state
if "documents" not in st.session_state:
    st.warning("Please upload and process documents first on the 'Home' page.")
else:
    documents = [doc["content"] for doc in st.session_state["documents"]]  # Extract text content

# Session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input box for user queries
if prompt := st.chat_input("Ask your question here..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Generating response..."):
            response = ask_mistral(st.session_state.messages, documents)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
