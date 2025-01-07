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

| **Component**               | **Purpose**                                               |
|-----------------------------|-----------------------------------------------------------|
| **Streamlit**               | Frontend framework for the web app.                      |
| **PyPDF2**                  | PDF text extraction.                                      |
| **FAISS**                   | Vector store for similarity search.                      |
| **LangChain**               | Chain and embedding management.                          |
| **Google Generative AI**    | Embedding model and conversational LLM.                  |
| **dotenv**                  | Environment variable management for API keys.            |
| **Logging**                 | Logs errors and warnings for easier debugging.           |

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

---

## Use Cases

1. **Research**:
   - Academics can upload research papers and ask specific questions about their content.

2. **Legal Documents**:
   - Lawyers can quickly extract relevant clauses or information from lengthy contracts.

3. **Manuals**:
   - Technical teams can query user manuals for specific instructions.

4. **Reports**:
   - Analysts can extract insights from corporate reports without manual reading.

---

## Installation and Usage

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>

