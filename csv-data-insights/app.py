from modules.data_handler import DataHandler
from modules.model_handler import ModelHandler
from modules.visualization import Visualizer
from modules.pdf_generator import PDFGenerator
from modules.ui import GradioUI

def main():
    
    data_handler = DataHandler()
    model_handler = ModelHandler(model_name="llama3:8b")
    visualizer = Visualizer()
    pdf_generator = PDFGenerator()
    
    
    ui = GradioUI(data_handler, model_handler, visualizer, pdf_generator)
    app = ui.build_interface()
    app.launch()

if __name__ == "__main__":
    main()