"""
Krisann Stephany
Physics 6810 Final Project
Incremental Game: Puppy Pound

This is an incremental (moreso a decremental) game meant to utilize tkinter. There are 3 files with which I have put different versions of the game so it is easy to view all of the
different outcomes. The files are the following:

Incremental_test.py: the main version of the game
    This file has all popups and normal numbers in the game. This is to say, that events that are in place in the game happen rarely and the game should
    take a decent amount of time to play. That being said, the game is still unfinished and winning in this "normal" mode is not exactly possible/easy yet.
    The game is not yet balanced, thus, it is highly discouraged to play the game in this original version in the hopes of completing it in it's entirety
    To make the game worthwhile, more buttons would need to be added as well as events and things to do. But so far, this is what has been created. As soon
    as the program is run, a message will pop up. Then the main window will pop up. This will have all the buttons needed to play. Observe the window. After five seconds,
    another window will pop up that will describe the purpose of the game. After this, it is highly encouraged to click the "info" button to see what all the
    other buttons do. Other than that, the game is yours to play.
Incremental_test2.py: the event version of the game_entry
    This file has all the same concepts as the original, however, events are set to happen much, much more often. This version is just for the user to be able to
    experience all of the events without having to play through the full version of the game. Ideally, more events will get added to the full version in the future,
    but for now, there are six possible events that can affect the game.
Incremental_test3.py: the endgame version of the game
    Because the original version of the game is not possible to win at this time, I have included this version to show what the endgame looks like. It's nothing
    special, but it is necessary to see. To see the endgame, I have made the 'puppies saved per second' for 'volunteers' equal to 10,000. In other words, if you
    increment your PupBucks to 20 and purchase a volunteer, the number of deaths per second will be 0, thus, you will have won the game. This will bring up a message
    explaining your victory and it will close the game window.
Incremental_test4.py: the shopoholic version of the game
    This version of the game gives you 10,000 PupBucks every time you click the 'Save a Life' button. This allows the user to make many purchases very quickly. The
    purpose of this version is to allow the user to see what purchasing certain perks will do without having to wait for the PupBucks to roll in. This version may
    also allow for the endgame if done correctly, but it is not necessarily the purpose of this version.

The game has a couple of bugs:
    1. Buttons that are not magenta do not change their original price after purchase, instead, the new price is placed after the original price and then that one is
        changed with the click of that button.
    2. An extra tk window appears with each messagebox. I will continue to try to stop this from happening, but as of right now, it is out of my power.
    3. Every once in awhile, messages that are meant to take time before they appear will appear instantly after clicking "ok" on the original messagebox,
        but this may prove to not be an issue.

Overall, I plan to continue to add to the game and create more dependencies between events, fetch, and the decrementation. But for now, this is it.
"""
