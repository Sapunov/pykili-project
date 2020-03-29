import tkinter as tk
import menu

all_scores = []
rows = []
columns = []
square_side = 50


def main():
    root = tk.Tk()
    root.geometry('150x150')  # Размеры окна
    app = menu.Window(root)
    root.mainloop()


if __name__ == '__main__':
    main()
