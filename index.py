import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import json
import math
import graphviz
import tkinter.messagebox as messagebox

class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Analizador de Operaciones")
        self.window.geometry("800x600")
        self.setup_navbar()
        self.setup_text_area()
        self.errors = []
        self.file_path = None 
        self.operacion = "" 
        self.error_count = 0
        self.results = []

    def setup_navbar(self):
        # Navbar
        navbar = ttk.Frame(self.window, style="Navbar.TFrame")
        navbar.pack(fill=tk.X)
        # Estilo para la Navbar
        self.window.tk_setPalette(background="blue")  
        self.window.option_add("*TButton*background", "black")  
        self.window.option_add("*TButton*foreground", "white")  
        self.window.option_add("*TCombobox*background", "white")  
        self.window.option_add("*TCombobox*foreground", "black")  
        # Menú Archivo
        archivo_menu = ttk.Combobox(navbar, values=["Abrir", "Guardar", "Guardar como", "Salir"], style="Navbar.TCombobox")
        archivo_menu.set("Archivo")
        archivo_menu.pack(side=tk.LEFT, padx=10)
        archivo_menu.bind("<<ComboboxSelected>>", self.handle_file_menu)
        # Botones de Acción
        analyze_button = ttk.Button(navbar, text="Analizar", command=self.analyze, style="Navbar.TButton")
        analyze_button.pack(side=tk.LEFT, padx=10)
        errors_button = ttk.Button(navbar, text="Errores", command=self.show_errors, style="Navbar.TButton")
        errors_button.pack(side=tk.LEFT, padx=10)
        report_button = ttk.Button(navbar, text=" Reporte", command=self.generate_graphs, style="Navbar.TButton")
        report_button.pack(side=tk.LEFT, padx=10)
        # Estilo para el Combobox en Navbar
        self.window.style = ttk.Style()
        self.window.style.configure("Navbar.TCombobox", background="white", foreground="black")

    def setup_text_area(self):
        self.text_area = tk.Text(self.window, bg="black", fg="white") 
        self.text_area.pack(fill=tk.BOTH, expand=True)

    def handle_file_menu(self, event):
        option = event.widget.get()
        if option == "Abrir":
            self.load_file()
        elif option == "Guardar":
            self.save_file()
        elif option == "Guardar como":
            self.save_file_as()
        elif option == "Salir":
            self.window.quit()

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            self.file_path = file_path
            with open(file_path, "r") as file:
                content = file.read()
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert(tk.END, content)

    def save_file(self):
        if self.file_path:
            content = self.text_area.get("1.0", tk.END)
            with open(self.file_path, "w") as file:
                file.write(content)
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if file_path:
            self.file_path = file_path
            self.save_file()

    def analyze_and_show_results(self):
        self.errors = []
        self.results = []
        content = self.text_area.get("1.0", tk.END)
        try:
            data = json.loads(content)
            if "operaciones" in data:
                operaciones = data["operaciones"]
                for i, operacion in enumerate(operaciones):
                    if "operacion" in operacion:
                        resultado = self.analyze_operation(operacion)
                        if resultado is not None:
                            self.results.append({"operacion": operacion, "resultado": resultado})
                        else:
                            self.errors.append(f"Error en operación {i + 1}: Resultado no válido")
                    else:
                        self.errors.append(f"Error en operación {i + 1}: Falta la clave 'operacion'")
        except json.JSONDecodeError as e:
            self.errors.append(f"Error en el formato del JSON: {e}")

        if self.errors:
            self.show_generic_error()
        else:
            self.show_results()

    def analyze(self):
        self.analyze_and_show_results()

    def show_results(self):
        if self.results:
            result_message = "\n".join([f"Operación {i + 1}: {result['resultado']:.2f}" for i, result in enumerate(self.results)])
            messagebox.showinfo("Resultados", result_message)
        else:
            messagebox.showinfo("Resultados", "No hay resultados para mostrar.")

    def show_generic_error(self):
        tk.messagebox.showerror("Error", "Se encontraron errores en las operaciones. Haga clic en 'Errores' para ver detalles.")

    def show_errors(self):
        error_message = "\n".join(self.errors)

        error_data = {
            "errores": []
        }
        for i, error in enumerate(self.errors):
            error_data["errores"].append({
                "No": i + 1,
                "descripcion": {
                    "Lexema": error,
                    "tipo": "error lexico",
                    "columna": 0,
                    "fila": 0
                }
            })
        error_file_path = "Errores.json" 
        with open(error_file_path, "w") as error_file:
            json.dump(error_data, error_file, indent=4)

        messagebox.showerror("Errores", error_message)
        messagebox.showinfo("Archivo de errores generado", f"Se ha generado el archivo de errores: {error_file_path}")

    def analyze_operation(self, operacion):
        if operacion["operacion"] == "suma":
            return self.suma(operacion)
        elif operacion["operacion"] == "resta":
            return self.resta(operacion)
        elif operacion["operacion"] == "multiplicacion":
            return self.multiplicacion(operacion)
        elif operacion["operacion"] == "division":
            return self.division(operacion)
        elif operacion["operacion"] == "potencia":
            return self.potencia(operacion)
        elif operacion["operacion"] == "raiz":
            return self.raiz(operacion)
        elif operacion["operacion"] == "inverso":
            return self.inverso(operacion)
        elif operacion["operacion"] == "seno":
            return self.seno(operacion)
        elif operacion["operacion"] == "coseno":
            return self.coseno(operacion)
        elif operacion["operacion"] == "tangente":
            return self.tangente(operacion)
        elif operacion["operacion"] == "modulo":
            return self.modulo(operacion)
        else:
            return None

    def suma(self, operacion):
        valor1 = self.obtener_valor(operacion.get("Valor1", operacion.get("valor1")))
        valor2 = self.obtener_valor(operacion.get("Valor2", operacion.get("valor2")))
        if valor1 is not None and valor2 is not None:
            return valor1 + valor2
        return None

    def resta(self, operacion):
        valor1 = self.obtener_valor(operacion.get("Valor1", operacion.get("valor1")))
        valor2 = self.obtener_valor(operacion.get("Valor2", operacion.get("valor2")))
        if valor1 is not None and valor2 is not None:
            return valor1 - valor2
        return None

    def multiplicacion(self, operacion):
        valor1 = self.obtener_valor(operacion.get("Valor1", operacion.get("valor1")))
        valor2 = self.obtener_valor(operacion.get("Valor2", operacion.get("valor2")))
        if valor1 is not None and valor2 is not None:
            return valor1 * valor2
        return None

    def division(self, operacion):
        valor1 = self.obtener_valor(operacion.get("Valor1", operacion.get("valor1")))
        valor2 = self.obtener_valor(operacion.get("Valor2", operacion.get("valor2")))
        if valor1 is not None and valor2 is not None:
            if valor2 != 0:
                return valor1 / valor2
            else:
                self.errors.append("Error de división por cero")
        return None

    def potencia(self, operacion):
        valor1 = self.obtener_valor(operacion.get("Valor1", operacion.get("valor1")))
        valor2 = self.obtener_valor(operacion.get("Valor2", operacion.get("valor2")))
        if valor1 is not None and valor2 is not None:
            resultado = math.pow(valor1, valor2)
            return resultado
        return None

    def raiz(self, operacion):
        valor1 = self.obtener_valor(operacion.get("Valor1", operacion.get("valor1")))
        valor2 = self.obtener_valor(operacion.get("Valor2", operacion.get("valor2")))
        if valor1 is not None and valor2 is not None:
            resultado = valor1 ** (1 / valor2)
            return resultado
        return None

    def inverso(self, operacion):
        valor1 = self.obtener_valor(operacion.get("Valor1", operacion.get("valor1")))
        if valor1 is not None:
            if valor1 != 0:
                resultado = 1 / valor1
                return resultado
            else:
                self.errors.append("Error de inverso: división por cero")
        return None

    def seno(self, operacion):
        valor1 = self.obtener_valor(operacion.get("Valor1", operacion.get("valor1")))
        if valor1 is not None:
            resultado = math.sin(math.radians(valor1))
            return resultado
        return None

    def coseno(self, operacion):
        valor1 = self.obtener_valor(operacion.get("Valor1", operacion.get("valor1")))
        if valor1 is not None:
            resultado = math.cos(math.radians(valor1))
            return resultado
        return None

    def tangente(self, operacion):
        valor1 = self.obtener_valor(operacion.get("Valor1", operacion.get("valor1")))
        if valor1 is not None:
            resultado = math.tan(math.radians(valor1))
            return resultado
        return None

    def modulo(self, operacion):
        valor1 = self.obtener_valor(operacion.get("Valor1", operacion.get("valor1")))
        valor2 = self.obtener_valor(operacion.get("Valor2", operacion.get("valor2")))
        if valor1 is not None and valor2 is not None:
            if valor2 != 0:
                resultado = valor1 % valor2
                return resultado
            else:
                self.errors.append("Error de módulo: división por cero")
        return None

    def obtener_valor(self, valor):
        if isinstance(valor, (int, float)):
            return valor
        elif isinstance(valor, list):
            if len(valor) == 1:
                return self.obtener_valor(valor[0])
            else:
                resultados = []
                for item in valor:
                    resultado = self.obtener_valor(item)
                    if resultado is not None:
                        resultados.append(resultado)
                return resultados
        elif isinstance(valor, dict) and "operacion" in valor:
            operacion = valor["operacion"]
            if operacion == "suma":
                return self.suma(valor)
            elif operacion == "resta":
                return self.resta(valor)
            elif operacion == "multiplicacion":
                return self.multiplicacion(valor)
            elif operacion == "division":
                return self.division(valor)
            elif operacion == "potencia":
                return self.potencia(valor)
            elif operacion == "raiz":
                return self.raiz(valor)
            elif operacion == "inverso":
                return self.inverso(valor)
            elif operacion == "seno":
                return self.seno(valor)
            elif operacion == "coseno":
                return self.coseno(valor)
            elif operacion == "tangente":
                return self.tangente(valor)
            elif operacion == "modulo":
                return self.modulo(valor)
        else:
            self.errors.append(f"Valor no válido: {valor}")
            return None

    def generate_report(self):
        pass

    def generate_graphs(self):
        def create_operation_graph(graph, operacion, parent_index, parent_node_name, configuracion):
            operacion_data = operacion["operacion"]
            resultado = self.analyze_operation(operacion)

            operacion_node_name = f"Operacion_{parent_index}_{operacion_data}"
            resultado_node_name = f"Resultado_{parent_index}_{operacion_data}"

            valor1 = self.obtener_valor(operacion.get("Valor1", operacion.get("valor1")))
            valor2 = self.obtener_valor(operacion.get("Valor2", operacion.get("valor2")))

            operacion_label = f"Operación {parent_index + 1}\nTipo: {operacion_data}\n"
            if valor1 is not None:
                operacion_label += f"Valor1: {valor1}\n"
            if valor2 is not None:
                operacion_label += f"Valor2: {valor2}\n"
            operacion_label += f"Resultado: {resultado:.2f}"

            graph.node(operacion_node_name, operacion_label)

            graph.edge(operacion_node_name, resultado_node_name)

            nodo_color = configuracion.get("color-fondo-nodo", "yellow")
            nodo_fuente_color = configuracion.get("color-fuente-nodo", "black")
            nodo_forma = configuracion.get("forma-nodo", "circle")

            graph.node(operacion_node_name, style="filled", fillcolor=nodo_color, fontcolor=nodo_fuente_color, shape=nodo_forma)

            if "operaciones" in operacion:
                subgraph = graph.subgraph(name=f"cluster_{operacion_node_name}")
                subgraph.attr(label="")
                for i, nested_operacion in enumerate(operacion["operaciones"]):
                    create_operation_graph(subgraph, nested_operacion, i, operacion_node_name, configuracion)

        main_graph = graphviz.Digraph(format='png')

        content = self.text_area.get("1.0", tk.END)
        try:
            data = json.loads(content)
            if "operaciones" in data:
                for i, operacion in enumerate(data["operaciones"]):
                    if "operacion" in operacion:
                        operacion_data = operacion["operacion"]
                        if isinstance(operacion_data, str):
                            configuracion = operacion.get("configuracion", {}) 
                            create_operation_graph(main_graph, operacion, i, f"Operacion_{i}", configuracion)

                graph_path = "graph.png"
                main_graph.render(filename=graph_path, directory='graphs', cleanup=True)

                tk.messagebox.showinfo("Reporte generado", "Se ha generado el informe en la carpeta 'graphs', " , f"Los gráficos se han generado en el archivo {graph_path}")
        except json.JSONDecodeError as e:
            print("Error al analizar el JSON:", e)


    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    gui = GUI()
    gui.run()
