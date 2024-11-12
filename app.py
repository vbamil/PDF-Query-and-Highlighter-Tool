import os
import fitz  # PyMuPDF
from flask import Flask, render_template, request, send_from_directory, jsonify
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_openai import OpenAI
from langchain.chains import RetrievalQA
from langchain_community.callbacks.manager import get_openai_callback

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
HIGHLIGHTED_FOLDER = 'highlighted'
VECTOR_DB_FOLDER = 'vector_db'
STATIC_FOLDER = 'static'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['HIGHLIGHTED_FOLDER'] = HIGHLIGHTED_FOLDER
app.config['VECTOR_DB_FOLDER'] = VECTOR_DB_FOLDER

# Ensure necessary folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(HIGHLIGHTED_FOLDER, exist_ok=True)
os.makedirs(VECTOR_DB_FOLDER, exist_ok=True)

# Set up vector DB and embedding function
openai_api_key = os.getenv("OPENAI_API_KEY")
embedding_function = OpenAIEmbeddings(openai_api_key=openai_api_key)
vector_store = Chroma(persist_directory=VECTOR_DB_FOLDER, embedding_function=embedding_function)

@app.route('/')
def index():
    return render_template('highlight.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Load the document into vector DB
    loader = PyMuPDFLoader(file_path)
    documents = loader.load()
    vector_store.add_documents(documents)

    return render_template('highlight.html', filename=file.filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/highlighted/<filename>')
def highlighted_file(filename):
    return send_from_directory(app.config['HIGHLIGHTED_FOLDER'], filename)

@app.route('/ask_question', methods=['POST'])
def ask_question():
    question = request.form['question']
    filename = request.form['filename']

    # Use LangChain to get an answer from the vector store
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(openai_api_key=openai_api_key),
        retriever=retriever
    )

    # Use a callback to get the metadata of retrieved chunks
    with get_openai_callback() as cb:
        response = qa.run(question)

    # Get the documents that were retrieved
    retrieved_docs = retriever.get_relevant_documents(question)
    retrieved_chunks = [{"content": doc.page_content, "metadata": doc.metadata} for doc in retrieved_docs]

    # Highlight retrieved chunks in the PDF
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    highlighted_pdf_path = os.path.join(app.config['HIGHLIGHTED_FOLDER'], filename.replace('.pdf', '_highlighted_from_chunks.pdf'))

    doc = fitz.open(pdf_path)
    highlighted = False
    highlighted_pages = []

    for chunk in retrieved_chunks:
        content = chunk["content"]
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text_instances = page.search_for(content)
            if text_instances:
                highlighted = True
                highlighted_pages.append(page_num + 1)  # PDF pages are 1-indexed

                for inst in text_instances:
                    page.add_highlight_annot(inst)

    # Save the highlighted PDF
    doc.save(highlighted_pdf_path)
    doc.close()

    if highlighted:
        return jsonify(answer=response, chunks=retrieved_chunks, highlightedPages=highlighted_pages, new_pdf=highlighted_pdf_path)
    else:
        return jsonify(answer=response, chunks=retrieved_chunks)

if __name__ == '__main__':
    app.run(debug=True)