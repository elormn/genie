import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
from tkinter import ttk
import math
from typing import List, Dict, Union, Tuple
from PIL import Image, ImageTk


class PlateCalculator:
    def __init__(self, plates_per_calculation: int = 28, multiplier: int = 3):
        self.plates_per_calculation = plates_per_calculation
        self.multiplier = multiplier
    
    def parse_combos(self, combo_drugs: List[str]) -> List[Tuple[str, ...]]:
        parsed = []
        for combo_str in combo_drugs:
            if not combo_str or combo_str.strip() == "" or str(combo_str).lower() in ['nan', 'none', 'null']:
                continue
            drugs = [drug.strip() for drug in str(combo_str).split("+") if drug.strip()]
            if drugs:
                parsed.append(tuple(sorted(drugs)))
        return parsed

    def calculate_plates(self, combo_drugs: List[str]) -> Dict[str, Union[int, float]]:
        combos = self.parse_combos(combo_drugs)
        if not combos:
            return {
                "singles": 0,
                "unique_constituent_drugs": 0,
                "total_combos": 0,
                "raw_result": 0.0,
                "final_result": 0,
                "error": "No valid combinations found"
            }

        single_count = sum(1 for combo in combos if len(combo) == 1)
        unique_constituent_drugs = []
        seen_drugs = set()
        for combo in combos:
            for drug in combo:
                if drug not in seen_drugs:
                    unique_constituent_drugs.append(drug)
                    seen_drugs.add(drug)
        unique_constituent_count = len(unique_constituent_drugs)
        total_combos = len(combos)
        raw_result = (unique_constituent_count + single_count + total_combos) / self.plates_per_calculation * self.multiplier
        final_result = math.ceil(raw_result)

        return {
            "singles": single_count,
            "unique_constituent_drugs": unique_constituent_count,
            "total_combos": total_combos,
            "raw_result": raw_result,
            "final_result": final_result
        }

