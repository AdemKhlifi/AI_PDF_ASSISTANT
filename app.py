import streamlit as st
from PyPDF2 import PdfReader
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")
client=genai.Client(api_key=api_key)

#-------------PAGE CONFIG----------------#
st.set_page_config(
    page_title="AI PDF Study Assistant",
    page_icon="logo.png",
    layout="wide"
)


#-------------SIDEBAR----------------#
with st.sidebar :
    st.title("⚙️ Settings")
    button_clear=st.button("🗑️ Clear Chat")
    st.title("📚 AI Tools")
    st.logo("logo.png")
    button_sum=st.button("📄 Summarize PDF")
    button_quiz=st.button("🧩 Generate Quiz")
    button_flashcards=st.button("🃏 Generate Flashcards")
    button_keyP=st.button("📌 Key Points")
    st.title("ℹ️ Information")
    butDev=st.button("👨‍💻 Developer")
    if "dev" not in st.session_state : 
         st.session_state.dev=False
    if butDev : 
        st.session_state.dev=not st.session_state.dev
    if st.session_state.dev : 
         st.info("Hello! I'm Adem Khlifi, 20 Years Old, a Computer Science student passionate about Artificial Intelligence, software development, and emerging technologies.I created this AI PDF Assistant as a personal project to explore Generative AI, Large Language Models, and how AI can be integrated into real-world applications.Through this project, I aim to improve my programming skills, learn more about AI engineering, and build useful tools that help students learn and solve problems more efficiently.")
    butAbt=st.button("📖 About")
    if "abt" not in st.session_state : 
         st.session_state.abt=False
    if butAbt : 
         st.session_state.abt=not st.session_state.abt
    if st.session_state.abt : 
         st.info("AI PDF Study Assistant is an AI-powered learning application built with Python, Streamlit, and Google Gemini. It helps students interact with their study materials by answering questions based on uploaded PDF documents.The application can analyze PDF content, provide accurate answers, generate summaries, create quizzes, and produce flashcards to make learning more efficient and engaging. Its goal is to simplify studying by transforming static documents into an interactive AI learning experience.This project was developed as a personal learning initiative to explore Generative AI, Large Language Models (LLMs), and modern AI application development while improving software engineering and problem-solving skills.")
        



#------------MAIN PAGE----------------#
st.title("📚 AI PDF Study Assistant")
st.write("Upload your study material and ask questions about its content using AI !")
PdfFile=st.file_uploader("📄 Upload your PDF",type="pdf")
if PdfFile is not None : 
    st.success("PDF Uploaded Successfully ✅")
    if "pdf_text" not in st.session_state : 
        reader=PdfReader(PdfFile)
        pdf_text=""
        for page in reader.pages : 
            pdf_text+=page.extract_text()
        st.session_state.pdf_text=pdf_text
    question=st.chat_input("Ask Something ...")
    if"messages" not in st.session_state : 
        st.session_state.messages=[]

    for message in st.session_state.messages : 
        st.chat_message(message["role"]).write(message["content"])
    if button_sum :
        prompt=(f"You are an AI study assistant. You will be provided with a PDF document's content , your task is to summarize the PDF content based on the information contained in the PDF ,\nPDF Content:\n{st.session_state.pdf_text} ")
        with st.spinner("💭 Summarizing... ") :
            response=client.models.generate_content(
                contents=prompt,
                model="gemini-3.1-flash-lite"
            )
            answer=response.text
        st.session_state.messages.append({"role":"assistant", "content":answer})
        st.rerun()
    if button_quiz :
        prompt=(f"You are an AI study assistant. You will be provided with a PDF document's content , your task is to give and generate a quiz based on the information contained in the PDF ,\nPDF Content:\n{st.session_state.pdf_text} ")
        with st.spinner("💭 Generating... ") :
            response=client.models.generate_content(
                contents=prompt,
                model="gemini-3.1-flash-lite"
            )
            answer=response.text
        st.session_state.messages.append({"role":"assistant", "content":answer})
        st.rerun()
    if button_flashcards :
            prompt=(f"You are an AI study assistant. You will be provided with a PDF document's content , your task is to give and generate flashcards based on the information contained in the PDF ,\nPDF Content:\n{st.session_state.pdf_text} ")
            with st.spinner("💭 Generating... ") :
                response=client.models.generate_content(
                    contents=prompt,
                    model="gemini-3.1-flash-lite"
                )
                answer=response.text
            st.session_state.messages.append({"role":"assistant", "content":answer})
            st.rerun()
    if button_keyP :
            prompt=(f"You are an AI study assistant. You will be provided with a PDF document's content , your task is to give and generate the key points based on the information contained in the PDF ,\nPDF Content:\n{st.session_state.pdf_text} ")
            with st.spinner("💭 Generating... ") :
                response=client.models.generate_content(
                    contents=prompt,
                    model="gemini-3.1-flash-lite"
                )
                answer=response.text
            st.session_state.messages.append({"role":"assistant", "content":answer})
            st.rerun()
    if question :
        prompt=(f"You are an AI study assistant. You will be provided with a PDF document's content and a question. Your task is to answer the question based on the information contained in the PDF. If the answer is not present in the PDF, respond with 'The uploaded document does not contain enough information to answer this question.'.\n\nPDF Content:\n{st.session_state.pdf_text}\n\nQuestion: {question}\n\nAnswer:")
        st.session_state.messages.append({"role": "user", "content": question})
        with st.spinner("💭 Thinking... ") :
            response=client.models.generate_content(
                contents=prompt,
                model="gemini-3.1-flash-lite"
            )
            answer=response.text
        st.session_state.messages.append({"role":"assistant", "content":answer})
        st.rerun()
    if button_clear : 
         st.session_state.clear()
         st.rerun()




