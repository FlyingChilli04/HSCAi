from dotenv import load_dotenv
import os
import openai
import pandas
import streamlit as st

st.title("HSCAi English Short Answer Question bot")

# Load environment variables
load_dotenv()
openai_api_key = os.environ.get('OPENAI_API_KEY')
openai.api_key = openai_api_key
client = openai.OpenAI(api_key=openai_api_key)

# Define system prompt
system_prompt = "You are an assistant that, when asked to create a paper 1 short answer HSC question, provides the title of a text, the actual text itself, the author of the text, the text type, the actual question about the text for students to answer and the reasonable amount of marks the question is worth (max 6 marks)."

# Check if the fine-tuned model and chat history are already in session state, initialize if not
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = 'ft:gpt-3.5-turbo-0125:personal::9QVEAIcy'
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Create English Short Answer Question..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare the messages for the API call including the system prompt
    messages = [{"role": "system", "content": system_prompt}] + st.session_state.messages

    # Get the assistant's response

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=messages
        ).choices[0].message.content
        processed_response = response.replace('\n', '  \n\n')
        # st.markdown(response)
        # st.markdown(processed_response)
        st.write(processed_response)
    
    # Add assistant's response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
