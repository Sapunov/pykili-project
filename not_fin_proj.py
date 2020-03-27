import tkinter as tk
import numpy as np
import random

all_scores = []
rows = []
columns = []
square_side = 50


class Window(tk.Frame):  # 1
    def __init__(self, master=None):  # 2
        tk.Frame.__init__(self, master)  # 3
        self.master = master  # 4
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
        settings_Button.grid(row=4, column=2)

    @staticmethod
    def game():
        Game()

    @staticmethod
    def records():
        Records()

    @staticmethod
    def settings():
        Settings()


class Game(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.score = 0
        self.num_foxes = 10
        self.num_rows = self.rows(rows)
        self.num_columns = self.columns(columns)
        self.clicked = []
        self.canvas = tk.Canvas(self, width=self.num_columns * square_side, height=self.num_rows * square_side)
        self.canvas.pack()
        self.field, self.fox_coordinates = self.fox_matrix(self.num_rows, self.num_columns, self.num_foxes)
        self.already_clicked = []
        self.game_loop()
        self.draw_grid(self.canvas)

    @staticmethod
    def rows(rows):
        if rows == []:
            num_rows = 8
        else:
            num_rows = rows[len(rows) - 1]
        return num_rows

    @staticmethod
    def columns(columns):
        if columns == []:
            num_columns = 8
        else:
            num_columns = columns[len(columns) - 1]
        return num_columns

    @staticmethod
    def fox_matrix(number_rows, number_columns, number_foxes):
        field = np.zeros((number_rows, number_columns))
        coordinates = []  # сюда вписываются координаты лис
        for fox in range(number_foxes):
            fox = [random.randrange(0, number_rows),
                   random.randrange(0, number_columns)]  # случайным образом для лиса выбирается
            # координата х и у
            if fox not in coordinates:
                coordinates.append(fox)
            else:
                while fox in coordinates:
                    fox = [random.randrange(0, number_rows), random.randrange(0, number_columns)]
                coordinates.append(fox)

        for fox_location in coordinates:
            fox_row, fox_column = fox_location
            field[fox_row][fox_column] = -1  # каждой лисе присваивается индекс -1

            for i in range(0, number_columns):
                if field[fox_row][i] != -1:  # цикл проходит по ячейкам ряда в котором лис и если индекс не равен -1,
                    # то индекс этой клетки увеличивается на 1. То же самое присходит в след. цикле, но в столбике
                    field[fox_row][i] += 1
            for j in range(0, number_rows):
                if field[j][fox_column] != -1:
                    field[j][fox_column] += 1
        print(field)  # можно отслеживать вссе ли так открывается на поле
        return field, coordinates

    def draw_grid(self, canvas):
        for row in range(self.num_rows):
            for column in range(self.num_columns):
                canvas.create_rectangle(column * square_side, row * square_side,
                                        column * square_side + square_side,
                                        row * square_side + square_side, fill='gray')

    def game(self, event):
        clicked_button = self.canvas.find_withtag(tk.CURRENT)[0]  # получаем номер объекта по которому кликнули
        if clicked_button > self.num_rows * self.num_columns:
            return
        y_coordinate = (clicked_button - 1) // self.num_columns  # из номера обекта получаем его координаты. 1
        # вычитается так как нумерация объектов на холсте начинается с 1, а нумерация в координатак с 0
        x_coordinate = (clicked_button - 1) - y_coordinate * self.num_columns
        clicked_coordinates = [y_coordinate, x_coordinate]
        if not self.is_clicked(clicked_coordinates):
            self.score += 1
            if clicked_coordinates in self.fox_coordinates:
                self.canvas.itemconfig(tk.CURRENT, fill="red")
                if self.are_foxes_left() == 0:
                    self.ending()
            else:
                self.canvas.itemconfig(tk.CURRENT, fill="green")
                self.canvas.itemconfig(clicked_button, fill="green")
                # Пишем на клетке количество мин вокруг
                self.canvas.create_text(square_side * x_coordinate + square_side / 2,
                                        square_side * y_coordinate + square_side / 2,
                                        text=str(int(self.field[y_coordinate][x_coordinate])),
                                        font="Arial {}".format(int(square_side / 2)),
                                        fill='yellow')

    def is_clicked(self, coordinates):
        i = None
        if coordinates in self.already_clicked:
            i = True
        else:
            self.already_clicked.append(coordinates)
            i = False
        return i

    def are_foxes_left(self):
        self.num_foxes -= 1
        return self.num_foxes

    def ending(self):
        self.destroy()
        all_scores.append(self.score)
        Ending()

    def game_loop(self):
        self.canvas.bind('<Button-1>', self.game)


class Ending(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.window()

    def window(self):
        self.title('final')
        message = tk.Message(self, width=50 * 8, text=('Поздравляю! Ваш счет: ', all_scores[len(all_scores) - 1]))
        message.pack(side='bottom')


class Records(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.window()

    def window(self):
        self.title('records')
        quit_Button = tk.Button(self, text='Quit', command=self.destroy)
        quit_Button.grid(row=0, column=0, sticky='nw')
        if self.best_score(all_scores) != None:
            label = tk.Label(self, text=('Ваш лучший счет: ', self.best_score(all_scores)))
            label.grid(row=1, column=1)
        else:
            label = tk.Label(self, text='У вас еще нет достижений')
            label.grid(row=1, column=1)

    @staticmethod
    def best_score(all_scores):
        if all_scores != []:
            best = all_scores[0]
            for score in all_scores:
                if score < best:
                    best = score
            return best
        else:
            return None


class Settings(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.window()

    def window(self):
        self.title('settings')
        label1 = tk.Label(self, text='Количество строк: ')
        label1.grid(row=1, column=1)
        self.text1 = tk.Text(self, height=2, width=7, font='Arial 14')
        self.text1.grid(row=1, column=2)
        ok_button1 = tk.Button(self, text='OK', command=self.get_rows)
        ok_button1.grid(row=1, column=3)
        label2 = tk.Label(self, text='Количество столбцов: ')
        label2.grid(row=2, column=1)
        self.text2 = tk.Text(self, height=2, width=7, font='Arial 14')
        self.text2.grid(row=2, column=2)
        ok_button2 = tk.Button(self, text='OK', command=self.get_columns)
        ok_button2.grid(row=2, column=3)

    def get_rows(self):
        rows.append(int(self.text1.get(1.0, tk.END)))
        print(rows)

    def get_columns(self):
        columns.append(int(self.text2.get(1.0, tk.END)))
        print(columns)


def main():
    root = tk.Tk()
    root.geometry('150x150')  # Размеры окна
    app = Window(root)
    root.mainloop()


if __name__ == '__main__':
    main()
