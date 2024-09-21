import tkinter as tk
from random import shuffle
from tkinter.messagebox import showinfo, showerror

colors = {1: "#0000FF", 2: "#008000", 3: "#FF0000", 4: "#000080", 5: "#800000", 6: "#00FFFF",
          7: "#FFFF00", 8: "#800080"}


class Butto(tk.Button):
    def __init__(self, master, x, y, number=None, *args, **kwargs):
        super(Butto, self).__init__(master, *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
        self.num_flag = 0
        self.is_open = False
        self.flaged = False


class Mainer:
    root = tk.Tk()
    first_clc = True
    rows = 9
    columns = 9
    mines = 15
    count_mine = mines
    flag = False

    def __init__(self):
        self.buttons = []
        self.frame = tk.Frame(self.root, borderwidth=1, relief="solid")
        self.frm_tools = tk.Frame(self.root)
        self.but_flag = tk.Button(self.frm_tools, text="1", width=4, height=1, foreground="blue",
                                  command=self.command_flag)
        self.label_cl_flag = tk.Label(self.frm_tools, text=f"💣{str(Mainer.count_mine)}", width=6, height=2,
                                      relief="groove")
        num_but = 1
        for i in range(self.rows + 2):
            row = []
            for j in range(self.columns + 2):
                button = Butto(self.frame, x=i, y=j, width=3)
                row.append(button)
                button.config(command=lambda btn=button: self.click(btn))
                if not (i == 0 or j == 0 or i == self.rows + 1 or j == self.columns + 1):
                    button.number = num_but
                    num_but += 1
                    button.grid(row=i, column=j)
            self.buttons.append(row)

    def command_flag(self):
        if Mainer.first_clc:
            pass
        elif Mainer.flag:
            Mainer.flag = False
            self.but_flag.config(text="1")
            for i in self.buttons:
                for j in i:
                    if not j.is_open:
                        j.config(command=lambda btn=j: self.click(btn))
        else:
            Mainer.flag = True
            self.but_flag.config(text="🏴")
            activ_buts = []
            for i in self.buttons:
                for j in i:
                    if not j.is_open:
                        activ_buts.append(j)
                        j.config(command=lambda btn=j: self.set_flag(btn))
            activ_buts.clear()

    def set_flag(self, btn: Butto):
        if Mainer.flag:
            if btn.flaged:
                Mainer.count_mine += 1
                self.label_cl_flag.config(text=f"💣{str(Mainer.count_mine)}")
                btn.flaged = False
                btn.is_open = False
                btn.config(text="", state="active")
            else:
                Mainer.count_mine -= 1
                self.label_cl_flag.config(text=f"💣{str(Mainer.count_mine)}")
                btn.flaged = True
                btn.is_open = True
                btn.config(text="🏴", disabledforeground="black")

    def click(self, btn: Butto):
        btn.config(state="disabled", relief="sunken")
        if self.first_clc:
            Mainer.first_clc = False
            mine = self.set_mine(btn)
            self.create_mine(mine)
            self.create_num_flags()
            self.print_field()
        btn.config(state="disabled", background="#C0C0C0", relief="sunken")
        if btn.is_mine:
            self.show_mines()
            showinfo("Mistake", "You Lose!")
            self.re_start()
        elif btn.num_flag:
            btn.config(text=f"{btn.num_flag}", disabledforeground=colors[btn.num_flag], background="#C0C0C0")
            btn.is_open = True
            self.check_win_game()
        else:
            self.open_empty_space(btn)

    def create_num_flags(self):
        for i in range(1, self.rows + 1):
            for j in range(1, self.columns + 1):
                if self.buttons[i][j].is_mine:
                    continue
                count = 0
                for ii in [-1, 0, 1]:
                    for jj in [-1, 0, 1]:
                        if self.buttons[i + ii][j + jj].is_mine:
                            count += 1
                self.buttons[i][j].num_flag = count

    def open_empty_space(self, clic_but):
        li = [clic_but]
        while li:
            but_main = li.pop()
            but_main.is_open = True
            if but_main.num_flag:
                but_main.config(text=f"{but_main.num_flag}", disabledforeground=colors[but_main.num_flag],
                                state="disabled", relief="sunken", background="#C0C0C0")
            else:
                but_main.config(text=" ", state="disabled", relief="sunken", background="#C0C0C0")
                x, y = but_main.x, but_main.y
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        close_but = self.buttons[x + i][y + j]
                        if not close_but.is_open and 1 <= close_but.x <= self.rows and \
                                1 <= close_but.y <= self.columns and close_but not in li:
                            li.append(close_but)
        self.check_win_game()

    def set_mine(self, first_btn):
        id_buttons = [i for i in range(1, (self.rows * self.columns) + 1)]
        id_buttons.remove(first_btn.number)
        shuffle(id_buttons)
        return id_buttons[:self.mines]

    def create_mine(self, mine):
        mine.sort()
        for i in self.buttons:
            for j in i:
                if j.number in mine:
                    j.is_mine = True

    def start(self):
        self.create_widget()
        self.frame.pack(padx=5, pady=5)
        self.frm_tools.pack()
        self.but_flag.pack(side="left", expand=1)
        self.label_cl_flag.pack(expand=1, padx=5)
        self.root.mainloop()

    def create_widget(self):
        higher_menu = tk.Menu(self.root)
        self.root.config(menu=higher_menu)
        low_menu = tk.Menu(higher_menu, tearoff=0)
        low_menu.add_command(label="Start", command=lambda: self.re_start())
        low_menu.add_command(label="Settings", command=lambda: self.ask_set())
        low_menu.add_command(label="Leave the game", command=lambda: self.root.destroy())
        higher_menu.add_cascade(label="Menu", menu=low_menu)

    def ask_set(self):
        sett = tk.Toplevel(self.root)
        sett.wm_title("Settings")
        tk.Label(sett, text="Number of columns:").grid(row=0, column=0)
        row = tk.Entry(sett)
        row.grid(row=0, column=1, padx=5, pady=5, )
        tk.Label(sett, text="Number of lines:").grid(row=1, column=0)
        column = tk.Entry(sett)
        column.grid(row=1, column=1, padx=5, pady=5, )
        tk.Label(sett, text="Number of bombs:").grid(row=2, column=0)
        mine = tk.Entry(sett)
        mine.grid(row=2, column=1, padx=5, pady=5)
        save_set = tk.Button(sett, text="Save changes", command=lambda: self.save_change(row, column, mine))
        save_set.grid(row=3, column=1)

    def save_change(self, row: tk.Entry, column: tk.Entry, mine: tk.Entry):
        try:
            int(row.get()), int(column.get()), int(mine.get())
        except ValueError:
            showerror("Error", "Incorrect Enter! Must be a number!")
            return
        r, w, m = int(row.get()), int(column.get()), int(mine.get())
        if 12 <= r * w <= 1200 and 0.8 <= (m * 100) / (r * w) <= 99.9 and r / w <= 1:
            Mainer.rows = r
            Mainer.columns = w
            Mainer.mines = m
            self.re_start()
        else:
            showerror("Error", "Row*column must be lower 2000 and mine lower 99.9%")

    def check_win_game(self):
        opened = []
        for i in self.buttons:
            for j in i:
                if j.is_open and not j.is_mine:
                    opened.append(j)
        if len(opened) == Mainer.columns * Mainer.rows - Mainer.mines:
            showinfo("Oooo", "Congratulations, you win!")
            self.re_start()

    def re_start(self):
        [child.destroy() for child in self.root.winfo_children()]
        self.__init__()
        Mainer.first_clc = True
        Mainer.count_mine = Mainer.mines
        self.label_cl_flag.config(text=f"💣{str(Mainer.count_mine)}")
        self.start()

    def show_mines(self):
        for i in self.buttons:
            for j in i:
                if j.is_mine:
                    j.config(text="*")
                j.config(state="disabled")

    def print_field(self):
        for i in self.buttons:
            for j in i:
                if not j.number:
                    continue
                elif j.is_mine:
                    print(f"#{j.num_flag}B", end=" ")
                else:
                    print(f"#{j.num_flag}", end=" ")
            print()


Start = Mainer()
Start.start()
