import tkinter as tk
from tkinter import messagebox
from tkinter import *
from math import *
from tkinter import simpledialog
import random
import math



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
    #global variables for games and timekeeping
    time = 0.
    event_time = 0.
    event4_flag = False
    event6_flag = False
    event7_flag = False
    game_entry = 0.
    game_flag = False
    game_time = 0.

    def __init__(self, parent):
        #initial button and clicker numbers
        self.parent = parent
        self.purchase_buttons = {}
        self.button = tk.Button(parent, text = "Save a life", width = 20, height=5, command=self.increment, background ='cyan')
        self.current_clicks = 0
        self.PupBucks = 0
        self.current_deaths = 0
        self.gear = {}
        def info():
            #info message
            messagebox.showinfo("Info", "Save a life adopts out one puppy and gets you one PupBuck\n\n" \
                                "Assistants can help you get more PupBucks each time you save a life\n\n" \
                                "Caffeine boosts make your assistants more effective\n\n" \
                                "Volunteers adopt out one puppy per second\n\n" \
                                "Giving your Volunteers Compensation makes them work harder\n\n" \
                                "Basing your commercials on people's sympathy really gets adoption rates up!\n\n" \
                                "Multiple puppies in endorsements? Who could say no? Double the help from endorsements!\n\n" \
                                "Puppy helpers get themselves and others adopted too! (At a rate of 5 per second that is)\n\n" \
                                "Train your puppies to help them adopt out faster!\n\n" \
                                "Advertisements are the way to get adoption rates up! Adopts out 10 puppies per second\n\n" \
                                "Commercials pull at the heartstrings! People adopt 50 puppies per second!\n\n" \
                                "Endorsements from celebrities is a must! Celebrities with puppies? Who could resist? Saves 100 puppies per second!")



        def message():
            #tutorial message
            messagebox.showinfo("Tutorial", "Oh no! It looks like throughout the country, 10,000 puppies are being put down per second! But we can fix that! Click the Save a life button to send a puppy out for adoption. Each puppy adopted earns you 1 PupBuck to spend on other things that may help you keep the puppies from being put down. Try to make your pound successful enough that 0 puppies per second are being put down! Good luck!")


        def game():
            #fetch button command
            window = tk.Tk()
            window.withdraw()
            Clicker.game_flag = True
            Clicker.game_entry = simpledialog.askfloat("entry", "How fast would you like to throw the ball? (In meters per second)")



        #extra buttons (and tutorial message)
        self.info = tk.Button(parent, text = "info", width = 10, height = 5, command=info)
        self.parent.after(5000, message)
        self.game = tk.Button(parent, text = "Play Fetch!", width = 10, height = 5, command=game)

        #Initialize Buttons
        self.gear['assistant'] = Gear('assistant', 10, quantity = 1, limit=10)
        self.gear['coffee'] = Gear('coffee', 50, quantity = 0, limit = 5)
        self.gear['puppy trainer'] = Gear('puppy trainer', 40, quantity = 0, limit = 2) #multiplier for puppies
        self.gear['compensation'] = Gear('compensation', 75, quantity = 0, limit=1) #based on assistant, helps volunteer
        self.gear['sympathies'] = Gear('sympathies', 20000, quantity = 0, limit=1) #based on puppies, helps commericals
        self.gear['multiple_puppies'] = Gear('multiple_puppies', 40000, quantity = 0, limit=3) #based on puppies, helps commericals
        self.gear['volunteer'] = Gear('volunteer', 20, 0, per_second = 10000, limit=99,
                                        synergy_unlocked=self.gear['compensation'], synergy_building=self.gear['assistant'])
        self.gear['puppies'] = Gear('puppies', 100, 0, per_second = 5, limit=20, multiplier=self.gear['puppy trainer'])
        self.gear['advertisement'] = Gear('advertisement', 200, 0, per_second = 10, limit=10)
        self.gear['commercial'] = Gear('commercial', 1000, 0, per_second = 50, limit=5,
                                        synergy_unlocked=self.gear['sympathies'], synergy_building=self.gear['puppies'])
        self.gear['endorsement'] = Gear('endorsement', 10000, 0, per_second = 100, limit=3, multiplier=self.gear['multiple_puppies'])

        #scrollbar
        self.upgrade_frame = tk.Frame(parent)
        self.upgrade_frame.grid(row=1, column=1, columnspan=2, rowspan=3)
        self.scrollbar = tk.Scrollbar(self.upgrade_frame, orient=tk.VERTICAL)
        self.upgrade_canvas = tk.Canvas(self.upgrade_frame, yscrollcommand=self.scrollbar.set)
        self.cframe = tk.Frame(self.upgrade_canvas)
        self.cframe.bind("<Configure>", lambda x: self.upgrade_canvas.configure(scrollregion=self.upgrade_canvas.bbox('all'), width=450, height=150))
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
        self.purchase_buttons['sympathies']= tk.Button(self.cframe, text='Play to sympathies (%d): 0' % self.gear['sympathies'].cost,
            command=lambda: self.purchase('sympathies'), background = 'yellow')
        self.purchase_buttons['multiple_puppies']= tk.Button(self.cframe, text='Multiple puppies for endorsements (%d): 0' % self.gear['multiple_puppies'].cost,
            command=lambda: self.purchase('multiple_puppies'), background = 'yellow')
        self.purchase_buttons['volunteer'] = tk.Button(self.cframe, text = 'Volunteers (%d): 0' % self.gear['volunteer'].cost,
            command=lambda: self.purchase('volunteer'), background = 'blue')
        self.purchase_buttons['puppies'] = tk.Button(self.cframe, text = 'Puppy helpers (%d): 0' % self.gear['puppies'].cost,
            command=lambda: self.purchase('puppies'), background = 'blue')
        self.purchase_buttons['advertisement'] = tk.Button(self.cframe, text = 'Advertisements (%d): 0' % self.gear['advertisement'].cost,
            command=lambda: self.purchase('advertisement'), background = 'blue')
        self.purchase_buttons['commercial'] = tk.Button(self.cframe, text = 'Commercials (%d): 0' % self.gear['commercial'].cost,
            command=lambda: self.purchase('commercial'), background = 'blue')
        self.purchase_buttons['endorsement'] = tk.Button(self.cframe, text = 'Endorsements (%d): 0' % self.gear['endorsement'].cost,
            command=lambda: self.purchase('endorsement'), background = 'blue')


        #gridding in window
        self.current_deaths_show = tk.Label(parent, text = 'Puppy Deaths\n 0')
        self.button.grid(row=0, column=0)
        self.current_deaths_show.grid(row=0, column=1)
        self.per_second_show = tk.Label(parent, text = 'Puppy Deaths/second\n 0')
        self.per_second_show.grid(row=0, column=2)
        self.PupBucks_show = tk.Label(parent, text = 'PupBucks\n 0')
        self.PupBucks_show.grid(row=1, column=0)
        self.info.grid(row=2, column=0)
        self.game.grid(row=3, column=0)

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
        #natural incrementation and decrementation for the game quantities
        self.PupBucks += self.gear['assistant'].quantity * 2**self.gear['coffee'].quantity
        self.current_clicks += self.gear['assistant'].quantity * 2**self.gear['coffee'].quantity
        self.current_deaths_show.config(text='Puppy Deaths\n {:,}'.format(self.current_deaths-self.current_clicks))
        self.PupBucks_show.config(text='PupBucks\n {:,}'.format(self.PupBucks))


    def purchase(self, name):
        #actions when purchases are made
        if self.PupBucks >= self.gear[name].cost:
            self.gear[name].quantity += 1
            self.PupBucks -= self.gear[name].cost
            self.gear[name].cost =int((self.gear[name].cost + 1)* 2)
            self.PupBucks_show.config(text = 'PupBucks\n {:,}'.format(self.PupBucks))
            self.purchase_buttons[name].config(
                text = self.purchase_buttons[name]['text'].split(': ')[0] + ': {:.1f}: {}'.format(
                self.gear[name].cost, self.gear[name].quantity))
            if self.gear[name].limit and self.gear[name].quantity >= self.gear[name].limit:
                self.purchase_buttons[name].config(state=tk.DISABLED)

    def update(self):
        #natural updater of game, updates every second
        Clicker.time += 1.
        deaths_per_second=base_deaths_per_second = 10000
        per_second=base_per_second = sum(gear.per_second*gear.quantity*(
            gear.multiplier and 2**gear.multiplier.quantity or 1) for gear in self.gear.values())-(base_deaths_per_second)
        for gear in self.gear.values():
            if gear.synergy_unlocked and gear.synergy_unlocked.quantity:
                per_second += int(gear.quantity * gear.synergy_building.quantity * 1.2)
        self.current_clicks += int(per_second+deaths_per_second)
        self.PupBucks += int(per_second+deaths_per_second)
        self.current_deaths += int(deaths_per_second)
        self.current_deaths_show.config(text = 'Puppy Deaths\n {:,}'.format(self.current_deaths-self.current_clicks))
        self.PupBucks_show.config(text = 'PupBucks\n {:,}'.format(self.PupBucks))
        self.per_second_show.config(text='Puppy Deaths/second\n {:,}'.format(int((-1)*per_second)))

        #End of Puppy Pound Game
        def endgame():
            messagebox.showinfo("End", "Congratulations! You have successfully created a pound where all the puppies in the country can live happily! And only " + str(self.current_deaths-self.current_clicks) + " died for the cause! You also ended with " + str(self.PupBucks) + " PupBucks in your pocket! I'm sure the puppies are ecstatic! Nice going! You're pawsome!")
            root.destroy()
        if((-1)*per_second < 1):
            endgame()

        #Fetch Updates
        if (Clicker.game_flag == True and Clicker.game_entry):
            self.game.config(state=DISABLED)
            if (Clicker.game_time <= 5):
                Clicker.game_time += 1
            else:
                self.game.config(state=NORMAL)
                Clicker.game_flag = False
                Clicker.game_time = 0.
                calc_time = 0.64 #(Assuming the player throws from about 2meter height)
                distance = Clicker.game_entry * calc_time
                #Scenarios
                if (Clicker.game_entry <= 10):
                    messagebox.showinfo("Game1", "Wow you threw the ball " + str(distance) + " meters! And look! The puppy brought back something with the ball! It's 5 PupBucks!")
                    self.PupBucks = int((self.PupBucks + 5))
                    self.PupBucks_show.config(text = 'PupBucks\n {:,}'.format(self.PupBucks))
                if (Clicker.game_entry <= 20 and Clicker.game_entry > 10):
                    if (self.gear['volunteer'].limit and self.gear['volunteer'].quantity < self.gear['volunteer'].limit):
                        messagebox.showinfo("Game2a", "Wow you threw the ball " + str(distance) + " meters! And look! The puppy brought back something with the ball! It's a volunteer! How lucky!")
                        self.gear['volunteer'].quantity += 1
                        self.gear['volunteer'].cost =int((self.gear['volunteer'].cost + 1)* 2)
                        self.purchase_buttons['volunteer'].config(
                            text = self.purchase_buttons['volunteer']['text'].split(': ')[0] + ': {:.1f}: {}'.format(
                            self.gear['volunteer'].cost, self.gear['volunteer'].quantity))
                        if self.gear['volunteer'].limit and self.gear['volunteer'].quantity >= self.gear['volunteer'].limit:
                            self.purchase_buttons['volunteer'].config(state=tk.DISABLED)
                    else:
                        messagebox.showinfo("Game2b", "Wow you threw the ball " + str(distance) + " meters! The puppy looks so happy as it drops the now slobbery ball into your hand and trots away.")
                if (Clicker.game_entry <= 50 and Clicker.game_entry > 20):
                    messagebox.showinfo("Game3", "Wow you threw the ball " + str(distance) + " meters! The puppy had a really fun time finding the ball!")
                if (Clicker.game_entry > 50):
                    messagebox.showinfo("Game4", "You threw the ball really far. " + str(distance) + " meters. And because it's so far, it looks like the puppy isn't coming back... You lost one puppy... and the ball... no more fetch")
                    self.current_deaths += 1
                    self.current_deaths_show.config(text = 'Puppy Deaths\n {:,}'.format(self.current_deaths-self.current_clicks))
                    self.game.config(state=DISABLED)
                Clicker.game_entry = 0.

        #Event Updates
        if (Clicker.time>10):
            self.Events()
        if (Clicker.event4_flag):
            if (Clicker.event_time <= 20):
                Clicker.event_time += 1
            else:
                Clicker.event_time = 0
                Clicker.event4_flag = False
                self.gear['assistant'].quantity = self.gear['assistant'].quantity / 2
                self.gear['volunteer'].quantity = self.gear['volunteer'].quantity / 2
        if (Clicker.event6_flag):
            if (clicker.event_time <= 5):
                Clicker.event_time += 1
            else:
                value6 = random.random()
                if (value6 >= 0.5):
                    messagebox.showinfo("Event 6a", "Oh no! The billionaire's puppy food was expired! Many puppies get tummy aches and you have to pay for their care. Cut your PupBucks in half")
                    self.PupBucks = int((self.PupBucks + int(per_second+deaths_per_second))/2)
                    self.PupBucks_show.config(text = 'PupBucks\n {:,}'.format(self.PupBucks))
                    Clicker.event_time = 0
                    Clicker.event6_flag = False
                else:
                    messagebox.showinfo("Event 6b", "That puppy food was incredible! Your puppies look so happy and healthy that a bunch got adopted. Double your PupBucks!")
                    self.PupBucks = int((self.PupBucks + int(per_second+deaths_per_second))*2)
                    self.PupBucks_show.config(text = 'PupBucks\n {:,}'.format(self.PupBucks))
                    Clicker.event_time = 0
                    Clicker.event6_flag = False

        self.parent.after(1000, self.update)

    def Events(self):
        #Random Events that occur
        value = math.floor(1000*random.random())
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
        if(value == 4. and Clicker.event4_flag == False):
            Clicker.event4_flag = True
            messagebox.showinfo("Event 4", "The puppies are so adorable, everyone is inspired to work harder! Volunteers and Assistants do twice as well for the next 20 seconds!")
            self.gear['assistant'].quantity = self.gear['assistant'].quantity * 2
            self.gear['volunteer'].quantity = self.gear['volunteer'].quantity * 2
        if(value == 5.):
            messagebox.showinfo("Event 5", "Oh no! An outbreak Puppitis has been spotted! 150,000 were affected and passed on to the big farm in the sky.")
            self.current_deaths = self.current_deaths + 150000
            self.current_deaths_show.config(text = 'Puppy Deaths\n {:,}'.format(self.current_deaths-self.current_clicks))
        if(value == 6. and Clicker.event6_flag == False):
            Clicker.event6_flag = True
            messagebox.showinfo("Event 6", "Some strange billionaire donated some high class puppy food to your pound. Your puppies eat it excitedly. Look at their tails wag!")




#Beginning of game message and game start
messagebox.showinfo("Start", "Welcome to the Puppy Pound! In this game, you are the owner of a home for puppies! But money is tight, and it's hard to keep so many puppies before they have to be put down. Your job is to stop the puppies from being put down by running a successful adoption program. Good luck!")
root = tk.Tk()
clicker = Clicker(root)
root.mainloop()

#To change
#'volunteer' and 'puppies' button doesn't change the cost but just adds it to the end
#rescale all costs
