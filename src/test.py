import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.signal import convolve2d

# --- Initialisation et configuration de la fenêtre ---
root = tk.Tk()
root.title("Jeu de la Vie Interactif")

N = 500                      # Nombre de cellules par côté
cell_size = 10              # Taille initiale d'une cellule (en unités de données)
x_offset = 0                # Décalage initial en x (origine de l'affichage)
y_offset = 0                # Décalage initial en y
sim_size = N * cell_size    # Taille totale de la zone de simulation (en unités de données)
panel_width = 200           # Largeur du panneau de contrôle
speed = 10                  # Vitesse de simulation

# Définir la taille de la fenêtre (la zone de simulation reste fixe en pixels)
root.geometry(f"{sim_size + panel_width}x{sim_size}")

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=0, minsize=panel_width)
root.rowconfigure(0, weight=1)

# --- Création de la figure matplotlib ---
fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.set_position([0, 0, 1, 1])
cmap = plt.get_cmap('binary')
# On définit l'étendue (extent) pour que chaque cellule ait une taille cell_size
grid_display = ax.imshow(np.zeros((N, N)), cmap=cmap, interpolation='nearest',
                           vmin=0, vmax=1,
                           extent=[x_offset, x_offset+sim_size, y_offset, y_offset+sim_size])
ax.axis('off')

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')
canvas.get_tk_widget().config(width=sim_size, height=sim_size, bd=0, highlightthickness=0)

# --- Initialisation de la grille du Jeu de la Vie ---
grid = np.random.choice([0, 1], N*N, p=[0.8, 0.2]).reshape(N, N)

# --- Fonctions de mise à jour du Jeu de la Vie ---
def update(grid):
    """Calcule la génération suivante du jeu de la vie en utilisant une convolution."""
    kernel = np.array([[1, 1, 1],
                       [1, 0, 1],
                       [1, 1, 1]])
    neighbors = convolve2d(grid, kernel, mode='same', boundary='wrap')
    new_grid = (neighbors == 3) | ((grid == 1) & (neighbors == 2))
    return new_grid.astype(int)

def update_plot():
    global grid, running
    grid = update(grid)
    grid_display.set_data(grid)
    canvas.draw()
    if running:
        root.after(speed, update_plot)

def toggle_simulation():
    global running
    if running:
        running = False
        toggle_button.config(text="Start")
    else:
        running = True
        toggle_button.config(text="Stop")
        update_plot()

def reset_simulation():
    global grid, running
    running = False
    toggle_button.config(text="Start")
    grid = np.random.choice([0, 1], N*N, p=[0.8, 0.2]).reshape(N, N)
    grid_display.set_data(grid)
    canvas.draw()

def update_speed(val):
    """Met à jour la vitesse de simulation en fonction de la valeur du slider."""
    global speed
    speed = int(float(val))

def on_closing():
    global running
    running = False
    root.quit()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# --- Panneau de contrôle ---
control_frame = ttk.Frame(root, width=panel_width, height=sim_size)
control_frame.grid(row=0, column=1, sticky='ns')
control_frame.grid_propagate(False)

toggle_button = ttk.Button(control_frame, text="Start", command=toggle_simulation)
toggle_button.pack(pady=10, fill='x')

reset_button = ttk.Button(control_frame, text="Reset", command=reset_simulation)
reset_button.pack(pady=10, fill='x')

# Ajouter un slider pour contrôler la vitesse de simulation
speed_slider = ttk.Scale(control_frame, from_=1, to=1000, orient='horizontal', command=update_speed)
speed_slider.set(speed)  # Valeur initiale
speed_slider.pack(pady=10, fill='x')

# Ajouter une visualisation de fonction
function_fig, function_ax = plt.subplots(figsize=(2, 2))
function_ax.set_title('α⋅exp(-βx²)')

# Paramètres initiaux de la gaussienne
x = np.linspace(-2, 2, 100)
function_line, = function_ax.plot(x, np.exp(-x**2))
function_ax.set_ylim(-0.2, 1.2)
function_ax.set_xticks([])
function_ax.set_yticks([])

function_canvas = FigureCanvasTkAgg(function_fig, master=control_frame)
function_canvas.get_tk_widget().pack(pady=10, fill='x')

# Sliders pour les paramètres de la gaussienne
ttk.Label(control_frame, text="α (amplitude)").pack(pady=(10,0))
alpha_slider = ttk.Scale(control_frame, from_=0.1, to=2.0, orient='horizontal')
alpha_slider.set(1.0)
alpha_slider.pack(pady=(0,10), fill='x')

ttk.Label(control_frame, text="β (largeur)").pack(pady=(10,0))
beta_slider = ttk.Scale(control_frame, from_=0.1, to=3.0, orient='horizontal')
beta_slider.set(1.0)
beta_slider.pack(pady=(0,10), fill='x')

def update_gaussian(val=None):
    x = np.linspace(-2, 2, 100)
    alpha = alpha_slider.get()
    beta = beta_slider.get()
    y = alpha * np.exp(-beta * x**2)
    function_line.set_ydata(y)
    function_ax.set_ylim(-0.2, alpha * 1.2)
    function_canvas.draw()

# Connecter la fonction de mise à jour aux sliders
alpha_slider.configure(command=update_gaussian)
beta_slider.configure(command=update_gaussian)

running = False

root.mainloop()
