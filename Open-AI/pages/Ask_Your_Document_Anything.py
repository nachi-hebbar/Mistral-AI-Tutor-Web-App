import streamlit as st
import numpy as np
import faiss
from openai import OpenAI

# Function to get OpenAI client
def get_openai_client():
    if not st.session_state.get("openai_api_key"):
        st.error("Please enter your OpenAI API key in the sidebar.")
        st.stop()
    return OpenAI(api_key=st.session_state.openai_api_key)

# Function to get text embeddings
def get_text_embedding(input_text: str):
    client = get_openai_client()
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=input_text
    )
    return response.data[0].embedding

# Function to implement RAG with the documents
def rag_pdf(documents: list, question: str):
    # Get question embedding
    question_embedding = get_text_embedding(question)
    
    # Create FAISS index for document chunks
    chunk_embeddings = []
    chunk_texts = []
    
    # Process each document
    for doc in documents:
        content = doc["content"]
        # Split content into chunks (simple splitting for now)
        chunks = [content[i:i+1000] for i in range(0, len(content), 1000)]
        
        for chunk in chunks:
            chunk_texts.append(chunk)
            chunk_embeddings.append(get_text_embedding(chunk))
    
    # Convert embeddings to numpy array
    embeddings_array = np.array(chunk_embeddings)
    
    # Create FAISS index
    dimension = len(embeddings_array[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings_array.astype('float32'))
    
    # Search for relevant chunks
    k = 3  # Number of chunks to retrieve
    D, I = index.search(np.array([question_embedding]).astype('float32'), k)
    
    # Get relevant chunks
    relevant_chunks = [chunk_texts[i] for i in I[0]]
    
    return relevant_chunks

# Function to ask OpenAI
def ask_openai(question: str, context: list):
    client = get_openai_client()
    
    # Prepare the messages
    messages = [
        {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided context. "
                                    "Always base your answers on the context provided."},
        {"role": "user", "content": f"Context:\n{''.join(context)}\n\nQuestion: {question}"}
    ]
    
    # Get response from OpenAI
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages
    )
    
    return response.choices[0].message.content

# Main page
st.title("📄 Ask Your Document Anything")
st.markdown("Ask questions about your uploaded documents and get AI-powered answers!")

# Check if documents exist in session state
if "documents" not in st.session_state:
    st.warning("Please upload documents on the home page first!")
    st.stop()

# Get user question
question = st.text_input("Ask a question about your documents:")

if question:
    with st.spinner("Finding answer..."):
        # Get relevant chunks using RAG
        relevant_chunks = rag_pdf(st.session_state["documents"], question)
        
        # Get answer from OpenAI
        answer = ask_openai(question, relevant_chunks)
        
        # Display answer
        st.markdown("### Answer:")
        st.write(answer)
        
        # Optionally display relevant chunks
        with st.expander("View relevant document chunks"):
            for i, chunk in enumerate(relevant_chunks, 1):
                st.markdown(f"**Chunk {i}:**")
                st.write(chunk)
                st.markdown("---")
