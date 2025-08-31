from tkinter import *
from tts import speak
from PIL import Image, ImageTk
import os

def planets():
    root2 = Toplevel()
    root2.configure(bg='#e2cffc')
    root2.title("PLANETS")

    base_path = os.path.dirname(__file__)
    planet_images = [
        os.path.join(base_path, "planetimages", "Mercury.jpg"),
        os.path.join(base_path, "planetimages", "Venus.jpg"),
        os.path.join(base_path, "planetimages", "Earth.jpg"),
        os.path.join(base_path, "planetimages", "Mars.jpg"),
        os.path.join(base_path, "planetimages", "Jupiter.jpg"),
        os.path.join(base_path, "planetimages", "Saturn.jpg"),
        os.path.join(base_path, "planetimages", "Uranus.jpg"),
        os.path.join(base_path, "planetimages", "Neptune.jpg")
    ]

    # Open and resize images
    images = []
    for img_path in planet_images:
        img = Image.open(img_path)
        img = img.resize((150, 100), Image.LANCZOS)
        photo_img = ImageTk.PhotoImage(img)
        images.append(photo_img)

    # Create labels and buttons
    planets = ["MERCURY", "VENUS", "EARTH", "MARS", "JUPITER", "SATURN", "URANUS", "NEPTUNE"]
    tts_spelling = {
        "MERCURY": ["M", "E", "R", "C", "U", "R", "Y", "MERCURY"],
        "VENUS": ["V", "E", "N", "U", "S", "VENUS"],
        "EARTH": ["E", "A", "R", "T", "H", "EARTH"],
        "MARS": ["M", "A", "R", "S", "MARS"],
        "JUPITER": ["J", "U", "P", "I", "T", "E", "R", "JUPITER"],
        "SATURN": ["S", "A", "T", "U", "R", "N", "SATURN"],
        "URANUS": ["U", "R", "A", "N", "U", "S", "URANUS"],
        "NEPTUNE": ["N", "E", "P", "T", "U", "N", "E", "NEPTUNE"]
    }

    # Grid layout
    for i in range(8):
        row = (i // 2) * 2
        col = i % 2
        
        label = Label(root2, image=images[i])
        label.grid(row=row, column=col, pady=(5,0) if row == 0 else 0)
        
        btn = Button(root2, text=planets[i], bg='#5b437d', fg='#ffffff', 
                    font=("Helvetica", 12, 'bold'),
                    command=lambda p=planets[i]: [speak(letter) for letter in tts_spelling[p]])
        btn.grid(row=row+1, column=col, padx=10, pady=5)

    root2.mainloop()

# Uncomment to test
# planets()
