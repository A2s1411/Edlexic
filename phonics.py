from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import random

# Try to import SpeechRecognition. If unavailable, we fail gracefully with UI hints.
try:
    import speech_recognition as sr  # type: ignore
except Exception:  # pragma: no cover
    sr = None  # fallback path

try:
    from tts import speak
except Exception:  # If TTS missing, just no-op speak
    def speak(text: str):  # type: ignore
        pass


CATEGORY_DIRS = {
    "Fruits": "fruitimages",
    "Planets": "planetimages",
    "Animals": "animalimages",      # adjust if you use a different folder name
    "Vegetables": "vegetableimages" # adjust if you use a different folder name
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


def _recognize_speech_once(parent) -> str | None:
    """Capture one utterance from the microphone and return recognized text (lowercased)."""
    if sr is None:
        messagebox.showerror(
            "Speech To Text Missing",
            "SpeechRecognition (and PyAudio) not installed.\n\n"
            "Please install: pip install SpeechRecognition PyAudio\n"
            "On Windows, PyAudio may require a prebuilt wheel."
        )
        return None

    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.6)
            speak("Please say the word now")
            audio = r.listen(source, timeout=5, phrase_time_limit=4)
        try:
            text = r.recognize_google(audio)
            return text.strip().lower()
        except sr.UnknownValueError:
            messagebox.showinfo("Try Again", "Sorry, I could not understand. Please try again.")
            return None
        except sr.RequestError:
            messagebox.showerror("Network Error", "Could not reach recognition service. Check internet connectivity.")
            return None
    except Exception as e:
        messagebox.showerror("Microphone Error", f"Problem accessing mic: {e}")
        return None


class STTPractice:
    def __init__(self, parent: Toplevel, category: str, mode: str):
        self.parent = parent
        self.category = category
        self.mode = mode  # "Phonics" or "Spelling" (both use STT for now)
        self.parent.title(f"{category} • {mode}")
        self.parent.configure(bg="#e2cffc")

        self.image_label = Label(self.parent, bg="#e2cffc")
        self.image_label.grid(row=1, column=0, columnspan=2, padx=10, pady=(6, 6))

        # Show the name of the current photo under the image
        self.name_label = Label(self.parent, text="", bg="#e2cffc", fg="#3c1361",
                                font=("Helvetica", 12, 'bold'))
        self.name_label.grid(row=2, column=0, columnspan=2, pady=(0, 8))

        self.prompt = Label(self.parent, text=f"Say the name of the picture", bg="#e2cffc", fg="#3c1361",
                             font=("Helvetica", 12, 'bold'))
        self.prompt.grid(row=0, column=0, columnspan=2, pady=(10, 4))

        Button(self.parent, text="Speak", bg="#5b437d", fg="#ffffff", font=("Helvetica", 12, 'bold'),
               command=self.on_speak).grid(row=3, column=0, padx=10, pady=8, ipadx=18, ipady=8)
        Button(self.parent, text="Next", bg="#5b437d", fg="#ffffff", font=("Helvetica", 12, 'bold'),
               command=self.load_random_image).grid(row=3, column=1, padx=10, pady=8, ipadx=20, ipady=8)

        self.current_answer = None
        self.current_photo = None  # keep reference to avoid GC

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
            # Fit into a reasonable size
            img = img.resize((240, 160), Image.LANCZOS)
            self.current_photo = ImageTk.PhotoImage(img)
            self.image_label.configure(image=self.current_photo)
            self.current_answer = _normalized_label_from_filename(filename)
            # Update the visible name under the image (title case for readability)
            self.name_label.configure(text=self.current_answer.title())
        except Exception as e:
            messagebox.showerror("Image Error", f"Unable to load image {filename}: {e}")

    def on_speak(self):
        if self.current_answer is None:
            return
        result = _recognize_speech_once(self.parent)
        if not result:
            return
        # Simple exact match; could be enhanced with fuzzy matching later
        if result == self.current_answer:
            speak("Great job! That's correct.")
            messagebox.showinfo("Correct", f"You said '{result}'. Correct!")
            self.load_random_image()
        else:
            speak("Incorrect answer.")
            self._show_incorrect_screen()

    def _show_incorrect_screen(self):
        """Show a simple error screen indicating the answer was incorrect."""
        err = Toplevel(self.parent)
        err.title("Incorrect")
        err.configure(bg="#ffebee")

        Label(err, text="Incorrect Answer", bg="#ffebee", fg="#b00020",
              font=("Helvetica", 16, 'bold')).grid(row=0, column=0, padx=16, pady=(14, 8))
        Button(err, text="OK", bg="#b00020", fg="#ffffff", font=("Helvetica", 12, 'bold'),
               command=err.destroy).grid(row=1, column=0, pady=(0, 14), ipadx=18, ipady=6)


# Public API used by practice.py

def start_phonics_session(category: str):
    parent = Toplevel()
    STTPractice(parent, category, mode="Phonics")


def start_spelling_session(category: str):
    parent = Toplevel()
    STTPractice(parent, category, mode="Spelling")
