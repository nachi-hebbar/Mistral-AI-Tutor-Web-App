
📚 Mistral-Powered AI Study Buddy
An AI-powered personal tutor that generates tailored summaries, quizzes, coding challenges, and answers questions based on uploaded documents. Built using the Mistral API for advanced NLP capabilities.
![image](https://github.com/user-attachments/assets/cef0543d-95d4-4924-aec8-5b57f4c6f92f)

🚀 Features

Document Summarization: Upload PDFs and receive concise summaries.
![image](https://github.com/user-attachments/assets/aa2f75c4-64a8-48a2-82c7-18011888874a)

Custom Quizzes: Generate quizzes with adjustable difficulty and number of questions.
![image](https://github.com/user-attachments/assets/b42765c2-7fd2-4504-af70-d412aa662186)


Coding Challenges: Create coding questions tailored to your study material.
![image](https://github.com/user-attachments/assets/8c50041e-5d10-49bf-9f15-9e9377ffe5d4)

Q&A System: Ask questions and get answers retrieved from your documents using RAG (Retrieval-Augmented Generation).

🛠️ Tech Stack

Frontend: Streamlit
Backend: Mistral AI API, FAISS for embedding-based search
Languages: Python

🔧 Setup Instructions

1. Clone the repository.
2. Install dependencies using pip install -r requirements.txt
3. Add your Mistral API key to secrets.toml in the .streamlit directory: toml
  MISTRAL_API_KEY = "your-api-key"
4. Run the app using: streamlit run Home.py
   
📄 Usage
Upload your study materials (PDFs).
Explore generated summaries, quizzes, coding challenges, and Q&A.
Customize difficulty levels and other settings for tailored experiences.

🤝 Contributing
Feel free to submit pull requests or issues.
