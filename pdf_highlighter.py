import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog

def select_pdf():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(title="Select PDF File", filetypes=[("PDF Files", "*.pdf")])
    return file_path

def highlight_sentence(pdf_path, sentence):
    # Open the PDF
    doc = fitz.open(pdf_path)
    
    # Iterate through the pages to search for the sentence
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text_instances = page.search_for(sentence)
        
        # Highlight each occurrence of the sentence
        for inst in text_instances:
            page.add_highlight_annot(inst)
    
    # Save the new PDF with highlights
    highlighted_pdf_path = pdf_path.replace('.pdf', '_highlighted.pdf')
    doc.save(highlighted_pdf_path)
    doc.close()
    
    print(f"Highlighted PDF saved as: {highlighted_pdf_path}")

if __name__ == "__main__":
    # Step 1: Select PDF File
    pdf_file = select_pdf()
    
    if not pdf_file:
        print("No PDF file selected. Exiting.")
    else:
        # Step 2: Enter Sentence to Highlight
        sentence_to_find = input("Enter the sentence you want to highlight in the PDF: ")

        # Step 3: Highlight the Sentence
        highlight_sentence(pdf_file, sentence_to_find)

