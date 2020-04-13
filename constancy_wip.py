### error description:
# erro 121 - senha ou usuario incorreto.
# erro 33 - valor ou descrição não definidos.
# erro 157 - erro de criacao de usuario (senha/usuario)
### hotkeys:
# f1 - enter with debit.
# f2 - enter with credit.
# enter create item.
# esc - reset entries.
### anotations:
# make log list a dict (action: time)

# Packages.
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import mplcyberpunk
import os
import ast
import json
import calendar
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from cryptography.fernet import Fernet
import PIL
from PIL import Image, ImageTk
from tkcalendar import DateEntry

# Global Variables.
username = ''
save_status = 'disabled'
log_list = ['Iniciado.', ]
M_FONT = 'Roboto 10'
M_COLOR = {'p0': 'white',
           'p1': '#aa84c7',
           'p2': '#5e4278',
           'p3': '#321a4c',
           'rp0': '#7a5796',
           'rp1': '#ffd9ff',
           'error': '#B00020'}
# __py_folder = r'C:/Users/luisg/OneDrive/Documentos/Python_Scripts/Constancy/'


class Main:
    def __init__(self, master):
        # Configs.
        self.master = master
        master.geometry('216x440+852+320')  # SE
        master.iconbitmap(resource_path('icon.ico'))
        master.attributes('-topmost', 1)
        master.overrideredirect(1)
        master.resizable(0, 0)
        master['bg'] = M_COLOR['p3']
        master.title('')

        # Files.
        self.users = {}
        profile_window = Profile(self.master)

        # Frames.
        self.f1_main = tk.Frame(master)
        self.f1_main['bg'] = M_COLOR['p3']
        self.f1_main.place(x=41, y=160)  # margin: 41 px.
        self.f1_main.grid_rowconfigure(4, minsize=56)

        # Background.
        init_bg = tk.PhotoImage(file=resource_path('init_back.png'))
        self.background = init_bg

        bg_label = tk.Label(master, width=214, height=160)
        bg_label['bg'] = M_COLOR['p3']
        bg_label['image'] = init_bg
        bg_label.place(x=-1, y=-2)

        # Labels.
        self.name_lb = tk.Label(self.f1_main, text='Nome:')
        self.name_lb['foreground'] = M_COLOR['p1']
        self.name_lb['font'] = M_FONT
        self.name_lb['bg'] = M_COLOR['p3']
        self.name_lb.grid(sticky=W)

        self.pw_lb = tk.Label(self.f1_main, text='Senha:')
        self.pw_lb['foreground'] = M_COLOR['p1']
        self.pw_lb['font'] = M_FONT
        self.pw_lb['bg'] = M_COLOR['p3']
        self.pw_lb.grid(row=2, sticky=W)

        # Entries.
        self.name_entry = ttk.Entry(self.f1_main, width=18)
        self.name_entry['font'] = M_FONT
        self.name_entry.grid(row=1, columnspan=2, sticky=W)
        self.name_entry.focus_force()

        self.pw_entry = ttk.Entry(self.f1_main, show='*', width=18)
        self.pw_entry['font'] = M_FONT
        self.pw_entry.grid(row=3, columnspan=2, sticky=W)

        # Buttons.
        self.create_bt = tk.Button(self.f1_main, width=4, height=3, bd=0, text='Criar', pady=0)
        self.create_bt['activebackground'] = M_COLOR['p3']
        self.create_bt['activeforeground'] = M_COLOR['p2']
        self.create_bt['foreground'] = M_COLOR['p1']
        self.create_bt['bg'] = M_COLOR['p3']
        self.create_bt['command'] = self.f_create
        self.create_bt['font'] = M_FONT
        self.create_bt.grid(row=4, sticky=W)

        self.sign_img = tk.PhotoImage(file=resource_path('in.png'))
        self.login_bt = tk.Button(self.f1_main, width=24, height=24, bd=0, pady=0)
        self.login_bt['activebackground'] = M_COLOR['p3']
        self.login_bt['command'] = self.f_sign
        self.login_bt['image'] = self.sign_img
        self.login_bt['bg'] = M_COLOR['p3']
        self.login_bt.grid(row=4, column=1, sticky=E)

        self.quit_bt = tk.Button(master, width=8, height=1, bd=0, text='Sair', pady=0)
        self.quit_bt['activebackground'] = M_COLOR['p3']
        self.quit_bt['activeforeground'] = M_COLOR['p2']
        self.quit_bt['foreground'] = M_COLOR['p1']
        self.quit_bt['bg'] = M_COLOR['p3']
        self.quit_bt['command'] = self.f_quit
        self.quit_bt['font'] = M_FONT
        self.quit_bt.place(x=72, y=412)

        # Window Movement.
        self._off_set_x = 0
        self._off_set_y = 0
        bg_label.bind('<Button-1>', self.click_win)
        bg_label.bind('<B1-Motion>', self.drag_win)
        self.master.bind('<Return>', lambda x: f_invoker(button=self.login_bt))
        self.master.bind('<Escape>', lambda x: f_invoker(button=self.quit_bt))

    def drag_win(self, event):
        x = self.master.winfo_pointerx() - self._off_set_x
        y = self.master.winfo_pointery() - self._off_set_y
        self.master.geometry('+{x}+{y}'.format(x=x, y=y))

    def f_deiconify(self):
        self.master.deiconify()

    def f_acc_validate(self, name, password):
        with open(resource_path('users.bin'), 'rb') as user_file:
            users = user_file.read().decode()
            self.users = ast.literal_eval(users)
        if name in self.users:
            f_key = Fernet(get_key())
            if password == f_key.decrypt(self.users.get(name).encode()).decode():
                return True
            else:
                return False
        else:
            return False

    def deactivate(self, state):
        self.create_bt['state'] = state
        self.login_bt['state'] = state
        self.name_entry['state'] = state
        self.pw_entry['state'] = state

    def click_win(self, event):
        self._off_set_x = event.x
        self._off_set_y = event.y

    def f_quit(self):
        self.deactivate('disabled')
        self.quit_bt['text'] = 'Saindo...'
        self.quit_bt['foreground'] = M_COLOR['error']
        self.master.after(250, self.master.destroy)

    def f_sign(self):
        global username
        if self.name_entry.get() != '' and self.pw_entry.get() != '':
            if self.f_acc_validate(self.name_entry.get(), self.pw_entry.get()):
                username = self.name_entry.get()
                self.master.withdraw()
                lateral_window = Peripheral(self.master)
                self.name_entry.delete(0, 'end')
                self.pw_entry.delete(0, 'end')
                lateral_window.value_entry.focus_force()
            else:
                self.f_error_msg('Nome ou senha incorreto.')
        else:
            self.f_error_msg('Campos obrigatórios não podem ficar em branco.')

    def f_create(self):
        leaf_window = Create(self.master)
        leaf_window.user_entry.focus_force()

    def f_error_msg(self, txt):
        self.master.attributes('-disabled', 1)
        messagebox.showerror('Erro 213!', txt)
        self.master.attributes('-disabled', 0)
        self.name_entry.focus_force()


