import streamlit as st
import PyPDF2
from utils.mistral_utils import generate_summary
import streamlit as st
from utils.mistral_utils import generate_coding_questions
import json


def display_interactive_quiz_with_form(quiz_data, doc_name):
    """
    Display the quiz interactively using a Streamlit form. The form collects all answers and submits them together.

    Args:
        quiz_data (list): List of dictionaries with 'Question', 'Options', and 'Answer' keys.
        doc_name (str): The name of the document for unique form keys.
    """
    form_key = f"quiz_form_{doc_name.replace(' ', '_')}"  # Ensure unique form key
    selected_answers = {}

    # Check if the form is submitted
    with st.form(form_key):
        st.write("Answer the questions and click 'Submit' to check your score.")

        # Display each question with radio buttons
        for idx, question_data in enumerate(quiz_data):
            st.subheader(f"Question {idx + 1}: {question_data['Question']}")
            selected_answers[idx] = st.radio(
                f"Choose an answer for Question {idx + 1}",
                options=question_data["Options"],
                key=f"{form_key}_q_{idx}",
                index=None
            )

        # Submit button to check the score
        submit_button = st.form_submit_button("Submit & Check Score")

    # Display results after form submission
    if submit_button:
        correct_count = 0
        total_questions = len(quiz_data)

        # Evaluate answers
        for idx, question_data in enumerate(quiz_data):
            user_answer = selected_answers.get(idx)
            correct_answer = question_data["Answer"]

            if user_answer == correct_answer:
                correct_count += 1
                st.success(f"Question {idx + 1}: Correct!")
            else:
                st.error(f"Question {idx + 1}: Wrong!")
                st.markdown(f"**Correct Answer:** {correct_answer}")

        # Display final score
        st.markdown(f"### Your Score: {correct_count}/{total_questions}")



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
        .difficulty-level {
            display: flex;
            justify-content: space-around;
            margin-top: 15px;
        }
        .difficulty-item {
            flex: 1;
            text-align: center;
            padding: 10px;
            font-weight: bold;
            border-radius: 5px;
        }
        .difficulty-item.easy {
            background-color: #d4edda;
            color: #155724;
        }
        .difficulty-item.medium {
            background-color: #fff3cd;
            color: #856404;
        }
        .difficulty-item.hard {
            background-color: #f8d7da;
            color: #721c24;
        }
        .highlight {
            border: 2px solid #000;
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

    # Render Difficulty Level Section
    difficulty = summary_data.get('difficulty', 'Medium').lower()  # Fallback to 'Medium'
    st.markdown(f"""
    <div class="summary-card">
        <h3>Difficulty Level</h3>
        <div class="difficulty-level">
            <div class="difficulty-item easy {'highlight' if difficulty == 'easy' else ''}">Easy</div>
            <div class="difficulty-item medium {'highlight' if difficulty == 'medium' else ''}">Medium</div>
            <div class="difficulty-item hard {'highlight' if difficulty == 'hard' else ''}">Hard</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Render Estimated Time to Completion
    st.markdown(f"""
    <div class="summary-card">
        <h3>Estimated Time to Completion</h3>
        <p class="time">{summary_data['estimated_time']} Minutes</p>
    </div>
    """, unsafe_allow_html=True)







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

