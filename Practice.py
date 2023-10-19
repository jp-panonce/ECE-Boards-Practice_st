import streamlit as st
import pandas as pd
from random import randrange
from random import shuffle
import unicodedata
from PIL import Image


st.set_page_config(page_title="Practice MCQ",page_icon="📃",layout="wide")

def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

def showanswerButtonClicked():
    st.session_state['highlight_answer'] = True


st.markdown('''
<style>
.katex-html {
    text-align: left;
}
</style>''',
unsafe_allow_html=True
)

#get questions data
if 'questions_df' not in st.session_state:
    questions_df = pd.read_excel('data/questions.xlsx', sheet_name='ECE',converters={
        'question_id':str,
        'Subject':str,
        'question_txt':str,
        'question_img':str,
        'mul_choice':str,
        'ANS':str,
        'A':str,
        'B':str,
        'C':str,
        'D':str,
        'explanation_txt':str,
        'explanation_img':str,
        'explanation_latex':str

    })
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

    question_id = applicable_questions.loc[applicable_questions.index[questionidx_to_display], 'question_id']
    question_to_display = applicable_questions.loc[applicable_questions.index[questionidx_to_display], 'question_txt']
    letter_correct_answer = applicable_questions.loc[applicable_questions.index[questionidx_to_display], 'ANS']
    mult_choice = applicable_questions.loc[applicable_questions.index[questionidx_to_display], 'mul_choice']
    explanation_txt = applicable_questions.loc[applicable_questions.index[questionidx_to_display], 'explanation_txt']
    question_img = applicable_questions.loc[applicable_questions.index[questionidx_to_display], 'question_img']
    explanation_ltx = applicable_questions.loc[applicable_questions.index[questionidx_to_display], 'explanation_latex']
    explanation_img = applicable_questions.loc[applicable_questions.index[questionidx_to_display], 'explanation_img']

    
    st.session_state['question_id'] = question_id
    st.session_state['question_to_display'] = question_to_display
    st.session_state['letter_correct_answer'] = letter_correct_answer
    st.session_state['mult_choice'] = mult_choice
    st.session_state['explanation_txt'] = explanation_txt
    st.session_state['question_img'] = question_img
    st.session_state['explanation_ltx'] = explanation_ltx
    st.session_state['explanation_img'] = explanation_img

    if mult_choice == "y":
        correct_answer = remove_control_characters(applicable_questions.loc[applicable_questions.index[questionidx_to_display], letter_correct_answer])
        st.session_state['correct_answer'] = correct_answer


else:

    question_id = st.session_state['question_id']
    question_to_display = st.session_state['question_to_display']
    letter_correct_answer = st.session_state['letter_correct_answer']
    mult_choice = st.session_state['mult_choice']
    explanation_txt = st.session_state['explanation_txt']
    question_img = st.session_state['question_img']
    explanation_ltx = st.session_state['explanation_ltx']
    explanation_img = st.session_state['explanation_img']

    if mult_choice == "y":
        correct_answer = st.session_state['correct_answer']
        


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

st.markdown("#### " + question_to_display)
if str(question_img) != "nan":
    try:
        q_img = Image.open("images/" + str(question_img))
        st.image(q_img)
    except:
        st.write("(image can't be loaded)")
        pass


if mult_choice == "y":
    # display shuffled choices
    choice_to_display = []
    for idx_choice, letter_choice in enumerate(["A","B","C","D"]):

        if (('highlight_answer' in st.session_state) & (shuffled_choices[idx_choice] == correct_answer)):
            st.markdown("#### :green[" + str(letter_choice) + ". " + str(shuffled_choices[idx_choice]).strip().replace("_x000D_","") + "]")
        else:
            st.markdown("#### " + str(letter_choice) + ". " + str(shuffled_choices[idx_choice]).strip().replace("_x000D_","") + "")
else:
    if (('highlight_answer' in st.session_state)):
        st.markdown("### ANS: :green[" + str(letter_correct_answer) + "]")
    else:
        st.markdown("### ANS: ?")

butt_col1, butt_col2, sp = st.columns([0.1,0.1,1])

anoth_question_button = st.button('Another Question')
checkAnswer_button = st.button('Check Answer',on_click = showanswerButtonClicked)
st.divider()

# SHOW EXPLANATION
if 'highlight_answer' in st.session_state:
    # highlight answer if MCQ or show if not MCQ
    if str(explanation_txt) != "nan":
        
        st.markdown("## :blue[EXPLANATION]")
        st.write(str(explanation_txt))
                
        if bool(explanation_img):

            expl_col1, expl_col2 = st.columns(2)

            with expl_col1:
                if str(explanation_ltx) != "nan":
                    st.latex(str(explanation_ltx))


            with expl_col2:

                if str(explanation_img) != "nan":
                    try:
                        e_img = Image.open("images/" + explanation_img)
                        st.image(e_img)
                    except:
                        st.write("(image can't be loaded)")
                        pass
            
            

        else:
            st.markdown("## :blue[EXPLANATION]")
            st.text(str(explanation_txt))
            if(str(explanation_ltx) != 'nan'):
                st.latex(str(explanation_ltx))



if anoth_question_button:
    for key in st.session_state.keys():
        if key != 'questions_df':
            del st.session_state[key]
    st.experimental_rerun()
