import tkinter as tk
import records
import settings
import game


class Window(tk.Frame):  
    def __init__(self, master=None):  
        tk.Frame.__init__(self, master)  
        self.master = master  
        self.window()

    def window(self):
        self.master.title('Охота на лис')
        self.pack(fill='both', expand=1)  # заполняет выскочившее окошко. без этого на него нельзя поместить кнопки
        quit_Button = tk.Button(self, text='Quit', command=self.master.destroy)  # в command передается функция
        # отвечающая за выполнение кого-либо действия
        quit_Button.grid(row=0, column=0, sticky='nw')  # расположение кнопки
        play_Button = tk.Button(self, text='Play', command=self.game)
        play_Button.grid(row=2, column=2)
        records_Button = tk.Button(self, text='Your records', command=self.records)
        records_Button.grid(row=3, column=2)
        settings_Button = tk.Button(self, text='Settings', command=self.settings)
        settings_Button.grid(row=4,column=2)

    @staticmethod
    def game():
        game.Game()

    @staticmethod
    def records():
        records.Records()

    @staticmethod
    def settings():
        settings.Settings()
