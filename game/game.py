import tkinter as tk
import numpy as np
import random
import project
import ending


class Game(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.score = 0
        self.num_foxes = 10
        self.num_rows = self.rows(project.rows)
        self.num_columns = self.columns(project.columns)
        self.clicked = []
        self.canvas = tk.Canvas(self, width=self.num_columns * project.square_side,
                                height=self.num_rows * project.square_side)
        self.canvas.pack()
        self.field, self.fox_coordinates = self.fox_matrix(self.num_rows, self.num_columns, self.num_foxes)
        self.already_clicked = []
        self.game_loop()
        self.draw_grid(self.canvas)

    @staticmethod
    def rows(rows):
        if rows == []:
            num_rows = 5
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
        return field, coordinates

    def draw_grid(self, canvas):
        for row in range(self.num_rows):
            for column in range(self.num_columns):
                canvas.create_rectangle(column * project.square_side, row * project.square_side,
                                        column * project.square_side + project.square_side,
                                        row * project.square_side + project.square_side, fill='gray')

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
                self.canvas.itemconfig(clicked_button, fill="dark green")
                y = clicked_coordinates[0] * 50
                x = clicked_coordinates[1] * 50
                self.fox(x, y, self.canvas)
                if self.are_foxes_left() == 0:
                    self.ending()
            else:
                self.canvas.itemconfig(clicked_button, fill="green")
                # Пишем на клетке количество мин вокруг
                self.canvas.create_text(project.square_side * x_coordinate + project.square_side / 2,
                                        project.square_side * y_coordinate + project.square_side / 2,
                                        text=str(int(self.field[y_coordinate][x_coordinate])),
                                        font="Arial {}".format(int(project.square_side / 2)),
                                        fill='yellow')

    def is_clicked(self, coordinates):
        i = None
        if coordinates in self.already_clicked:
            i = True
        else:
            self.already_clicked.append(coordinates)
            i = False
        return i

    def fox(self, x, y, canvas):
        canvas.create_polygon(x + 0, y + 25, x + 50, y + 25, x + 25, y + 50, fill='orange')
        canvas.create_polygon(x + 0, y + 25, x + 10, y + 12, x + 20, y + 25, fill='orange')
        canvas.create_polygon(x + 50, y + 25, x + 40, y + 12, x + 30, y + 25, fill='orange')
        canvas.create_polygon(x + 25, y + 50, x + 20, y + 45, x + 30, y + 45, fill='black')
        canvas.create_oval(x + 15, y + 26, x + 20, y + 31, fill='black')
        canvas.create_oval(x + 30, y + 26, x + 35, y + 31, fill='black')

    def are_foxes_left(self):
        self.num_foxes -= 1
        return self.num_foxes

    def ending(self):
        self.destroy()
        project.all_scores.append(self.score)
        ending.Ending()

    def game_loop(self):
        self.canvas.bind('<Button-1>', self.game)
