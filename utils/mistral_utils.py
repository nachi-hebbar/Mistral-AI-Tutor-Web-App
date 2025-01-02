from mistralai import Mistral
import json
import os
from getpass import getpass
import streamlit as st

# Generate Quiz
from mistralai import Mistral
import os



# Initialize Mistral client
api_key = os.getenv("MISTRAL_API_KEY") or getpass("Enter Mistral API Key: ")
client = Mistral(api_key=api_key)

# Generate Summary
@st.cache_data
def generate_summary(content):
    messages = [
        {
            "role": "user",
            "content": (
                "You are a professional summarization assistant. Your task is to provide a structured summary for the given document "
                "and output it in JSON format with the following keys:\n"
                "- `summary`: A concise summary of the document (150-200 words).\n"
                "- `key_skills`: A list of key skills required to learn or understand the content.\n"
                "- `difficulty`: The estimated difficulty level (Easy, Medium, or Hard) for a STEM college student.\n"
                "- `estimated_time`: The estimated time (in minutes) required for a STEM college student to read and thoroughly comprehend the document.\n\n"
                "#### Few-shot Examples:\n"
                "Example 1:\n"
                "```\n"
                "{\n"
                "  \"summary\": \"This document discusses the fundamentals of machine learning, including supervised, unsupervised, "
                "and reinforcement learning. It provides an overview of common algorithms, such as linear regression, k-means clustering, "
                "and Q-learning, along with their applications in various industries like healthcare, finance, and technology.\",\n"
                "  \"key_skills\": [\"Basic programming knowledge\", \"Understanding of mathematical concepts (e.g., linear algebra, statistics)\", \"Familiarity with algorithms\"],\n"
                "  \"difficulty\": \"Intermediate\",\n"
                "  \"estimated_time\": 45\n"
                "}\n"
                "```\n\n"
                "Example 2:\n"
                "```\n"
                "{\n"
                "  \"summary\": \"This document introduces the principles of cybersecurity, including common threats such as phishing, malware, "
                "and ransomware. It outlines strategies for securing systems and data, such as using encryption, firewalls, and multifactor authentication.\",\n"
                "  \"key_skills\": [\"Basic understanding of networking\", \"Knowledge of encryption techniques\", \"Awareness of common cybersecurity threats\"],\n"
                "  \"difficulty\": \"Beginner\",\n"
                "  \"estimated_time\": 30\n"
                "}\n"
                "```\n\n"
                "#### Document Content:\n"
                f"{content[:4000]}"
            ),
        }
    ]
    response = client.chat.complete(
        model="pixtral-12b-2409",  # Replace with your chosen free model
        messages=messages,
        temperature=0.7,
        response_format={"type": "json_object"},  # Enforce JSON response
        max_tokens=2000,
    )

    return response.choices[0].message.content



@st.cache_data
def generate_quiz(content, num_questions=10, difficulty="Medium", include_explanations=False):
    """
    Generates a quiz based on the provided content using the Mistral model.

    Args:
        content (str): The content to generate quiz questions from.
        num_questions (int): The number of questions to generate.
        difficulty (str): The difficulty level of the questions ("Easy", "Medium", "Hard").
        include_explanations (bool): Whether to include explanations for the answers.

    Returns:
        list: A list of quiz questions in the specified format.
    """
    try:
        # Additional instruction for including explanations
        explanation_text = "Provide explanations for each correct answer." if include_explanations else ""

        # Construct the message for the model
        messages = [
            {
                "role": "user",
                "content": (
                    f"You are a Teacher/Professor creating a quiz to test understanding of the provided content. "
                    f"Your task is to generate **{num_questions} {difficulty.lower()}-level multiple-choice questions** based on the content. "
                    f"Each question should have **4 options**, with **one correct answer clearly labeled**. Ensure the questions "
                    f"are diverse, engaging, and span across different aspects of the content to comprehensively test knowledge.\n\n"
                    f"{explanation_text}\n\n"
                    "#### Instructions:\n"
                    "- Write each question clearly and concisely.\n"
                    "- Provide 4 options for each question, ensuring the options are plausible.\n"
                    "- Mark the correct answer explicitly in the specified format.\n"
                    "\n"
                    "#### Output Format:\n"
                    "Provide the output as a list of JSON objects with the following keys:\n"
                    "1. **Question**: The multiple-choice question.\n"
                    "2. **Options**: A list containing 4 options.\n"
                    "3. **Answer**: The correct option (must match one of the provided options).\n"
                    "4. **Explanation** (Optional): A short explanation for the correct answer, if explanations are included.\n"
                    "\n"
                    "#### Few-shot Example:\n"
                    "[\n"
                    "  {\n"
                    "    \"Question\": \"What is the capital of France?\",\n"
                    "    \"Options\": [\"Paris\", \"London\", \"Berlin\", \"Madrid\"],\n"
                    "    \"Answer\": \"Paris\",\n"
                    "    \"Explanation\": \"Paris has been the capital of France since the 10th century.\"\n"
                    "  },\n"
                    "  {\n"
                    "    \"Question\": \"Which gas do plants absorb during photosynthesis?\",\n"
                    "    \"Options\": [\"Oxygen\", \"Carbon Dioxide\", \"Nitrogen\", \"Hydrogen\"],\n"
                    "    \"Answer\": \"Carbon Dioxide\",\n"
                    "    \"Explanation\": \"Plants absorb carbon dioxide from the air to produce energy via photosynthesis.\"\n"
                    "  }\n"
                    "]\n\n"
                    "#### Content:\n"
                    f"{content[:4000]}"
                ),
            },
        ]

        # Call the Mistral model API
        response = client.chat.complete(
            model="pixtral-12b-2409",
            messages=messages,
            temperature=0.7,
            response_format={"type": "json_object"},  # Specify JSON object output
        )

        # Return the JSON response content
        return response.choices[0].message.content

    except Exception as e:
        print(f"Error generating quiz: {e}")
        return None


