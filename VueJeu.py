# -*- coding: utf-8 -*-
from tkinter import *


class VueJeu:
    """ Classe contenant l'interface graphique du jeu
    - model : Teeko -> contient les informations de la partie en cours
    - fond : contient l'image de fond du jeu
    - canvas : canvas contenant le jeu
    """

    def __init__(self, model, frame, actionOnMouseEvent):
        self.model = model
        self.labelText = StringVar()
        self.labelText.set('Initialisation de la partie...')
        self.label = Label(
            frame, textvariable=self.labelText, fg='red', bg='white')
        self.label.pack()
        self.canvas = Canvas(frame, width=500, height=500)
        self.fond = PhotoImage(file="fond_teeko.png")
        self.canvas.create_image(250, 250, image=self.fond)
        self.canvas.bind('<Button-1>', actionOnMouseEvent)
        self.canvas.pack()

    def affichage(self):
        self.canvas.delete("all")
        self.canvas.create_image(250, 250, image=self.fond)

        self.update_status_label()

        for x in range(5):
            for y in range(5):
                val = self.model.get_case_value(x, y)
                if val == 1:
                    self.canvas.create_oval(
                        65 + x * 82, 65 + y * 82, 105 + x * 82, 105 + y * 82, fill='red')
                if val == 2:
                    self.canvas.create_oval(
                        65 + x * 82, 65 + y * 82, 105 + x * 82, 105 + y * 82, fill='black')
                if val == 3:
                    self.canvas.create_oval(
                        75 + x * 82, 75 + y * 82, 95 + x * 82, 95 + y * 82, fill='blue')

    def update_status_label(self):
        if self.model.tour == 1 and self.model.joueur1 == self.model.TYPE_IA:
            self.labelText.set("C'est au tour de l'IA Rouge")
            self.label.config(fg="red")
        elif self.model.tour == 2 and self.model.joueur2 == self.model.TYPE_IA:
            self.labelText.set("C'est au tour de l'IA Noire")
            self.label.config(fg="black")
        elif self.model.tour == 1:
            self.labelText.set("C'est au tour du Joueur Rouge")
            self.label.config(fg="red")
        else:
            self.labelText.set("C'est au tour du Joueur Noir")
            self.label.config(fg="black")