class Create(tk.Toplevel):
    def __init__(self, master):
        # Configs.
        tk.Toplevel.__init__(self, master)
        self.master = master
        self.grab_set()
        self.x = master.winfo_x()
        self.y = master.winfo_y()
        self.geometry('304x200+{}+{}'.format(self.x-45, self.y+94))
        self.iconbitmap(resource_path('icon.ico'))
        self.attributes('-topmost', 1)
        self.resizable(0, 0)
        self.title('Novo Usuário')
        self['bg'] = M_COLOR['p3']

        # Files.
        with open(resource_path('users.bin'), 'rb') as self.user_file:
            users = self.user_file.read().decode()
            self.users = ast.literal_eval(users)

        # Frames.
        self.f2_create = tk.Frame(self)
        self.f2_create['bg'] = M_COLOR['p3']
        self.f2_create.place(x=24, y=24)  # margin: 41 px.
        self.f2_create.grid_rowconfigure(1, minsize=56)

        # Labels.
        self.user_lb = tk.Label(self.f2_create, text='Nome:')
        self.user_lb['foreground'] = M_COLOR['p1']
        self.user_lb['font'] = M_FONT
        self.user_lb['bg'] = M_COLOR['p3']
        self.user_lb.grid(sticky=W)

        self.password_lb = tk.Label(self.f2_create, text='Senha:')
        self.password_lb['foreground'] = M_COLOR['p1']
        self.password_lb['font'] = M_FONT
        self.password_lb['bg'] = M_COLOR['p3']
        self.password_lb.grid(row=1, sticky=W)

        self.info_img = tk.PhotoImage(file=resource_path('info.png'))
        self.info_pw_lb = tk.Label(self.f2_create, width=24, height=24)
        self.info_pw_lb['image'] = self.info_img
        self.info_pw_lb['bg'] = M_COLOR['p3']
        self.info_pw_lb.grid(row=1, sticky=E)

        self.r_password_lb = tk.Label(self.f2_create, text='Reinserir Senha:')
        self.r_password_lb['foreground'] = M_COLOR['p1']
        self.r_password_lb['font'] = M_FONT
        self.r_password_lb['bg'] = M_COLOR['p3']
        self.r_password_lb.grid(row=2, sticky=W)

        self.pw_info_lb = tk.Label(self.f2_create, text='')
        self.pw_info_lb['foreground'] = M_COLOR['p1']
        self.pw_info_lb['font'] = M_FONT
        self.pw_info_lb['bg'] = M_COLOR['p3']
        self.pw_info_lb.grid(row=5, columnspan=2)

        # Entries.
        self.user_entry = ttk.Entry(self.f2_create, width=20)
        self.user_entry['font'] = M_FONT
        self.user_entry.grid(row=0, column=1)
        self.user_entry.focus_set()

        self.password_entry = ttk.Entry(self.f2_create, show='*', width=20)
        self.password_entry['font'] = M_FONT
        self.password_entry.grid(row=1, column=1)

        self.r_password_entry = ttk.Entry(self.f2_create, show='*', width=20)
        self.r_password_entry['font'] = M_FONT
        self.r_password_entry.grid(row=2, column=1)

        # Buttons.
        self.cancel_bt = tk.Button(self.f2_create, width=8, height=3, bd=0, text='Cancelar', pady=0)
        self.cancel_bt['activebackground'] = M_COLOR['p3']
        self.cancel_bt['activeforeground'] = M_COLOR['p2']
        self.cancel_bt['foreground'] = M_COLOR['p1']
        self.cancel_bt['bg'] = M_COLOR['p3']
        self.cancel_bt['command'] = self.f_cancel
        self.cancel_bt['font'] = M_FONT
        self.cancel_bt.grid(row=4)

        self.confirm_bt = tk.Button(self.f2_create, width=8, height=3, bd=0, text='Confirmar', pady=0)
        self.confirm_bt['activebackground'] = M_COLOR['p3']
        self.confirm_bt['activeforeground'] = M_COLOR['p2']
        self.confirm_bt['foreground'] = M_COLOR['p1']
        self.confirm_bt['bg'] = M_COLOR['p3']
        self.confirm_bt['command'] = self.f_confirm
        self.confirm_bt['font'] = M_FONT
        self.confirm_bt.grid(row=4, column=1, sticky=E)
        
        # Binds.
        self.info_pw_lb.bind('<Enter>', self.on_enter)
        self.info_pw_lb.bind('<Leave>', self.on_leave)
        self.bind('<Return>', lambda x: f_invoker(button=self.confirm_bt))
        self.bind('<Escape>', lambda x: f_invoker(button=self.cancel_bt))

    def on_enter(self, event):
        self.pw_info_lb.configure(text='Mínimo de quatro caracteres.')

    def on_leave(self, event):
        self.pw_info_lb.configure(text='')

    def f_cancel(self):
        self.destroy()

    def f_confirm(self):
        if self.user_entry.get() != '' and self.password_entry.get() != '':
            if self.user_entry.get() not in self.users:
                if len(self.password_entry.get()) >= 4:
                    if self.password_entry.get() == self.r_password_entry.get():
                        self.users.update({self.user_entry.get(): f_encrypt(self.password_entry.get()).decode()})
                        with open(resource_path('users.bin'), 'wb') as self.user_file:
                            self.user_file.write(str(self.users).encode())
                        messagebox.showinfo('Novo Usuário', 'Usuário criado com sucesso!')
                        with open(resource_path(str(self.user_entry.get() + '.encrypted')), 'w+') as user_init:
                            user_init.write('[]')
                        self.destroy()
                    else:
                        self.f_error_msg('As senhas não coincidem.')
                        self.password_entry.focus()
                else:
                    self.f_error_msg('Senha não atende aos requisitos.')
                    self.password_entry.focus()
            else:
                self.f_error_msg('Usuário já existente.')
        else:
            self.f_error_msg('Campos obrigatórios não podem ficar em branco.')

    def f_error_msg(self, txt):
        self.attributes('-disabled', 1)
        messagebox.showerror('Erro 157!', txt)
        self.attributes('-disabled', 0)
        self.user_entry.focus_force()