def generate_coding_questions(content, num_questions=5, difficulty="Medium", include_explanations=True):
    """
    Generate coding questions based on provided study content.

    Args:
        content (str): Study material to base questions on.
        num_questions (int): Number of questions to generate.
        difficulty (str): Difficulty level ("Easy", "Medium", "Hard").
        include_explanations (bool): Whether to include explanations for answers.

    Returns:
        str: JSON string containing the coding questions.
    """
    try:
        messages = [
            {
                "role": "user",
                "content": (
                    f"You are an expert programming instructor creating coding challenges for students."
                    f" Based on the provided content, create **{num_questions} coding questions** for students with a difficulty level of '{difficulty}'."
                    " Each question should focus on programming concepts, debugging, or completing code. Only coding related, nothing else and pertaining to the document provided."
                    "\n\n#### Instructions:\n"
                    "- Ensure the questions are relevant to the provided content. They can be programming tasks required to implement the content or show understanding of the content\n"
                    "- For each question, include a short problem description and the code snippet if applicable.\n"
                    "- Specify the type of activity (e.g., 'What does this code do?', 'Debug this code', 'Complete the code').\n"
                    f"{'Include detailed explanations for the correct answers.' if include_explanations else ''}"
                    "\n\n#### Output Format:\n"
                    "Provide the output as a list of JSON objects with the following keys:\n"
                    "- **Question**: The text of the question.\n"
                    "- **TaskType**: The type of coding activity ('Understanding', 'Debugging', 'Completion').\n"
                    "- **CodeSnippet**: The relevant code snippet, if applicable.\n"
                    "- **Answer**: The correct answer or explanation.\n"
                    "\n#### Few-shot Examples:\n"
                    "[\n"
                    "  {\n"
                    "    \"Question\": \"What does this Python function do?\",\n"
                    "    \"TaskType\": \"Understanding\",\n"
                    "    \"CodeSnippet\": \"def is_even(n):\\n    return n % 2 == 0\",\n"
                    "    \"Answer\": \"This function checks whether a number is even. It returns True if the number is even and False otherwise.\"\n"
                    "  },\n"
                    "  {\n"
                    "    \"Question\": \"Debug the following code to fix the error.\",\n"
                    "    \"TaskType\": \"Debugging\",\n"
                    "    \"CodeSnippet\": \"def add_numbers(a, b):\\n    return a + b\\nprint(add_numbers(5))\",\n"
                    "    \"Answer\": \"The function 'add_numbers' is called with only one argument. To fix this, call it with two arguments like: 'print(add_numbers(5, 3))'.\"\n"
                    "  },\n"
                    "  {\n"
                    "    \"Question\": \"Complete the following code to calculate the factorial of a number.\",\n"
                    "    \"TaskType\": \"Completion\",\n"
                    "    \"CodeSnippet\": \"def factorial(n):\\n    if n == 0:\\n        return 1\\n    else:\",\n"
                    "    \"Answer\": \"Add 'return n * factorial(n - 1)' inside the 'else' block.\"\n"
                    "  }\n"
                    "]\n\n"
                    "#### Content:\n"
                    f"{content[:4000]}"
                ),
            }
        ]

        # Call Codestral Instruct endpoint
        response = client.chat.complete(
            model="pixtral-12b-2409",
            #model="open-codestral-mamba",#Disabling codestral for incorrect output format for now
            messages=messages,
            temperature=0.4,
            response_format={"type": "json_object"},
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"Error generating coding questions: {e}")
        return None






