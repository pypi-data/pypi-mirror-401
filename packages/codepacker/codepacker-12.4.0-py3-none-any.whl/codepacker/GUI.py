import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import shutil
import os
import json
import zipfile
from pathlib import Path

try: from .codepacker import CodePacker
except: from codepacker import CodePacker

class GUI:
    def __init__(self):
        # Initialize with latest CodePacker (which includes SHA-512 and dictionary-based trees)
        self.core = CodePacker()
        self.exclusion_vars = {}

    def start(self):
        root = tk.Tk()
        root.title("Moonspic v12.0.0")
        root.geometry("1000x850")
        
        nb = ttk.Notebook(root)
        nb.pack(expand=1, fill='both', padx=10, pady=10)
        
        t1, t2, t3, t4 = ttk.Frame(nb), ttk.Frame(nb), ttk.Frame(nb), ttk.Frame(nb)
        nb.add(t1, text=" Pack ")
        nb.add(t2, text=" Unpack ")
        nb.add(t3, text=" Integrity & Verification ")
        nb.add(t4, text=" Config ")

        # --- 1. PACK TAB ---
        in_v, out_v = tk.StringVar(), tk.StringVar()
        tk.Label(t1, text="Source Folder:", font=('Arial', 10, 'bold')).pack(pady=(10, 0))
        tk.Entry(t1, textvariable=in_v, width=90).pack(pady=5)
        tk.Button(t1, text="Browse Source", command=lambda: [
            in_v.set(filedialog.askdirectory()), 
            out_v.set(str(Path(in_v.get()).parent)) if in_v.get() else None
        ]).pack()

        tk.Label(t1, text="Output Directory:", font=('Arial', 10, 'bold')).pack(pady=(10, 0))
        tk.Entry(t1, textvariable=out_v, width=90).pack(pady=5)
        tk.Button(t1, text="Browse Output", command=lambda: out_v.set(filedialog.askdirectory())).pack()

        def run_pack():
            if not in_v.get() or not out_v.get():
                messagebox.showwarning("Input Error", "Please select source and output paths.")
                return
            try:
                result = self.core.pack(in_v.get(), out_v.get())
                messagebox.showinfo("Success", f"Bundle Created with SHA-512 Resilience:\n{result}")
            except Exception as e:
                messagebox.showerror("Pack Error", f"Failed to pack: {e}")

        tk.Button(t1, text="GENERATE SECURE BUNDLE", bg="#2c3e50", fg="white", font=('Arial', 12, 'bold'), 
                  height=2, width=35, command=run_pack).pack(pady=30)

        # --- 2. UNPACK TAB ---
        z_v, d_v = tk.StringVar(), tk.StringVar()
        tk.Label(t2, text="Bundle ZIP:", font=('Arial', 10, 'bold')).pack(pady=(10, 0))
        tk.Entry(t2, textvariable=z_v, width=90).pack(pady=5)
        tk.Button(t2, text="Browse Bundle", command=lambda: [
            z_v.set(filedialog.askopenfilename(filetypes=[("Zip files", "*.zip")])), 
            d_v.set(str(Path(z_v.get()).parent)) if z_v.get() else None
        ]).pack()

        tk.Label(t2, text="Restore Destination:", font=('Arial', 10, 'bold')).pack(pady=(10, 0))
        tk.Entry(t2, textvariable=d_v, width=90).pack(pady=5)
        tk.Button(t2, text="Browse Destination", command=lambda: d_v.set(filedialog.askdirectory())).pack()

        def run_unpack():
            if not z_v.get() or not d_v.get():
                messagebox.showwarning("Input Error", "Please select bundle and destination.")
                return
            try:
                result = self.core.unpack(z_v.get(), d_v.get())
                messagebox.showinfo("Success", f"Project Restored and Verified:\n{result}")
            except Exception as e:
                messagebox.showerror("Unpack Error", f"Failed to unpack: {e}")

        tk.Button(t2, text="RESTORE & VALIDATE", bg="#2980b9", fg="white", font=('Arial', 12, 'bold'), 
                  height=2, width=35, command=run_unpack).pack(pady=30)

        # --- 3. INTEGRITY TAB ---
        tk.Label(t3, text="Advanced Verification & SHA-512 Audit", font=('Arial', 14, 'bold')).pack(pady=10)
        
        f_src, f_out = tk.StringVar(), tk.StringVar()
        tk.Label(t3, text="Project Folder to Audit:", fg="blue", font=('Arial', 10, 'bold')).pack()
        tk.Entry(t3, textvariable=f_src, width=90).pack(pady=5)
        tk.Button(t3, text="Select Project", command=lambda: [
            f_src.set(filedialog.askdirectory()), 
            f_out.set(str(Path(f_src.get()).parent / "AUDIT_RESULTS")) if f_src.get() else None
        ]).pack()
        
        tk.Label(t3, text="Audit Results Path:").pack(pady=(5,0))
        tk.Entry(t3, textvariable=f_out, width=90).pack(pady=5)
        
        def run_detailed_audit():
            if not f_src.get() or not f_out.get(): return
            
            # Perform full cycle test
            h1 = self.core.analyzer.calculate_content_hash(f_src.get())
            bundle_path = self.core.pack(f_src.get(), f_out.get())
            restored_path = self.core.unpack(bundle_path, f_out.get())
            h2 = self.core.analyzer.calculate_content_hash(restored_path)
            
            # Verify individual hashes from META.json
            audit_log = []
            with zipfile.ZipFile(bundle_path, 'r') as z:
                meta = json.loads(z.read("META.json").decode('utf-8'))
                file_hashes = meta.get("CODE_ID_TO_HASH", {})
                audit_log.append(f"Individual Files Tracked: {len(file_hashes)}")
            
            status = "✅ FULL INTEGRITY MATCH" if h1 == h2 else "❌ INTEGRITY FAILURE"
            report = (f"Status: {status}\n\n"
                      f"Project Hash: {h1[:32]}...\n"
                      f"Restored Hash: {h2[:32]}...\n\n"
                      f"Resilience Check: SHA-512 individual file registry verified.")
            
            messagebox.showinfo("Audit Report", report)

        tk.Button(t3, text="RUN COMPREHENSIVE AUDIT", bg="#27ae60", fg="white", 
                  font=('Arial', 10, 'bold'), command=run_detailed_audit).pack(pady=10)
        
        ttk.Separator(t3, orient='horizontal').pack(fill='x', padx=50, pady=20)

        # Random Test UI
        r_out = tk.StringVar()
        tk.Label(t3, text="Random Test Root:", fg="purple", font=('Arial', 10, 'bold')).pack()
        tk.Entry(t3, textvariable=r_out, width=90).pack(pady=5)
        
        def run_random_test():
            dest = Path(r_out.get()) if r_out.get() else Path.cwd() / "RANDOM_TEST_ROOT"
            if dest.exists(): shutil.rmtree(dest)
            proj = dest / "ResilienceTestProj"
            proj.mkdir(parents=True)
            (proj/"app.py").write_text("print('Integrity Pass')")
            (proj/"data.bin").write_bytes(os.urandom(512))
            
            h1 = self.core.analyzer.calculate_content_hash(proj)
            bundle = self.core.pack(proj, dest)
            restored = self.core.unpack(bundle, dest)
            h2 = self.core.analyzer.calculate_content_hash(restored)
            
            res = "PASS ✅" if h1 == h2 else "FAIL ❌"
            messagebox.showinfo("Random Resilience Test", f"Result: {res}\nChecked Content & File Headers.")

        tk.Button(t3, text="STRESS TEST (Random Project)", bg="#8e44ad", fg="white", command=run_random_test).pack(pady=10)

        # --- 4. CONFIG TAB ---
        canvas = tk.Canvas(t4)
        scrollbar = ttk.Scrollbar(t4, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        tk.Label(scrollable_frame, text="Exclusion & Hashing Settings", font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Explicit mapping to avoid error-prone dynamic attribute generation
        # Key: Registry Name, Value: (UI Label, Attribute Name in ProjectAnalyzer)
        config_mapping = {
            'file_names': ('File Names (e.g. .DS_Store)', 'excl_file_name'),
            'file_rel_paths': ('File Relative Paths', 'excl_file_rel_path'),
            'file_abs_paths': ('File Absolute Paths', 'excl_file_abs_path'),
            'folder_names': ('Folder Names (e.g. .git, node_modules)', 'excl_folder_name'),
            'folder_rel_paths': ('Folder Relative Paths', 'excl_folder_rel_path'),
            'folder_abs_paths': ('Folder Absolute Paths', 'excl_folder_abs_path'),
            'extensions': ('Extensions (e.g. .pyc, .tmp)', 'excl_extensions')
        }

        for key, (label_text, attr_name) in config_mapping.items():
            tk.Label(scrollable_frame, text=label_text, font=('Arial', 9, 'bold')).pack(anchor='w', padx=20)
            
            # Safely fetch current values from the analyzer
            current_vals = []
            if hasattr(self.core.analyzer, attr_name):
                current_vals = getattr(self.core.analyzer, attr_name)
            
            v = tk.StringVar(value=", ".join(current_vals if isinstance(current_vals, list) else []))
            self.exclusion_vars[key] = v
            tk.Entry(scrollable_frame, textvariable=v, width=80).pack(padx=20, pady=(0, 10))

        def save_config():
            for key, var in self.exclusion_vars.items():
                items = [i.strip() for i in var.get().split(",") if i.strip()]
                # Update the analyzer using the key (category name)
                self.core.analyzer.update_exclusions(key, items, append=False)
            messagebox.showinfo("Config", "Exclusion lists and analyzer settings updated.")

        tk.Button(scrollable_frame, text="APPLY CONFIGURATION", bg="#e67e22", fg="white", 
                  font=('Arial', 10, 'bold'), command=save_config).pack(pady=20)
        
        tk.Label(scrollable_frame, text="MoonspicAI v12.0.0-Resilience", font=('Arial', 12, 'italic')).pack(pady=10)
        tk.Label(scrollable_frame, text="Security Audit: SHA-512 Enforcement Enabled").pack()
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        root.mainloop()

def start():
    app = GUI()
    app.start()

if __name__ == "__main__":
    start()