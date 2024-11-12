# Project Name: PDF Query and Highlighter Tool

## Overview

The PDF Query and Highlighter Tool is a versatile application that allows users to upload PDF documents, extract text, ask questions related to the content, and receive answers in real-time. The tool also features a highlighting mechanism to visually point out relevant chunks of text that correspond to the user's queries. The backend is powered by Flask, integrated with OpenAI's language models, and the PDF is processed using multiple open-source libraries.

This application leverages state-of-the-art AI technologies to provide an intuitive interface for querying and understanding document content, making it useful for researchers, students, and professionals who need to analyze complex documents.

## Features

- PDF Uploading and Management: Upload PDFs easily via a user-friendly interface.

- Text Extraction: Extracts text from uploaded PDF documents, processing both images and text-based data.

- Question-Answering: Users can ask questions about the document and get relevant answers with highlighted sections.

- Highlighting: Visually highlights the sections of the PDF that correspond to the answers, allowing for better comprehension.

- Chunking and Vector Store: Uses chunking and FAISS indexing for fast and accurate information retrieval.

## Project Structure

- env/: Python virtual environment files.

- highlighted/: Stores highlighted versions of the processed PDF documents.

- pdfjs/: Contains resources for rendering PDF documents in the web interface.

- build/: JavaScript and map files for handling PDFs.

- web/: Viewer resources such as HTML, CSS, and images.

- static/: Contains static resources like CSS, JavaScript, and images.

- templates/: HTML templates used for rendering the web pages.

- highlight.html: Template for viewing highlighted PDFs.

- index.html: Main page for uploading and interacting with PDFs.

- uploads/: Stores uploaded PDF files.

- vector_db/: Directory for storing vectorized data for quick retrieval.

- vector_store/: Stores data related to vector embeddings.

- .env: Environment variables such as API keys.

- app.py: Main Flask application for handling routes and API requests.

- pdf_highlighter.py: Script for processing PDFs and highlighting relevant sections.

- pdfjs-dist.zip: Compressed package for PDF.js used in the project.

## Requirements

- Python 3.8+

- Flask

- pdf2image

- openai

- PyMuPDF

- langchain

- langchain-community

- chromadb

- python-dotenv

## Setup Instructions

#### Clone the Repository

git clone <repository-url>
cd pdf_highlighter_Copy

#### Create Virtual Environment

python -m venv env
source env/bin/activate   # On Windows use `env\Scripts\activate`

#### Install Dependencies

pip install -r requirements.txt

#### Set Up Environment Variables

Create a .env file in the project root with the following content:

OPENAI_API_KEY=your_openai_api_key_here

#### Run the Application

flask run

#### Access the Web Interface

Open your browser and navigate to http://127.0.0.1:5000 to start using the application.

## Usage

#### Upload a PDF

On the main page, upload your PDF document.

#### Ask Queries

After uploading, use the provided interface to ask questions about the document.

#### View Highlights

The application will highlight relevant sections of the document that correspond to the answers.

## Technologies Used

- Flask: For serving the web application.

- OpenAI API: To provide intelligent responses to user queries.

- FAISS: For efficient similarity search and information retrieval.

- PyMuPDF: To extract and manipulate PDF content.

- pdf2image: Convert PDF pages to images for processing.

- Langchain: Text processing and chunking.

- PDF.js: To render PDFs in the browser for highlighting.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

Special thanks to the open-source community for providing the tools that make this project possible.

Inspired by the need for accessible and efficient document analysis tools.


