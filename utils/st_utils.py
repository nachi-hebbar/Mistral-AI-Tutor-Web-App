import streamlit as st
import PyPDF2
from utils.mistral_utils import generate_summary
import streamlit as st
from utils.mistral_utils import generate_coding_questions
import json


def display_interactive_quiz_with_form(quiz_data,id):
    """
    Display the quiz interactively using a Streamlit form. The form collects all answers and submits them together.

    Args:
        quiz_data (list): List of dictionaries with 'Question', 'Options', and 'Answer' keys.
    """
    #st.title("Interactive Quiz")
    form_key="quiz_form_"+str(id)

    # Check if the form is submitted
    with st.form(form_key):
        st.write("Answer the questions and click 'Submit' to check your score.")

        # Dictionary to hold user-selected answers
        selected_answers = {}

        # Display each question with radio buttons
        for idx, question_data in enumerate(quiz_data):
            idx=idx+id*5
            st.subheader(f"Question {idx + 1}: {question_data['Question']}")
            selected_answers[idx] = st.radio(
                f"Choose an answer for Question {idx + 1}",
                options=question_data["Options"],
                key=f"q_{idx}",
            )

        # Submit button to check the score
        submit_button = st.form_submit_button("Submit & Check Score")

    # Display results after form submission
    if submit_button:
        correct_count = 0
        total_questions = len(quiz_data)

        # Evaluate answers
        for idx, question_data in enumerate(quiz_data):
            idx=idx+id*5
            user_answer = selected_answers[idx]
            if user_answer == question_data["Answer"]:
                correct_count += 1
                st.success(f"Question {idx + 1}: Correct!")
            else:
                st.error(f"Question {idx + 1}: Wrong! Correct answer is: {question_data['Answer']}")

        # Display final score
        st.write(f"Your Score: {correct_count}/{total_questions}")


@st.cache_data
def extract_text_from_pdfs(uploaded_files):
    documents = []
    for uploaded_file in uploaded_files:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        documents.append({"name": uploaded_file.name, "content": text})
    return documents

# Display quiz in Streamlit
def parse_quiz_response(raw_response):
    """
    Parse the raw response from the model to extract questions, options, and answers.

    Args:
        raw_response (str): The raw response string from the model.

    Returns:
        list: A list of dictionaries with 'Question', 'Options', and 'Answer' keys.
    """
    try:
        parsed_quiz = json.loads(raw_response)
        return parsed_quiz
    except json.JSONDecodeError as e:
        st.error(f"JSONDecodeError: {e}")
        return []
    except Exception as e:
        st.error(f"Error: {e}")
        return []



