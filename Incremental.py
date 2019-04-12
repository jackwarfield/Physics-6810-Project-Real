import tkinter as tk
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
    def __init__(self, parent):
        self.parent = parent
        self.purchase_buttons = {}
        self.button = tk.Button(parent, text = "Tap", width = 20, height=5, command=self.increment, background ='cyan')
        self.current_clicks = 0
        self.gear = {}
        #self.tools = {}
        self.gear['clicker'] = Gear('clicker', 10, quantity = 1, limit=100)
        self.gear['clicker upgrade'] = Gear('clicker upgrade', 50, quantity = 0, limit = 5)
        self.gear['puppy trainer'] = Gear('puppy trainer', 40, quantity = 0, limit = 2)
        self.gear['addition'] = Gear('addition', 75, quantity = 0, limit=1) #based on clicker, helps something
        self.gear['something'] = Gear('something', 20, 0, per_second = 1,
                                        synergy_unlocked=self.gear['addition'], synergy_building=self.gear['clicker'])
        self.gear['want'] = Gear('want', 100, 0, per_second = 5, limit=20, multiplier=self.gear['puppy trainer'])
        self.gear['need'] = Gear('need', 200, 0, per_second = 10, limit=10)

        ''' for name, description in (('clicker', 'Hits: (%d): 0'),
                                  ('clicker upgrade', 'Two handed hit: (%d): 0'),
                                  ('something', 'Something (%d): 0'),
                                  ('want', 'You want this (%d): 0'))
            self.purchase_buttons['name']= tk.Button(parent,
                                           text=description % self.gear[name].cost,
                                           command=lamda: x=name: self.purchase(x))
        '''

        self.purchase_buttons['clicker']= tk.Button(parent, text='Hits: (%d): 0' % self.gear['clicker'].cost,
            command=lambda: self.purchase('clicker'), background = 'magenta')
        self.purchase_buttons['clicker upgrade']= tk.Button(parent, text='Two handed hit: (%d): 0' % self.gear['clicker upgrade'].cost,
            command=lambda: self.purchase('clicker upgrade'), background = 'magenta')
        self.purchase_buttons['puppy trainer'] = tk.Button(parent, text = 'Here come the puppies! (%d): 0' % self.gear['puppy trainer'].cost,
            command=lambda: self.purchase('puppy trainer'), background='yellow')
        self.purchase_buttons['addition']= tk.Button(parent, text='Give a boost: (%d): 0' % self.gear['addition'].cost,
            command=lambda: self.purchase('addition'), background = 'yellow')
        self.purchase_buttons['something'] = tk.Button(parent, text = 'Something (%d): 0' % self.gear['something'].cost,
            command=lambda: self.purchase('something'), background = 'blue')
        self.purchase_buttons['want'] = tk.Button(parent, text = 'You want this (%d): 0' % self.gear['want'].cost,
            command=lambda: self.purchase('want'), background = 'blue')
        self.purchase_buttons['need'] = tk.Button(parent, text = 'You need this (%d): 0' % self.gear['need'].cost,
            command=lambda: self.purchase('need'), background = 'blue')

        #self.tooltips = {'clicker':Tip(self.purchase_buttons['clicker'], 'more clicks'),
        #                'something':Tip(self.purchase_buttons['something'], 'This is totally something') }
        self.current_click_show = tk.Label(parent, text = '0')
        self.button.grid(row=0, column=0)
        self.current_click_show.grid(row=0, column=1)
        self.per_second_show = tk.Label(parent, text = '0')
        self.per_second_show.grid(row=0, column=2)
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
        self.current_clicks += self.gear['clicker'].quantity * 2**self.gear['clicker upgrade'].quantity
        self.current_click_show.config(text='{:,}'.format(self.current_clicks))

    def purchase(self, name):
        if self.current_clicks >= self.gear[name].cost:
            #print('exceeded limit', self.gear[name].limit, self.gear[name].quantity)
            self.gear[name].quantity += 1
            self.current_clicks -= self.gear[name].cost
            self.gear[name].cost =int((self.gear[name].cost + 1)* 2)
            self.current_click_show.config(text = '{:,}'.format(self.current_clicks))
            self.purchase_buttons[name].config(
                text = self.purchase_buttons[name]['text'].split(': ')[0] + ': {:.1f}: {}'.format(
                self.gear[name].cost, self.gear[name].quantity))
            if self.gear[name].limit and self.gear[name].quantity >= self.gear[name].limit:
                self.purchase_buttons[name].config(state=tk.DISABLED)

    def update(self):
        per_second=base_per_second = sum(gear.per_second*gear.quantity*(
            gear.multiplier and 2**gear.multiplier.quantity or 1) for gear in self.gear.values())
        for gear in self.gear.values():
            if gear.synergy_unlocked and gear.synergy_unlocked.quantity:
                per_second += gear.quantity * gear.synergy_building.quantity * 2 * base_per_second
        self.current_clicks += int(per_second)
        self.current_click_show.config(text = '{:,}'.format(self.current_clicks))
        self.per_second_show.config(text='{:,}'.format(int(per_second)))
        self.parent.after(1000, self.update)

root = tk.Tk()
clicker = Clicker(root)
root.mainloop()


#To change
#change names and make an actual story
#'something' and 'want' button doesn't change the cost but just adds it to the end
#rescale all costs
#clicker upgrade button needs to not be so powerful
#re-enable button after a certain point?
#can make a for loop for buttons: video 3
