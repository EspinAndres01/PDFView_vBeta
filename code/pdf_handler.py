import PyPDF2
import pypdfium2 as pdfium
from pathlib import Path
import img2pdf
import os
from PIL import Image
class PDFHandler:
    def __init__(self):
        self.pdf_writer = PyPDF2.PdfWriter()

    def merge_pdfs(self, file_paths, output_path):
        pdf_writer = PyPDF2.PdfWriter()
        for file_path in file_paths:
            with open(file_path, "rb") as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                for page in pdf_reader.pages:
                    pdf_writer.add_page(page)
        with open(output_path, "wb") as output_pdf:
            pdf_writer.write(output_pdf)

    def split_pdf(self, start_page, end_page, pdf_file, output_path):
        with open(pdf_file, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            pdf_writer = PyPDF2.PdfWriter()
            for page_number in range(int(start_page) - 1, int(end_page)):
                pdf_writer.add_page(pdf_reader.pages[page_number])
            with open(output_path, "wb") as output_pdf:
                pdf_writer.write(output_pdf)
    
    def compress_pdf(self, input_pdf, output_pdf, scale=2, quality=1):
        nombre_pdf_sin_extension = Path(input_pdf).stem
        pdf = pdfium.PdfDocument(input_pdf)
        cantidad_paginas = len(pdf)
        imagenes = []

        # Extraer cada página del PDF como imagen
        for indice_pagina in range(cantidad_paginas):
            numero_pagina = indice_pagina + 1
            nombre_imagen = f"{nombre_pdf_sin_extension}_{numero_pagina}.jpg"
            imagenes.append(nombre_imagen)
            print(f"Extrayendo página {numero_pagina} de {cantidad_paginas}")
            pagina = pdf.get_page(indice_pagina)
            imagen_para_pil = pagina.render(scale=scale).to_pil()
            imagen_para_pil.save(nombre_imagen)

        imagenes_comprimidas = []

        # Comprimir imágenes
        for nombre_imagen in imagenes:
            print(f"Comprimiendo {nombre_imagen}...")
            nombre_imagen_sin_extension = Path(nombre_imagen).stem
            nombre_imagen_salida = nombre_imagen_sin_extension + \
                "_comprimida" + nombre_imagen[nombre_imagen.rfind("."):]
            imagen = Image.open(nombre_imagen)
            imagen.save(nombre_imagen_salida, optimize=True, quality=quality)
            imagenes_comprimidas.append(nombre_imagen_salida)

        # Escribir imágenes en un nuevo PDF
        print("Creando PDF comprimido...")
        with open(output_pdf, "wb") as documento:
            documento.write(img2pdf.convert(imagenes_comprimidas))

        # Eliminar imágenes temporales
        for imagen in imagenes + imagenes_comprimidas:
            os.remove(imagen)