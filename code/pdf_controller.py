from pdf_handler import PDFHandler
from pdf_view import PDFView
import threading
class PDFController:
    def __init__(self):
        self.handler = PDFHandler()
        self.view = PDFView(self)
    
    def merge_pdfs(self):
        files = self.view.select_files()
        if files:
            output_path = self.view.select_output_path()
            if output_path:
                self.handler.merge_pdfs(files, output_path)
                self.view.update_message(f"Archivo PDF unido y guardado correctamente '{output_path}'")

    def open_split_pdf_window(self):
        self.view.open_split_pdf_window()

    def split_pdf(self, start_page, end_page, pdf_file, output_path):
        if start_page and end_page and output_path and pdf_file:
            self.handler.split_pdf(start_page, end_page, pdf_file, output_path)
            self.view.update_message(f"Archivo PDF separado y guardado correctamente '{output_path}'")
    def compress_pdf(self):
        input_pdf = self.view.select_files()[0]  # Selecciona un solo archivo para comprimir
        if input_pdf:
            output_path = self.view.select_output_path()
            if output_path:
                # Mostrar ventana de progreso en un hilo separado
                self.view.show_progress_window()
                threading.Thread(target=self.compress_pdf_thread, args=(input_pdf, output_path)).start()

    def compress_pdf_thread(self, input_pdf, output_path):
        self.handler.compress_pdf(input_pdf, output_path)
        self.view.progress_window.destroy()  # Cerrar la ventana de progreso
        self.view.update_message(f"Archivo PDF comprimido y guardado correctamente '{output_path}'")

    def run(self):
        self.view.run()

if __name__ == "__main__":
    controller = PDFController()
    controller.run()