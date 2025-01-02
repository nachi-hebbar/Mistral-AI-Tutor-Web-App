import streamlit as st
from utils.mistral_utils import generate_quiz
from utils.st_utils import parse_quiz_response, display_interactive_quiz_with_form

# Page title and description
st.title("📝 Quiz Generator")
st.markdown("""
    <style>
        .custom-container {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .custom-container h3 {
            font-family: 'Roboto', sans-serif;
            color: #2c3e50;
            margin-bottom: 15px;
        }
        .custom-container p {
            font-family: 'Lato', sans-serif;
            color: #2c3e50;
            line-height: 1.6;
        }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <div class="custom-container">
        <h3>Generate Instant Quizzes for Your Study Material</h3>
        <p>Customize and create quizzes to test your understanding of the uploaded documents. You can tailor the quiz to your preferences by selecting the number of questions, difficulty level, and more!</p>
    </div>
""", unsafe_allow_html=True)

# Ensure documents exist in session state
if "documents" not in st.session_state:
    st.warning("Please upload and process documents first on the 'Home' page.")
else:
    documents = st.session_state["documents"]

    # Initialize session state to track which form to show
    if "show_quiz" not in st.session_state:
        st.session_state["show_quiz"] = False
    if "quiz_data" not in st.session_state:
        st.session_state["quiz_data"] = {}

    # Show the quiz customization form if "show_quiz" is False
    if not st.session_state["show_quiz"]:
        st.markdown("""
            <style>
                .form-container {
                    background-color: #f9f9f9;
                    border-radius: 10px;
                    padding: 20px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    margin-bottom: 20px;
                }
                .form-container h3 {
                    font-family: 'Roboto', sans-serif;
                    color: #2c3e50;
                    margin-bottom: 10px;
                }
                .form-container .form-item {
                    margin-bottom: 15px;
                }
            </style>
            <div class="form-container">
                <h3>Quiz Customization</h3>
            </div>
        """, unsafe_allow_html=True)

        with st.form("quiz_customization_form"):
            # Quiz Customization Options
            st.slider(
                "Number of Questions",
                min_value=5, max_value=20, step=1, value=10,
                key="num_questions"
            )

            st.selectbox(
                "Difficulty Level",
                options=["Easy", "Medium", "Hard"],
                index=1,
                key="difficulty"
            )

            st.checkbox(
                "Include Explanations for Answers",
                value=False,
                key="include_explanations"
            )

            st.checkbox(
                "Allow Downloading Quiz Response",
                value=False,
                key="allow_download"
            )

            # Multi-select for documents
            selected_documents = st.multiselect(
                "Select documents to generate quizzes for",
                options=[doc["name"] for doc in documents],
                key="selected_documents"
            )

            # Submit button for customization form
            submitted = st.form_submit_button("Generate Quiz")

        # If form is submitted, generate quizzes
        if submitted:
            if not selected_documents:
                st.error("Please select at least one document to generate a quiz.")
            else:
                st.session_state["quiz_data"] = {}
                for doc_name in selected_documents:
                    doc_content = next(doc["content"] for doc in documents if doc["name"] == doc_name)
                    raw_response = generate_quiz(
                        content=doc_content,
                        num_questions=st.session_state["num_questions"],
                        difficulty=st.session_state["difficulty"],
                        include_explanations=st.session_state["include_explanations"]
                    )
                    st.session_state["quiz_data"][doc_name] = parse_quiz_response(raw_response)

                # Switch to quiz display
                st.session_state["show_quiz"] = True

    # Show the quiz form if "show_quiz" is True
    if st.session_state["show_quiz"]:
        for doc_name, quiz_data in st.session_state["quiz_data"].items():
            st.markdown(f"### Quiz for {doc_name}")
            display_interactive_quiz_with_form(quiz_data, doc_name)

        # Add a button to return to customization form
        if st.button("Back to Customization"):
            st.session_state["show_quiz"] = False
