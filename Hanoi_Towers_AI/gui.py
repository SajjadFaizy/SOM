from vpython import box, cylinder, vector, color, ring, scene, rate
import time
import random

class HanoiGUI:
    """
    A class to represent the graphical user interface for the Towers of Hanoi game.
    Attributes
    ----------
    ring_count : int
        The number of rings in the game.
    speed : float
        The speed of the animation.
    stabs : list
        A list to store the rods (cylinders) in the game.
    rings : list of lists
        A list containing three sublists, each representing the rings on a rod.
    Methods
    -------
    setupScene():
        Configures the scene, creates the base, rods, and rings.
    moveRing(from_stab, to_stab):
        Moves a ring from one rod to another with animation.
    """
    def __init__(self, ring_count, speed):
        self.ring_count = ring_count
        self.speed = speed  # Animationsgeschwindigkeit
        self.stabs = []
        self.rings = [[], [], []]  # Drei Unterlisten für die Ringe der Stäbe
        self.setupScene()

    def setupScene(self):
        # Szene konfigurieren
        scene.title = "Türme von Hanoi"
        scene.width = 800
        scene.height = 600
        scene.background = color.gray(0.8)
        
        # Basis erstellen
        base = box(pos=vector(0, -1, 0), size=vector(12, 0.2, 4), color=color.gray(0.5))
        
        # Stäbe erstellen
        for i in range(3):
            stab = cylinder(pos=vector(-4 + i * 4, -1, 0), axis=vector(0, 3, 0), radius=0.2, color=color.white)
            self.stabs.append(stab)
        
        # Maximaler und minimaler Ring-Durchmesser
        max_thickness = 0.3  # Dicke des dicksten Rings
        min_thickness = 0.1  # Dicke des dünnsten Rings
        
        # Proportionaler Abstand für die Skalierung der Dicke
        step = (max_thickness - min_thickness) / (self.ring_count - 1) if self.ring_count > 1 else 0
        
        colors = [color.red, color.orange, color.yellow, color.green, color.blue, color.purple]

        # Ringe erstellen und auf den ersten Stab legen
        height = -0.9
        last_thickness = max_thickness
        for i in range(self.ring_count):
            current_thickness = max_thickness - i * step
            height += current_thickness + last_thickness if i > 0 else current_thickness
            last_thickness = current_thickness
            
            ring_color = colors[i % len(colors)]
            ring_obj = ring(pos=vector(-4, height, 0), axis=vector(0, 1, 0),
                            radius=1 - i * 0.1, thickness=current_thickness, color=ring_color)
            self.rings[0].append(ring_obj)  # Ringe dem ersten Stab zuweisen
    
    def moveRing(self, from_stab, to_stab):
        # Ring vom Startstab entfernen
        ring = self.rings[from_stab].pop()
        
        # Zielhöhe berechnen
        target_height = -0.9  # Basis-Höhe
        for r in self.rings[to_stab]:
            target_height += r.thickness * 2  # Stapelhöhe berechnen
        target_height += ring.thickness  # Höhe des aktuellen Rings hinzufügen
        
        # Zielposition berechnen
        target_x = -4 + to_stab * 4  # x-Koordinate des Ziel-Stabs
        
        # Animation: Ring nach oben bewegen
        while ring.pos.y < 3:  # Hebe den Ring auf eine Höhe über den Stäben
            rate(50 * self.speed)
            ring.pos.y += 0.05
        
        # Animation: Ring horizontal bewegen
        while abs(ring.pos.x - target_x) > 0.01:  # Bewegt den Ring horizontal zur Zielposition
            rate(50 * self.speed)
            ring.pos.x += 0.05 if ring.pos.x < target_x else -0.05
        
        # Animation: Ring nach unten bewegen
        while ring.pos.y > target_height:  # Bewegt den Ring zur Zielhöhe
            rate(50 * self.speed)
            ring.pos.y -= 0.05
        
        # Exakte Position setzen (zur Sicherheit)
        ring.pos.x = target_x
        ring.pos.y = target_height
        
        # Ring dem Zielstab hinzufügen
        self.rings[to_stab].append(ring)

# Programm läuft aktiv, bis es geschlossen wird
#while True:
#    pass
