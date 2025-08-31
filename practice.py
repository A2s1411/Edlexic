from tkinter import *
from tkinter import messagebox
from tkvideo import tkvideo
from tts import speak
from phonics import start_phonics_session
from spelling import start_spelling_session


def practice_main():
    root=Toplevel()
    root.configure(bg='#e2cffc')
    root.title("PRACTICE")
    root.geometry("360x640")
    # Background video (same as ed.py for consistency)
    bg_label = Label(root)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    player = tkvideo("mainwindowbackvid1.mp4", bg_label, loop=1, size=(360, 640))
    player.play()

    def open_categories():
        """Opens the categories view: Fruits, Planets, Animals, Vegetables."""
        frame = Frame(root, bg='#cab5e8', relief=RAISED)
        frame.place(x=180, y=250, anchor='center')

        btn = Button(frame, text="FRUITS", bg='#712b75', fg='#ffffff',
                     font=("Helvetica", 12, 'bold'), command=lambda: open_practice_options("Fruits"))
        btn.grid(row=0, column=0, padx=10, pady=5, ipadx=40, ipady=30)

        btn = Button(frame, text="PLANETS", bg='#712b75', fg='#ffffff',
                     font=("Helvetica", 12, 'bold'), command=lambda: open_practice_options("Planets"))
        btn.grid(row=0, column=1, padx=10, pady=5, ipadx=33, ipady=30)

        btn = Button(frame, text="ANIMALS", bg='#712b75', fg='#ffffff',
                     font=("Helvetica", 12, 'bold'), command=lambda: open_practice_options("Animals"))
        btn.grid(row=1, column=0, padx=10, pady=5, ipadx=33, ipady=30)

        btn = Button(frame, text="VEGETABLES", bg='#712b75', fg='#ffffff',
                     font=("Helvetica", 12, 'bold'), command=lambda: open_practice_options("Vegetables"))
        btn.grid(row=1, column=1, padx=10, pady=5, ipadx=16, ipady=30)

    def open_practice_options(category_name: str):
        """For a category, open a window with Phonics and Spelling practice options."""
        win = Toplevel(root)
        win.title(f"{category_name} • Practice")
        win.configure(bg='#e2cffc')

        Label(win, text=f"{category_name} - Choose Practice Mode", bg='#e2cffc',
              fg='#3c1361', font=("Helvetica", 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=(12, 10), padx=10)

        Button(win, text="PHONICS", bg='#5b437d', fg='#ffffff', font=("Helvetica", 12, 'bold'),
               command=lambda: start_phonics(category_name)).grid(row=1, column=0, padx=10, pady=10, ipadx=24, ipady=12)

        Button(win, text="SPELLING", bg='#5b437d', fg='#ffffff', font=("Helvetica", 12, 'bold'),
               command=lambda: start_spelling(category_name)).grid(row=1, column=1, padx=10, pady=10, ipadx=22, ipady=12)

        Label(win, text="(These are placeholders. We can wire these to real practice flows.)",
              bg='#e2cffc', fg='#5b437d', font=("Helvetica", 9, 'italic')).grid(row=2, column=0, columnspan=2, pady=(4, 12))

    def start_phonics(category: str):
        # Launch speech-to-text phonics session
        start_phonics_session(category)

    def start_spelling(category: str):
        # Launch speech-to-text spelling session (same engine currently)
        start_spelling_session(category)

    # Show categories immediately when Practice screen opens
    open_categories()

    root.mainloop()


# Uncomment to run this screen standalone for quick testing
# if __name__ == "__main__":
#     root = Tk()
#     root.withdraw()  # hide main if running from a larger app
#     practice_main()
