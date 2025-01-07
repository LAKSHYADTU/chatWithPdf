import streamlit as st
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import io
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_api():
    """Initialize Gemini API key from environment or user input"""
    load_dotenv()
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        api_key = st.sidebar.text_input('Enter your Google API key:', type='password')
        if api_key:
            os.environ['GOOGLE_API_KEY'] = api_key
            genai.configure(api_key=api_key)
        else:
            st.sidebar.warning('Please enter your Google API key to continue.')
            return False
    else:
        genai.configure(api_key=api_key)
    return True

def is_valid_pdf(file_content):
    """Check if the file is a valid PDF"""
    try:
        # Try to create a PDF reader object
        PdfReader(io.BytesIO(file_content))
        return True
    except Exception as e:
        logger.error(f"PDF validation error: {str(e)}")
        return False

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file with improved error handling"""
    try:
        # Read the file content
        pdf_content = pdf_file.read()
        
        # Validate PDF
        if not is_valid_pdf(pdf_content):
            st.error(f"Invalid or corrupted PDF file: {pdf_file.name}")
            return None
        
        # Create PDF reader from bytes
        pdf_reader = PdfReader(io.BytesIO(pdf_content))
        
        # Reset file pointer
        pdf_file.seek(0)
        
        text = ""
        for page_num, page in enumerate(pdf_reader.pages):
            try:
                text += page.extract_text() + "\n"
            except Exception as e:
                logger.error(f"Error extracting text from page {page_num}: {str(e)}")
                st.warning(f"Skipped page {page_num + 1} due to extraction error")
                continue
        
        if not text.strip():
            st.warning(f"No text could be extracted from {pdf_file.name}. The PDF might be scanned or contain images only.")
            return None
            
        return text
        
    except Exception as e:
        logger.error(f"PDF processing error: {str(e)}")
        st.error(f"Error processing PDF {pdf_file.name}: {str(e)}")
        return None

def split_text_into_chunks(text):
    """Split text into smaller chunks for processing"""
    try:
        if not text:
            return []
            
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)
        return chunks
    except Exception as e:
        logger.error(f"Text splitting error: {str(e)}")
        st.error(f"Error splitting text into chunks: {str(e)}")
        return []

@st.cache_resource
def get_embeddings_model():
    """Get the Google embeddings model"""
    return GoogleGenerativeAIEmbeddings(model="models/embedding-001")

def create_vectorstore(text_chunks):
    """Create vector store from text chunks"""
    try:
        if not text_chunks:
            st.error("No text chunks to process")
            return None
            
        embeddings = get_embeddings_model()
        vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
        return vectorstore
    except Exception as e:
        logger.error(f"Vector store creation error: {str(e)}")
        st.error(f"Error creating embeddings: {str(e)}")
        return None

def create_conversation_chain(vectorstore):
    """Create conversation chain for Q&A"""
    try:
        if not vectorstore:
            st.error("Vector store is not initialized")
            return None
            
        llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.7,
            convert_system_message_to_human=True
        )
        
        memory = ConversationBufferMemory(
            memory_key='chat_history',
            return_messages=True,
            output_key='answer'
        )
        
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(),
            memory=memory,
            return_source_documents=True,
            get_chat_history=lambda h: h,
        )
        
        return conversation_chain
    except Exception as e:
        logger.error(f"Conversation chain creation error: {str(e)}")
        st.error(f"Error creating conversation chain: {str(e)}")
        return None

def process_query(conversation, question):
    """Process a query and return the response"""
    try:
        if not conversation:
            st.error("Conversation chain is not initialized")
            return None
            
        response = conversation({
            "question": question
        })
        
        return response["answer"]
    except Exception as e:
        logger.error(f"Query processing error: {str(e)}")
        st.error(f"Error processing question: {str(e)}")
        return None

def main():
    # Set page configuration
    st.set_page_config(page_title="Chat with PDF", layout="wide")
    
    # Add header
    st.header("Chat with Your PDF 💬")
    
    # Initialize API
    if not init_api():
        return
    
    # Initialize session state
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "processed_pdfs" not in st.session_state:
        st.session_state.processed_pdfs = False

    # Upload PDF section
    with st.sidebar:
        st.subheader("Upload PDF")
        pdf_files = st.file_uploader(
            "Upload your PDF here", 
            type=['pdf'],
            accept_multiple_files=True
        )
        
        # Add a button to reset the chat
        if st.button("Reset Chat"):
            st.session_state.conversation = None
            st.session_state.chat_history = []
            st.session_state.processed_pdfs = False
            st.experimental_rerun()
        
        if pdf_files and not st.session_state.processed_pdfs:
            with st.spinner("Processing PDFs..."):
                all_text = ""
                processed_files = []
                
                # Process each PDF file
                for pdf in pdf_files:
                    st.info(f"Processing {pdf.name}...")
                    text = extract_text_from_pdf(pdf)
                    if text:
                        all_text += text + "\n\n"
                        processed_files.append(pdf.name)
                
                if all_text.strip():
                    # Get text chunks
                    text_chunks = split_text_into_chunks(all_text)
                    
                    if text_chunks:
                        # Create vector store
                        vectorstore = create_vectorstore(text_chunks)
                        if vectorstore:
                            # Create conversation chain
                            conversation_chain = create_conversation_chain(vectorstore)
                            if conversation_chain:
                                st.session_state.conversation = conversation_chain
                                st.session_state.processed_pdfs = True
                                st.success(f"Successfully processed PDFs: {', '.join(processed_files)}")
                else:
                    st.error("No valid text could be extracted from any of the uploaded PDFs")

    # Chat interface
    if st.session_state.conversation:
        user_question = st.chat_input("Ask a question about your PDF:")
        
        if user_question:
            with st.spinner("Thinking..."):
                response = process_query(st.session_state.conversation, user_question)
                if response:
                    st.session_state.chat_history.append(("user", user_question))
                    st.session_state.chat_history.append(("assistant", response))

        # Display chat history
        for role, message in st.session_state.chat_history:
            if role == "user":
                st.chat_message("user").write(message)
            else:
                st.chat_message("assistant").write(message)
    else:
        st.info("Please upload a PDF to start chatting!")

if __name__ == "__main__":
    main()