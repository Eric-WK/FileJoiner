import streamlit as st 
import pandas as pd 
import os 


## UX - Upload multiple files 
st.title("File Joiner")

## instructions: 
st.header("Instructions")

## markdown with steps 
st.markdown("""
1. Upload all the files to join. 
2. Click the process button. 
3. Download the joined file. 
""")

## upload multiple files
uploaded_files = st.file_uploader("Upload files", type=["csv","tsv"], accept_multiple_files=True)

if uploaded_files:
    ## more than 1 file has to be uploaded to proceed 
    if len(uploaded_files) > 1: 
        ## get the file names 
        all_files_names = [x.name for x in uploaded_files]

        ## we get the first common part of the filename
        stub = os.path.commonprefix(all_files_names)
        if stub: 
            st.success("All files have the same prefix. You can proceed.")
            ## count the number of files that have the same stub
            count = len([x for x in all_files_names if x.startswith(stub)])

            ## create two columns: 
            col1, col2 = st.columns(2)

            ## show the number of files that have been uploaded 
            col1.metric("Number of files uploaded: ", len(uploaded_files))

            ## show the count, and make sure it is equal to the number of files uploaded 
            col2.metric("Number of files with the same prefix: ", count)

            ## input the stub from the user, it is prefilled with the common part of the filename
            stub = st.text_input("Enter the file names to be joined", stub)

            ## create two more columns: process & download button 
            process_btn, download_btn = st.columns(2)

            ## if the process button is clicked, then we join the files
            if process_btn.button("Process"):
                ## create an empty list to store the dataframes 
                dfs = []

                ## iterate through the uploaded files 
                for file in uploaded_files:
                    ## read the file as a dataframe 
                    df = pd.read_csv(file, encoding = 'utf-16', sep='\t')
                    ## append the dataframe to the list 
                    dfs.append(df)

                ## join the dataframes 
                joined_df = pd.concat(dfs)

                ## fill the na values with 0's
                joined_df.fillna(0, inplace=True)

                ## drop the "#" column 
                joined_df.drop("#", axis=1, inplace=True)

                ## show the joined dataframe 
                st.dataframe(joined_df)

                ## download the joined file 
                download_btn.download_button("Download", joined_df.to_csv(index=False), f"{stub}_joined.csv")

        else: 
            st.warning("The files do not have the same prefix. Please upload files with the same prefix.")
    ## else show a warning message, please upload more than one file 
    else:
        st.warning("Please upload more than one file to perform the join.")

