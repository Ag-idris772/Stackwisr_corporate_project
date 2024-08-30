import streamlit as st
import openai
import os

# Set your OpenAI API key here
openai.api_key = 'your_openai_api_key'

def generate_exam_questions_from_text(text):
    response = openai.Completion.create(
        engine="gpt-4",  # or use "gpt-3.5-turbo"
        prompt=f"Generate a list of exam questions for the following text:\n{text}",
        max_tokens=150
    )
    return response.choices[0].text.strip()

def summarize_text(text):
    response = openai.Completion.create(
        engine="gpt-4",  # or use "gpt-3.5-turbo"
        prompt=f"Summarize the following text:\n{text}",
        max_tokens=150
    )
    return response.choices[0].text.strip()

st.image("Stackwisrlogo.jpg", caption="stackwisr", width=880)
st.title('Exam Question and Text Summarizer')

# Input for generating exam questions
st.header('Generate Exam Questions')

# Option to enter a topic or upload a folder
topic = st.text_input('Enter the topic:')
folder = st.file_uploader('Or upload a folder with text files for generating questions', type=['zip'])

if st.button('Generate Questions'):
    if topic:
        questions = generate_exam_questions_from_text(topic)
        st.subheader('Generated Exam Questions:')
        st.text(questions)
    elif folder:
        # Extract text from all files in the uploaded folder
        import zipfile
        with zipfile.ZipFile(folder, 'r') as zip_ref:
            zip_ref.extractall('extracted_folder')
        
        questions = ""
        for root, dirs, files in os.walk('extracted_folder'):
            for file in files:
                with open(os.path.join(root, file), 'r') as f:
                    text = f.read()
                    questions += generate_exam_questions_from_text(text) + "\n\n"
        
        st.subheader('Generated Exam Questions from Folder:')
        st.text(questions)
    else:
        st.error('Please enter a topic or upload a folder.')

# Input for summarizing text
st.header('Summarize Text')

# Option to enter text or upload a file
text_to_summarize = st.text_area('Enter the text to summarize:')
uploaded_file = st.file_uploader("Or upload a text file for summarization", type=['txt'])

if st.button('Summarize Text'):
    if text_to_summarize:
        summary = summarize_text(text_to_summarize)
        st.subheader('Text Summary:')
        st.text(summary)
    elif uploaded_file:
        text = uploaded_file.read().decode('utf-8')
        summary = summarize_text(text)
        st.subheader('File Summary:')
        st.text(summary)
    else:
        st.error('Please enter text or upload a file to summarize.')

if __name__ == "__main__":
    st.write("Streamlit app is running.")