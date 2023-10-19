import streamlit as st
from pathlib import Path
import pandas as pd

def read_markdown_file(markdown_file_path):
    return open(markdown_file_path, 'r')

def getFormulaData():
    # get Formulas
    df = pd.read_excel('data/references.xlsx', sheet_name='formulas')
    
    return df



# get all required data
df_formulas = getFormulaData()

st.set_page_config(page_title="Quick Reference",page_icon="📃",layout="wide")

#sets alignment of latex to left-align
st.markdown('''
<style>
.katex-html {
    text-align: left;
}
</style>''',
unsafe_allow_html=True
)

tab_tableConstants, tab_formula, tab_caltech, tab_dictionary, tab_mnemonics, tab_ckts = st.tabs(["Tables/Constants", "Formulas", "Calcutech", "Dictionary","Mnemonics","Circuits"])

with tab_tableConstants:

    st.markdown("## CONSTANTS")

    # TODO: for calculator type dropdown

    # TODO: create data file containing all constants

    #


    st.markdown("## TABLES")


with tab_dictionary:


    option = st.selectbox('Enter term to see definition',('ECE','matter'))

    #TODO: Add definition section
    pass

with tab_formula:

    formulaNames_list = sorted(df_formulas['name'].unique())
    selected_formulas = st.multiselect("Search Formula",formulaNames_list,default=formulaNames_list[0],placeholder = "All Formulas")

    for index, row in df_formulas.iterrows():
        if row['name'] in selected_formulas:
            st.markdown("#### " + str(row['name']))

            spc,form_col1, spc2,form_col2 = st.columns([0.1,1,0.4,1.5])

            with form_col1:
                st.latex(str(row['formula_latex']))
                st.latex("where:")

                form_col1_cols = st.columns([0.1,1])
                form_col1_cols[1].latex(str(row['where_latex']))
            
            with form_col2:
                st.markdown("##### Description")
                st.write(str(row['description']))

            st.divider()


# st.markdown(md_file.read(), unsafe_allow_html=True)