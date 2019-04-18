import tkinter as tk
from tkinter import messagebox
import random
import math


#from idlelib.ToolTip import ToolTip as Tip

class Gear:
    def __init__(self, name, cost, quantity, per_second=0, limit=0, multiplier=None, synergy_unlocked=None, synergy_building=None):
        self.gear = name
        self.cost = cost
        self.quantity = quantity
        self.per_second = per_second
        self.limit = limit
        self.multiplier=multiplier
        self.synergy_unlocked=synergy_unlocked
        self.synergy_building=synergy_building

class Clicker:
    time = 0.

    def __init__(self, parent):
        self.parent = parent
        self.purchase_buttons = {}
        self.button = tk.Button(parent, text = "Save a life", width = 20, height=5, command=self.increment, background ='cyan')
        self.current_clicks = 0
        self.current_deaths = 10000000
        self.gear = {}
        def info():
            messagebox.showinfo("Info", "Save a life adopts out one puppy and gets you one dollar\n\n" \
                                "Assistants can help you get more money each time you save a life\n\n" \
                                "Caffeine boosts make your assistants more effective\n\n" \
                                "Volunteers adopt out one puppy per second\n\n" \
                                "Giving your Volunteers Compensation makes them work harder\n\n" \
                                "Puppy helpers get themselves and others adopted too! (At a rate of 5 per second that is)\n\n" \
                                "Train your puppies to help them adopt out faster!\n\n" \
                                "Automation is the way to get adoption rates up!")

        self.info = tk.Button(parent, text = "info", width = 10, height = 5, command=info)

        def message():
            messagebox.showinfo("Tutorial", "Oh no! It looks like 10,000 puppies are being put down per second! But we can fix that! Click the Save a life button to send a puppy out for adoption. Each puppy adopted earns you 1 PupBuck to spend on other things that may help you keep the puppies from being put down. Try to make your pound one where 0 puppies per second are being put down! Good luck!")
        self.parent.after(5000, message)
        #message()
        #self.tools = {}


        #Initialize Buttons
        self.gear['assistant'] = Gear('assistant', 10, quantity = 1, limit=10)
        self.gear['coffee'] = Gear('coffee', 50, quantity = 0, limit = 5)
        self.gear['puppy trainer'] = Gear('puppy trainer', 40, quantity = 0, limit = 2)
        self.gear['compensation'] = Gear('compensation', 75, quantity = 0, limit=1) #based on assistant, helps volunteer
        self.gear['volunteer'] = Gear('volunteer', 20, 0, per_second = 1, limit=1,
                                        synergy_unlocked=self.gear['compensation'], synergy_building=self.gear['assistant'])
        self.gear['puppies'] = Gear('puppies', 100, 0, per_second = 5, limit=20, multiplier=self.gear['puppy trainer'])
        self.gear['automation'] = Gear('automation', 200, 0, per_second = 10, limit=10)

        #scrollbar
        self.upgrade_frame = tk.Frame(parent)
        self.upgrade_frame.grid(row=1, column=1, columnspan=2, rowspan=2)
        self.scrollbar = tk.Scrollbar(self.upgrade_frame, orient=tk.VERTICAL)
        self.upgrade_canvas = tk.Canvas(self.upgrade_frame, yscrollcommand=self.scrollbar.set)
        self.cframe = tk.Frame(self.upgrade_canvas)
        self.cframe.bind("<Configure>", lambda x: self.upgrade_canvas.configure(scrollregion=self.upgrade_canvas.bbox('all'), width=450, height=100))
        self.window = self.upgrade_canvas.create_window((0,0), window=self.cframe, anchor= 'nw')
        self.scrollbar.config(command=self.upgrade_canvas.yview)
        self.upgrade_canvas.grid(row=0, column=0)
        self.scrollbar.grid(row=0, column=1, sticky='NS')
        self.parent.bind('<MouseWheel>', lambda x: self.upgrade_canvas.yview_scroll(-1*(x.delta//30), 'units'))

        #Buttons
        self.purchase_buttons['assistant']= tk.Button(self.cframe, text='Assistant: (%d): 1' % self.gear['assistant'].cost,
            command=lambda: self.purchase('assistant'), background = 'magenta')
        self.purchase_buttons['coffee']= tk.Button(self.cframe, text='Caffeine boost: (%d): 0' % self.gear['coffee'].cost,
            command=lambda: self.purchase('coffee'), background = 'magenta')
        self.purchase_buttons['puppy trainer'] = tk.Button(self.cframe, text = 'Train your puppies! (%d): 0' % self.gear['puppy trainer'].cost,
            command=lambda: self.purchase('puppy trainer'), background='yellow')
        self.purchase_buttons['compensation']= tk.Button(self.cframe, text='Compensation for your volunteers (%d): 0' % self.gear['compensation'].cost,
            command=lambda: self.purchase('compensation'), background = 'yellow')
        self.purchase_buttons['volunteer'] = tk.Button(self.cframe, text = 'Volunteers (%d): 0' % self.gear['volunteer'].cost,
            command=lambda: self.purchase('volunteer'), background = 'blue')
        self.purchase_buttons['puppies'] = tk.Button(self.cframe, text = 'Puppy helpers (%d): 0' % self.gear['puppies'].cost,
            command=lambda: self.purchase('puppies'), background = 'blue')
        self.purchase_buttons['automation'] = tk.Button(self.cframe, text = 'Automation (%d): 0' % self.gear['automation'].cost,
            command=lambda: self.purchase('automation'), background = 'blue')

        #self.tooltips = {'assistant':Tip(self.purchase_buttons['assistant'], 'more clicks'),
        #                'volunteer':Tip(self.purchase_buttons['volunteer'], 'This is totally volunteer') }
        self.current_deaths_show = tk.Label(parent, text = 'Puppy Deaths\n 0')
        self.button.grid(row=0, column=0)
        self.current_deaths_show.grid(row=0, column=1)
        self.per_second_show = tk.Label(parent, text = 'Puppy Deaths/second\n 0')
        self.per_second_show.grid(row=0, column=2)
        self.current_clicks_show = tk.Label(parent, text = 'PupBucks\n 0')
        self.current_clicks_show.grid(row=1, column=0)
        self.info.grid(row=2, column=0)
        #Clicker.time.grid(row=3, column=0)



        manual_row = 0
        auto_row= 0
        for name in sorted(self.gear, key=lambda x: self.gear[x].cost):
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
        self.current_clicks += self.gear['assistant'].quantity * 2**self.gear['coffee'].quantity
        self.current_deaths_show.config(text='Puppy Deaths\n {:,}'.format(self.current_deaths-self.current_clicks))
        self.current_clicks_show.config(text='PupBucks\n {:,}'.format(self.current_clicks))


    def purchase(self, name):
        if self.current_clicks >= self.gear[name].cost:
            #print('exceeded limit', self.gear[name].limit, self.gear[name].quantity)
            self.gear[name].quantity += 1
            self.current_clicks -= self.gear[name].cost
            self.current_deaths = self.current_deaths-self.gear[name].cost
            self.gear[name].cost =int((self.gear[name].cost + 1)* 2)
            self.current_clicks_show.config(text = 'PupBucks\n {:,}'.format(self.current_clicks))
            self.current_deaths_show.config(text = 'Puppy Deaths\n {:,}'.format(self.current_deaths))
            self.purchase_buttons[name].config(
                text = self.purchase_buttons[name]['text'].split(': ')[0] + ': {:.1f}: {}'.format(
                self.gear[name].cost, self.gear[name].quantity))
            if self.gear[name].limit and self.gear[name].quantity >= self.gear[name].limit:
                self.purchase_buttons[name].config(state=tk.DISABLED)

    def update(self):
        Clicker.time += 1.
        deaths_per_second=base_deaths_per_second = 10000
        per_second=base_per_second = sum(gear.per_second*gear.quantity*(
            gear.multiplier and 2**gear.multiplier.quantity or 1) for gear in self.gear.values())-(base_deaths_per_second)
        for gear in self.gear.values():
            if gear.synergy_unlocked and gear.synergy_unlocked.quantity:
                per_second += int(gear.quantity * gear.synergy_building.quantity * 1.1)
        self.current_clicks += int(per_second+deaths_per_second)
        self.current_deaths += int(deaths_per_second)
        self.current_deaths_show.config(text = 'Puppy Deaths\n {:,}'.format(self.current_deaths-self.current_clicks))
        self.current_clicks_show.config(text = 'PupBucks\n {:,}'.format(self.current_clicks))
        self.per_second_show.config(text='Puppy Deaths/second\n {:,}'.format(int((-1)*per_second)))
        if (Clicker.time>15):
            self.Events()
        self.parent.after(1000, self.update)

    def Events(self):
        value = math.floor(10*random.random())
        print(value)
        if (value == 1. and self.gear['assistant'].quantity<10):
            messagebox.showinfo("Event 1", "Wow! You've reached a random event!! Cool beans! Assistant +1")
            self.gear['assistant'].quantity += 1
            self.gear['assistant'].cost =int((self.gear['assistant'].cost + 1)* 2)
            self.purchase_buttons['assistant'].config(
                text = self.purchase_buttons['assistant']['text'].split(': ')[0] + ': {:.1f}: {}'.format(
                self.gear['assistant'].cost, self.gear['assistant'].quantity))
            if self.gear['assistant'].limit and self.gear['assistant'].quantity >= self.gear['assistant'].limit:
                self.purchase_buttons['assistant'].config(state=tk.DISABLED)
        if(value == 2. and self.gear['assistant'].quantity>1):
            messagebox.showinfo("Event 2", "Oh no! One of your assistants has stopped caring about the cause! They quit! Assistants -1")
            self.gear['assistant'].quantity -= 1
            self.purchase_buttons['assistant'].config(
                text = self.purchase_buttons['assistant']['text'].split(': ')[0] + ': {:.1f}: {}'.format(
                self.gear['assistant'].cost, self.gear['assistant'].quantity))
            if self.gear['assistant'].limit and self.gear['assistant'].quantity >= self.gear['assistant'].limit:
                self.purchase_buttons['assistant'].config(state=tk.DISABLED)
        if(value == 3. and self.gear['volunteer'].quantity == self.gear['volunteer'].limit):
            messagebox.showinfo("Event 3", "Your place has expanded. You can get more volunteers!!")
            self.gear['volunteer'].limit += 2
            self.purchase_buttons['volunteer'].config(state=tk.NORMAL)
        if(value == 4.):
            messagebox.showinfo("Event 4", "The puppies are so adorable, everyone is inspired to work harder! Volunteers and Assistants do twice as well for the next 20 seconds!")
            self.gear['assistant'].quantity = self.gear['assistant'].quantity * 2
            self.gear['volunteer'].quantity = self.gear['volunteer'].quantity * 2

            self.gear['assistant'].quantity = self.gear['assistant'].quantity / 2
            self.gear['volunteer'].quantity = self.gear['volunteer'].quantity / 2
        #if(value == 5.):




messagebox.showinfo("Start", "Welcome to the Puppy Pound! In this game, you are the owner of a home for puppies! But money is tight, and it's hard to keep so many puppies before they have to be put down. Your job is to stop the puppies from being put down by running a successful adoption program. Good luck!")
root = tk.Tk()
clicker = Clicker(root)
root.mainloop()

#To change
#'volunteer' and 'puppies' button doesn't change the cost but just adds it to the end
#rescale all costs
#can make a for loop for buttons: video 3


#timer
#random events
#achievements
#Buttons show only when certain conditions are met?
#z[1::2, i] odd points where i is time, z[0::2] even points
