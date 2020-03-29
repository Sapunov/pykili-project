import tkinter as tk
import project


class Ending(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.window()

    def window(self):
        self.title('final')
        message = tk.Message(self, width=50*8, text=('Поздравляю! Ваш счет: ', project.all_scores[len(project.all_scores)-1]))
        message.pack(side='bottom')
