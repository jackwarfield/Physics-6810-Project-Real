import sys
sys.path.append("C:/Users/krist/Downloads/Physics 6810 Project")
sys.path.append("C:/Users/krist/Downloads/Physics 6810 Project/appJar")
from appJar import gui
print ("Hello World")
test = gui("Rock")

test.addLabel("Hit", "......you are alone......")

flag = 0

count = 0

def hit(button):
    global count
    global flag
    flag = 0
    count = count+1
    if (count == 1):
        test.setLabel("Hit", "You see a hammer at your feet and rock to your left")
    if (count == 2):
        test.setLabel("Hit", "You pick up the hammer and begin to hit the rock")
        test.setButton("Continue", "Hit")
    if (2 < count < 12):
        test.setLabel("Hit", "Hits = " +str(count-2))
    if (count == 12):
        test.setLabel("Hit", "You have a pile of pebbles")
    if (12 < count < 22):
        test.setLabel("Hit", "Hits = " +str(count-2))
    if (count == 22):
        test.setLabel("Hit", "You have dust")
    if (count == 23):
        flag = True
        test.addLabel("Refine", "You can refine the dust")
        test.addButton("Refine", refine)
    if (flag == True):
        test.setLabel("Hit", "Hits = " +str(count-2))
        test.setButton("Refine", refine)


ref = 0
def refine(button):
    global ref
    global count
    ref = ref + 1
    count = count - 10
    if (count >= 10):
        test.setLabel("Refine", "Refined " + str(ref) + " times")
        test.setLabel("Hit", "Hits = " +str(count-2))
    if (count < 10):
        test.setLabel("Refine", "Need more dust for further refinement")
        test.setLabel("Hit", "Hits = " +str(count-2))








test.addButton("Continue", hit)



if flag:
    test.addButton("Refine", launch)
    test.startSubWindow("Refinement")
    test.addButton("more?", refine)
    test.addLabel("Refinement")
    test.stopSubWindow()

test.go()
