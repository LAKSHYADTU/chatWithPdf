# Chat with PDF 💬

## Overview

This project is a **Streamlit-based web application** that allows users to:
1. Upload PDF files.
2. Extract and process the content from these PDFs.
3. Interact with the content using a conversational interface powered by **Google's Generative AI**.

---

## Core Features

1. **PDF Upload and Processing**
   - Users can upload one or multiple PDF files.
   - The application validates the PDF format and extracts text using `PyPDF2`.
   - Extracted text is split into smaller chunks for efficient processing.

2. **Embedding and Vector Store Creation**
   - Text chunks are converted into embeddings using **Google Generative AI embeddings**.
   - These embeddings are stored in a **FAISS vector store**, enabling efficient retrieval of relevant content.

3. **Conversational Interface**
   - A conversational model powered by **Google Generative AI** handles the Q&A.
   - A `ConversationalRetrievalChain` integrates the conversational model with the vector store to fetch contextually relevant chunks.
   - Users interact with the application via a chat interface to ask questions about the PDF content.

4. **Session Management**
   - Conversation history is stored to maintain context across user queries.
   - A "Reset Chat" button allows users to start fresh.

5. **Error Handling**
   - Extensive error handling ensures smooth operation, including PDF validation, API key issues, and empty content warnings.

---

## Workflow

### 1. Setting Up the Environment
- The app uses the `dotenv` library to read the **Google API key** from an `.env` file.
- If the key isn't found, the app prompts the user to input it via a sidebar.
- The API key is then passed to `google.generativeai` for configuration.

### 2. User Interface with Streamlit
The app has:
1. **Sidebar**:
   - Users can upload PDFs, reset the chat, and enter the Google API key.
2. **Main Section**:
   - Displays the chat interface where users can ask questions and see the app's responses.

### 3. Uploading and Processing PDFs
- Users can upload PDFs through the sidebar.
- The app validates and processes these files using `PyPDF2`, extracting text and splitting it into manageable chunks.

### 4. Embedding and Vector Store Creation
- Text chunks are converted into high-dimensional embeddings using **Google Generative AI embeddings**.
- These embeddings are stored in a **FAISS vector store**, enabling similarity-based retrieval.

### 5. Creating the Conversational Chain
- A `ConversationalRetrievalChain` integrates:
  1. **LLM (Large Language Model)** powered by `ChatGoogleGenerativeAI`.
  2. **Retriever** for fetching relevant text chunks from the vector store.
  3. **Memory** for maintaining conversation history.

### 6. Chat Interface
- Users type questions into a chat box, and the app responds with contextually relevant answers.
- Chat history is displayed to provide a conversational experience.

---

## Technical Stack
1. **STREAMLIT :**
   - Acts as an interface.
   - Provides a user-friendly interface for uploading PDFs and interacting with the app.
   - Enables the creation of interactive widgets such as file uploaders, buttons, and chat input fields.
   - Displays extracted content and conversation history in an organized manner.
2. **Environment Setup (dotenv) :**
   - Loads API keys securely.
  
3. **PyPDF2 :**
   - The uploaded files are validated using PdfReader.
   - Text is extracted page by page using the extract_text method.
   - Error handling ensures corrupted or image-only PDFs do not disrupt the workflow.
   - Extracted text is concatenated for all pages and prepared for splitting.

4. **Text Splitting (LangChain) :**
   - The text is split into manageable chunks using RecursiveCharacterTextSplitter.
   - Overlapping chunks ensure context is preserved across splits.
   - These chunks are passed to the embedding model.

5. **Embedding Creation (Google Generative AI) :**
   - The text chunks produced during the text splitting phase are passed to the embedding model, Each chunk is treated as a standalone    piece of text to ensure it fits within the token limits of the model.
   - The GoogleGenerativeAIEmbeddings model processes the text chunks and converts them into high-dimensional vectors, These vectors are mathematical representations that capture the semantic and contextual essence of the text.

6. **FAISS (Facebook AI Similarity Search) :**
   - Enables efficient similarity-based retrieval of text chunks.
   - When a user asks a question, the app generates an embedding for the query and retrieves similar chunks from the vector store.

7. **Conversational Model (LangChain + Google Generative AI) :**
   - The ChatGoogleGenerativeAI model to generate responses based on the retrieved chunks and conversation history.
   

---

## Benefits

1. **Efficiency**:
   - Users can interact with large documents without manually searching through them.

2. **Contextual Conversations**:
   - The conversational chain ensures responses are relevant and contextual.

3. **Scalable**:
   - Supports multiple PDFs, enabling users to query across several documents.

4. **User-Friendly Interface**:
   - Simple upload and chat functionality with real-time feedback.

