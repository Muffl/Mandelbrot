"""
Mandelbrot Set - Ultra Einfache Version
Zeigt den Zoom-Effekt des Mandelbrot-Sets
"""

import tkinter as tk
from tkinter import messagebox
import math

class MandelbrotZoom:
    def __init__(self):
        # Fenster erstellen
        self.root = tk.Tk()
        self.root.title("Mandelbrot Set - Zoom Explorer")
        self.root.geometry("600x700")
        
        # Parameter
        self.canvas_size = 400
        self.max_iterations = 25
        self.zoom_level = 1.0
        self.center_real = -0.5
        self.center_imag = 0.0
        
        self.create_interface()
        self.draw()
        
    def create_interface(self):
        """Erstellt die Benutzeroberfläche"""
        # Titel
        title_label = tk.Label(self.root, text="🌀 Mandelbrot Set Explorer 🌀", 
                              font=("Arial", 16, "bold"), fg="darkblue")
        title_label.pack(pady=10)
        
        # Canvas für das Mandelbrot-Set
        self.canvas = tk.Canvas(self.root, width=self.canvas_size, height=self.canvas_size, 
                               bg="black", relief=tk.SUNKEN, bd=3)
        self.canvas.pack(pady=10)
        
        # Maus-Events
        self.canvas.bind("<Button-1>", self.handle_left_click)
        self.canvas.bind("<Button-3>", self.handle_right_click)
        
        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="🔍 Hineinzoomen", command=self.zoom_in,
                 bg="lightgreen", font=("Arial", 12), width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="🔍 Herauszoomen", command=self.zoom_out,
                 bg="lightcoral", font=("Arial", 12), width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="🏠 Zurücksetzen", command=self.reset,
                 bg="lightblue", font=("Arial", 12), width=15).pack(side=tk.LEFT, padx=5)
        
        # Qualitäts-Einstellungen
        quality_frame = tk.Frame(self.root)
        quality_frame.pack(pady=10)
        
        tk.Label(quality_frame, text="Qualität:", font=("Arial", 12)).pack(side=tk.LEFT)
        
        tk.Button(quality_frame, text="Schnell (20)", 
                 command=lambda: self.set_quality(20), bg="yellow").pack(side=tk.LEFT, padx=2)
        tk.Button(quality_frame, text="Normal (35)", 
                 command=lambda: self.set_quality(35), bg="orange").pack(side=tk.LEFT, padx=2)
        tk.Button(quality_frame, text="Hoch (50)", 
                 command=lambda: self.set_quality(50), bg="red").pack(side=tk.LEFT, padx=2)
        
        # Interessante Punkte
        preset_frame = tk.Frame(self.root)
        preset_frame.pack(pady=10)
        
        tk.Label(preset_frame, text="🎯 Interessante Stellen:", font=("Arial", 12, "bold")).pack()
        
        preset_buttons = tk.Frame(preset_frame)
        preset_buttons.pack(pady=5)
        
        locations = [
            ("🌊 Übersicht", -0.5, 0.0, 1.0),
            ("🌀 Spirale", -0.235125, 0.827215, 4.0),
            ("⚡ Blitzform", -0.7463, 0.1102, 8.0),
        ]
        
        for name, real, imag, zoom in locations:
            tk.Button(preset_buttons, text=name, 
                     command=lambda r=real, i=imag, z=zoom: self.jump_to(r, i, z),
                     font=("Arial", 10), width=12).pack(side=tk.LEFT, padx=3)
        
        # Status
        self.status_label = tk.Label(self.root, text="Bereit! Klicken Sie ins Bild zum Zoomen.", 
                                    font=("Arial", 11), fg="darkgreen")
        self.status_label.pack(pady=10)
        
        # Info
        info_text = "💡 Tipp: Linksklick = Hineinzoomen, Rechtsklick = Herauszoomen"
        info_label = tk.Label(self.root, text=info_text, font=("Arial", 10), fg="gray")
        info_label.pack()
        
    def calculate_mandelbrot(self, c):
        """Berechnet ob ein Punkt im Mandelbrot-Set ist"""
        z = 0
        for iteration in range(self.max_iterations):
            if abs(z) > 2:
                return iteration
            z = z * z + c
        return self.max_iterations
        
    def get_pixel_color(self, iterations):
        """Wandelt Iterationen in eine Farbe um"""
        if iterations >= self.max_iterations:
            return "#000000"  # Schwarz für Mandelbrot-Set
        
        # Bunte Farben für Punkte außerhalb des Sets
        normalized = iterations / self.max_iterations
        
        # Regenbogen-Farbschema
        if normalized < 0.16:
            r, g, b = 255, int(255 * normalized * 6), 0
        elif normalized < 0.33:
            r, g, b = int(255 * (1 - (normalized - 0.16) * 6)), 255, 0
        elif normalized < 0.5:
            r, g, b = 0, 255, int(255 * (normalized - 0.33) * 6)
        elif normalized < 0.66:
            r, g, b = 0, int(255 * (1 - (normalized - 0.5) * 6)), 255
        elif normalized < 0.83:
            r, g, b = int(255 * (normalized - 0.66) * 6), 0, 255
        else:
            r, g, b = 255, 0, int(255 * (1 - (normalized - 0.83) * 6))
            
        return f"#{r:02x}{g:02x}{b:02x}"
        
    def draw(self):
        """Zeichnet das Mandelbrot-Set"""
        self.status_label.config(text="🔄 Zeichne Mandelbrot-Set...")
        self.root.update()
        
        # Canvas leeren
        self.canvas.delete("all")
        
        # Koordinatenbereich berechnen
        width = 4.0 / self.zoom_level
        height = 4.0 / self.zoom_level
        
        x_min = self.center_real - width / 2
        x_max = self.center_real + width / 2
        y_min = self.center_imag - height / 2
        y_max = self.center_imag + height / 2
        
        # Pixel-Größe für Performance
        pixel_step = max(1, int(2.5 - math.log2(self.zoom_level + 1)))
        
        # Mandelbrot-Set zeichnen
        for py in range(0, self.canvas_size, pixel_step):
            for px in range(0, self.canvas_size, pixel_step):
                # Pixel-Koordinaten in komplexe Zahlen umwandeln
                real_part = x_min + (px / self.canvas_size) * (x_max - x_min)
                imag_part = y_min + (py / self.canvas_size) * (y_max - y_min)
                complex_point = complex(real_part, imag_part)
                
                # Mandelbrot-Berechnung
                iterations = self.calculate_mandelbrot(complex_point)
                color = self.get_pixel_color(iterations)
                
                # Pixel zeichnen
                self.canvas.create_rectangle(px, py, px + pixel_step, py + pixel_step,
                                           fill=color, outline=color)
            
            # Fortschritt anzeigen
            if py % (pixel_step * 8) == 0:
                progress = int((py / self.canvas_size) * 100)
                self.status_label.config(text=f"🔄 Zeichne... {progress}%")
                self.root.update()
        
        # Fertig
        self.status_label.config(text=f"✅ Fertig! Zoom: {self.zoom_level:.1f}x - Klicken für mehr!")
        
    def handle_left_click(self, event):
        """Behandelt Linksklicks zum Hineinzoomen"""
        # Berechne neue Mitte basierend auf Klickposition
        width = 4.0 / self.zoom_level
        height = 4.0 / self.zoom_level
        
        x_min = self.center_real - width / 2
        y_min = self.center_imag - height / 2
        
        # Neue Mitte setzen
        self.center_real = x_min + (event.x / self.canvas_size) * width
        self.center_imag = y_min + (event.y / self.canvas_size) * height
        
        # Hineinzoomen
        self.zoom_level *= 2
        self.draw()
        
    def handle_right_click(self, event):
        """Behandelt Rechtsklicks zum Herauszoomen"""
        self.zoom_level /= 2
        if self.zoom_level < 1:
            self.zoom_level = 1
        self.draw()
        
    def zoom_in(self):
        """Zoomt in die Mitte hinein"""
        self.zoom_level *= 2
        self.draw()
        
    def zoom_out(self):
        """Zoomt heraus"""
        self.zoom_level /= 2
        if self.zoom_level < 1:
            self.zoom_level = 1
        self.draw()
        
    def reset(self):
        """Setzt alles zurück"""
        self.zoom_level = 1.0
        self.center_real = -0.5
        self.center_imag = 0.0
        self.draw()
        
    def set_quality(self, iterations):
        """Setzt die Qualität (Anzahl Iterationen)"""
        self.max_iterations = iterations
        self.draw()
        
    def jump_to(self, real, imag, zoom):
        """Springt zu einem interessanten Punkt"""
        self.center_real = real
        self.center_imag = imag
        self.zoom_level = zoom
        self.draw()
        
    def start(self):
        """Startet die Anwendung"""
        # Begrüßung
        welcome_msg = ("🌀 Willkommen zum Mandelbrot-Set Explorer!\n\n"
                      "Das Mandelbrot-Set ist ein wunderschönes mathematisches Fraktal.\n"
                      "Beim Hineinzoomen werden Sie unendlich komplexe Strukturen entdecken!\n\n"
                      "🖱️ Linksklick: Auf einen Punkt zoomen\n"
                      "🖱️ Rechtsklick: Herauszoomen\n"
                      "🎯 Probieren Sie die Preset-Punkte aus!\n\n"
                      "Der echte Mandelbrot-Effekt zeigt sich beim Zoomen! 🚀")
        
        messagebox.showinfo("Mandelbrot Explorer", welcome_msg)
        
        # Hauptschleife starten
        self.root.mainloop()

def main():
    """Hauptfunktion"""
    mandelbrot_app = MandelbrotZoom()
    mandelbrot_app.start()

if __name__ == "__main__":
    main()