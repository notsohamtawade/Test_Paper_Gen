import PyPDF2
import spacy
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import tkinter as tk
from tkinter import filedialog
from datetime import datetime  # Added import for timestamp

class QuestionPaperGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Question Paper Generator")

        # UI components
        self.label = tk.Label(root, text="Select PDF Files:")
        self.label.pack(pady=10)

        self.pdf_files_button = tk.Button(root, text="Browse", command=self.browse_pdf_files)
        self.pdf_files_button.pack(pady=10)

        self.chapter_label = tk.Label(root, text="Select Chapters:")
        self.chapter_label.pack(pady=10)

        self.chapter_entry = tk.Entry(root)
        self.chapter_entry.pack(pady=10)

        self.marks_label = tk.Label(root, text="Enter Total Marks:")
        self.marks_label.pack(pady=10)

        self.marks_entry = tk.Entry(root)
        self.marks_entry.pack(pady=10)

        self.generate_button = tk.Button(root, text="Generate Question Paper", command=self.generate_question_paper)
        self.generate_button.pack(pady=20)

        # Load spaCy English model
        self.nlp = spacy.load("en_core_web_sm")

    def browse_pdf_files(self):
        pdf_files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        self.pdf_files_button["text"] = ", ".join(pdf_files)
        self.pdf_files = pdf_files

    def extract_text_from_pdf(self, pdf_path):
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ''
            for page_number in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page_number].extract_text()
        return text

    def generate_question_paper(self):
        pdf_files = self.pdf_files
        chapters = self.chapter_entry.get().split(',')
        total_marks = self.marks_entry.get()

        # Iterate through each selected PDF file
        for pdf_path in pdf_files:
            text = self.extract_text_from_pdf(pdf_path)

            # Get meaningful sentences using spaCy
            sentences = self.get_meaningful_sentences(text)

            # Create PDF with subjective questions
            self.create_subjective_paper(sentences, chapters, total_marks)

    def get_meaningful_sentences(self, text):
        doc = self.nlp(text)
        meaningful_sentences = [sent.text for sent in doc.sents if len(sent.text.split()) > 5]
        return meaningful_sentences

    def create_subjective_paper(self, sentences, chapters, total_marks):
        # Create a unique PDF file name with a timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        output_pdf_path = f"output_subjective_paper_{timestamp}.pdf"

        c = canvas.Canvas(output_pdf_path, pagesize=letter)
        c.setFont("Helvetica", 12)

        # Add a title
        c.drawCentredString(300, 750, "Question Paper")

        # Add chapters
        c.drawRightString(550, 750, f"Chapters: {', '.join(chapters)}")

        # Add total marks
        c.drawRightString(550, 730, f"Total Marks: {total_marks}")

        # Add subjective questions to the PDF with serial numbers
        y_position = 700
        question_number = 1
        for sentence in sentences:
            question = f"{question_number}. Q: {sentence.strip()}?"
            c.drawString(50, y_position, question)
            y_position -= 30
            if y_position < 50:
                break  # Stop adding questions if the page is full
            question_number += 1

        # Save the PDF
        c.save()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuestionPaperGenerator(root)
    root.mainloop()
