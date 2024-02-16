# -*- coding: utf-8 -*-
"""Untitled10.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QF8jWuVRiXMjbovC34Y3BwQplan5WVdZ
"""

import os
import dotenv
from langchain_openai import OpenAI
from langchain_openai.chat_models import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
import streamlit as st


# Load the .env file and invoke the secret API key from the file
dotenv.load_dotenv('API.env')
OpenAI.api_key = os.getenv("OPEN_API_KEY")

#summarize_pdf function

def summarize_pdf(pdf_file_path, chunk_size, chunk_overlap, prompt):
    #Instantiate LLM model gpt-3.5-turbo-16k
    llm=ChatOpenAI(model="gpt-4-turbo-preview", temperature=0, openai_api_key=OpenAI.api_key)

    #Load PDF file
    loader = PyPDFLoader(pdf_file_path)
    docs_raw = loader.load()

    #Create multiple documents
    docs_raw_text = [doc.page_content for doc in docs_raw]

    #Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs_chunks = text_splitter.create_documents(docs_raw_text)

    #Summarize the chunks
    chain = load_summarize_chain(llm, chain_type="stuff", prompt = prompt)
    #Return the summary
    summary = chain.invoke(docs_chunks, return_only_outputs=True)
    return summary['output_text']

#streamlit app main() function

def main():
    #Set page config and title
    st.set_page_config(page_title="PDF Summarizer", page_icon=":book:", layout="wide")
    st.title("PDF Summarizer")

    #Input pdf file path
    pdf_file_path = st.text_input("Enter PDF file path:")
    if pdf_file_path != "":
       st.write("PDF file was loaded successfully.")

    #prompt input
    user_prompt = st.text_input("Enter prompt:")
    user_prompt = user_prompt + """{text}"""
    prompt = PromptTemplate(input_variables=["text"], template=user_prompt)

    #Summarize button
    if st.button("Summarize"):
        summary = summarize_pdf(pdf_file_path, 1000, 20, prompt=prompt)
        st.write(summary)

if __name__ == "__main__":
    main()