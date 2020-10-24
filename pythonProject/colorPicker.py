from tkinter import *
import tkinter.messagebox as mbox
import PIL.ImageGrab
import mouse
import time
import pyperclip

red = ''
green = ''
blue = ''
HEX = ''


def debounce(s):
    def decorate(f):
        t = None

        def wrapped(*args, **kwargs):
            nonlocal t
            t_ = time.time()
            if t is None or t_ - t >= s:
                result = f(*args, **kwargs)
                t = time.time()
                return result

        return wrapped

    return decorate


# Use Thread case
# def hello():
# px, py = root.winfo_pointerxy()
# # posx, posy = pyautogui.position() :  결과는 동일하다...
# print(px, py)
# print(mouse.get_position())
# r, g, b = PIL.ImageGrab.grab().load()[px, py]
# # print(r, g, b)
# HEX = rgb_to_hex(r, g, b)
# # print(HEX)
# Timer(1.0, hello).start()


def rgb_to_hex(r, g, b):
    r, g, b = int(r), int(g), int(b)
    return '#' + hex(r)[2:].zfill(2) + hex(g)[2:].zfill(2) + hex(b)[2:].zfill(2)


def start_mouse(dummpy):
    mouse.hook(mouse_position)
    showinfo_text.set(start_info_text)


def stop_mouse(dummpy):
    mouse.unhook_all()
    showinfo_text.set(stop_info_text)


def copyToClipboard(rgb_text):
    global red
    global green
    global blue
    global HEX
    if rgb_text == 'rgb' and red and green and blue:
        pyperclip.copy('rgb(' + str(red) + ',' + str(green) + ',' + str(blue) + ')')
        mbox.showinfo('Done', 'RGB to Clipboard.')
    elif rgb_text == 'hex' and HEX:
        pyperclip.copy(str(HEX))
        mbox.showinfo('Done', 'HEX to Clipboard.')
    else:
        pass


@debounce(0.1)
def mouse_position(event):
    global red
    global green
    global blue
    global HEX
    # time.sleep(1)
    px, py = mouse.get_position()
    # print(event)
    red, green, blue = PIL.ImageGrab.grab().load()[px, py]
    HEX = rgb_to_hex(red, green, blue)
    message_text_A.set('rgb(' + str(red) + ',' + str(green) + ',' + str(blue) + ')')
    message_text_B.set(str(HEX))
    DisplayColorBtn.configure(bg=str(HEX))
    frameSecond.update()


default_info_text = 'Start and Wait 1sec'
start_info_text = 'Getting Pixel Color'
stop_info_text = 'Done, Check your color'

root = Tk()  # 메인창
# root.config()
w = 250  # width of tk window
h = 250  # height of tk window
ws = root.winfo_screenwidth()  # width of the windows screen
hs = root.winfo_screenheight()  # height of the windows screen
x = (ws / 2) - (w / 2)  # center X
y = (hs / 2) - (h / 2)  # center Y
root.geometry('%dx%d+%d+%d' % (w, h, x, y))
root.resizable(False, False)
root.title("PyColorPicker")  # 타이틀
root.bind('<Control-s>', start_mouse)
root.bind('<Control-x>', stop_mouse)
root.wm_attributes("-topmost", 1)  # AOT

showinfo_text = StringVar()
showinfo_text.set(default_info_text)
showinfo = Label(root, text="on the way…", bd=1, relief='flat', anchor='w', textvariable=showinfo_text)
showinfo.pack(side='bottom', fill='x', padx=10, pady=5)

frameTop = LabelFrame(root, text="Mouse")
startBtn = Button(frameTop, text="start: ctrl+s", command=lambda: start_mouse('e'), width=12)
startBtn.pack(side='left', padx=5)
stopBtn = Button(frameTop, text="stop: ctrl+x", command=lambda: stop_mouse('e'), width=12)
stopBtn.pack(side='right', padx=5)
frameTop.pack(side='top', padx=10, pady=5, ipadx=5, ipady=5)

message_text_A = StringVar()
message_text_B = StringVar()
frameSecond = LabelFrame(root, text="Result")

labelA = Label(frameSecond, text="RGB :").pack(side='top', anchor="w")
messageA = Message(frameSecond, width=150, relief="solid", textvariable=message_text_A, bg='#ffffff').pack(side='top',
                                                                                                           fill='x')

labelB = Label(frameSecond, text="HEX :").pack(side='top', anchor="w")
messageB = Message(frameSecond, width=150, relief="solid", textvariable=message_text_B, bg='#ffffff').pack(side='top',
                                                                                                           fill='x')

message_text_A.set('RGB')
message_text_B.set('HEX')

RGBclipCopyBtn = Button(frameSecond, text="rgb2clip", command=lambda: copyToClipboard('rgb'), relief="raised")
RGBclipCopyBtn.pack(side='right', padx=5)

HEXclipCopyBtn = Button(frameSecond, text="hex2clip", command=lambda: copyToClipboard('hex'), relief="raised")
HEXclipCopyBtn.pack(side='right', padx=5)

DisplayColorBtn = Button(frameSecond, width=10, text="COLOR", command=None,
                         relief="groove")  # flat, groove, raised, ridge, solid, or sunken
DisplayColorBtn.pack(side='right', padx=5)

frameSecond.pack(side='top', anchor="w", padx=10, pady=5, ipadx=5, ipady=5, fill='x')
# root.bind('<Motion>', mouse_position)
# hello()
root.mainloop()

# Tkinter key bind code
# root.bind('<Ctrl-c>', callback)
# | event                 | name                  |
# | Ctrl-c                | Control-c             |
# | Ctrl-/                | Control-slash         |
# | Ctrl-\                | Control-backslash     |
# | Ctrl+(Mouse Button-1) | Control-1             |
# | Ctrl-1                | Control-Key-1         |
# | Enter key             | Return                |
# |                       | Button-1              |
# |                       | ButtonRelease-1       |
# |                       | Home                  |
# |                       | Up, Down, Left, Right |
# |                       | Configure             |
# | window exposed        | Expose                |
# | mouse enters widget   | Enter                 |
# | mouse leaves widget   | Leave                 |
# |                       | Key                   |
# |                       | Tab                   |
# |                       | space                 |
# |                       | BackSpace             |
# |                       | KeyRelease-BackSpace  |
# | any key release       | KeyRelease            |
# | escape                | Escape                |
# |                       | F1                    |
# |                       | Alt-h                 |
