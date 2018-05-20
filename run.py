import threading
import tkinter.font
from tkinter import *

from iot_locker_gui.connector import get_value

root = Tk()
root.overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.focus_set()  # <-- move focus to this widget
root.bind("<Escape>", lambda e: e.widget.quit())
root.title('IoT Locker')
helv36 = tkinter.font.Font(family='Helvetica', size=16, weight='bold')
consolas = tkinter.font.Font(family='Consolas', size=12)

# Debug Panel
S = Scrollbar(root)
T = Text(root, font=consolas, width=30)
S.pack(side=RIGHT, fill=Y)
T.pack(side=RIGHT, fill=Y)
S.config(command=T.yview)
T.config(yscrollcommand=S.set)
S.config(command=T.yview)
T.config(yscrollcommand=S.set)
## Debug panel END


# uncomment this two line[29-30] to hide the debug panel
# T.pack_forget()
# S.pack_forget()


# lockers and buttons
buttons = {}
lockers = "ABCDEFGHIJKLMNOPQRSTUVWX"
lockers = [val for val in lockers]
lockers.append('?')
button_identities = []


def change_other_buttons():
    str_val = get_value('?')
    if str_val.find('COM_PORT_ERROR') >= 0:
        T.insert(END, str_val+'\n')
        return

    # comment this line[48] to run the actual code
    # str_val = str(randint(0,16777215))

    try:
        str_val = str_val.decode()
    except AttributeError:
        print('Not Enocoded')

    # changing attributes of buttons
    proned_val = str_val.replace('\n', '').replace('\r', '')
    bit_string = "{0:b}".format(int(proned_val))
    bit_string = bit_string[::-1]  # as the LSB of binary is 0th locker
    bit_string_len = len(bit_string)
    for i in range(bit_string_len):

        if bit_string[i] == '1':
            btn = button_identities[i]
            btn.config(state=NORMAL)
            btn.config(bg='green')
        elif bit_string[i] == '0':
            btn = button_identities[i]
            btn.config(state=DISABLED)
            btn.config(bg='red')

        out = 'Locker No: ' + str(i + 1) + ': ' + bit_string[i] + '\n'
        T.insert(END, out)


def handler(id, btn):
    if btn['text'] == '?':
        change_other_buttons()
        return

    if btn['state'] == DISABLED:
        return
    get_value(btn['text'])
    btn.config(state=DISABLED)
    out = 'Clicked On Button:' + btn['text'] + '\n'
    T.insert(END, out)
    try:
        btn.config(bg='red')
    except TypeError:
        print('already red')


def makeChoice(event):
    global buttons
    global lockers
    global button_identities
    idx = [buttons[event.widget]][0]
    btn = button_identities[idx]
    handler(idx, btn)


def createBoard():
    global buttons
    buttonNum = 0
    initial_x = -1200
    width = 8
    height = 3
    del_y = 110
    del_x = 150
    x = initial_x
    y = 100
    bg = 'green'
    for b in range(5):
        for b2 in range(5):
            if buttonNum == 24: bg = 'blue'

            button = Button(root, text=lockers[buttonNum], font=helv36, width=width, height=height, bg=bg, fg='white');
            button.place(relx=1, x=x, y=y)
            buttons[button] = buttonNum
            buttonNum += 1
            button.bind("<Button-1>", makeChoice)
            button_identities.append(button)

            x += del_x
        x = initial_x
        y += del_y


def timer():
    threading.Timer(1, timer).start()
    change_other_buttons()


createBoard()

# uncomment this to call '?' (update locker status) with 1 sec interval
# timer()

root.mainloop()
