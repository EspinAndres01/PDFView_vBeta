import tkinter as tk
from tkinter import messagebox

class Validation:

    @staticmethod
    def is_empty(value, field_name):
        if not value:
            Validation.show_error_message(f"El campo '{field_name}' no puede estar vacío.")
            return True
        return False

    @staticmethod
    def validate_page_numbers(start_page, end_page, total_pages):
        try:
            start_page = int(start_page)
            end_page = int(end_page)
        except ValueError:
            Validation.show_error_message("Los campos de página deben ser números enteros.")
            return False

        if start_page <= 0 or end_page <= 0 or start_page > total_pages or end_page > total_pages:
            Validation.show_error_message(f"Los números de página deben estar entre 1 y {total_pages}.")
            return False

        if start_page > end_page:
            Validation.show_error_message("La página de inicio debe ser menor o igual a la página de fin.")
            return False

        return True

    @staticmethod
    def show_error_message(message):
        messagebox.showerror("Error", message)
