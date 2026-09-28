import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
CORE = ROOT / 'Core_Modules'

def show_message(t, m):
    messagebox.showinfo(t, m)

def run_all():
    res = []
    for n in ['1', '2', '3', '4']:
        p = CORE / f'hw_b2b_module_0{n}_build.pyc'
        cmd = ['python3', str(p)]
        if n == '3': cmd.append('test_payload.json')
        r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
        s = 'OK' if r.returncode == 0 else 'FAILED'
        res.append(f'Module {n}: {s}')

    show_message('RUN ALL Complete', '\n'.join(res))

root = tk.Tk()
root.title('HeadWater Kit')
root.geometry('400x300')
tk.Button(root, text='Run System Check', command=lambda: show_message('Check', 'Ready'), font=('Arial', 12)).pack(pady=20)
tk.Button(root, text='Run All Modules', command=run_all, font=('Arial', 12)).pack(pady=20)
root.mainloop()
