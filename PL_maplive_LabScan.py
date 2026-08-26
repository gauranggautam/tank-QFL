import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import AMC, os

os.system('cls' if os.name == 'nt' else 'clear')

stpp=0.1
xstpp,ystpp,fstpp=stpp,stpp,stpp

logf=True
invxy=False
# === Load data ===
def load_data(filepath):
    data = np.loadtxt(filepath, comments='#', delimiter='\t')
    x_req = data[:, 0]
    y_req = data[:, 2]
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
for a in [0, 1, 2]: amc.control.setControlOutput(a, True); amc.control.setControlMove(a, True)
#amc.control.setControlOutput(1, False); amc.control.setControlMove(1, False)

def wait_until_stable(timeout=10):
    moving=True
    import time
    start = time.time()
    while True:
        if all(amc.status.getStatusMoving(a) == 0 for a in [0, 1, 2]) and \
        all(amc.status.getStatusTargetRange(a) for a in [0, 1, 2]):
            moving=False
            break
        for a in [0, 1, 2]: amc.control.setControlOutput(a, True); amc.control.setControlMove(a, True)
        if time.time() - start > timeout:
            moving=False
            break
        time.sleep(0.01)


# === Main App ===
class PLMapGUI:
    def __init__(self, root, file_path):
        self.root = root
        self.file_path = file_path
        self.root.title("PL Map Viewer for LabScan data with Go To")

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
        ax.set_title("Live PLmap")
        ax.set_xlabel("X (µm)")
        ax.set_ylabel("Y (µm)")
        if invxy:
            ax.invert_xaxis()
            ax.invert_yaxis()
        fig.colorbar(self.im, ax=ax, label='Log10 Counts' if logf else 'Counts')
        plt.tight_layout()
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

        tk.Label(frame, text="Requested Y:").grid(row=1, column=0)
        self.y_req_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.y_req_var, width=10).grid(row=1, column=1)
        
        
        self.goto_btn = tk.Button(frame, text="Go To", command=self.go_to_position)
        self.goto_btn.grid(row=0, column=2, padx=10)

        #self.on_btn = tk.Button(frame, text="Moving")
        #self.on_btn.grid(row=1, column=4, padx=10)


        tk.Label(frame, text="Current X:").grid(row=0, column=3)
        self.x_act_var = tk.StringVar()
        tk.Label(frame, textvariable=self.x_act_var, width=10).grid(row=0, column=4)

        tk.Label(frame, text="Current Y:").grid(row=1, column=3)
        self.y_act_var = tk.StringVar()
        tk.Label(frame, textvariable=self.y_act_var, width=10).grid(row=1, column=4)
        
        tk.Label(frame, text="Current F:").grid(row=2, column=3)
        self.f_act_var = tk.StringVar()
        tk.Label(frame, textvariable=self.f_act_var, width=10).grid(row=2, column=4)
        
        #self.current_pos_var = tk.StringVar()
        #tk.Label(frame, textvariable=self.current_pos_var).grid(row=1, column=7)
        

        self.moving_var = tk.StringVar()
        tk.Label(frame, textvariable=self.moving_var).grid(row=2, column=0)
        
        #tk.Label(frame, text="Step X:").grid(row=0, column=5)
        #self.x_step_var = tk.StringVar()
        #tk.Entry(frame, textvariable=self.x_step_var, width=10).grid(row=0, column=6)

        #tk.Label(frame, text="Step Y:").grid(row=1, column=5)
        #self.y_step_var = tk.StringVar()
        #tk.Entry(frame, textvariable=self.y_step_var, width=10).grid(row=1, column=6)
        
        self.go_to_fup_btn = tk.Button(frame, text="Focus (+)", command=self.go_to_fup)
        self.go_to_fup_btn.grid(row=0, column=9, padx=10)
        


        self.go_to_fdown_btn = tk.Button(frame, text="Focus (-)", command=self.go_to_fdown)
        self.go_to_fdown_btn.grid(row=2, column=9, padx=10)        

        
        self.go_to_up_btn = tk.Button(frame, text="Up", command=self.go_to_up)
        self.go_to_up_btn.grid(row=0, column=7, padx=10)
        

        self.go_to_down_btn = tk.Button(frame, text="Down", command=self.go_to_down)
        self.go_to_down_btn.grid(row=2, column=7, padx=10)

        self.go_to_left_btn = tk.Button(frame, text="Left", command=self.go_to_left)
        self.go_to_left_btn.grid(row=1, column=6, padx=10)

        self.go_to_right_btn = tk.Button(frame, text="Right", command=self.go_to_right)
        self.go_to_right_btn.grid(row=1, column=8, padx=10)
        
        #Keybindings
        
        frame.bind_all("<Up>", lambda event: self.go_to_up())
        frame.bind_all("<Down>", lambda event: self.go_to_down())
        frame.bind_all("<Left>", lambda event: self.go_to_left())
        frame.bind_all("<Right>", lambda event: self.go_to_right())
        frame.bind_all("<Prior>", lambda event: self.go_to_fup())
        frame.bind_all("<Next>", lambda event: self.go_to_fdown())

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
            #self.on_btn.config(highlightbackground="green", highlightthickness=50)
            self.moving_var.set("Moving")
            wait_until_stable()
            
            #self.on_btn.config(highlightthickness=0)
            x_act = amc.move.getPosition(0) / 1000
            y_act = amc.move.getPosition(2) / 1000
            self.x_act_var.set(f"{x_act:.3f}")
            self.y_act_var.set(f"{y_act:.3f}")
            self.moving_var.set("")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def go_to_up(self): 
        try:
            y_act = amc.move.getPosition(2) / 1000
            amc.move.setControlTargetPosition(2, int((y_act+ystpp) * 1000))
            wait_until_stable()
            y_act = amc.move.getPosition(2) / 1000
            self.y_act_var.set(f"{y_act:.3f}")
        except Exception as e:
                    messagebox.showerror("Error", str(e))
    def go_to_down(self): 
        try:
            y_act = amc.move.getPosition(2) / 1000
            amc.move.setControlTargetPosition(2, int((y_act-ystpp) * 1000))
            wait_until_stable()   
            y_act = amc.move.getPosition(2) / 1000
            self.y_act_var.set(f"{y_act:.3f}")
        except Exception as e:
                    messagebox.showerror("Error", str(e))
    def go_to_left(self): 
        try:
            x_act = amc.move.getPosition(0) / 1000
            amc.move.setControlTargetPosition(0, int((x_act-xstpp) * 1000))
            wait_until_stable()   
            x_act = amc.move.getPosition(0) / 1000
            self.x_act_var.set(f"{x_act:.3f}")

        except Exception as e:
                    messagebox.showerror("Error", str(e))
    def go_to_right(self, direction=None): 
        try:
            x_act = amc.move.getPosition(0) / 1000
            amc.move.setControlTargetPosition(0, int((x_act+xstpp) * 1000))
            wait_until_stable()   
            x_act = amc.move.getPosition(0) / 1000
            self.x_act_var.set(f"{x_act:.3f}")
        except Exception as e:
                    messagebox.showerror("Error", str(e))
                
    def go_to_fup(self): 
        try:
            #ystpp =float( self.y_step_var.get())
            f_act = amc.move.getPosition(1) / 1000
            amc.move.setControlTargetPosition(1, int((f_act+fstpp) * 1000))
            wait_until_stable()   
            f_act = amc.move.getPosition(1) / 1000
            self.f_act_var.set(f"{f_act:.3f}")
        except Exception as e:
                    messagebox.showerror("Error", str(e))
    def go_to_fdown(self): 
        try:
            #ystpp =float( self.y_step_var.get())
            f_act = amc.move.getPosition(1) / 1000
            amc.move.setControlTargetPosition(1, int((f_act-fstpp) * 1000))
            wait_until_stable()   
            f_act = amc.move.getPosition(1) / 1000
            self.f_act_var.set(f"{f_act:.3f}")
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
