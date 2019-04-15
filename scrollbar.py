import tkinter as tk

class Scroll_Bar:
    def __init__(self, parent):
        self.parent = parent
        self.scrollbar=tk.Scrollbar(parent, orient=tk.VERTICAL)
        self.canvas = tk.Canvas(parent, yscrollcommand=self.scrollbar.set, background='green')
        self.frame = tk.Frame(self.canvas)
        self.frame.bind("<Configure>", lambda x: self.canvas.configure(scrollregion=self.canvas.bbox('all'), width=200, height=200))
        self.window = self.canvas.create_window((0,0), window=self.frame, anchor= 'nw')
        self.scrollbar.config(command=self.canvas.yview)
        self.canvas.grid(row=0, column=0)
        self.scrollbar.grid(row=0, column=1, sticky='NS')
        self.parent.bind('<MouseWheel>', lambda x: self.canvas.yview_scroll(-1*(x.delta//30), 'units'))
        self.labels = []
        for i in range(30):
            self.labels.append(tk.Label(self.frame, text=str(i)))
            self.labels[-1].grid(row=i, column=0)

root = tk.Tk()
scrollbar = Scroll_Bar(root)
root.mainloop()
