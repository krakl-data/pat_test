import streamlit as st
from pypdf import PdfReader 
import re
import pandas as pd

re1 = '(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}'
re2 = '\d{1,2}\/\d{1,2}\/\d{2,4}'
re3 = '(0[1-9]|[12][0-9]|3[01])\/(0[1-9]|1[1,2])\/(19|20)\d{2}'

dates = []

suppliers = ['DEMO - Sliced Invoices',
            'Global Enterprises',
            
            ]

suppliers_l = []
money = []
    
with st.form("my-form", clear_on_submit=True):
    st.header("Hi Pat, upload those pdf's I sent you here and click 'UPLOAD!'")
    files = st.file_uploader("FILE UPLOADER",accept_multiple_files=True)
    submitted = st.form_submit_button("UPLOAD!")

    if submitted and files is not None:
        for file in files:
            reader =  PdfReader(file)
            page = reader.pages[0]
            text = page.extract_text()
            
            temp_money = re.findall(r'(?:[\£\$\€]{1}[,\d]+.?\d*)', text)
            temp_money = [re.sub('[a-zA-Z]','',mon) for mon in temp_money]
            money.append(temp_money[-1])
            
            temp_dates = re.compile("(%s|%s|%s)" % (re1, re2, re3)).findall(text)
            temp_dates = [i for ix in temp_dates for i in ix]
            temp_dates = [date for date in temp_dates if date]
            
            dates.append(temp_dates[-1])
            
            temp_suppliers_l = [i for i in suppliers if i in text]
            for sup in temp_suppliers_l:
                suppliers_l.append(sup)

            
        # st.write(suppliers_l,money,dates)
        
        df = pd.DataFrame({'Supplier':suppliers_l,
                          'Amount':money,
                          'Due Date':dates})
        
        st.header('Hover Over Table to Download')
        st.dataframe(df)