def display_home_page():
    # Page title
    st.title("📚 Your Mistral-Powered AI Study Buddy")
    st.markdown("""
        <style>
            .centered-box {
                background-color: #f9f9f9;
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                margin: 20px auto;
                max-width: 800px;
            }
            .btn-container {
                margin-top: 30px;
                display: flex;
                justify-content: space-around;
                flex-wrap: wrap;
            }
            .btn {
                color: white; /* White text for contrast */
                padding: 15px 30px; /* Larger padding for better clickability */
                border-radius: 25px; /* Rounded corners for a modern look */
                font-size: 16px; /* Increase font size for readability */
                font-weight: bold;
                text-decoration: none;
                text-align: center;
                transition: all 0.3s ease; /* Smooth hover effect */
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
                margin: 10px; /* Spacing between buttons */
                border: none; /* Remove border */
            }
            .btn:hover {
                background-color: #16a085; /* Slightly darker teal on hover */
                box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15); /* Deeper shadow on hover */
                transform: translateY(-2px); /* Hover "lift" effect */
            }
            .upload-box {
                text-align: center;
                margin-bottom: 20px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Introductory section
    st.markdown("""
        <div class="centered-box">
            <h2>Step 1: Upload Your Study Material</h2>
            <p>Upload one or more PDFs to generate instant summaries, study plans, and quizzes tailored just for you!</p>
        </div>
    """, unsafe_allow_html=True)

    # File uploader
    uploaded_files = st.file_uploader("Upload one or more PDFs", type=["pdf"], accept_multiple_files=True)

    if uploaded_files:
        # Spinning loader for processing
        with st.spinner("Hang tight! We're summarizing your documents..."):

            documents = extract_text_from_pdfs(uploaded_files)

            # Generate summaries
            summaries = {}
            for doc in documents:
                summaries[doc["name"]] = generate_summary(doc["content"])

            # Save summaries in session state
            st.session_state["summaries"] = summaries
            st.session_state["documents"] = documents

        # Display summaries using columns
        st.markdown("<h3 style='text-align: center;'>Document Summaries</h3>", unsafe_allow_html=True)
        cols = st.columns(len(summaries))  # Create as many columns as there are summaries
        for i, (name, summary) in enumerate(summaries.items()):
            with cols[i]:  # Place each summary in its respective column
                st.markdown(f"Document Name: **{name}**")
                display_enhanced_summary(json.loads(summary))

        # Success message
        st.success("Documents processed successfully! Use the sidebar to explore quiz generation, coding questions, and flashcards.")



def display_enhanced_summary(summary_data):
    # CSS Styles
    st.markdown("""
    <style>
        .summary-card {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .summary-card h2, .summary-card h3 {
            font-family: 'Roboto', sans-serif;
            color: #2c3e50;
            margin-bottom: 15px;
        }
        .summary-card p {
            font-family: 'Lato', sans-serif;
            color: #2c3e50;
            line-height: 1.6;
            margin-bottom: 10px;
        }
        .key-skills ul {
            list-style: none;
            padding-left: 0;
        }
        .key-skills li::before {
            content: "✔️";
            color: #27ae60;
            margin-right: 8px;
        }
        .difficulty, .time {
            font-weight: bold;
            color: #e67e22;
        }
    </style>
    """, unsafe_allow_html=True)

    # Render Summary Section
    st.markdown(f"""
    <div class="summary-card">
        <h2>Summary</h2>
        <p>{summary_data['summary']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Render Key Skills Section
    st.markdown(f"""
    <div class="summary-card">
        <h3>Key Skills</h3>
        <div class="key-skills">
            <ul>
                {"".join(f"<li>{skill}</li>" for skill in summary_data['key_skills'])}
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Render Difficulty Level
    st.markdown(f"""
    <div class="summary-card">
        <h3>Difficulty Level</h3>
        <p class="difficulty">{summary_data['difficulty']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Render Estimated Time to Completion
    st.markdown(f"""
    <div class="summary-card">
        <h3>Estimated Time to Completion</h3>
        <p class="time">{summary_data['estimated_time']} Minutes</p>
    </div>
    """, unsafe_allow_html=True)




def display_code_generation_page():
    """
    Displays the Code Generation page with options to customize coding questions and view the results.
    """
    st.title("🧑‍💻 Code Generation")

    st.markdown("""
    Generate coding challenges based on your study material. Customize the type of questions, difficulty level, and number of tasks to create tailored coding exercises.
    """)

    # Customization options
    st.markdown("### Customize Your Coding Questions")
    with st.form("code_generation_form"):
        num_questions = st.slider("Number of Questions", 1, 10, 5)
        difficulty = st.selectbox("Select Difficulty Level", ["Easy", "Medium", "Hard"])
        include_explanations = st.checkbox("Include Explanations for Answers", value=True)

        # Submit button
        submit_button = st.form_submit_button("Generate Coding Questions")

    # Check if session state has study material
    if "documents" not in st.session_state:
        st.warning("Please upload and process documents first on the 'Home' page.")
    else:
        if submit_button:
            documents = st.session_state["documents"]

            st.markdown("### Generated Coding Questions")
            for doc in documents:
                st.markdown(f"#### Coding Questions for: {doc['name']}")

                # Generate questions using the utility function
                raw_response = generate_coding_questions(
                    content=doc["content"],
                    num_questions=num_questions,
                    difficulty=difficulty,
                    include_explanations=include_explanations
                )
                print("The model gave this: ",raw_response)

                # Parse and display the generated questions
                parsed_questions = json.loads(raw_response)
                for question in parsed_questions:
                    display_coding_question_with_answer(question)

def display_coding_question_with_answer(question_data, show_explanation=True):
    """
    Display a coding question with a "See Answer" button to reveal the answer.

    Args:
        question_data (dict): A dictionary containing the question, code snippet, and answer.
        show_explanation (bool): Whether to display the explanation/answer button.
    """
    st.markdown(f"**Question:** {question_data['Question']}")

    # Display the code snippet (if available)
    if "CodeSnippet" in question_data and question_data["CodeSnippet"]:
        st.code(question_data["CodeSnippet"], language="python")
    else:
        st.warning("No code snippet provided for this question.")

    # Show "See Answer" button
    if show_explanation and "Answer" in question_data:
        with st.expander("💡 See Answer"):
            st.markdown(f"**Answer/Explanation:** {question_data['Answer']}")

