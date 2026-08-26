import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from QFLv4 import *
from attocube import AMC

logf=True
# === Load data ===
def load_data(filepath):
    data = np.loadtxt(filepath, comments='#', delimiter='\t')
    x_req = data[:, 0]
    y_req = data[:, 1]
    if logf:
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
amc = AMC.Device('amc100num-a01-0248.local')
amc.connect()
for a in [0, 2]: amc.control.setControlOutput(a, True); amc.control.setControlMove(a, True)
amc.control.setControlOutput(1, False); amc.control.setControlMove(1, False)

def wait_until_stable(timeout=10):
    import time
    start = time.time()
    while True:
        if all(amc.status.getStatusMoving(a) == 0 for a in [0, 2]) and \
           all(amc.status.getStatusTargetRange(a) for a in [0, 2]):
            break
        for a in [0, 2]: amc.control.setControlOutput(a, True); amc.control.setControlMove(a, True)
        if time.time() - start > timeout:
            break
        time.sleep(0.01)

# === Main App ===
class PLMapGUI:
    def __init__(self, root, file_path):
        self.root = root
        self.file_path = file_path
        self.root.title("PL Map Viewer with Go To")

        # Load data
        x, y, z = load_data(file_path)
        self.Xgrid, self.Ygrid, self.Zgrid = make_grid(x, y, z)

        self.x_click = None
        self.y_click = None

        # Plot
        fig, ax = plt.subplots(figsize=(6, 5))
        self.im = ax.imshow(self.Zgrid, extent=[
            self.Xgrid.min(), self.Xgrid.max(),
            self.Ygrid.min(), self.Ygrid.max()
        ], origin='lower', cmap='plasma', aspect='auto')
        ax.set_title("Click on a point to Go To")
        ax.set_xlabel("X (µm)")
        ax.set_ylabel("Y (µm)")
        ax.invert_xaxis()
        ax.invert_yaxis()
        fig.colorbar(self.im, ax=ax, label="Total Counts")

        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        self.canvas.mpl_connect("button_press_event", self.on_click)

        # Controls
        frame = tk.Frame(self.root)
        frame.pack(pady=5)

        tk.Label(frame, text="Requested X:").grid(row=0, column=0)
        self.x_req_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.x_req_var, width=10).grid(row=0, column=1)

        tk.Label(frame, text="Requested Y:").grid(row=0, column=2)
        self.y_req_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.y_req_var, width=10).grid(row=0, column=3)

        self.goto_btn = tk.Button(frame, text="Go To", command=self.go_to_position)
        self.goto_btn.grid(row=0, column=4, padx=10)

        tk.Label(frame, text="Actual X:").grid(row=1, column=0)
        self.x_act_var = tk.StringVar()
        tk.Label(frame, textvariable=self.x_act_var).grid(row=1, column=1)

        tk.Label(frame, text="Actual Y:").grid(row=1, column=2)
        self.y_act_var = tk.StringVar()
        tk.Label(frame, textvariable=self.y_act_var).grid(row=1, column=3)

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
            amc.move.setControlTargetPosition(0, int(x * 1000))
            amc.move.setControlTargetPosition(2, int(y * 1000))
            wait_until_stable()

            x_act = amc.move.getPosition(0) / 1000
            y_act = amc.move.getPosition(2) / 1000
            self.x_act_var.set(f"{x_act:.3f}")
            self.y_act_var.set(f"{y_act:.3f}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

# === File Selection and App Launch ===
if __name__ == "__main__":
    root = tk.Tk()
    file_path = filedialog.askopenfilename(title="Select PL Mapping File", filetypes=[("Text files", "*.txt")])
    if file_path:
        app = PLMapGUI(root, file_path)
        root.mainloop()
    else:
        print("No file selected.")