class Peripheral(tk.Toplevel):
    def __init__(self, master):
        # Configs.
        global username, save_status
        tk.Toplevel.__init__(self, master)
        self.master = master
        self['bg'] = M_COLOR['rp0']
        self.title('Constancy WIP')
        self.x = master.winfo_x()
        self.y = master.winfo_y()
        self.geometry('428x216+{}+{}'.format(self.x-107, self.y+49))
        self.protocol('WM_DELETE_WINDOW', self.f_del_window)
        self.resizable(0, 0)
        self.iconbitmap(resource_path('icon.ico'))
        self.register_f = self.register(self.f_validate_float)
        self.register_i = self.register(self.f_validate_integer)

        # Variables.
        self.item_id = 0
        self.balance = 0
        self.balance_status = 0
        self.sub_item_total = 0
        self.sub_item_counter = 0
        self.sub_item_list = []
        self.json_file = []
        self.f_load()

        # Styles.
        self.style_check = ttk.Style()
        self.style_check.configure('my.TCheckbutton', background=M_COLOR['rp0'],
                                   foreground=M_COLOR['p0'],
                                   font=M_FONT)
        self.style_check.map('my.TCheckbutton', indicatoron=[('pressed', '#ececec'), ('selected', '#4a6984')])

        # Canvas.
        self.c1_peri = tk.Canvas(self, width=480, height=48)
        self.c1_peri['highlightthickness'] = 0
        self.c1_peri['bg'] = M_COLOR['p3']
        self.c1_peri.place(x=0, y=0)

        self.c2_peri = tk.Canvas(self, width=480, height=24)
        self.c2_peri['highlightthickness'] = 0
        self.c2_peri['bg'] = M_COLOR['p1']
        self.c2_peri.place(x=0, y=192)

        # Frames.
        self.f3_peri = tk.Frame(self)
        self.f3_peri['bg'] = M_COLOR['rp0']
        self.f3_peri.place(x=10, y=60)
        self.f3_peri.grid_rowconfigure(2, minsize=48)

        # Labels.
        self.balance_lbl = self.c1_peri.create_text(304, 24, font=M_FONT,
                                                    text='Saldo: R$ ' + '{0:.2f}'.format(self.balance),
                                                    fill=M_COLOR['p1'], anchor=W)

        self.welcome_lbl = self.c1_peri.create_text(44, 24, font=M_FONT,
                                                    text='Bem vindo, ' + username + '.',
                                                    fill=M_COLOR['p1'], anchor=W)
        self.c1_peri.itemconfig(2, text='Bem vindo, ' + username + '.')

        self.value_lbl = tk.Label(self.f3_peri, text='Valor:')
        self.value_lbl['foreground'] = M_COLOR['p0']
        self.value_lbl['font'] = M_FONT
        self.value_lbl['bg'] = M_COLOR['rp0']
        self.value_lbl.grid(row=0, column=0, sticky=W)

        self.desc_lbl = tk.Label(self.f3_peri, text='Descrição:')
        self.desc_lbl['foreground'] = M_COLOR['p0']
        self.desc_lbl['font'] = M_FONT
        self.desc_lbl['bg'] = M_COLOR['rp0']
        self.desc_lbl.grid(row=0, column=1, sticky=W)

        self.date_lbl = tk.Label(self.f3_peri, text='Data:')
        self.date_lbl['foreground'] = M_COLOR['p0']
        self.date_lbl['font'] = M_FONT
        self.date_lbl['bg'] = M_COLOR['rp0']
        self.date_lbl.grid(row=0, column=2, sticky=W)

        self.type_lbl = tk.Label(self.f3_peri, text='Tipo:')
        self.type_lbl['foreground'] = M_COLOR['p0']
        self.type_lbl['font'] = M_FONT
        self.type_lbl['bg'] = M_COLOR['rp0']
        self.type_lbl.grid(row=0, column=3, sticky=W)

        self.log_lbl = self.c2_peri.create_text(8, 12, font=M_FONT, text=log_list[-1],
                                                fill=M_COLOR['p3'], anchor=W)
        self.c2_peri.itemconfig(1, text=log_list[-1])
        self.sub_item_total_lbl = self.c2_peri.create_text(420, 12, font=M_FONT, text='',
                                                           fill=M_COLOR['p3'], anchor=E)

        # Entries.
        self.value_entry = ttk.Entry(self.f3_peri, width=10, justify=CENTER)
        self.value_entry.config(validate='key', validatecommand=(self.register_f, '%P'))
        self.value_entry['font'] = M_FONT
        self.value_entry.grid(row=1, column=0)

        self.desc_entry = ttk.Entry(self.f3_peri, width=24)
        self.desc_entry['font'] = M_FONT
        self.desc_entry.grid(row=1, column=1, sticky=W)

        self.date_entry = DateEntry(self.f3_peri, width=8, date_pattern='dd/mm/yy')
        self.date_entry['borderwidth'] = 1
        self.date_entry['foreground'] = M_COLOR['p0']
        self.date_entry['background'] = M_COLOR['rp0']
        self.date_entry['font'] = M_FONT
        self.date_entry['style'] = 'my.DateEntry'
        self.date_entry.grid(row=1, column=2, sticky=W)

        self.type_entry = ttk.Combobox(self.f3_peri, width=8)
        self.type_entry['values'] = ['Debit', 'Credit']
        self.type_entry['height'] = 2
        self.type_entry['state'] = 'readonly'
        self.type_entry['font'] = M_FONT
        self.type_entry.grid(row=1, column=3)
        self.type_entry.set('Debit')

        self.sub_value_entry = ttk.Entry(self.f3_peri, width=10, justify=CENTER)
        self.sub_value_entry.insert(0, 0)
        self.sub_value_entry.config(validate='key', validatecommand=(self.register_f, '%P'))
        self.sub_value_entry['font'] = M_FONT
        self.sub_value_entry['state'] = 'disabled'
        self.sub_value_entry.grid(row=2, column=0)

        self.sub_desc_entry = ttk.Entry(self.f3_peri, width=24)
        self.sub_desc_entry.insert(0, 'Descrição do Subitem')
        self.sub_desc_entry['font'] = M_FONT
        self.sub_desc_entry['state'] = 'disabled'
        self.sub_desc_entry.grid(row=2, column=1)

        # CheckBoxes.
        self.sub_item_check = ttk.Checkbutton(self.f3_peri, style='my.TCheckbutton')
        self.sub_item_check['underline'] = 0
        self.sub_item_check['command'] = self.f_sub_item_check
        self.sub_item_check['text'] = 'Subitem'
        self.sub_item_check.state(['!alternate', '!selected'])
        self.sub_item_check.grid(row=2, column=2)

        # Buttons.
        self.menu_img = PIL.Image.open('menu.png')
        self.menu_photo = ImageTk.PhotoImage(self.menu_img)
        self.menu_bt = tk.Menubutton(self.c1_peri, width=28, height=28, pady=0, bd=0)
        self.menu_bt['activebackground'] = M_COLOR['p3']
        self.menu_bt['foreground'] = M_COLOR['p0']
        self.menu_bt['image'] = self.menu_photo
        self.menu_bt['font'] = M_FONT
        self.menu_bt.config(bg=M_COLOR['p3'])
        self.menu_bt.place(x=10, y=10)

        self.menu_bt.menu = tk.Menu(self.menu_bt, tearoff=0)
        self.menu_bt.menu['activebackground'] = M_COLOR['p2']
        self.menu_bt.menu['activeforeground'] = M_COLOR['p0']
        self.menu_bt.menu['disabledforeground'] = M_COLOR['p3']
        self.menu_bt.menu['foreground'] = M_COLOR['p3']
        self.menu_bt.menu['font'] = M_FONT
        self.menu_bt.menu['bg'] = M_COLOR['rp1']
        self.menu_bt.menu['bd'] = 0
        self.menu_bt['menu'] = self.menu_bt.menu
        self.menu_bt.menu.add_command(label='Perfil', command=self.f_profile)
        self.menu_bt.menu.add_command(label='Salvar', command=self.f_save)
        self.menu_bt.menu.add_command(label='Gráfico', command=self.f_graph)
        self.menu_bt.menu.add_command(label='Extrato', state='disabled')
        self.menu_bt.menu.add_command(label='Log', state='disabled')
        self.menu_bt.menu.add_separator()
        self.menu_bt.menu.add_command(label='Ajuda', state='disabled')
        self.menu_bt.menu.add_separator()
        self.menu_bt.menu.add_command(label='Logout', command=self.f_logout)

        self.show_img = tk.PhotoImage(file=resource_path('eye.png'))
        self.show_bt = tk.Button(self.c1_peri, width=24, height=24, bd=0, pady=0)
        self.show_bt['activebackground'] = M_COLOR['p3']
        self.show_bt['command'] = self.f_show_balance
        self.show_bt['image'] = self.show_img
        self.show_bt['bg'] = M_COLOR['p3']
        self.show_bt.place(x=272, y=10)

        self.add_img = tk.PhotoImage(file=resource_path('add.png'))
        self.add_bt = tk.Button(self.f3_peri, width=24, height=24, bd=0, pady=0)
        self.add_bt['activebackground'] = M_COLOR['rp0']
        self.add_bt['command'] = self.f_create_item
        self.add_bt['image'] = self.add_img
        self.add_bt['bg'] = M_COLOR['rp0']
        self.add_bt.grid(row=2, column=3, sticky=E)

        self.x_img = tk.PhotoImage(file=resource_path('x.png'))
        self.clear_bt = tk.Button(self.f3_peri, width=24, height=24, bd=0)
        self.clear_bt['activebackground'] = M_COLOR['rp0']
        self.clear_bt['command'] = self.f_reset_all
        self.clear_bt['image'] = self.x_img
        self.clear_bt['bg'] = M_COLOR['rp0']
        self.clear_bt.grid(row=2, column=3)

        self.check_img = tk.PhotoImage(file=resource_path('check.png'))
        self.sub_item_bt = tk.Button(self.f3_peri, width=24, height=24, bd=0)
        self.sub_item_bt['activebackground'] = M_COLOR['rp0']
        self.sub_item_bt['disabledforeground'] = M_COLOR['rp0']
        self.sub_item_bt['command'] = self.f_create_sub_item
        self.sub_item_bt['image'] = self.check_img
        self.sub_item_bt['state'] = 'disabled'
        self.sub_item_bt['bg'] = M_COLOR['rp0']
        self.sub_item_bt.grid(row=2, column=3, sticky=W)

        # Binds.
        self.bind('<Return>', lambda x: f_invoker(button=self.add_bt))
        self.bind('<Escape>', lambda x: f_invoker(button=self.clear_bt))
        self.bind('<Alt-s>', lambda x: f_invoker(button=self.sub_item_check))
        self.bind('<F1>', lambda x: self.f_bind(1))
        self.bind('<F2>', lambda x: self.f_bind(2))

    def f_load(self):
        global save_status
        try:
            with open(resource_path(username + '.encrypted'), 'rb') as j_file:
                r_file = j_file.read()
                f = Fernet(get_key())
                d_j_file = f.decrypt(r_file).decode()
                self.json_file = json.loads(d_j_file)
                print(self.json_file)
            for i in self.json_file:
                self.item_id = i['id']
        except Exception:  # <class 'cryptography.fernet.InvalidToken'> constancy_wip.py 541
            self.json_file = []
        self.f_balance_load()
        save_status = 'normal'

    def f_bind(self, in_type):
        if in_type == 1:
            self.type_entry.set('Debit')
            f_invoker(self.add_bt)
        else:
            self.type_entry.set('Credit')
            f_invoker(self.add_bt)

    def f_balance_load(self):
        for b in self.json_file:
            self.balance = self.balance + float(b['value'])

    def f_show_balance(self):
        if self.balance_status == 0:
            self.c1_peri.itemconfig(1, text='Saldo: R$ XXXX.XX')
            self.balance_status = 1
        else:
            self.c1_peri.itemconfig(1, text='Saldo: R$ ' + '{0:.2f}'.format(self.balance))
            self.balance_status = 0

    def f_save(self):
        global save_status
        with open(resource_path(str(username + '.encrypted')), 'wb') as j_file:
            f = Fernet(get_key())
            token = f.encrypt(json.dumps(self.json_file).encode())
            j_file.write(token)
        self.f_log_update('Salvo.')
        save_status = 'normal'

    def f_error_msg(self, txt):
        self.attributes('-disabled', 1)
        messagebox.showwarning(title='Erro 33!', message=txt)
        self.attributes('-disabled', 0)

    def f_del_window(self):
        if save_status == 'disabled':
            self.attributes('-disabled', 1)
            if messagebox.askyesno('Saindo', 'Deseja sair sem salvar?'):
                plt.close()
                self.quit()
                self.master.destroy()
            else:
                self.attributes('-disabled', 0)
                self.value_entry.focus_force()
        else:
            plt.close()
            self.master.destroy()

    def f_logout(self):
        if save_status == 'disabled':
            if messagebox.askyesno('Saindo', 'Deseja sair sem salvar?'):
                plt.close()
                self.destroy()
                self.master.deiconify()
            else:
                self.value_entry.focus_force()
        else:
            plt.close()
            self.destroy()
            self.master.deiconify()

    def f_profile(self):
        global log_list
        profile_window = Profile(self.master)
        log_list.append('Perfil aberto.')
        self.withdraw()
        profile_window.focus_force()

    def f_validate_float(self, key_in):
        if key_in == '':
            return True
        try:
            float(key_in)
            return True
        except ValueError:
            self.bell()
            return False

    def f_validate_integer(self, key_in):
        if key_in.isdigit():
            if int(key_in) in [1, 2, 3, 4, 6, 8, 10, 12, 24, 48, 64, 128]:
                return True
            else:
                return False
        elif key_in == '':
            return True
        else:
            self.bell()
            return False

    def f_log_update(self, txt):
        global log_list
        log_list.append(txt)
        self.c2_peri.itemconfig(1, text=log_list[-1])

    def f_reset_all(self):
        if self.value_entry.get() != '' or self.desc_entry.get() != '':
            self.f_log_update('Campos resetados.')
        self.sub_item_total = 0
        self.c2_peri.itemconfig(2, text='')
        self.value_entry.delete(0, 'end')
        self.desc_entry.delete(0, 'end')
        self.sub_item_list.clear()
        self.value_entry.focus_force()

    def f_sub_item_check(self):
        if self.value_entry.get() != '' and self.desc_entry.get() != '':
            if self.sub_item_check.instate(statespec=('selected',)):
                self.sub_desc_entry['state'] = ''
                self.sub_value_entry['state'] = ''
                self.sub_item_bt['state'] = 'normal'
                self.desc_entry['state'] = 'disabled'
                self.value_entry['state'] = 'disabled'
                self.date_entry['state'] = 'disabled'
                self.type_entry['state'] = 'disabled'
                self.clear_bt['state'] = 'disabled'
                self.add_bt['state'] = 'disabled'
                self.sub_desc_entry.delete(0, 'end')
                self.sub_value_entry.delete(0, 'end')
                self.sub_value_entry.focus()
                if self.sub_item_total == 0:
                    self.sub_item_total = float(self.value_entry.get())
                self.c2_peri.itemconfig(2, text='Valor total: ' + str(self.sub_item_total))
            else:
                self.sub_desc_entry.delete(0, 'end')
                self.sub_value_entry.delete(0, 'end')
                self.sub_desc_entry.insert(0, 'Descrição do Subitem')
                self.sub_value_entry.insert(0, 0)
                self.desc_entry['state'] = ''
                self.value_entry['state'] = ''
                self.date_entry['state'] = ''
                self.type_entry['state'] = ''
                self.clear_bt['state'] = 'normal'
                self.add_bt['state'] = 'normal'
                self.sub_desc_entry['state'] = 'disabled'
                self.sub_value_entry['state'] = 'disabled'
                self.sub_item_bt['state'] = 'disabled'
                self.attributes('-disabled', 0)
                self.value_entry.focus()
        else:
            self.f_error_msg(txt='O item precisa ser definido.')
            self.sub_item_check.state(statespec=('!active', '!selected'))
            self.value_entry.focus()

    def f_create_sub_item(self):
        if self.sub_value_entry.get() != '' and self.sub_desc_entry.get() != '':
            if float(self.sub_value_entry.get()) <= float('{0:.2f}'.format(self.sub_item_total)):
                self.sub_item_counter += 1
                self.sub_item_list.append({'sValue': self.sub_value_entry.get(),
                                           'sDesc': self.sub_desc_entry.get()})
                self.sub_item_total = self.sub_item_total - float(self.sub_value_entry.get())
                self.c2_peri.itemconfig(2, text='Valor total: ' + str('{0:.2f}'.format(self.sub_item_total)))
                log_list.append(str(self.sub_item_counter) + 'º Subitem criado.')
                self.c2_peri.itemconfigure(1, text=log_list[-1])
                self.sub_desc_entry.delete(0, 'end')
                self.sub_value_entry.delete(0, 'end')
                self.sub_value_entry.focus()
                if float('{0:.2f}'.format(self.sub_item_total)) == 0:
                    self.sub_item_check.state(statespec=('!selected', '!active'))
                    self.c2_peri.itemconfig(2, text='')
                    self.f_sub_item_check()
            else:
                self.f_error_msg(txt='Valor do subitem fora do valor total.')
                self.sub_value_entry.focus()
        else:
            self.f_error_msg(txt='O subitem precisa ser definido.')
            self.sub_value_entry.focus()

    def f_type(self, value):
        if self.type_entry.get() == 'Debit':
            return str(-float(value))
        else:
            return value

    def f_create_item(self):
        global save_status
        if self.value_entry.get() != '' and self.desc_entry.get() != '':
            if self.sub_item_counter == 0:
                item = {
                    'id': self.item_id + 1,
                    'value': self.f_type(self.value_entry.get()),
                    'description': self.desc_entry.get(),
                    'date': self.date_entry.get(),
                    'type': self.type_entry.get(),
                    'sub': 'None'
                }
                self.json_file.append(item)
                self.item_id += 1
                save_status = 'disabled'
                print(self.json_file)
            else:
                item = {
                    'id': self.item_id + 1,
                    'value': self.f_type(self.value_entry.get()),
                    'description': self.desc_entry.get(),
                    'date': self.date_entry.get(),
                    'type': self.type_entry.get(),
                    'sub': []
                }
                for i in range(0, self.sub_item_counter):
                    item['sub'].append(self.sub_item_list[i])
                self.json_file.append(item)
                self.item_id += 1
                save_status = 'disabled'
                print(self.json_file)
            self.balance = self.balance + float(self.f_type(self.value_entry.get()))
            self.f_reset_all()
            self.f_log_update(txt=str(self.item_id) + 'º Item criado.')
            self.c1_peri.itemconfigure(1, text='Saldo: R$ ' + '{0:.2f}'.format(self.balance))
            self.sub_item_counter = 0
        else:
            self.f_error_msg(txt='O item precisa ser definido.')
            self.value_entry.focus_force()

    def f_graph(self):
        plt.close()
        data = {}
        dates_list = []
        values_list = []
        for d in self.json_file:
            if d['date'] in data:
                n_value = float(d['value']) + float(data.get(d['date']))
                data.update({d['date']: str(n_value)})
            else:
                data.update({d['date']: d['value']})
        ordered_data = sorted(data.items(), key=lambda x: dt.datetime.strptime(x[0], '%d/%m/%y'),
                              reverse=False)
        for d, v in ordered_data:
            values_list.append(float(v))
            dates_list.append(d)
        series = pd.Series(values_list, dtype='float64')
        cumulative_sum = series.cumsum()
        serialized_date = [dt.datetime.strptime(d, '%d/%m/%y').date() for d in dates_list]
        plt.style.use("cyberpunk")
        plt.plot(serialized_date, cumulative_sum, 'm', marker='o')
        plt.xticks(rotation=20)
        plt.subplots_adjust(right=0.95, top=0.93, bottom=0.15)
        fig = plt.gcf()
        manager = plt.get_current_fig_manager()
        fig.canvas.set_window_title('Saldo ao longo do tempo')
        manager.window.wm_iconbitmap(resource_path('icon.ico'))
        # manager.window.SetPosition()
        plt.xlabel('Data')
        plt.ylabel('Saldo')
        self.f_log_update(txt='Gráfico gerado.')
        mplcyberpunk.add_glow_effects()
        plt.show()


