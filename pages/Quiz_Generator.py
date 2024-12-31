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


# Check if documents are in session state
if "documents" not in st.session_state:
    st.warning("Please upload and process documents first on the 'Home' page.")
else:
    documents = st.session_state["documents"]


    # Customization Form
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

        # Submit button for customization form
        submitted = st.form_submit_button("Generate Quiz")

    # Generate the quiz after customization form is submitted
    if submitted:
        num_questions = st.session_state["num_questions"]
        difficulty = st.session_state["difficulty"]
        include_explanations = st.session_state["include_explanations"]
        allow_download = st.session_state["allow_download"]

        st.write("Generating your customized quiz...")

        count = 0  # Document ID
        for doc in documents:
            st.markdown(f"### Quiz for {doc['name']}")

            # Generate quiz with custom parameters
            raw_response = generate_quiz(
                content=doc["content"],
                num_questions=num_questions,
                difficulty=difficulty,
                include_explanations=include_explanations
            )

            # Parse the raw response
            parsed_quiz = parse_quiz_response(raw_response)

            if parsed_quiz:
                display_interactive_quiz_with_form(parsed_quiz, count)
                count += 1

                # Allow downloading the raw quiz response if enabled
                if allow_download:
                    st.download_button(
                        label="Download Quiz Response",
                        data=raw_response,
                        file_name=f"{doc['name']}_quiz.json",
                        mime="application/json"
                    )
            else:
                st.error(f"Could not parse a valid quiz for {doc['name']}. Please try again.")
