
# ==========================================================
# COLLEGE ENQUIRY CHATBOT
# Generative AI Mini Project - Roll No. 11
# MIT ADT Engineering College
# Powered by Ollama + Llama 3.2
# ==========================================================

# STEP 1: IMPORT LIBRARIES

import streamlit as st
import ollama


# STEP 2: PAGE CONFIGURATION

st.set_page_config(
    page_title="MIT ADT College Enquiry Chatbot",
    page_icon="🎓",
    layout="centered"
)


# STEP 3: OLLAMA CONFIGURATION

MODEL_NAME = "llama3.2"

client = ollama.Client(
    host="http://localhost:11434"
)


# STEP 4: LOAD COLLEGE INFORMATION

try:
    with open("college_info.txt", "r", encoding="utf-8") as file:
        college_info = file.read()

    if not college_info.strip():
        st.error("Your college_info.txt file is empty.")
        st.stop()

except FileNotFoundError:
    st.error(
        "college_info.txt file not found. "
        "Please keep it in the same folder as app.py."
    )
    st.stop()


# STEP 5: SYSTEM INSTRUCTION

system_instruction = f"""
You are an intelligent College Enquiry Chatbot
for MIT ADT Engineering College.

Your purpose is to help students with:

1. College admissions
2. Courses offered
3. Fee structure
4. Eligibility criteria
5. Admission procedures
6. Important college information
7. Contact details

STRICT INSTRUCTIONS:

- Answer only college-related questions.
- Use ONLY the information provided below.
- Never invent fees, dates, courses or contact details.
- Never assume missing information.
- If information is unavailable, say:
  "Sorry, this information is not available
  in the college information sheet."
- Use simple and understandable English.
- Keep answers clear, polite and helpful.
- If a question is unrelated to college enquiries,
  politely explain that you only answer
  college-related questions.

COLLEGE INFORMATION:

{college_info}
"""


# STEP 6: CHATBOT HEADER

st.title("🎓 MIT ADT College Enquiry Chatbot")

st.write(
    "Welcome to the College Enquiry Assistant!"
)

st.write(
    "Ask me about admissions, courses, fees "
    "and eligibility criteria."
)

st.caption("Powered by Ollama | Llama 3.2")

st.divider()


# STEP 7: INITIALIZE CHAT HISTORY

if "messages" not in st.session_state:
    st.session_state.messages = []


# STEP 8: DISPLAY CHAT HISTORY

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# STEP 9: ACCEPT USER INPUT

user_question = st.chat_input(
    "Type your college enquiry here..."
)


# STEP 10: GENERATE AI RESPONSE

if user_question:

    # Display user message

    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    with st.chat_message("user"):
        st.markdown(user_question)

    # Generate assistant response

    with st.chat_message("assistant"):

        with st.spinner("Finding your answer..."):

            try:

                # Prepare conversation
                conversation = [
                    {
                        "role": "system",
                        "content": system_instruction
                    }
                ]

                # Include recent conversation history
                for message in st.session_state.messages[-8:]:

                    conversation.append({
                        "role": message["role"],
                        "content": message["content"]
                    })

                # Connect to Ollama
                response = client.chat(
                    model=MODEL_NAME,
                    messages=conversation
                )

                answer = response.message.content

                if not answer:
                    answer = "Sorry, no response was generated."

            except Exception as error:

                answer = (
                    "Unable to connect to Ollama. "
                    "Please check whether Ollama is running "
                    "and the Llama 3.2 model is installed."
                )

                st.error(f"Error details: {error}")

            # Display response
            st.markdown(answer)

    # Save response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })


# STEP 11: SIDEBAR

with st.sidebar:

    st.title("🎓 About")

    st.write("MIT ADT College Enquiry Chatbot")

    st.divider()

    st.subheader("Technologies Used")

    st.write("""
    - Python
    - Ollama
    - Llama 3.2
    - Streamlit
    - Natural Language Processing
    """)

    st.divider()

    st.subheader("Chat Options")

    if st.button("🗑️ Clear Chat", use_container_width=True):

        st.session_state.messages = []

        st.rerun()

    st.divider()

    st.caption(
        "Academic Generative AI Mini Project | 2026"
    )
