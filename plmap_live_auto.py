import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from QFLv4 import *
import os

# Set dark background style for matplotlib
plt.style.use('dark_background')

stpp = 0.1
xstpp, ystpp, fstpp = stpp, stpp, stpp

logf = False
invxy = False

# === Load data ===
def load_data(filepath, use_log):
    data = np.loadtxt(filepath, comments='#', delimiter='\t')
    x_req = data[:, 0]
    y_req = data[:, 1]
    if use_log:
        total = np.log10(data[:, 6])
    else:
        total = data[:, 6]
    return x_req, y_req, total

# === Build grid ===
def make_grid(x, y, z):
    x_unique = np.unique(x)
    y_unique = np.unique(y)
    X, Y = np.meshgrid(x_unique, y_unique)
    Z = np.zeros_like(X)
    for i, xi in enumerate(x_unique):
        for j, yj in enumerate(y_unique):
            match = (x == xi) & (y == yj)
            if np.any(match):
                Z[j, i] = z[match][0]
    return X, Y, Z

# === AMC Init ===
amc = start_attocube()

# === Main App ===
class PLMapGUI:
    def __init__(self, root, file_path):
        self.root = root
        self.file_path = file_path
        self.root.title("PL Map Viewer")
        self.root.configure(bg="#1e1e1e")

        # Load data
        x, y, z = load_data(file_path, logf)
        self.Xgrid, self.Ygrid, self.Zgrid = make_grid(x, y, z)

        self.x_click = None
        self.y_click = None

        # === TOP FRAME: File & Data Settings ===
        top_frame = tk.Frame(self.root, bg="#1e1e1e")
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.open_btn = tk.Button(top_frame, text="Open File", command=self.open_new_file, bg="#333333", fg="#ffffff")
        self.open_btn.pack(side=tk.LEFT, padx=5)

        self.log_var = tk.BooleanVar(value=logf)
        self.log_chk = tk.Checkbutton(top_frame, text="Log Filter", variable=self.log_var, command=self.toggle_log, bg="#1e1e1e", fg="#ffffff", selectcolor="#333333")
        self.log_chk.pack(side=tk.LEFT, padx=5)

        self.inv_var = tk.BooleanVar(value=invxy)
        self.inv_chk = tk.Checkbutton(top_frame, text="Invert XY", variable=self.inv_var, command=self.toggle_invert, bg="#1e1e1e", fg="#ffffff", selectcolor="#333333")
        self.inv_chk.pack(side=tk.LEFT, padx=5)

        tk.Label(top_frame, text="Step Size:", bg="#1e1e1e", fg="#ffffff").pack(side=tk.LEFT, padx=(15, 2))
        self.step_var = tk.StringVar(value=str(stpp))
        self.step_entry = tk.Entry(top_frame, textvariable=self.step_var, width=8, bg="#2d2d2d", fg="#ffffff", insertbackground="white")
        self.step_entry.pack(side=tk.LEFT, padx=2)
        
        self.set_step_btn = tk.Button(top_frame, text="Set Step", command=self.update_step_size, bg="#333333", fg="#ffffff")
        self.set_step_btn.pack(side=tk.LEFT, padx=5)

        # === PLOT ===
        self.fig, self.ax = plt.subplots(figsize=(6, 5))
        self.fig.patch.set_facecolor('#1e1e1e')
        self.ax.set_facecolor('#1e1e1e')
        
        self.im = self.ax.imshow(self.Zgrid, extent=[
            self.Xgrid.min(), self.Xgrid.max(),
            self.Ygrid.min(), self.Ygrid.max()
        ], origin='lower', cmap='plasma', aspect='auto')
        self.ax.set_title("Live PLmap", color="white")
        self.ax.set_xlabel("X (µm)", color="white")
        self.ax.set_ylabel("Y (µm)", color="white")
        
        if invxy:
            self.ax.invert_xaxis()
            self.ax.invert_yaxis()
            
        cbar = self.fig.colorbar(self.im, ax=self.ax, label='Log10 Counts' if logf else 'Counts')
        cbar.ax.yaxis.label.set_color('white')
        cbar.ax.tick_params(colors='white')
        
        plt.tight_layout()
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.canvas.mpl_connect("button_press_event", self.on_click)

        # === BOTTOM FRAME: Movement & Position Controls ===
        bottom_frame = tk.Frame(self.root, bg="#1e1e1e")
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        tk.Label(bottom_frame, text="Requested X:", bg="#1e1e1e", fg="#ffffff").grid(row=0, column=0, sticky="w")
        self.x_req_var = tk.StringVar()
        tk.Entry(bottom_frame, textvariable=self.x_req_var, width=10, bg="#2d2d2d", fg="#ffffff", insertbackground="white").grid(row=0, column=1)

        tk.Label(bottom_frame, text="Requested Y:", bg="#1e1e1e", fg="#ffffff").grid(row=1, column=0, sticky="w")
        self.y_req_var = tk.StringVar()
        tk.Entry(bottom_frame, textvariable=self.y_req_var, width=10, bg="#2d2d2d", fg="#ffffff", insertbackground="white").grid(row=1, column=1)
        
        self.goto_btn = tk.Button(bottom_frame, text="Go To", command=self.go_to_position, bg="#333333", fg="#ffffff")
        self.goto_btn.grid(row=0, column=2, padx=10)

        tk.Label(bottom_frame, text="Current X:", bg="#1e1e1e", fg="#ffffff").grid(row=0, column=3, sticky="w")
        self.x_act_var = tk.StringVar()
        tk.Label(bottom_frame, textvariable=self.x_act_var, width=10, bg="#2d2d2d", fg="#ffffff").grid(row=0, column=4)

        tk.Label(bottom_frame, text="Current Y:", bg="#1e1e1e", fg="#ffffff").grid(row=1, column=3, sticky="w")
        self.y_act_var = tk.StringVar()
        tk.Label(bottom_frame, textvariable=self.y_act_var, width=10, bg="#2d2d2d", fg="#ffffff").grid(row=1, column=4)
        
        tk.Label(bottom_frame, text="Current F:", bg="#1e1e1e", fg="#ffffff").grid(row=2, column=3, sticky="w")
        self.f_act_var = tk.StringVar()
        tk.Label(bottom_frame, textvariable=self.f_act_var, width=10, bg="#2d2d2d", fg="#ffffff").grid(row=2, column=4)

        self.moving_var = tk.StringVar()
        tk.Label(bottom_frame, textvariable=self.moving_var, bg="#1e1e1e", fg="#00ff00").grid(row=2, column=0)
        
        self.go_to_fup_btn = tk.Button(bottom_frame, text="Focus (+)", command=self.go_to_fup, bg="#333333", fg="#ffffff")
        self.go_to_fup_btn.grid(row=0, column=9, padx=10)

        self.go_to_fdown_btn = tk.Button(bottom_frame, text="Focus (-)", command=self.go_to_fdown, bg="#333333", fg="#ffffff")
        self.go_to_fdown_btn.grid(row=2, column=9, padx=10)        

        self.go_to_up_btn = tk.Button(bottom_frame, text="Up", command=self.go_to_up, bg="#333333", fg="#ffffff")
        self.go_to_up_btn.grid(row=0, column=7, padx=10)

        self.go_to_down_btn = tk.Button(bottom_frame, text="Down", command=self.go_to_down, bg="#333333", fg="#ffffff")
        self.go_to_down_btn.grid(row=2, column=7, padx=10)

        self.go_to_left_btn = tk.Button(bottom_frame, text="Left", command=self.go_to_left, bg="#333333", fg="#ffffff")
        self.go_to_left_btn.grid(row=1, column=6, padx=10)

        self.go_to_right_btn = tk.Button(bottom_frame, text="Right", command=self.go_to_right, bg="#333333", fg="#ffffff")
        self.go_to_right_btn.grid(row=1, column=8, padx=10)
        
        # Keybindings
        bottom_frame.bind_all("<Up>", lambda event: self.go_to_up())
        bottom_frame.bind_all("<Down>", lambda event: self.go_to_down())
        bottom_frame.bind_all("<Left>", lambda event: self.go_to_left())
        bottom_frame.bind_all("<Right>", lambda event: self.go_to_right())
        bottom_frame.bind_all("<Prior>", lambda event: self.go_to_fup())
        bottom_frame.bind_all("<Next>", lambda event: self.go_to_fdown())

        self.update_current_positions()

    def update_step_size(self):
        global stpp, xstpp, ystpp, fstpp
        try:
            val = float(self.step_var.get())
            stpp = val
            xstpp, ystpp, fstpp = val, val, val
        except ValueError:
            messagebox.showerror("Error", "Invalid step size value.")

    def toggle_log(self):
        global logf
        logf = self.log_var.get()
        self.reload_plot_data()

    def toggle_invert(self):
        global invxy
        invxy = self.inv_var.get()
        if invxy:
            self.ax.invert_xaxis()
            self.ax.invert_yaxis()
        else:
            self.ax.set_xlim(self.Xgrid.min(), self.Xgrid.max())
            self.ax.set_ylim(self.Ygrid.min(), self.Ygrid.max())
        self.canvas.draw()

    def reload_plot_data(self):
        try:
            x, y, z = load_data(self.file_path, logf)
            self.Xgrid, self.Ygrid, self.Zgrid = make_grid(x, y, z)
            self.ax.clear()
            self.ax.set_facecolor('#1e1e1e')
            self.im = self.ax.imshow(self.Zgrid, extent=[
                self.Xgrid.min(), self.Xgrid.max(),
                self.Ygrid.min(), self.Ygrid.max()
            ], origin='lower', cmap='plasma', aspect='auto')
            self.ax.set_title("Live PLmap", color="white")
            self.ax.set_xlabel("X (µm)", color="white")
            self.ax.set_ylabel("Y (µm)", color="white")
            if invxy:
                self.ax.invert_xaxis()
                self.ax.invert_yaxis()
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reload data:\n{e}")

    def update_current_positions(self):
        try:
            x_act = amc.move.getPosition(0) / 1000
            y_act = amc.move.getPosition(2) / 1000
            f_act = amc.move.getPosition(1) / 1000
            self.x_act_var.set(f"{x_act:.3f}")
            self.y_act_var.set(f"{y_act:.3f}")
            self.f_act_var.set(f"{f_act:.3f}")
        except Exception:
            pass

    def open_new_file(self):
        new_file_path = filedialog.askopenfilename(title="Select PL Mapping File", filetypes=[("Text files", "*.txt")])
        if new_file_path:
            self.file_path = new_file_path
            self.reload_plot_data()

    def on_click(self, event):
        if event.inaxes != self.im.axes:
            return
        x = event.xdata
        y = event.ydata
        self.x_click = x
        self.y_click = y
        self.x_req_var.set(f"{x:.3f}")
        self.y_req_var.set(f"{y:.3f}")

    def go_to_position(self):
        try:
            x = float(self.x_req_var.get())
            y = float(self.y_req_var.get())
            self.moving_var.set("Moving")
            self.root.update_idletasks()
            
            amc.move.setControlTargetPosition(0, int(x * 1000))
            wait_until_stable(amc_dev=amc, axis=0)
            amc.move.setControlTargetPosition(2, int(y * 1000))
            wait_until_stable(amc_dev=amc, axis=2)
            
            self.update_current_positions()
            self.moving_var.set("")
        except Exception as e:
            self.moving_var.set("")
            messagebox.showerror("Error", str(e))

    def go_to_up(self): 
        try:
            y_act = amc.move.getPosition(2) / 1000
            amc.move.setControlTargetPosition(2, int((y_act + ystpp) * 1000))
            wait_until_stable(amc_dev=amc, axis=2)
            self.update_current_positions()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def go_to_down(self): 
        try:
            y_act = amc.move.getPosition(2) / 1000
            amc.move.setControlTargetPosition(2, int((y_act - ystpp) * 1000))
            wait_until_stable(amc_dev=amc, axis=2)
            self.update_current_positions()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def go_to_left(self): 
        try:
            x_act = amc.move.getPosition(0) / 1000
            amc.move.setControlTargetPosition(0, int((x_act - xstpp) * 1000))
            wait_until_stable(amc_dev=amc, axis=0)
            self.update_current_positions()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def go_to_right(self): 
        try:
            x_act = amc.move.getPosition(0) / 1000
            amc.move.setControlTargetPosition(0, int((x_act + xstpp) * 1000))
            wait_until_stable(amc_dev=amc, axis=0)
            self.update_current_positions()
        except Exception as e:
            messagebox.showerror("Error", str(e))
                
    def go_to_fup(self): 
        try:
            f_act = amc.move.getPosition(1) / 1000
            amc.move.setControlTargetPosition(1, int((f_act + fstpp) * 1000))
            wait_until_stable(amc_dev=amc, axis=1)
            self.update_current_positions()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def go_to_fdown(self): 
        try:
            f_act = amc.move.getPosition(1) / 1000
            amc.move.setControlTargetPosition(1, int((f_act - fstpp) * 1000))
            wait_until_stable(amc_dev=amc, axis=1)
            self.update_current_positions()
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    initial_file_path = filedialog.askopenfilename(title="Select PL Mapping File", filetypes=[("Text files", "*.txt")])
    if initial_file_path:
        app = PLMapGUI(root, initial_file_path)
        root.mainloop()
    else:
        print("No file selected.")