import tkinter as tk
import project


class Records(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.window()

    def window(self):
        self.title('records')
        quit_Button = tk.Button(self, text='Quit', command=self.destroy)
        quit_Button.grid(row=0,column=0, sticky='nw')
        if self.best_score(project.all_scores) is not None:
            label = tk.Label(self, text=('Ваш лучший счет: ', self.best_score(project.all_scores)))
            label.grid(row=1, column=1)
        else:
            label = tk.Label(self, text='У вас еще нет достижений')
            label.grid(row=1,column=1)

    @staticmethod
    def best_score(all_scores):
        if all_scores:
            best = project.all_scores[0]
            for score in all_scores:
                if score < best:
                    best = score
            return best
        else:
            return None
