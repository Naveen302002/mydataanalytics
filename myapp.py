import pandas as pd 
import plotly.express as px
import streamlit as st 

st.set_page_config(
    page_title='Analytics Portal',
    page_icon='📊'
    )

st.title(':rainbow[Data Analytics Portal]')
st.subheader(':gray[Explore Data with ease]',divider='rainbow')

file=st.file_uploader(label='Drop csv or excel file',type=['csv','xslx'])

if file!=None:
    if file.name.endswith('.csv'):
        data=pd.read_csv(file)
    else:
        data=pd.read_excel(file)
    
    st.dataframe(data)
    st.info('File is successfully Uploaded',icon="🚨")
    st.subheader(':rainbow[Basic information of the dataset]',divider='rainbow')
    tab1,tab2,tab3,tab4=st.tabs(['Summary','Top and Bottom Rows','Data Types','Columns'])
    
    with tab1:
        st.write(f'There are {data.shape[0]} rows in dataset and {data.shape[1]} columns in dataset')
        st.subheader(':gray[Statistical summary of the dataset]')
        st.dataframe(data.describe())

    with tab2:
        st.subheader(':gray[Top Rows]')
        toprows=st.slider(label='No. of rows you want',max_value=data.shape[0],min_value=1,key='topslider')
        st.dataframe(data.head(toprows))
        st.subheader(':gray[Bottom Rows]')
        bottomrows=st.slider(label='No. of rows you want',max_value=data.shape[0],min_value=1,key='bottomslider')
        st.dataframe(data.tail(bottomrows))

    with tab3:
        st.subheader(':gray[Data Types of column]')
        st.dataframe(data.dtypes)

    with tab4:
        st.subheader(':gray[Column Names in Dataset]')
        st.write(list(data.columns))
    
    st.subheader(':rainbow[Column Values Count]',divider='rainbow')
    with st.expander('Value Count'):
        col1,col2=st.columns(2)
        with col1:
            column=st.selectbox('Choose Column name',options=list(data.columns))
        with col2:
            toprows=st.number_input('Top rows',min_value=1,step=1)
        
        count=st.button('Count')
        if count:
            result=data[column].value_counts().reset_index().head(toprows)
            st.dataframe(result)
            st.subheader('Visualization',divider='gray')
            fig=px.bar(data_frame=result,x=column,y='count',text='count',template='plotly_white')
            st.plotly_chart(fig)
            fig=px.line(data_frame=result,x=column,y='count',text='count',template='plotly_white')
            st.plotly_chart(fig)
            fig=px.pie(data_frame=result,names=column,values='count')
            st.plotly_chart(fig)
    st.subheader(':rainbow[Group By: Simplify Your Data Analysis]',divider='rainbow')
    st.write('The Groupby lets you summarize data by specific category and groups')
    with st.expander(label='Groupby Operations'):
        col1,col2,col3=st.columns(3)
        with col1:
            col_grpby=st.multiselect('Choose columns to groupby',options=list(data.columns))
        with col2:
            col_operation=st.selectbox('Choose Column for operations',options=list(data.columns))
        with col3:
            col_agg=st.selectbox('Choose operation to perform',options=['sum','max','min','mean','median','count'])
        if col_grpby:
            result=data.groupby(col_grpby).agg(newcol=(col_operation,col_agg)).reset_index()
            st.dataframe(result)
            st.subheader(':gray[Data Visualization]',divider='gray')
            graphs=st.selectbox('Choose your graph',options=['line','bar','scatter','pie','sunburst'])
            if graphs=='line':
                x_axis=st.selectbox('Choose X axis',options=list(result.columns))
                y_axis=st.selectbox('Choose Y axis',options=list(result.columns))
                color=st.selectbox('Color information',options=[None]+list(result.columns))
                fig=px.line(data_frame=result,x=x_axis,y=y_axis,color=color,markers='o')
                st.plotly_chart(fig)
            elif graphs=='bar':
                x_axis=st.selectbox('Choose X axis',options=list(result.columns))
                y_axis=st.selectbox('Choose Y axis',options=list(result.columns))
                color=st.selectbox('Color information',options=[None]+list(result.columns))
                facet_col=st.selectbox('Column Information',options=[None]+list(result.columns))
                fig=px.bar(data_frame=result,x=x_axis,y=y_axis,color=color,facet_col=facet_col,barmode='group')
                st.plotly_chart(fig)
            elif graphs=='scatter':
                x_axis=st.selectbox('Choose X axis',options=list(result.columns))
                y_axis=st.selectbox('Choose Y axis',options=list(result.columns))
                color=st.selectbox('Color information',options=[None]+list(result.columns))
                size=st.selectbox('Size Column',options=[None]+list(result.columns))
                fig=px.scatter(data_frame=result,x=x_axis,y=y_axis,color=color,size=size)
                st.plotly_chart(fig)

            elif graphs=='pie':
                values=st.selectbox('Choose Numerical Values',options=list(result.columns))
                names=st.selectbox('Choose labels',options=list(result.columns))
                fig=px.pie(data_frame=result,values=values,names=names)
                st.plotly_chart(fig)
            
            elif graphs=='sunburst':
                path=st.multiselect('Choose Path',options=[None]+list(result.columns))
                if path:
                    fig=px.sunburst(data_frame=result,path=path,values='newcol')
                    st.plotly_chart(fig)
