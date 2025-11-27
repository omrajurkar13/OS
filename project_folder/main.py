import tkinter as tk
from tkinter import ttk, messagebox

class DeadlockDetector:
    def __init__(self, root):
        self.root = root
        self.root.title("Deadlock Detection Tool")
        self.root.geometry("850x800")
        self.root.configure(bg="#f4f6f8")  # Very soft professional gray background

        self.entries_alloc = []
        self.entries_req = []
        self.entries_total = []

        # --- Title ---
        title = tk.Label(root, text="Deadlock Detection System",
                         font=("Segoe UI", 24, "bold"),
                         bg="#f4f6f8", fg="#1f2937", pady=20)
        title.pack()

        # --- Input Frame ---
        input_frame = tk.Frame(root, bg="#ffffff", bd=1, relief="solid")
        input_frame.pack(pady=20, padx=30, fill="x")

        tk.Label(input_frame, text="Number of Processes:", font=("Segoe UI", 12), bg="#ffffff").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_proc = tk.Entry(input_frame, width=10, font=("Segoe UI", 11), bg="#e5e7eb", bd=1, relief="solid")
        self.entry_proc.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(input_frame, text="Number of Resources:", font=("Segoe UI", 12), bg="#ffffff").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_res = tk.Entry(input_frame, width=10, font=("Segoe UI", 11), bg="#e5e7eb", bd=1, relief="solid")
        self.entry_res.grid(row=1, column=1, padx=10, pady=10)

        style = ttk.Style()
        style.configure("Accent.TButton",
                        font=("Segoe UI", 11, "bold"),
                        foreground="#ffffff",
                        background="#2563eb",
                        padding=6)
        style.map("Accent.TButton",
                  background=[("active", "#1d4ed8")])

        generate_btn = ttk.Button(input_frame, text="Generate Tables", command=self.generate_tables, style="Accent.TButton")
        generate_btn.grid(row=2, column=0, columnspan=2, pady=20)

        # --- Preset Button ---
        preset_btn = ttk.Button(input_frame, text="Load Preset Matrices", command=self.preset_matrices, style="Accent.TButton")
        preset_btn.grid(row=3, column=0, columnspan=2, pady=10)

        # --- Table Frame ---
        self.table_frame = tk.Frame(root, bg="#ffffff", bd=1, relief="solid")
        self.table_frame.pack(pady=20, padx=30, fill="both", expand=True)

        # --- Bottom Buttons ---
        button_frame = tk.Frame(root, bg="#f4f6f8")
        button_frame.pack(pady=20)

        detect_btn = ttk.Button(button_frame, text="Detect Deadlock", command=self.detect_deadlock, style="Accent.TButton")
        detect_btn.grid(row=0, column=0, padx=30)

        clear_btn = ttk.Button(button_frame, text="Clear All", command=self.clear_all, style="Accent.TButton")
        clear_btn.grid(row=0, column=1, padx=30)

    def generate_tables(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        self.entries_alloc, self.entries_req, self.entries_total = [], [], []

        try:
            self.num_proc = int(self.entry_proc.get())
            self.num_res = int(self.entry_res.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integers for processes and resources.")
            return

        # Allocation Matrix
        tk.Label(self.table_frame, text="Allocation Matrix", font=("Segoe UI", 13, "bold"), bg="#ffffff", fg="#374151").grid(row=0, column=0, columnspan=self.num_res + 1, pady=8)
        for i in range(self.num_proc):
            row_entries = []
            tk.Label(self.table_frame, text=f"P{i}", bg="#ffffff", font=("Segoe UI", 11)).grid(row=i + 1, column=0, padx=5)
            for j in range(self.num_res):
                e = tk.Entry(self.table_frame, width=5, font=("Segoe UI", 10), justify="center", bg="#e5e7eb", bd=1, relief="solid")
                e.grid(row=i + 1, column=j + 1, padx=4, pady=4)
                row_entries.append(e)
            self.entries_alloc.append(row_entries)

        offset = self.num_proc + 2

        # Request Matrix
        tk.Label(self.table_frame, text="Request Matrix", font=("Segoe UI", 13, "bold"), bg="#ffffff", fg="#374151").grid(row=offset, column=0, columnspan=self.num_res + 1, pady=8)
        for i in range(self.num_proc):
            row_entries = []
            tk.Label(self.table_frame, text=f"P{i}", bg="#ffffff", font=("Segoe UI", 11)).grid(row=offset + i + 1, column=0, padx=5)
            for j in range(self.num_res):
                e = tk.Entry(self.table_frame, width=5, font=("Segoe UI", 10), justify="center", bg="#e5e7eb", bd=1, relief="solid")
                e.grid(row=offset + i + 1, column=j + 1, padx=4, pady=4)
                row_entries.append(e)
            self.entries_req.append(row_entries)

        offset = offset + self.num_proc + 2

        # Total Resources
        tk.Label(self.table_frame, text="(Optional) Total Resources", font=("Segoe UI", 12, "italic"), bg="#ffffff", fg="#6b7280").grid(row=offset, column=0, columnspan=self.num_res, pady=8)
        for j in range(self.num_res):
            e = tk.Entry(self.table_frame, width=5, font=("Segoe UI", 10), justify="center", bg="#e5e7eb", bd=1, relief="solid")
            e.grid(row=offset + 1, column=j, padx=4, pady=4)
            self.entries_total.append(e)

    def detect_deadlock(self):
        try:
            alloc = [[int(e.get()) for e in row] for row in self.entries_alloc]
            req = [[int(e.get()) for e in row] for row in self.entries_req]
        except ValueError:
            messagebox.showerror("Input Error", "All matrix entries must be integers.")
            return

        total_resources = []
        for j in range(self.num_res):
            try:
                val = self.entries_total[j].get()
                total_resources.append(int(val) if val else 0)
            except ValueError:
                messagebox.showerror("Input Error", "Total Resources must be integers.")
                return

        for j in range(self.num_res):
            if total_resources[j] == 0:
                total = sum([alloc[i][j] for i in range(self.num_proc)]) + max([req[i][j] for i in range(self.num_proc)])
                total_resources[j] = total

        available = [total_resources[j] - sum(alloc[i][j] for i in range(self.num_proc)) for j in range(self.num_res)]

        p, r = self.num_proc, self.num_res
        finish = [False] * p
        work = available.copy()
        deadlocked = []

        while True:
            found = False
            for i in range(p):
                if not finish[i] and all(req[i][j] <= work[j] for j in range(r)):
                    for j in range(r):
                        work[j] += alloc[i][j]
                    finish[i] = True
                    found = True
            if not found:
                break

        for i in range(p):
            if not finish[i]:
                deadlocked.append(i)

        # Deadlock Conditions
        condition_1 = any(total_resources[j] <= 1 for j in range(r))
        condition_2 = any(any(alloc[i][j] > 0 for j in range(r)) and any(req[i][j] > 0 for j in range(r)) for i in range(p))
        condition_3 = all(req[i][j] > 0 and available[j] == 0 for i in deadlocked for j in range(r) if req[i][j] > 0)
        condition_4 = len(deadlocked) > 0
        all_true = all([condition_1, condition_2, condition_3, condition_4])

        result_msg = f"""
Total Resources: {total_resources}
Available Resources: {available}

Deadlock Conditions:
1. Mutual Exclusion: {'Yes' if condition_1 else 'No'}
2. Hold and Wait: {'Yes' if condition_2 else 'No'}
3. No Preemption: {'Yes' if condition_3 else 'No'}
4. Circular Wait: {'Yes' if condition_4 else 'No'}

Result: {'Deadlock Detected' if all_true else 'No Deadlock'}

Deadlocked Processes: {["P"+str(i) for i in deadlocked] if deadlocked else "None"}
"""
        self.show_popup_result(result_msg, all_true)

    def show_popup_result(self, result_msg, is_deadlock):
        if is_deadlock:
            icon = "🛑"  # Red for deadlock
        else:
            icon = "✅"  # Green for no deadlock

        messagebox.showinfo(
            "Detection Result", 
            f"{icon} {result_msg.strip()}",
            icon='info'
        )

    def clear_all(self):
        self.entry_proc.delete(0, tk.END)
        self.entry_res.delete(0, tk.END)
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        self.entries_alloc.clear()
        self.entries_req.clear()
        self.entries_total.clear()

    def preset_matrices(self):
        preset_alloc = [[1, 0], [0, 1], [1, 1]]
        preset_req = [[1, 1], [1, 0], [0, 1]]
        for i in range(self.num_proc):
            for j in range(self.num_res):
                self.entries_alloc[i][j].delete(0, tk.END)
                self.entries_alloc[i][j].insert(0, preset_alloc[i][j])
                self.entries_req[i][j].delete(0, tk.END)
                self.entries_req[i][j].insert(0, preset_req[i][j])

if __name__ == "__main__":
    root = tk.Tk()
    app = DeadlockDetector(root)
    root.mainloop()

