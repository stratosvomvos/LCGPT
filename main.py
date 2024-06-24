import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QDialog, QLineEdit, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from langchain.prompts import PromptTemplate
from langchain_community.llms import LlamaCpp

template = """
<<SYS>>
you are a helpful assistant that gives short and simple answers.
<</SYS>>

{text}
"""

class AboutWindow(QDialog):
    """
    About Window
    
    This window displays information about the application.
    """
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("About Yaps Lock")
        self.setStyleSheet("background-color: #1e90ff; color: #fff;")
        
        about_text = "Yap Lock\n\nCreated by Stratosvomvos\n\nPowered by LlamaCPP and LangChain"
        self.about_label = QLabel(about_text)
        self.about_label.setAlignment(Qt.AlignCenter)
        self.about_label.setStyleSheet("font-size: 16px; color: #fff;")
        
        layout = QVBoxLayout()
        layout.addWidget(self.about_label)
        self.setLayout(layout)

class YapLock(QWidget):
    """
    Yap Lock Application
    
    This application allows the user to input a prompt and generates text using LlamaCPP API.
    """
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Yaps Lock")
        self.setStyleSheet("background-color: #000;")
        
        self.banner_label = QLabel()
        self.banner_label.setAlignment(Qt.AlignCenter)
        
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setStyleSheet("font-size: 18px; color: #fff; background-color: rgba(255, 255, 255, 0.8); border: 2px solid #ccc; border-radius: 8px; padding: 20px;")
        
        self.prompt_input = QLineEdit()
        self.prompt_input.setPlaceholderText("Enter your prompt here...")
        self.prompt_input.setStyleSheet("font-size: 18px; color: #000; background-color: #fff; border: 2px solid #ccc; border-radius: 8px; padding: 10px;")
        
        self.generate_button = QPushButton("Yap!")
        self.generate_button.clicked.connect(self.generate_text)
        self.generate_button.setStyleSheet("background-color: #1e90ff; color: #fff; border: 1px solid #1e90ff; border-radius: 5px; padding: 5px 10px;")
        
        self.about_button = QPushButton("About")
        self.about_button.clicked.connect(self.show_about_window)
        self.about_button.setStyleSheet("background-color: #1e90ff; color: #fff; border: 1px solid #1e90ff; border-radius: 5px; padding: 5px 10px;")
        
        layout = QVBoxLayout()
        layout.addWidget(self.banner_label)
        layout.addWidget(self.prompt_input)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.output_area)
        layout.addWidget(self.about_button, alignment=Qt.AlignRight)
        self.setLayout(layout)
        
        self.set_banner()

        self.model_path = "models/silibot.gguf"  # Ensure this path is correct
        self.llm = LlamaCpp(
            model_path=self.model_path,
            temperature=0.5,
            max_tokens=500,
            top_p=1.0
        )

    def set_banner(self):
        """
        Set an image banner above the text area.
        """
        pixmap = QPixmap("banner_image.png")  # Replace "banner_image.png" with the path to your image
        self.banner_label.setPixmap(pixmap)
    
    def generate_text(self):
        """
        Generate text using the LlamaCPP API with the user-specified prompt.
        """
        # Get the user-specified prompt
        prompt_text = self.prompt_input.text()
        
        if prompt_text.strip() == "":
            self.output_area.setPlainText("Please enter a prompt.")
            return
        
        # Create the prompt template
        prompt = PromptTemplate(input_variables=["text"], template=template)
        
        # Format the prompt
        formatted_prompt = prompt.format(text=prompt_text)
        
        # Generate the text
        generated_text = self.llm.invoke(formatted_prompt)
        
        # Clean the generated text
        clean_text = self.clean_generated_text(generated_text)
        
        self.output_area.setPlainText(clean_text)
    
    def clean_generated_text(self, text):
        """
        Clean the generated text by removing any unwanted prefixes or template-related text.
        """
        # Strip the assistant prefix and any other template text
        clean_text = text.replace("<<SYS>>", "").replace("<<</SYS>>", "").strip()
        return clean_text
    
    def show_about_window(self):
        """
        Show the About window.
        """
        about_window = AboutWindow()
        about_window.exec_()
        self.setFocus()  # Set focus back to the main window when the About window is closed

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YapLock()
    window.show()
    sys.exit(app.exec_())