class Profile(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        global username
        self.master = master
        self['bg'] = M_COLOR['p3']
        self.title('Constancy WIP')
        self.geo_x = master.winfo_x()
        self.geo_y = master.winfo_y()
        self.transient(master)
        self.geometry('216x260+{}+{}'.format(self.geo_x+0, self.geo_y+0))
        self.protocol('WM_DELETE_WINDOW', self.f_accept)  # change close func
        self.resizable(0, 0)
        self.iconbitmap(resource_path('icon.ico'))

        # Variables.
        self.hidden = True
        self.debit_mean = 0
        self.date_list = []
        self.credit_mean = 0
        try:
            with open(resource_path(username + '.encrypted'), 'rb') as j_file:
                r_file = j_file.read()
                f = Fernet(get_key())
                d_j_file = f.decrypt(r_file).decode()
                self.json_file = json.loads(d_j_file)
                print(self.json_file)
            for i in self.json_file:
                self.item_id = i['id']
        except Exception:  # <class 'cryptography.fernet.InvalidToken'> constancy_wip.py 541
            self.json_file = []
        self.values = set()
        for d in self.json_file:
            self.values.add(d['date'].split('/')[1] + '/' + d['date'].split('/')[2])
        self.values = sorted(list(self.values))
        print(self.values)

        # Background.
        prof_bg = tk.PhotoImage(file=resource_path('prof_back.png'))
        self.background = prof_bg

        self.bg_label = tk.Label(self, width=214, height=36)
        self.bg_label['bg'] = M_COLOR['p3']
        self.bg_label['image'] = prof_bg
        self.bg_label.place(x=0, y=-2)

        prof_f_bg = tk.PhotoImage(file=resource_path('prof_frame_back.png'))
        self.frame_background = prof_f_bg

        self.bg_label = tk.Label(self, width=198, height=146)
        self.bg_label['bg'] = M_COLOR['p3']
        self.bg_label['image'] = prof_f_bg
        self.bg_label.place(x=8, y=106)

        # Frames.
        self.f4_prof = tk.Frame(self)
        self.f4_prof['bg'] = M_COLOR['p3']
        self.f4_prof.place(x=8, y=48)
        self.f4_prof.rowconfigure(1, minsize=40)

        self.f5_prof = tk.Frame(self)  # pass
        self.f5_prof['bg'] = M_COLOR['p3']
        self.f5_prof.place(x=22, y=128)
        self.f5_prof.rowconfigure(1, minsize=25)

        self.f6_prof = tk.Frame(self)
        self.f6_prof['bg'] = M_COLOR['p3']
        self.f6_prof.place(x=22, y=124)
        #
        # self.f7_prof = tk.Frame(self)  # useless
        # self.f7_prof['bg'] = M_COLOR['p3']
        # self.f7_prof.place(x=24, y=268)
        # self.f7_prof.columnconfigure(1, minsize=134)

        # Labels.
        self.name_lb = tk.Label(self.f4_prof, text='Nome:')
        self.name_lb['foreground'] = M_COLOR['p1']
        self.name_lb['background'] = M_COLOR['p3']
        self.name_lb['font'] = M_FONT
        self.name_lb.grid(row=0, column=0, sticky=W)

        self.gmm_lb = tk.Label(self.f6_prof)
        self.gmm_lb['foreground'] = M_COLOR['p1']
        self.gmm_lb['background'] = M_COLOR['p3']
        self.gmm_lb['text'] = ''
        self.gmm_lb['font'] = M_FONT
        self.gmm_lb.grid(row=0, column=0, columnspan=2, sticky=W)

        self.lmm_lb = tk.Label(self.f6_prof)
        self.lmm_lb['foreground'] = M_COLOR['p1']
        self.lmm_lb['background'] = M_COLOR['p3']
        self.lmm_lb['text'] = ''
        self.lmm_lb['font'] = M_FONT
        self.lmm_lb.grid(row=1, column=0, columnspan=2, sticky=W)

        self.gmt_lb = tk.Label(self.f6_prof)
        self.gmt_lb['foreground'] = M_COLOR['p1']
        self.gmt_lb['background'] = M_COLOR['p3']
        self.gmt_lb['text'] = ''
        self.gmt_lb['font'] = M_FONT
        self.gmt_lb.grid(row=2, column=0, columnspan=2, sticky=W)

        self.lmt_lb = tk.Label(self.f6_prof)
        self.lmt_lb['foreground'] = M_COLOR['p1']
        self.lmt_lb['background'] = M_COLOR['p3']
        self.lmt_lb['text'] = ''
        self.lmt_lb['font'] = M_FONT
        self.lmt_lb.grid(row=3, column=0, columnspan=2, sticky=W)

        self.month_lb = tk.Label(self.f6_prof, text='Mês de referência:')
        self.month_lb['foreground'] = M_COLOR['p1']
        self.month_lb['background'] = M_COLOR['p3']
        self.month_lb['font'] = M_FONT
        self.month_lb.grid(row=4, column=0, sticky=W)

        self.old_pw_lb = tk.Label(self.f5_prof, text='Senha atual:')
        self.old_pw_lb['foreground'] = M_COLOR['p1']
        self.old_pw_lb['background'] = M_COLOR['p3']
        self.old_pw_lb['font'] = M_FONT
        self.old_pw_lb.grid(row=0, column=0, sticky=W)

        self.new_pw_lb = tk.Label(self.f5_prof, text='Nova senha:')
        self.new_pw_lb['foreground'] = M_COLOR['p1']
        self.new_pw_lb['background'] = M_COLOR['p3']
        self.new_pw_lb['font'] = M_FONT
        self.new_pw_lb.grid(row=1, column=0, sticky=W)

        self.conf_pw_lb = tk.Label(self.f5_prof, text='Confirme:')
        self.conf_pw_lb['foreground'] = M_COLOR['p1']
        self.conf_pw_lb['background'] = M_COLOR['p3']
        self.conf_pw_lb['font'] = M_FONT
        self.conf_pw_lb.grid(row=2, column=0, sticky=W)

        # Entries.
        self.name_entry = tk.Entry(self.f4_prof, width=18, bd=0)
        self.name_entry.insert(0, username)
        self.name_entry['state'] = 'disabled'
        self.name_entry['font'] = M_FONT
        self.name_entry['background'] = M_COLOR['p3']
        self.name_entry['disabledbackground'] = M_COLOR['p3']
        self.name_entry['foreground'] = M_COLOR['p1']
        self.name_entry['disabledforeground'] = M_COLOR['p1']
        self.name_entry.grid(row=0, column=1)

        self.old_pw_entry = ttk.Entry(self.f5_prof, width=14, show='*')
        self.old_pw_entry.grid(row=0, column=1)

        self.new_pw_entry = ttk.Entry(self.f5_prof, width=14, show='*')
        self.new_pw_entry.grid(row=1, column=1)

        self.conf_pw_entry = ttk.Entry(self.f5_prof, width=14, show='*')
        self.conf_pw_entry.grid(row=2, column=1)

        self.month_cBox = ttk.Combobox(self.f6_prof, width=6)
        self.month_cBox['values'] = self.values
        self.month_cBox.grid(row=4, column=1, sticky=E)
        self.month_cBox.set(self.values[-1])

        self.f_month_mean()

        # Buttons.
        self.edit_img = tk.PhotoImage(file=resource_path('edit.png'))
        self.name_edit_bt = tk.Button(self.f4_prof, width=20, height=16, bd=0)
        self.name_edit_bt['activebackground'] = M_COLOR['p3']
        self.name_edit_bt['image'] = self.edit_img
        self.name_edit_bt['command'] = self.f_name_edit
        self.name_edit_bt['bg'] = M_COLOR['p3']
        self.name_edit_bt.grid(row=0, column=2)

        self.confirm_img = tk.PhotoImage(file=resource_path('check2.png'))
        self.name_confirm_bt = tk.Button(self.f4_prof, width=20, height=16, bd=0)
        self.name_confirm_bt['activebackground'] = M_COLOR['p3']
        self.name_confirm_bt['image'] = self.confirm_img
        self.name_confirm_bt['command'] = self.f_name_edit
        self.name_confirm_bt['bg'] = M_COLOR['p3']
        self.name_confirm_bt.grid(row=0, column=2)
        self.name_confirm_bt.grid_remove()

        self.change_pw_toggle_bt = tk.Button(self.f4_prof, text='Mudar senha', width=9, height=1, bd=0)
        self.change_pw_toggle_bt['activebackground'] = M_COLOR['p3']
        self.change_pw_toggle_bt['activeforeground'] = M_COLOR['p1']
        self.change_pw_toggle_bt['foreground'] = M_COLOR['p1']
        self.change_pw_toggle_bt['font'] = M_FONT
        self.change_pw_toggle_bt['command'] = lambda: self.f_change_frame(self.f5_prof)
        self.change_pw_toggle_bt['bg'] = M_COLOR['p3']
        self.change_pw_toggle_bt.grid(row=1, column=0, columnspan=2, sticky=W)

        self.back_bt = tk.Button(self.f5_prof, text='Voltar', width=6, height=2, bd=0)
        self.back_bt['activebackground'] = M_COLOR['p3']
        self.back_bt['activeforeground'] = M_COLOR['p1']
        self.back_bt['foreground'] = M_COLOR['p1']
        self.back_bt['font'] = M_FONT
        self.back_bt['command'] = lambda: self.f_change_frame(self.f6_prof)
        self.back_bt['bg'] = M_COLOR['p3']
        self.back_bt.grid(row=3, column=0, sticky=W)

        self.change_pw_bt = tk.Button(self.f5_prof, text='Confirmar', width=11, height=2, bd=0)
        self.change_pw_bt['activebackground'] = M_COLOR['p3']
        self.change_pw_bt['activeforeground'] = M_COLOR['p1']
        self.change_pw_bt['foreground'] = M_COLOR['p1']
        self.change_pw_bt['font'] = M_FONT
        # self.change_pw_bt['command'] = lambda: self.f_change_frame(self.f6_prof)
        self.change_pw_bt['bg'] = M_COLOR['p3']
        self.change_pw_bt.grid(row=3, column=1, sticky=E)

        # Binds.
        self.month_cBox.bind('<<ComboboxSelected>>', self.f_month_mean)

    def f_name_edit(self):
        global username, log_list
        if self.hidden:
            self.name_entry['state'] = 'normal'
            self.name_entry.focus()
            self.name_entry.select_range(0, 'end')
            self.name_edit_bt.grid_remove()
            self.name_confirm_bt.grid()
            self.hidden = False
        else:
            if self.name_entry.get() != username:
                with open(resource_path('users.bin'), 'rb') as r_users:
                    users_dict = r_users.read().decode()
                with open(resource_path('users.bin'), 'wb') as w_users:
                    w_users.write(users_dict.replace(username, self.name_entry.get()).encode())
                os.rename(resource_path(username + '.encrypted'), resource_path(self.name_entry.get() + '.encrypted'))
                username = self.name_entry.get()
                log_list.append('Perfil modificado.')
            self.name_entry['state'] = 'disabled'
            self.name_confirm_bt.grid_remove()
            self.name_edit_bt.grid()
            self.hidden = True

    def f_month_mean(self, event=None):
        self.month_cBox.select_clear()
        month = self.month_cBox.get().split('/')[0]  # self.date.get()
        year = self.month_cBox.get().split('/')[1]  # self.date.get()
        debit_list = []
        credit_list = []
        for t in self.json_file:
            if month == t['date'].split('/')[1]:
                if t['type'] == "Debit":
                    debit_list.append(float(t["value"]))
                else:
                    credit_list.append(float(t['value']))
        if month == dt.datetime.now().strftime('%m'):
            d_mean = sum(debit_list)/int(dt.date.today().day)
            c_mean = sum(credit_list)/int(dt.date.today().day)
        else:
            d_mean = sum(debit_list)/calendar.monthrange(int(year), int(month))[1]
            c_mean = sum(credit_list)/calendar.monthrange(int(year), int(month))[1]
        d_total = sum(debit_list)
        c_total = sum(credit_list)
        self.gmm_lb.configure(text='Gasto médio diário: ' + str('{0:.2f}'.format(-d_mean)))
        self.lmm_lb.configure(text='Lucro médio diário: ' + str('{0:.2f}'.format(c_mean)))
        self.gmt_lb.configure(text='Despesa mensal: ' + str('{0:.2f}'.format(-d_total)))
        self.lmt_lb.configure(text='Receita mensal: ' + str('{0:.2f}'.format(c_total)))

    def f_change_frame(self, frame):
        frame.tkraise()
        self.old_pw_entry.focus()

    def f_accept(self):  # acept pw change (change file/encrypt pw)
        self.withdraw()
        peripheral_window = Peripheral(self.master)


def f_invoker(button, event=None):
    button.invoke()


def get_key():
    with open(resource_path('lk.key'), 'rb') as key_file:
        key = key_file.read()
    return key


def f_encrypt(password):
    f_key = Fernet(get_key())
    token = f_key.encrypt(str(password).encode())
    return token


def resource_path(relative_path):
    # Get absolute path to resource, works for dev and for PyInstaller
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def main():
    primary = tk.Tk()
    login_window = Main(primary)
    primary.mainloop()


if __name__ == '__main__':
    # Faz com que o programa não rode assim que importado/criado.
    main()
