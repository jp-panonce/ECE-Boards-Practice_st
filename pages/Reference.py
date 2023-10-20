import streamlit as st
from pathlib import Path
import pandas as pd
from PIL import Image

def read_markdown_file(markdown_file_path):
    return open(markdown_file_path, 'r')

def getFormulaData():
    # get Formulas
    df = pd.read_excel('data/references.xlsx', sheet_name='formulas')
    
    return df

def getConstantsData():
    # get Formulas
    df = pd.read_excel('data/references.xlsx', sheet_name='constants',dtype=str)
    
    return df

def getMnemonicGuides():
    # get Formulas
    df = pd.read_excel('data/references.xlsx', sheet_name='mnemonic_guide',dtype=str)
    
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

tab_tableConstants, tab_formula, tab_caltech, tab_dictionary, tab_mnemonics, tab_ckts = st.tabs(["Tables/Constants", "Formulas", "Calcutech", "Dictionary","Mnemonics/Guides","Circuits"])

with tab_tableConstants:

    st.markdown("## CONSTANTS")

    with st.expander('SEARCH CONSTANTS'):
        constants_data = getConstantsData()
        constants_data['Constant Name'] = constants_data['Constant Name'].astype(str)


        # Search constant
        constants_list = sorted(constants_data['Constant Name'].astype(str).unique())
        selected_formulas = st.multiselect("Search Constant",constants_list,placeholder = "All Constants")
        # TODO: create data file containing all constants
        if bool(selected_formulas):
            constants_to_display =  constants_data[(constants_data['Constant Name'].isin(selected_formulas))]
        else:
            constants_to_display = constants_data

        # TODO: display df
        constants_to_display = constants_to_display.drop(['ID', 'Topic','Table Name'], axis=1)
        st.dataframe(constants_to_display,hide_index=True,use_container_width=True)

    st.markdown("## TABLE OF CONSTANTS")

    with st.expander('SEARCH TABLE'):
        # Create Tables Data. Explode according to topic with delimeter ";"
        tables_data = constants_data
        tables_data['Topic'] = tables_data['Topic'].str.split(';')
        tables_data = tables_data.explode('Topic')

        # Create search box for Table Name
        constTable_list = sorted(tables_data['Topic'].astype(str).unique())
        selected_constTable = st.selectbox("Select Table to Display",constTable_list)

        # if a table is selected, display the table
        if selected_constTable:
            # filter table and remove some fields
            table_to_display =  tables_data[(tables_data['Topic'] == selected_constTable)]
            table_to_display = table_to_display.drop(['ID', 'Topic','Constant Name'], axis=1)

            table_to_display.rename(columns={'Table Name':'Name'}, inplace=True)

            # if table is not for SciCal constants, remove SciCal Constants
            if selected_constTable != "SciCal Constants":
                table_to_display = table_to_display.drop(['SciCal_Constant'], axis=1)

            # display table
            st.dataframe(table_to_display,hide_index=True,use_container_width=True)

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

with tab_mnemonics:
    guides_data = getMnemonicGuides()

    
    guideNames_list = sorted(guides_data['name'].unique())
    selected_guide = st.selectbox("Search Guide",guideNames_list)

    guide_to_display =  guides_data[(guides_data['name'] == selected_guide)].iloc[0]

    st.markdown("#### " + str(guide_to_display['name']))

    guide_spc,guide_col1, guide_spc2,guide_col2 = st.columns([0.1,1,0.4,1.5])

    with guide_col1:
        try:
            guide_img = Image.open("images/" + str(guide_to_display['related_img']))
            st.image(guide_img)
        except:
            st.write("(image can't be loaded)")
            pass
    
    with guide_col2:
        st.markdown("##### Description")
        st.write(str(guide_to_display['description']))

    pass

# st.markdown(md_file.read(), unsafe_allow_html=True)