# ---------- GUI ----------
class PlateCalculatorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("DiaMOND Genie 🧞‍♀️")
        self.root.geometry("900x750")
        
        # genie icon
        genie_icon = Image.open("/Users/eninsi01/Documents/DiaMOND/scripts/genie.png")   # keep this in same folder as script
        genie_image = ImageTk.PhotoImage(genie_icon)
        self.root.iconphoto(True, genie_image)

        # color scheme
        self.colors = {
            'background_main': "#E1D8F4",
            'background_secondary': "#E1D8F4",
            'background_dark': "#943BE8",
            'text_dark': "#943BE8",
            'text_light': "#2E2C2C",
            'accent': "#943BE8",
            'success': "#18C641",
            'error': "#DC143C"
        }
        self.root.configure(background=self.colors['background_main'])

        # ---------- VARIABLES ----------
        self.calculation_status = tk.StringVar(value="Ready to calculate No. of plates!")
        self.plates_per_calc = tk.StringVar(value="28")
        self.multiplier = tk.StringVar(value="3")

        # ---------- CALCULATOR ----------
        self.calculator = PlateCalculator()

        # ---------- STYLE ----------
        self.style = ttk.Style()
        self.setup_styles()

        # ---------- SETUP UI ----------
        self.setup_ui()

    # ---------- STYLE SETUP ----------
    def setup_styles(self):
        # General Frame
        self.style.configure("Custom.TFrame", background=self.colors['background_secondary'])

        # Notebook
        self.style.configure("Custom.TNotebook", background=self.colors['background_main'])
        self.style.configure("Custom.TNotebook.Tab", background=self.colors['background_secondary'], foreground=self.colors['text_dark'], font=("San Francisco", 11, "bold"))
        # Buttons
        self.style.configure("Accent.TButton", background=self.colors['accent'], foreground=self.colors['text_light'], font=("San Francisco", 12, "bold"), padding=5)
        self.style.map("Accent.TButton",
                       foreground=[('active', self.colors['text_light'])],
                       background=[('active', self.colors['background_dark'])])
        self.style.configure("Success.TButton", background=self.colors['success'], foreground=self.colors['text_light'], font=("San Francisco", 11, "bold"), padding=5)
        self.style.map("Success.TButton",
                       background=[('active', self.colors['accent'])])
        # Labels
        self.style.configure("Custom.TLabel", background=self.colors['background_secondary'], foreground=self.colors['text_dark'], font=("San Francisco", 12, "bold"))

    # ---------- UI SETUP ----------
    def setup_ui(self):
        self.notebook = ttk.Notebook(self.root, style="Custom.TNotebook")
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)

        self.create_manual_tab()
        self.create_unique_drugs_tab()
    
    # function to clear all entries
    def clear_all(self):
        # Clear manual input
        self.manual_text.delete(1.0, tk.END)
        # Clear unique drugs input
        self.unique_drugs_text.delete(1.0, tk.END)
        # Clear unique drugs listbox
        self.unique_drugs_listbox.delete(0, tk.END)
        # Reset count label
        self.unique_count_label.config(text="Total constituent drugs: 0")
        # Reset status
        self.calculation_status.set("Ready to calculate No. of plates!")

    

    # function to creat text section for manually entering drug combinations
    def create_manual_tab(self):
        manual_frame = ttk.Frame(self.notebook, style="Custom.TFrame")
        self.notebook.add(manual_frame, text="Plate Calculator")

        input_frame = ttk.Frame(manual_frame, style="Custom.TFrame")
        input_frame.pack(fill='both', expand=True, padx=10, pady=10)

        label = ttk.Label(input_frame, text="Drug Combinations:", style="Custom.TLabel")
        label.pack(anchor='w', pady=(0,5))

        self.manual_text = scrolledtext.ScrolledText(
            input_frame, height=15, wrap=tk.WORD,
            font=("San Francisco", 10), background='white', foreground='black', insertbackground='black'
        )
        self.manual_text.pack(fill='both', expand=True)

        calc_button = ttk.Button(input_frame, text="Calculate no. of plates", command=self.calculate_manual, style="Accent.TButton")
        calc_button.pack(pady=10)
        clear_button = ttk.Button(input_frame, text="Clear All", command=self.clear_all, style="Accent.TButton")
        clear_button.pack(pady=5)



    # ---------- UNIQUE DRUGS TAB ----------
    def create_unique_drugs_tab(self):
        unique_frame = ttk.Frame(self.notebook, style="Custom.TFrame")
        self.notebook.add(unique_frame, text="Constituent Drugs")

        # label secrion
        label = ttk.Label(unique_frame, text="Drug Combinations:", style="Custom.TLabel")
        label.pack(anchor='w', pady=(0,5))

        # Input Section
        input_section = ttk.Frame(unique_frame, style="Custom.TFrame")
        input_section.pack(fill='both', expand=True, padx=10, pady=10)

        self.unique_drugs_text = scrolledtext.ScrolledText(
            input_section, height=8, wrap=tk.WORD,
            font=("San Francisco", 10), background='white', foreground='black', insertbackground='black'
        )
        self.unique_drugs_text.pack(fill='both', expand=True)

        # Buttons Frame
        buttons_frame = ttk.Frame(input_section, style="Custom.TFrame")
        buttons_frame.pack(fill='x', padx=10, pady=5)

        extract_button = ttk.Button(buttons_frame, text="Extract Unique Drugs", command=self.extract_unique_drugs, style="Accent.TButton")
        extract_button.pack(side='left', padx=(0,5))

        import_button = ttk.Button(buttons_frame, text="Import from Plate Calculator", command=self.import_from_manual_tab, style="Success.TButton")
        import_button.pack(side='right', padx=(5,0))

         # label secrion
        label = ttk.Label(unique_frame, text="Constiruent Drug List:", style="Custom.TLabel")
        label.pack(anchor='w', pady=(0,5))

        # Results Section
        results_section = ttk.LabelFrame(unique_frame, style="Custom.TFrame")
        results_section.pack(fill='both', expand=True, padx=10, pady=10)

         
        results_frame = ttk.Frame(results_section, style="Custom.TFrame")
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.unique_drugs_listbox = tk.Listbox(results_frame, font=("San Francisco", 10), background='white', foreground='black', height=8)
        self.unique_drugs_listbox.pack(side='left', fill='both', expand=True)

        scrollbar = tk.Scrollbar(results_frame, command=self.unique_drugs_listbox.yview)
        scrollbar.pack(side='right', fill='y')
        self.unique_drugs_listbox.config(yscrollcommand=scrollbar.set)

        # Stats + Export
        stats_frame = ttk.Frame(results_section, style="Custom.TFrame")
        stats_frame.pack(fill='x', padx=10, pady=5)

        self.unique_count_label = ttk.Label(stats_frame, text="Total constituent drugs: 0", style="Custom.TLabel")
        self.unique_count_label.pack(side='left')

        export_button = ttk.Button(stats_frame, text="Export List", command=self.export_unique_drugs, style="Accent.TButton")
        export_button.pack(side='right')

    # ---------- FUNCTIONALITY ----------
    def calculate_manual(self):
        try:
            text_content = self.manual_text.get(1.0, tk.END).strip()
            if not text_content:
                messagebox.showwarning("⚠️ Warning", "Please enter some drug combinations!")
                return

            self.calculator.plates_per_calculation = int(self.plates_per_calc.get())
            self.calculator.multiplier = int(self.multiplier.get())

            drug_combos = [line.strip() for line in text_content.split('\n') if line.strip()]
            results = self.calculator.calculate_plates(drug_combos)
            self.show_results(results)

        except ValueError:
            messagebox.showerror("❌ Error", "Please enter valid numbers for parameters.")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Calculation failed:\n{str(e)}")

    def show_results(self, results):
        if 'error' in results:
            messagebox.showerror("❌ Error", results['error'])
            return

        result_message = (
            f"You'll need {results['final_result']} plates for your DiaMOND Assay!\n\n"
            f"• Total number of drug combinations: {results['total_combos']}\n"
            f"• Unique constituent drugs: {results['unique_constituent_drugs']}\n"
            f"• Single drugs: {results['singles']}\n"
        )
        messagebox.showinfo("✅ Calculation Results", result_message)

    def import_from_manual_tab(self):
        manual_content = self.manual_text.get(1.0, tk.END).strip()
        if manual_content:
            self.unique_drugs_text.delete(1.0, tk.END)
            self.unique_drugs_text.insert(1.0, manual_content)
            messagebox.showinfo("✅ Success", "Drugs imported from platw calculator tab!")
        else:
            messagebox.showwarning("⚠️ Warning", "No data found in Manual Input tab!")

    def extract_unique_drugs(self):
        text_content = self.unique_drugs_text.get(1.0, tk.END).strip()
        if not text_content:
            messagebox.showwarning("⚠️ Warning", "Please enter some drug combinations!")
            return

        lines = [line.strip() for line in text_content.split('\n') if line.strip()]
        self.unique_drugs_listbox.delete(0, tk.END)

        seen_drugs = set()
        unique_drugs_ordered = []
        for line in lines:
            drugs_in_combo = [drug.strip() for drug in line.split("+") if drug.strip()]
            for drug in drugs_in_combo:
                if drug and drug not in seen_drugs:
                    unique_drugs_ordered.append(drug)
                    seen_drugs.add(drug)

        for drug in unique_drugs_ordered:
            self.unique_drugs_listbox.insert(tk.END, drug)

        self.unique_count_label.config(text=f"Total unique drugs: {len(unique_drugs_ordered)}")
        messagebox.showinfo("✅ Success", f"Found {len(unique_drugs_ordered)} unique drugs!")

    def export_unique_drugs(self):
        if self.unique_drugs_listbox.size() == 0:
            messagebox.showwarning("⚠️ Warning", "No unique drugs to export!")
            return

        drugs_list = [self.unique_drugs_listbox.get(i) for i in range(self.unique_drugs_listbox.size())]

        filename = filedialog.asksaveasfilename(title="Save Unique Drugs List", defaultextension=".txt",
                                                filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*")])
        if filename:
            with open(filename, 'w') as f:
                if filename.endswith('.csv'):
                    f.write("Unique_Drugs\n")
                    for drug in drugs_list:
                        f.write(f"{drug}\n")
                else:
                    f.write("Unique Drugs List\n")
                    f.write("=" * 20 + "\n")
                    f.write(f"Total count: {len(drugs_list)}\n\n")
                    for i, drug in enumerate(drugs_list, 1):
                        f.write(f"{i:2d}. {drug}\n")

            messagebox.showinfo("✅ Success", f"Unique drugs list exported to:\n{filename}")


# ---------- RUN APP ----------
if __name__ == "__main__":
    app = PlateCalculatorGUI()
    app.root.mainloop()
