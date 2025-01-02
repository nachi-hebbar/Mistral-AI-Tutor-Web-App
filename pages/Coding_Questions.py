# File: pages/3_Code_Generation.py
import streamlit as st
from utils.st_utils import display_coding_question_with_answer,generate_coding_questions
import json


# File: pages/3_Code_Generation.py
import streamlit as st
from utils.st_utils import display_coding_question_with_answer, generate_coding_questions
import json


st.title("🧑‍💻 Code Generation")

st.markdown("""
Generate coding challenges based on your study material. Customize the type of questions, difficulty level, and number of tasks to create tailored coding exercises.
""")

# Check if session state has study material
if "documents" not in st.session_state or not st.session_state["documents"]:
    st.warning("Please upload and process documents first on the 'Home' page.")
else:
    documents = st.session_state["documents"]

    # Customization form
    st.markdown("### Customize Your Coding Questions")
    with st.form("code_generation_form"):
        # Dropdown to select a document
        selected_document = st.selectbox(
            "Select a document to generate coding questions for",
            options=[doc["name"] for doc in documents], index=None
        )

        num_questions = st.slider("Number of Questions", 1, 10, 5)
        difficulty = st.selectbox("Select Difficulty Level", ["Easy", "Medium", "Hard"])
        include_explanations = st.checkbox("Include Explanations for Answers", value=True)

        # Submit button
        submit_button = st.form_submit_button("Generate Coding Questions")

    # Generate coding questions for the selected document
    if submit_button:
        st.markdown(f"### Coding Questions for: {selected_document}")

        # Find the selected document
        selected_doc_content = next(
            (doc["content"] for doc in documents if doc["name"] == selected_document), None
        )

        if selected_doc_content:
            # Display a spinner while generating questions
            with st.spinner("Generating your tailored quiz..."):
                # Generate questions using the utility function
                raw_response = generate_coding_questions(
                    content=selected_doc_content,
                    num_questions=num_questions,
                    difficulty=difficulty,
                    include_explanations=include_explanations
                )


            # Parse and display the generated questions
            parsed_questions = json.loads(raw_response)
            for question in parsed_questions:
                display_coding_question_with_answer(question)

            # Success message
            st.success("Your quiz is ready!")
        else:
            st.error(f"Could not find the content for the document: {selected_document}")
