import streamlit as st
import pandas as pd
from random import randrange
from random import shuffle
import unicodedata

st.set_page_config(page_title="Practice MCQ",page_icon="📃",layout="wide")

def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

def showanswerButtonClicked():
    st.session_state['highlight_answer'] = True

#get questions data

if 'questions_df' not in st.session_state:
    questions_df = pd.read_excel('data/questions.xlsx', sheet_name='ECE')
    st.session_state['questions_df'] = questions_df
else:
    questions_df = st.session_state['questions_df']    
    

#Selection to let user select subjects to include
selected_subjects = st.multiselect("Select Subject",["MATH","GEAS","ELECS","EST"],default="GEAS",placeholder = "All Subjects")

# Apply filter according to selected subject
if selected_subjects:
    applicable_questions = questions_df[questions_df['Subject'].isin(selected_subjects)] 
else:
    applicable_questions = questions_df

#get random row
print(len(applicable_questions))
questionidx_to_display = randrange(0,len(applicable_questions)) 


# GET QUESTION DATA
if 'question_loaded' not in st.session_state:

    st.session_state['question_loaded'] = True

    question_to_display = applicable_questions.loc[applicable_questions.index[questionidx_to_display], 'question_txt']
    letter_correct_answer = applicable_questions.loc[applicable_questions.index[questionidx_to_display], 'ANS']
    mult_choice = applicable_questions.loc[applicable_questions.index[questionidx_to_display], 'mul_choice']
    correct_answer = remove_control_characters(applicable_questions.loc[applicable_questions.index[questionidx_to_display], letter_correct_answer])
    explanation_txt = applicable_questions.loc[applicable_questions.index[questionidx_to_display], 'explanation_txt']

    
    st.session_state['question_to_display'] = question_to_display
    st.session_state['letter_correct_answer'] = letter_correct_answer
    st.session_state['mult_choice'] = mult_choice
    st.session_state['correct_answer'] = correct_answer
    st.session_state['explanation_txt'] = explanation_txt

    

else:
    question_to_display = st.session_state['question_to_display']
    letter_correct_answer = st.session_state['letter_correct_answer']
    mult_choice = st.session_state['mult_choice']
    correct_answer = st.session_state['correct_answer']
    explanation_txt = st.session_state['explanation_txt']


correct_choice = "-"
shuffled_choices = "-"
if mult_choice == "y":
    print("Multiple Choice Question")

    if 'choices' not in st.session_state:
        choices = [
            remove_control_characters(applicable_questions.loc[applicable_questions.index[questionidx_to_display], 'A']),
            remove_control_characters(applicable_questions.loc[applicable_questions.index[questionidx_to_display], 'B']),
            remove_control_characters(applicable_questions.loc[applicable_questions.index[questionidx_to_display], 'C']),
            remove_control_characters(applicable_questions.loc[applicable_questions.index[questionidx_to_display], 'D'])
        ]
        st.session_state['choices'] = choices
    else:
        choices = st.session_state['choices']

    if 'shuffled_choices' not in st.session_state:
        shuffled_choices = choices
        shuffle(shuffled_choices)
        st.session_state['shuffled_choices'] = shuffled_choices
    else:
        shuffled_choices = st.session_state['shuffled_choices']

    correct_choice = (["A","B","C","D"])[shuffled_choices.index(correct_answer)]
else:
    print("not a multiple choice question")




# st.dataframe(questions_df)
st.markdown("#### " + question_to_display)

# display shuffled choices
choice_to_display = []
for idx_choice, letter_choice in enumerate(["A","B","C","D"]):

    if (('highlight_answer' in st.session_state) & (shuffled_choices[idx_choice] == correct_answer)):
        st.markdown("#### :green[" + str(letter_choice) + ". " + str(shuffled_choices[idx_choice]).strip().replace("_x000D_","") + "]")
    else:
        st.markdown("#### " + str(letter_choice) + ". " + str(shuffled_choices[idx_choice]).strip().replace("_x000D_","") + "")


butt_col1, butt_col2, sp = st.columns([0.1,0.1,1])

with butt_col1:
    anoth_question_button = st.button('Another Question')

with butt_col2:
    checkAnswer_button = st.button('Check Answer',on_click = showanswerButtonClicked)

if 'highlight_answer' in st.session_state:
    # highlight answer if MCQ or show if not MCQ
    if bool(explanation_txt):
        st.markdown("## :blue[EXPLANATION]")

        st.text(str(explanation_txt))


    


if anoth_question_button:
    for key in st.session_state.keys():
        if key != 'questions_df':
            del st.session_state[key]
    st.experimental_rerun()
