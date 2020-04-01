###
# erro 121 - senha ou usuario incorreto.
# erro 33 - valor ou descrição não definidos.
# erro 157 - erro de criacao de usuario (senha/usuario)

# f1 - enter with debit.
# f2 - enter with credit.
# esc - reset entries.
###

# Packages.
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import os
import ast
import json
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
        master.geometry('216x440+220+500')  # SE
        master.iconbitmap(resource_path('icon.ico'))
        master.attributes('-topmost', 1)
        master.overrideredirect(1)
        master.resizable(0, 0)
        master.attributes('-alpha', 0.9)
        master['bg'] = M_COLOR['p3']
        master.title('')

        # Files.
        self.users = {}

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
        self.name_entry.focus_set()

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
        self.login_bt = tk.Button(self.f1_main, width=24, height=24, bd=0, text='Login', pady=0)
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


class Create(tk.Toplevel):  # usar strvar e trace para validar o nome de usuario
    def __init__(self, master):
        # Configs.
        tk.Toplevel.__init__(self, master)
        self.master = master
        self.grab_set()
        self.geometry('304x200+420+500')  # SE
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
                        with open(resource_path(str(self.user_entry.get() + '.json')), 'w+') as user_init:
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
        self.geometry('480x216+220+500')
        self.iconbitmap(resource_path('icon.ico'))
        self['bg'] = M_COLOR['rp0']
        self.protocol('WM_DELETE_WINDOW', self.f_del_window)
        self.title('Constancy WIP')
        self.register_f = self.register(self.f_validate_float)
        self.register_i = self.register(self.f_validate_integer)

        # Variables.
        self.item_id = 0
        self.balance = 0
        self.balance_status = 0
        self.sub_item_total = 0
        self.sub_item_counter = 0
        self.log_list = ['Iniciado.', ]
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
        self.balance_lbl = self.c1_peri.create_text(356, 24, font=M_FONT,
                                                    text='Saldo: R$ ' + '{0:.2f}'.format(self.balance),
                                                    fill=M_COLOR['p1'], anchor=W)

        self.welcome_lbl = self.c1_peri.create_text(44, 24, font=M_FONT,
                                                    text='Bem vindo, ' + username + '.',
                                                    fill=M_COLOR['p1'], anchor=W)

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

        self.parc_lbl = tk.Label(self.f3_peri, text='Fração:')
        self.parc_lbl['foreground'] = M_COLOR['p0']
        self.parc_lbl['font'] = M_FONT
        self.parc_lbl['bg'] = M_COLOR['rp0']
        self.parc_lbl.grid(row=0, column=3, sticky=W)

        self.type_lbl = tk.Label(self.f3_peri, text='Tipo:')
        self.type_lbl['foreground'] = M_COLOR['p0']
        self.type_lbl['font'] = M_FONT
        self.type_lbl['bg'] = M_COLOR['rp0']
        self.type_lbl.grid(row=0, column=4, sticky=W)

        self.log_lbl = self.c2_peri.create_text(8, 12, font=M_FONT, text=self.log_list[-1],
                                                fill=M_COLOR['p3'], anchor=W)

        self.sub_item_total_lbl = self.c2_peri.create_text(472, 12, font=M_FONT, text='',
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

        self.parc_entry = ttk.Combobox(self.f3_peri, width=4, justify=RIGHT)
        self.parc_entry['values'] = [1, 2, 3, 4, 6, 8, 10, 12, 24, 32, 64, 128]
        self.parc_entry['height'] = 5
        self.parc_entry['font'] = M_FONT
        self.parc_entry.grid(row=1, column=3, sticky=W)
        self.parc_entry.config(validate='key', validatecommand=(self.register_i, '%P'))
        self.parc_entry.set(1)

        self.type_entry = ttk.Combobox(self.f3_peri, width=8)
        self.type_entry['values'] = ['Debit', 'Credit']
        self.type_entry['height'] = 2
        self.type_entry['state'] = 'readonly'
        self.type_entry['font'] = M_FONT
        self.type_entry.grid(row=1, column=4)
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
        self.menu_bt.menu.add_command(label='Log', state='disabled')
        self.menu_bt.menu.add_command(label='Abrir', command=self.f_load)
        self.menu_bt.menu.add_command(label='Salvar', command=self.f_save)
        self.menu_bt.menu.add_command(label='Gráfico', command=self.f_graph)
        self.menu_bt.menu.add_command(label='Extrato', state='disabled')
        self.menu_bt.menu.add_separator()
        self.menu_bt.menu.add_command(label='Perfil', state='disabled')
        self.menu_bt.menu.add_separator()
        self.menu_bt.menu.add_command(label='Logout', command=self.f_logout)

        self.show_img = tk.PhotoImage(file=resource_path('eye.png'))
        self.show_bt = tk.Button(self.c1_peri, width=24, height=24, bd=0, pady=0)
        self.show_bt['activebackground'] = M_COLOR['p3']
        self.show_bt['command'] = self.f_show_balance
        self.show_bt['image'] = self.show_img
        self.show_bt['bg'] = M_COLOR['p3']
        self.show_bt.place(x=324, y=10)

        self.add_img = tk.PhotoImage(file=resource_path('add.png'))
        self.add_bt = tk.Button(self.f3_peri, width=24, height=24, bd=0, pady=0)
        self.add_bt['activebackground'] = M_COLOR['rp0']
        self.add_bt['command'] = self.f_create_item
        self.add_bt['image'] = self.add_img
        self.add_bt['bg'] = M_COLOR['rp0']
        self.add_bt.grid(row=2, column=4, sticky=E)

        self.x_img = tk.PhotoImage(file=resource_path('x.png'))
        self.clear_bt = tk.Button(self.f3_peri, width=24, height=24, bd=0)
        self.clear_bt['activebackground'] = M_COLOR['rp0']
        self.clear_bt['command'] = self.f_reset_all
        self.clear_bt['image'] = self.x_img
        self.clear_bt['bg'] = M_COLOR['rp0']
        self.clear_bt.grid(row=2, column=4)

        self.check_img = tk.PhotoImage(file=resource_path('check.png'))
        self.sub_item_check_bt = tk.Button(self.f3_peri, width=24, height=24, bd=0)
        self.sub_item_check_bt['activebackground'] = M_COLOR['rp0']
        self.sub_item_check_bt['disabledforeground'] = M_COLOR['rp0']
        self.sub_item_check_bt['command'] = self.f_create_sub_item
        self.sub_item_check_bt['image'] = self.check_img
        self.sub_item_check_bt['state'] = 'disabled'
        self.sub_item_check_bt['bg'] = M_COLOR['rp0']
        self.sub_item_check_bt.grid(row=2, column=3, sticky=W)

        # Binds.
        self.parc_entry.bind('<<ComboboxSelected>>', self.f_reset_parc_selection)
        self.bind('<Return>', lambda x: f_invoker(button=self.add_bt))
        self.bind('<Escape>', lambda x: f_invoker(button=self.clear_bt))

    def f_load(self):  # abrir filedialog > escolher arquivo > substituir self.json_file
        with open(resource_path(str(username + '.json')), 'r', encoding='utf-8') as j_file:
            self.json_file = json.load(j_file)
            print(self.json_file)
        for i in self.json_file:
            self.item_id = i['id']
        self.f_balance_load()

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
        with open(resource_path(str(username + '.json')), 'w', encoding='utf-8') as j_file:
            json.dump(self.json_file, j_file, indent=4)
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
                self.quit()
                self.master.destroy()
            else:
                self.attributes('-disabled', 0)
                self.value_entry.focus_force()
        else:
            self.master.destroy()

    def f_logout(self):
        if save_status == 'disabled':
            if messagebox.askyesno('Saindo', 'Deseja sair sem salvar?'):
                self.destroy()
                self.master.deiconify()
            else:
                self.value_entry.focus_force()
        else:
            self.destroy()

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
        self.log_list.append(txt)
        self.c2_peri.itemconfig(1, text=self.log_list[-1])

    def f_reset_parc_selection(self, event=None):
        self.parc_entry.selection_clear()

    def f_reset_all(self):
        if self.value_entry.get() != '' or self.desc_entry.get() != '':
            self.f_log_update('Campos resetados.')
        self.sub_item_total = 0
        self.c2_peri.itemconfig(2, text='')
        self.value_entry.delete(0, 'end')
        self.parc_entry.set('1')
        self.desc_entry.delete(0, 'end')
        self.sub_item_list.clear()
        self.value_entry.focus_force()

    def f_sub_item_check(self):
        if self.value_entry.get() != '' and self.desc_entry.get() != '':
            if self.sub_item_check.instate(statespec=('selected',)):
                self.sub_desc_entry['state'] = ''
                self.sub_value_entry['state'] = ''
                self.sub_item_check_bt['state'] = 'normal'
                self.desc_entry['state'] = 'disabled'
                self.value_entry['state'] = 'disabled'
                self.date_entry['state'] = 'disabled'
                self.parc_entry['state'] = 'disabled'
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
                self.parc_entry['state'] = ''
                self.type_entry['state'] = ''
                self.clear_bt['state'] = 'normal'
                self.add_bt['state'] = 'normal'
                self.sub_desc_entry['state'] = 'disabled'
                self.sub_value_entry['state'] = 'disabled'
                self.sub_item_check_bt['state'] = 'disabled'
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
                self.log_list.append(str(self.sub_item_counter) + 'º Subitem criado.')
                self.c2_peri.itemconfigure(1, text=self.log_list[-1])
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
        if self.value_entry.get() != '' and self.desc_entry.get() != '':
            if self.sub_item_counter == 0:
                item = {
                    'id': self.item_id + 1,
                    'value': self.f_type(self.value_entry.get()),
                    'description': self.desc_entry.get(),
                    'date': self.date_entry.get(),
                    'parc': self.parc_entry.get(),
                    'type': self.type_entry.get(),
                    'sub': 'None'
                }
                self.json_file.append(item)
                self.item_id += 1
                print(self.json_file)
            else:
                item = {
                    'id': self.item_id + 1,
                    'value': self.f_type(self.value_entry.get()),
                    'description': self.desc_entry.get(),
                    'date': self.date_entry.get(),
                    'parc': self.parc_entry.get(),
                    'type': self.type_entry.get(),
                    'sub': []
                }
                for i in range(0, self.sub_item_counter):
                    item['sub'].append(self.sub_item_list[i])
                self.json_file.append(item)
                self.item_id += 1
                print(self.json_file)
            self.balance = self.balance + float(self.f_type(self.value_entry.get()))
            self.f_reset_all()
            self.f_log_update(txt=str(self.item_id) + 'º Item criado.')
            self.c1_peri.itemconfigure(1, text='Saldo: R$ ' + '{0:.2f}'.format(self.balance))
            self.sub_item_counter = 0
        else:
            self.f_error_msg(txt='O item precisa ser definido.')

    def f_graph(self):
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
        series = pd.Series(values_list)
        cumulative_sum = series.cumsum()
        serialized_date = [dt.datetime.strptime(d, '%d/%m/%y').date() for d in dates_list]
        plt.plot(serialized_date, cumulative_sum, 'm', marker='o')
        plt.xticks(rotation=20)
        plt.subplots_adjust(right=0.95, top=0.93, bottom=0.15)
        plt.title('Saldo ao longo do tempo.')
        plt.xlabel('Data')
        plt.ylabel('Saldo')
        self.f_log_update(txt='Gráfico gerado.')
        plt.show()


def f_invoker(button, event=None):
    button.invoke()


def get_key():
    with open(resource_path('lk.bin'), 'rb') as key_file:
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
