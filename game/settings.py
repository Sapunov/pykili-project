import tkinter as tk
import project


class Settings(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.text2 = tk.Text(self, height=2, width=7, font='Arial 14')
        self.text1 = tk.Text(self, height=2, width=7, font='Arial 14')
        self.window()

    def window(self):
        self.title('settings')
        label1 = tk.Label(self, text='Количество строк: ')
        label1.grid(row=1, column=1)
        self.text1.grid(row=1, column=2)
        ok_button1 = tk.Button(self, text='OK', command=self.get_rows)
        ok_button1.grid(row=1, column=3)
        label2 = tk.Label(self, text='Количество столбцов: ')
        label2.grid(row=2, column=1)
        self.text2.grid(row=2, column=2)
        ok_button2 = tk.Button(self, text='OK', command=self.get_columns)
        ok_button2.grid(row=2, column=3)

    def get_rows(self):
        project.rows.append(int(self.text1.get(1.0, tk.END)))

    def get_columns(self):
        project.columns.append(int(self.text2.get(1.0, tk.END)))
