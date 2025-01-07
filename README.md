# chatWithPdf
A Streamlit-based web application that allows users to upload PDFs and chat with their content using Google's Gemini-Pro AI model. The application processes PDFs, converts them into embeddings, and enables natural language interactions with the document content.
🌟 Features

PDF Processing: Upload and process single or multiple PDF documents
Interactive Chat: Ask questions about your PDF content
AI-Powered Responses: Utilizes Google's Gemini-Pro model for accurate responses
Source Tracking: Identifies which parts of the document were used to answer questions
User-Friendly Interface: Clean and intuitive Streamlit-based UI
Multiple Deployment Options: Can be deployed on Streamlit Cloud or Render

🚀 Quick Start
Local Development

Clone the repository

bashCopygit clone https://github.com/yourusername/pdf-chat-app.git
cd pdf-chat-app

Set up a virtual environment

bashCopypython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies

bashCopypip install -r requirements.txt

Set up environment variables
Create a .env file in the root directory:

envCopyGOOGLE_API_KEY=your_google_api_key_here

Run the application

bashCopystreamlit run app.py
🌐 Deployment Options
Streamlit Cloud Deployment

Push your code to GitHub
Visit Streamlit Cloud
Deploy using your GitHub repository
Add your GOOGLE_API_KEY to Streamlit secrets

Render Deployment

Push your code to GitHub
Visit Render
Create a new Web Service
Select your repository
Configure as a Docker deployment
Add your GOOGLE_API_KEY to environment variables

📦 Project Structure
Copypdf-chat-app/
├── app.py              # Main application file
├── Dockerfile          # Docker configuration for Render deployment
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (local development only)
└── README.md          # Project documentation
💻 Tech Stack

Frontend: Streamlit
Backend: Python
AI/ML:

Google Gemini-Pro
LangChain
FAISS for vector storage


PDF Processing: PyPDF2
Deployment: Docker

📋 Requirements

Python 3.9+
Google API Key (Gemini-Pro access)
Required Python packages (see requirements.txt)

🛠️ Configuration
Environment Variables

GOOGLE_API_KEY: Your Google API key for Gemini-Pro access

Application Settings
The application can be configured through Streamlit's configuration:

Adjust chunk size for PDF processing
Modify embedding parameters
Configure conversation memory settings

🤝 Contributing

Fork the repository
Create a new branch
Make your changes
Submit a pull request

🐛 Troubleshooting
Common Issues

PDF Loading Errors

Ensure PDFs are not corrupted
Check PDF permissions
Verify PDF is text-based (not scanned)


Deployment Issues

Verify all dependencies are in requirements.txt
Check environment variables are set
Review deployment logs for errors


Memory Issues

Reduce chunk size for large PDFs
Adjust overlap settings
Consider using a paid tier for large documents



📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
🙏 Acknowledgments

Google Generative AI
Streamlit team
LangChain community

📧 Contact
For questions or support, please open an issue in the GitHub repository.
🔮 Future Improvements

 Add support for more document types
 Implement document highlighting
 Add conversation memory persistence
 Improve error handling and recovery
 Add user authentication
 Implement rate limiting
 Add support for custom prompts
