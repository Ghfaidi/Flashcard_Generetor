import question_generation_mcqs

import streamlit as st
import streamlit.components.v1 as components
import random
import pandas as pd

# -------------- app config ---------------

st.set_page_config(page_title="Flashcards", page_icon="🚀")

# ---------------- functions ----------------

# external css
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# callbacks
def callback():
    st.session_state.button_clicked = True


def callback2():
    st.session_state.button2_clicked = True


# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.write("**Streamlit app**")


# ---------------- CSS ----------------

local_css("style.css")

# ---------------- SESSION STATE ----------------
import streamlit as st
import PyPDF2
import io

    
uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'txt'])

if uploaded_file is not None:
    if uploaded_file.type == 'text/plain':
        text = uploaded_file.read().decode("utf-8")
    elif uploaded_file.type == 'application/pdf':
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text() 

        # process pdf here
    key_words=question_generation_mcqs.extract(text)
       
    ques=[]
    ans=[]
    for i in range(len(key_words)):
        question=question_generation_mcqs.get_question(key_words[i],text)
        answer=question_generation_mcqs.question_answerer(question,text)
        ans.append(answer)
        ques.append(question)
    
if "button_clicked" not in st.session_state:
    st.session_state["button_clicked"] = False

if "button2_clicked" not in st.session_state:
    st.session_state["button2_clicked"] = False

if "q_no" not in st.session_state:
    st.session_state["q_no"] = 0

if "q_no_temp" not in st.session_state:
    st.session_state.q_no_temp = 0

# ---------------- Main page ----------------

tab1, tab2 = st.tabs(["Flashcards", " "])


with tab1:


    # ---------------- Questions & answers logic ----------------

    col1, col2 = st.columns(2)
    with col1:
        question = st.button(
            "Draw question", on_click=callback, key="Draw", use_container_width=True
        )
    with col2:
        answer = st.button(
            "Show answer", on_click=callback2, key="Answer", use_container_width=True
        )
    
    if st.session_state["button_clicked"]:
        
        st.session_state["q_no"] = random.randint(0, len(key_words) - 1)
        # this 'if' checks if algorithm should use value from temp or new value (temp assigment in else)
        if st.session_state.button2_clicked:
            
            st.markdown(
                f'<div class="blockquote-wrapper"><div class="blockquote"><h1><span style="color:#000000">{ques[st.session_state.q_no_temp]}</span></h1><h4>&mdash; Question no. {st.session_state.q_no_temp+1}</em></h4></div></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="blockquote-wrapper"><div class="blockquote"><h1><span style="color:#000000">{ques[st.session_state.q_no]}</span></h1><h4>&mdash; Question no. {st.session_state.q_no+1}</em></h4></div></div>',
                unsafe_allow_html=True,
            )
            
            # keep memory of question number in order to show answer
            st.session_state.q_no_temp = st.session_state.q_no

        if answer:
            st.markdown(
                f"<div class='answer'><span style='font-weight: bold; color:#6d7284;'>Answer</span><br><br>{ans[st.session_state.q_no_temp]['answer']}</div>",
                unsafe_allow_html=True,
            )
            st.session_state.button2_clicked = False

    # this part normally should be on top however st.markdown always adds divs even it is rendering non visible parts?

    st.markdown(
        '<div><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Abril+Fatface&family=Barlow+Condensed&family=Cabin&display=swap" rel="stylesheet"></div>',
        unsafe_allow_html=True,
    )

    

    