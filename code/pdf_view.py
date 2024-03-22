import tkinter as tk
from tkinter import filedialog
import fitz
import os
from validations import Validation
import tkinter.ttk as ttk
class PDFView:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Operaciones con PDFs")
        self.root.geometry("800x600")
        self.menu_principal()

    def menu_principal(self):
        self.merge_button = tk.Button(self.root, text="Unir PDF", command=self.controller.merge_pdfs)
        self.merge_button.pack(side="top", fill="x", padx=10, pady=5)

        self.split_button = tk.Button(self.root, text="Separar PDF", command=self.open_split_pdf_window)
        self.split_button.pack(side="top", fill="x", padx=10, pady=5)
        self.compress_button = tk.Button(self.root, text="Comprimir PDF", command=self.controller.compress_pdf)
        self.compress_button.pack(side="top", fill="x", padx=10, pady=5)
        self.message_label = tk.Label(self.root, text="")
        self.message_label.pack(side="top", fill="x", padx=10, pady=5)
        

    def select_files(self):
        files = filedialog.askopenfilenames(title="Selecciona los archivos PDF", filetypes=[("Archivos PDF", ".pdf")])
        return files

    def select_output_path(self):
        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Archivos PDF", ".pdf")])
        return output_path

    def update_message(self, message):
        self.message_label.config(text=message)

    def open_split_pdf_window(self):
        self.root.withdraw()  # Oculta la ventana principal
        self.split_pdf_window = tk.Toplevel()  # Crea una nueva ventana secundaria
        self.split_pdf_window.title("Separar PDF")
        self.split_pdf_window.geometry("800x600")

        # Left frame for parameter inputs
        parameter_frame = tk.Frame(self.split_pdf_window)
        parameter_frame.pack(side="left", fill="both", padx=10, pady=10)

        # Right frame for PDF preview
        preview_frame = tk.Frame(self.split_pdf_window)
        preview_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.select_pdf_button = tk.Button(parameter_frame, text="Seleccione el PDF", command=self.select_and_show_preview)
        self.select_pdf_button.pack(side="top", fill="x", padx=10, pady=5)

        self.start_page_label = tk.Label(parameter_frame, text="Desde la página:")
        self.start_page_label.pack(side="top", fill="x", padx=10, pady=5)
        self.start_page_entry = tk.Entry(parameter_frame)
        self.start_page_entry.pack(side="top", fill="x", padx=10, pady=5)

        self.end_page_label = tk.Label(parameter_frame, text="Hasta la página:")
        self.end_page_label.pack(side="top", fill="x", padx=10, pady=5)
        self.end_page_entry = tk.Entry(parameter_frame)
        self.end_page_entry.pack(side="top", fill="x", padx=10, pady=5)

        self.split_button = tk.Button(parameter_frame, text="Separar", command=self.split_pdf)
        self.split_button.pack(side="top", fill="x", padx=10, pady=5)

        self.split_button = tk.Button(parameter_frame, text="Reregresar al menu", command=self.regresar_menu)
        self.split_button.pack(side="top", fill="x", padx=10, pady=5)
        # Canvas for PDF preview
        self.preview_canvas = tk.Canvas(preview_frame)
        self.preview_canvas.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        self.preview_canvas.bind("<MouseWheel>", self.scroll_with_mouse_wheel)  # Vincular evento de la rueda del ratón
        self.preview_canvas.bind("<Up>", lambda event: self.preview_canvas.yview_scroll(-1, "units"))  # Vincular flecha hacia arriba
        self.preview_canvas.bind("<Down>", lambda event: self.preview_canvas.yview_scroll(1, "units"))  # Vincular flecha hacia abajo
        self.preview_canvas.bind("<Left>", lambda event: self.preview_canvas.xview_scroll(-1, "units"))  # Vincular flecha hacia la izquierda
        self.preview_canvas.bind("<Right>", lambda event: self.preview_canvas.xview_scroll(1, "units"))  # Vincular flecha hacia la derecha
    

        # Scrollbars for canvas
        self.scrollbar_vertical = tk.Scrollbar(preview_frame, orient=tk.VERTICAL)
        self.scrollbar_vertical.pack(side="right", fill="y")
        self.scrollbar_vertical.config(command=self.preview_canvas.yview)

        self.scrollbar_horizontal = tk.Scrollbar(preview_frame, orient=tk.HORIZONTAL)
        self.scrollbar_horizontal.pack(side="bottom", fill="x")
        self.scrollbar_horizontal.config(command=self.preview_canvas.xview)

        self.preview_canvas.config(yscrollcommand=self.scrollbar_vertical.set, xscrollcommand=self.scrollbar_horizontal.set)

        # Labels for displaying information
        self.page_count_label = tk.Label(preview_frame, text="", anchor="w")
        self.page_count_label.pack(side="bottom", fill="x", padx=10, pady=5)

        self.file_size_label = tk.Label(preview_frame, text="", anchor="w")
        self.file_size_label.pack(side="bottom", fill="x", padx=10, pady=5)
        self.file_info_label = tk.Label(preview_frame, text="", anchor="w")
        self.file_info_label.pack(side="bottom", fill="x", padx=10, pady=5)
    def regresar_menu(self):
        self.split_pdf_window.destroy()  # Cierra la ventana secundaria
        self.root.deiconify()  # Muestra la ventana principal nuevamente
        self.__init__
    def scroll_with_mouse_wheel(self, event):
        if event.delta:
            self.preview_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    def select_and_show_preview(self):
        file_path = filedialog.askopenfilename(title="Seleccionar archivo PDF", filetypes=[("Archivos PDF", ".pdf")])
        if file_path:
            self.selected_pdf = file_path
            self.show_preview(file_path)
    def show_preview(self, pdf_path):
        # Clear previous preview
        self.preview_canvas.delete("all")

        # Open PDF
        doc = fitz.open(pdf_path)
        
        # Render each page and calculate total height
        total_height = 0
        rendered_images = []
        for i, page in enumerate(doc):
            pix = page.get_pixmap(alpha=False)
            img = tk.PhotoImage(data=pix.tobytes("ppm"))

            # Calculate the scale factor to fit the image onto the canvas
            scale_factor = min(self.preview_canvas.winfo_width() / pix.width, self.preview_canvas.winfo_height() / pix.height)

            # Rescale the image
            img = img.subsample(int(1/scale_factor), int(1/scale_factor))

            # Calculate total height including the height of the scaled image
            image_id = self.preview_canvas.create_image(0, total_height, anchor="nw", image=img, tags=("pdf_page",))
            rendered_images.append((img, page))

            # Add page number label
            # Add page number label with background
            text_id = self.preview_canvas.create_text(10, total_height + 10, anchor="nw", text=f"Página {i+1}", fill="orange")

            # Get the bounding box of the text
            x0, y0, x1, y1 = self.preview_canvas.bbox(text_id)

            # Create a rectangle with the same coordinates as the text bounding box
            self.preview_canvas.create_rectangle(x0-2, y0-2, x1+2, y1+2, fill="black")

            # Raise the text to be above the rectangle
            self.preview_canvas.tag_raise(text_id)


            
            total_height += img.height()

        # Store a reference to the rendered images to prevent them from being garbage collected
        self.rendered_images = rendered_images

        # Adjust canvas scrolling region
        self.preview_canvas.config(scrollregion=(0, 0, pix.width, total_height))

        # Configure scrollbars
        self.scrollbar_vertical.config(command=self.preview_canvas.yview)
        self.scrollbar_horizontal.config(command=self.preview_canvas.xview)

        # Update page count and file size labels
        self.page_count_label.config(text=f"Número de páginas: {len(doc)}")
        file_size = os.path.getsize(pdf_path) / (1024 * 1024)  # Convert file size to MB
        self.file_size_label.config(text=f"Tamaño del archivo: {file_size:.2f} MB")
        file_name = os.path.basename(pdf_path)
        self.file_info_label.config(text=f"Archivo: {file_name}")
    def split_pdf(self):
        start_page = self.start_page_entry.get()
        end_page = self.end_page_entry.get()
        
        if Validation.is_empty(start_page, "Desde la página") or Validation.is_empty(end_page, "Hasta la página"):
            return
        
        total_pages = len(self.rendered_images)  # Suponiendo que rendered_images contiene todas las páginas del PDF
        if not Validation.validate_page_numbers(start_page, end_page, total_pages):
            return
        
        output_path = self.select_output_path()
        if start_page and end_page and output_path and hasattr(self, 'selected_pdf'):
            self.controller.split_pdf(start_page, end_page, self.selected_pdf, output_path)
            self.update_message(f"Archivo PDF separado y guardado correctamente en '{output_path}'")

    
    def show_progress_window(self):
        self.progress_window = tk.Toplevel()
        self.progress_window.title("Progreso")
        self.progress_window.geometry("300x100")
        
        self.progress_label = tk.Label(self.progress_window, text="Comprimiendo archivo...")
        self.progress_label.pack(pady=20)
        
        self.progress_bar = ttk.Progressbar(self.progress_window, orient="horizontal", length=200, mode="indeterminate")
        self.progress_bar.pack(pady=10)
        self.progress_bar.start(10)  # Iniciar la barra de progreso indeterminada
        
    def run(self):
        self.root.mainloop()

    