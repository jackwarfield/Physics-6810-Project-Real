import tkinter as tk

class Gear:
    def __init__(self, name, cost, quantity, per_second=0):
        self.gear = name
        self.cost = cost
        self.quantity = quantity
        self.per_second = per_second

class Clicker:
    def __init__(self, parent):
        self.parent = parent
        self.purchase_buttons = {}
        self.button = tk.Button(parent, text = "Tap", width = 20, height=5, command=self.increment)
        self.current_clicks = 0
        self.gear = {}
        self.tools = {}
        self.gear['clicker'] = Gear('clicker', 10, quantity = 1)
        self.gear['something'] = Gear('something', 20, 0, per_second = 1)
        self.purchase_buttons['clicker']= tk.Button(parent, text='Hits (%d): 0' % self.gear['clicker'].cost,
            command=lambda: self.purchase('clicker'))
        self.purchase_buttons['something'] = tk.Button(parent, text = 'Something (%d): 0' % self.gear['something'].cost,
            command=lambda: self.purchase('something'))
        self.current_click_show = tk.Label(parent, text = '0')
        self.button.grid(row=0, column=0)
        self.current_click_show.grid(row=1, column=0)
        manual_row = -1
        auto_row=-1
        for name in self.gear:
            if self.gear[name].per_second:
                manual_row += 1
                row = manual_row
                column = 2
            else:
                auto_row += 1
                row = auto_row
                column = 1
            self.purchase_buttons[name].grid(row=row, column=column)

        self.update()

    def increment(self):
        self.current_clicks += self.gear['clicker'].quantity
        self.current_click_show.config(text='%d' % self.current_clicks)
    def purchase(self, name):
        if self.current_clicks >= self.gear[name].cost:
            self.gear[name].quantity += 1
            self.current_clicks -= self.gear[name].cost
            self.current_click_show.config(text = '%d' % self.current_clicks)
            self.purchase_buttons[name].config(
                text = self.purchase_buttons[name]['text'].split(':')[0] + ': %d' % self.gear[name].quantity)

    def update(self):
        for gear in self.gear.values():
            self.current_clicks += gear.per_second*gear.quantity
        self.current_click_show.config(text = '%d' % self.current_clicks)
        self.parent.after(1000, self.update)

root = tk.Tk()
clicker = Clicker(root)
root.mainloop()
