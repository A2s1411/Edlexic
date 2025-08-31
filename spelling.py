from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import random

try:
    from tts import speak
except Exception:  # Fallback no-op
    def speak(text: str):  # type: ignore
        pass


CATEGORY_DIRS = {
    "Fruits": "fruitimages",
    "Planets": "planetimages",
    "Animals": "animalimages",      # adjust if different
    "Vegetables": "vegetableimages"  # adjust if different
}

VALID_EXTS = {".jpg", ".jpeg", ".png"}


def _list_images_for_category(category: str):
    base_path = os.path.dirname(__file__)
    folder = CATEGORY_DIRS.get(category)
    if not folder:
        return [], None
    dir_path = os.path.join(base_path, folder)
    if not os.path.isdir(dir_path):
        return [], dir_path
    files = [f for f in os.listdir(dir_path) if os.path.splitext(f)[1].lower() in VALID_EXTS]
    return files, dir_path


def _normalized_label_from_filename(filename: str) -> str:
    name, _ = os.path.splitext(os.path.basename(filename))
    return name.strip().lower()


class TypingPractice:
    def __init__(self, parent: Toplevel, category: str):
        self.parent = parent
        self.category = category
        self.parent.title(f"{category} • Spelling")
        self.parent.configure(bg="#e2cffc")

        self.image_label = Label(self.parent, bg="#e2cffc")
        self.image_label.grid(row=0, column=0, columnspan=3, padx=10, pady=(10, 6))

        # Input row
        self.entry = Entry(self.parent, font=("Helvetica", 12))
        self.entry.grid(row=2, column=0, padx=10, pady=8, ipadx=40, ipady=6)
        Button(self.parent, text="Check", bg="#5b437d", fg="#ffffff", font=("Helvetica", 12, 'bold'),
               command=self.on_check).grid(row=2, column=1, padx=8, pady=8, ipadx=14, ipady=6)
        self.next_btn = Button(self.parent, text="Next", bg="#5b437d", fg="#ffffff",
                               font=("Helvetica", 12, 'bold'), command=self.on_next, state=DISABLED)
        self.next_btn.grid(row=2, column=2, padx=8, pady=8, ipadx=14, ipady=6)

        # TTS controls
        Button(self.parent, text="Hear Name", bg="#712b75", fg="#ffffff", font=("Helvetica", 11, 'bold'),
               command=self.speak_current_name).grid(row=1, column=0, columnspan=3, pady=(2, 6))

        self.current_answer = None
        self.current_photo = None
        self.answered_correctly = False

        # Inline feedback label (no popups for correct/incorrect)
        self.feedback_label = Label(self.parent, text="", bg="#e2cffc", fg="#3c1361",
                                    font=("Helvetica", 12, 'bold'))
        self.feedback_label.grid(row=3, column=0, columnspan=3, pady=(2, 8))

        self.files, self.dir_path = _list_images_for_category(self.category)
        if not self.dir_path or not os.path.isdir(self.dir_path):
            messagebox.showerror("Missing Folder", f"Folder for {self.category} not found: {self.dir_path}")
            return
        if not self.files:
            messagebox.showerror("No Images", f"No images found in {self.dir_path}")
            return
        self.load_random_image()

    def load_random_image(self):
        if not self.files:
            return
        filename = random.choice(self.files)
        path = os.path.join(self.dir_path, filename)
        try:
            img = Image.open(path)
            img = img.resize((240, 160), Image.LANCZOS)
            self.current_photo = ImageTk.PhotoImage(img)
            self.image_label.configure(image=self.current_photo)
            self.current_answer = _normalized_label_from_filename(filename)
            # Do not auto-speak the name; only speak when user presses "Hear Name"
            # Prepare entry for typing
            self.entry.delete(0, END)
            self.entry.focus_set()
            # Clear old feedback
            self.feedback_label.configure(text="", fg="#3c1361")
            # Reset correctness gate for this new image
            self.answered_correctly = False
            # Grey out Next until answered correctly
            self.next_btn.configure(state=DISABLED)
        except Exception as e:
            messagebox.showerror("Image Error", f"Unable to load image {filename}: {e}")

    def speak_current_name(self):
        if self.current_answer:
            speak(self.current_answer)

    def on_check(self):
        if not self.current_answer:
            return
        user = self.entry.get().strip().lower()
        if user == self.current_answer:
            # Mark as correct and auto-advance to the next image
            self.answered_correctly = True
            self.feedback_label.configure(
                text=f"Correct! It is '{self.current_answer.title()}'",
                fg="#1b5e20"
            )
            # Enable Next
            self.next_btn.configure(state=NORMAL)
            self.parent.after(400, self.load_random_image)
        else:
            # Block forward navigation until correct
            self.answered_correctly = False
            self.feedback_label.configure(
                text="give correct answer before moving forward",
                fg="#b00020"
            )
            # Keep Next disabled
            self.next_btn.configure(state=DISABLED)

    def on_next(self):
        # Only allow moving forward if the current item was answered correctly
        if self.answered_correctly:
            self.load_random_image()
        else:
            self.feedback_label.configure(
                text="give correct answer before moving forward",
                fg="#b00020"
            )


# Public API used by practice.py

def start_spelling_session(category: str):
    parent = Toplevel()
    TypingPractice(parent, category)
