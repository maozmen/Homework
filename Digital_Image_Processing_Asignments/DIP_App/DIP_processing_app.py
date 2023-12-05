# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 13:11:36 2022

@author: ozmen
"""
import tkinter.filedialog
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from collections import defaultdict
from matplotlib import pyplot as plt
from os import remove
import copy
from math import pi, e

class App(tk.Tk):
    def __init__(self):
        super().__init__()     
        
        self.options_frame = None
        self.image_frame = None
        self.navigation_frame = None
        self.image = None
        self.image_zoom = None
        self.zoom_ratio = 1.0
        self.zoom_ratio_change = 0.9
        self.zoom_nw = 0, 0
        self.image_display = None
        self.button_press = None
        self.format = tk.StringVar()
        
        Si = 0.7 #Size ratio of main screen to display screen
        Wi = round(self.winfo_screenwidth()*Si) #Width 
        He = round(self.winfo_screenheight()*Si) #Height
        self.geometry(f"{Wi}x{He}+{round(Wi*(0.5/Si-0.5))}+"\
                      f"{round(He*(0.5/Si-0.5))}")
        self.title('Login')
        self.resizable(False, False)

        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=5)
        self.rowconfigure(0, weight = 7)
        self.rowconfigure(1, weight = 1)
        
        self.create_frames()
        self.create_window1(None)
    
    def create_frames(self):
        self.options_frame = ttk.Frame(self,relief='ridge',borderwidth=5)
        self.options_frame.grid(column = 0, row = 0,sticky='nsew')
        
        self.image_frame = ttk.Frame(self,relief='ridge',borderwidth=5)
        self.image_frame.grid(column = 1, row = 0,sticky='nsew')
        
        self.navigation_frame = ttk.Frame(self,relief='ridge',borderwidth=5)
        self.navigation_frame.grid(column = 1, row = 1,sticky='nsew')
        
        self.update_idletasks()
        next_button = ttk.Button(self.navigation_frame, text="İleri")
        next_button.pack(side=tk.RIGHT,padx=round(self.winfo_width()*0.05))        
        prev_button = ttk.Button(self.navigation_frame, text="Geri")
        prev_button.pack(side= tk.RIGHT)
    
    def destroy_widgets(self, e):
        for frame in self.winfo_children()[:-1]:
            for widget in frame.winfo_children():
                widget.destroy()
    
    def create_window1(self, e):

        image_label = ttk.Label(self.image_frame, image=self.image_display)
        image_label.pack(pady=round(self.winfo_height()*0.04))

        open_image_button = ttk.Button(self.options_frame, text="Resim Aç",
                                       command=self.select_file)
        open_image_button.pack(pady=round(self.winfo_height()*0.04))
        
        show_path_label = ttk.Label(self.options_frame)
        show_path_label.pack(pady=round(self.winfo_height()*0.04))
        
        next_button = self.navigation_frame.winfo_children()[0]
        prev_button = self.navigation_frame.winfo_children()[1]
        prev_button['state'] = 'disabled'
        next_button.bind("<Button-1>", self.destroy_widgets)
        next_button.bind("<Button-1>", self.create_window2, add = '+')
        
    def create_window2(self, e):
        next_button = self.navigation_frame.winfo_children()[0]
        prev_button = self.navigation_frame.winfo_children()[1]
        prev_button['state'] = 'normal'
        prev_button.bind("<Button-1>", self.destroy_widgets)
        prev_button.bind("<Button-1>", self.create_window1, add = '+')
        prev_button.bind("<Button-1>", self.zoom_remove, add = '+')
        next_button.bind("<Button-1>", self.destroy_widgets)
        next_button.bind("<Button-1>", self.create_window3, add = '+')
        next_button.bind("<Button-1>", self.zoom_remove, add = '+')
        
        rb_option = tk.StringVar()
        rb1 = ttk.Radiobutton(self.options_frame, text = 'Ön İşleme'\
                              'Uygulamak İstiyorum', value = 'Uygula',
                              variable = rb_option,
                              command= lambda: \
                                  self.options_frame.winfo_children()[2].\
                                      configure(state = 'normal'))
        rb2 = ttk.Radiobutton(self.options_frame, text = 'Ön İşleme'\
                              'Uygulamak İstemiyorum', value = 'Uygulama',
                              variable = rb_option,
                              command= lambda: \
                                  self.options_frame.winfo_children()[2].\
                                      configure(state = 'disabled'))
        rb1.pack(pady=round(self.winfo_height()*0.04))
        rb2.pack()
        
        menu_option = tk.StringVar()
        menu_button = ttk.Menubutton(self.options_frame, 
                                     text ='Ön İşlem Menüsü - 1')
        menu = tk.Menu(menu_button, tearoff = False)
        menu.add_radiobutton(label = 'Renkli resmi gri seviye resme dönüştür',
                             variable = menu_option,
                             command = self.gray_scale)
        menu.add_radiobutton(label = 'Gri seviye resmi siyah beyaz'\
                             ' resme dönüştür',
                             variable = menu_option,
                             command = self.black_and_white_start)
        menu.add_radiobutton(label = 'Resmi kırp',
                             variable = menu_option,
                             command = self.crop_prepare)
        menu.add_radiobutton(label = 'Resme zoom yap',
                             variable = menu_option,
                             command = self.zoom_prepare)
        menu_button['menu'] = menu
        menu_button.pack(pady=round(self.winfo_height()*0.04))
        menu_button['state'] ='disabled'
        
        image_label = ttk.Label(self.image_frame, image=self.image_display)
        image_label.pack(pady=round(self.winfo_height()*0.04))
    
    

    def create_window3(self, e):
        next_button = self.navigation_frame.winfo_children()[0]
        prev_button = self.navigation_frame.winfo_children()[1]
        prev_button.bind("<Button-1>", self.destroy_widgets)
        prev_button.bind("<Button-1>", self.create_window2, add = '+')
        next_button.bind("<Button-1>", self.destroy_widgets)
        next_button.bind("<Button-1>", self.create_window4, add = '+')
        
        rb_option = tk.StringVar()
        rb1 = ttk.Radiobutton(self.options_frame, text = 'Ön İşleme'\
                              'Uygulamak İstiyorum', value = 'Uygula',
                              variable = rb_option,
                              command= lambda: \
                                  self.options_frame.winfo_children()[2].\
                                      configure(state = 'normal'))
        rb2 = ttk.Radiobutton(self.options_frame, text = 'Ön İşleme'\
                              'Uygulamak İstemiyorum', value = 'Uygulama',
                              variable = rb_option,
                              command= lambda: \
                                  self.options_frame.winfo_children()[2].\
                                      configure(state = 'disabled'))
        rb1.pack(pady=round(self.winfo_height()*0.04))
        rb2.pack()
        
        menu_option = tk.StringVar()
        menu_button = ttk.Menubutton(self.options_frame, 
                                     text ='Ön İşlem Menüsü - 2')
        menu = tk.Menu(menu_button, tearoff = False)
        menu.add_radiobutton(label = 'Histogram oluştur',
                             variable = menu_option,
                             command = self.histogram)
        menu.add_radiobutton(label = 'Histogram eşitle',
                             variable = menu_option,
                             command = self.histogram_equalization)
        menu.add_radiobutton(label = 'Görüntü Nicemle',
                             variable = menu_option,
                             command = self.quantization_start)
        menu_button['menu'] = menu
        menu_button.pack(pady=round(self.winfo_height()*0.04))
        menu_button['state'] ='disabled'
        
        image_label = ttk.Label(self.image_frame, image=self.image_display)
        image_label.pack(pady=round(self.winfo_height()*0.04))
        
    def create_window4(self, e):
        next_button = self.navigation_frame.winfo_children()[0]
        prev_button = self.navigation_frame.winfo_children()[1] 
        prev_button.bind("<Button-1>", self.destroy_widgets)
        prev_button.bind("<Button-1>", self.create_window3, add = '+')
        next_button.bind("<Button-1>", self.destroy_widgets)
        next_button.bind("<Button-1>", self.create_window5, add = '+')
        
        rb_option = tk.StringVar()
        rb1 = ttk.Radiobutton(self.options_frame, text = 'Filtreleme'\
                              'Uygulamak İstiyorum', value = 'Uygula',
                              variable = rb_option,
                              command= lambda: \
                                  self.options_frame.winfo_children()[2].\
                                      configure(state = 'normal'))
        rb2 = ttk.Radiobutton(self.options_frame, text = 'Filtreleme'\
                              'Uygulamak İstemiyorum', value = 'Uygulama',
                              variable = rb_option,
                              command= lambda: \
                                  self.options_frame.winfo_children()[2].\
                                      configure(state = 'disabled'))
        rb1.pack(pady=round(self.winfo_height()*0.04))
        rb2.pack()
        
        menu_option = tk.StringVar()
        menu_button = ttk.Menubutton(self.options_frame, 
                                     text ='Filtreleme Menüsü')
        menu = tk.Menu(menu_button, tearoff = False)
        menu.add_radiobutton(label = 'Gaussian bulanıklaştırma filtresi',
                             variable = menu_option,
                             command = self.gaussian_filter_start)
        menu.add_radiobutton(label = 'Keskinleştirme filtresi',
                             variable = menu_option,
                             command = self.sharpening_filter)
        menu.add_radiobutton(label = 'Kenar bulma filtresi',
                             variable = menu_option,
                             command = self.edge_detection_filter)
        menu.add_radiobutton(label = 'Ortalama filtresi',
                             variable = menu_option,
                             command = self.mean_filter)
        menu.add_radiobutton(label = 'Ortanca filtresi',
                             variable = menu_option,
                             command = self.median_filter)
        menu.add_radiobutton(label = 'Kontra harmonik ortalama filtresi',
                             variable = menu_option,
                             command = self.contra_harmonic_filter_start)
        menu_button['menu'] = menu
        menu_button.pack(pady=round(self.winfo_height()*0.04))
        menu_button['state'] ='disabled'
        
        image_label = ttk.Label(self.image_frame, image=self.image_display)
        image_label.pack(pady=round(self.winfo_height()*0.04))
        
    def create_window5(self, e):
        next_button = self.navigation_frame.winfo_children()[0]
        prev_button = self.navigation_frame.winfo_children()[1]
        next_button['state'] = 'normal'
        prev_button.bind("<Button-1>", self.destroy_widgets)
        prev_button.bind("<Button-1>", self.create_window4, add = '+')
        next_button.bind("<Button-1>", self.destroy_widgets)
        next_button.bind("<Button-1>", self.create_window6, add = '+')
        
        rb_option = tk.StringVar()
        rb1 = ttk.Radiobutton(self.options_frame, text = 'Morfolojik işlem'\
                              'Uygulamak İstiyorum', value = 'Uygula',
                              variable = rb_option,
                              command= lambda: \
                                  self.options_frame.winfo_children()[2].\
                                      configure(state = 'normal'))
        rb2 = ttk.Radiobutton(self.options_frame, text = 'Morfolojik işlem'\
                              'Uygulamak İstemiyorum', value = 'Uygulama',
                              variable = rb_option,
                              command= lambda: \
                                  self.options_frame.winfo_children()[2].\
                                      configure(state = 'disabled'))
        rb1.pack(pady=round(self.winfo_height()*0.04))
        rb2.pack()
        
        menu_option = tk.StringVar()
        menu_button = ttk.Menubutton(self.options_frame, 
                                     text ='Morfolojik İşlem Menüsü')
        menu = tk.Menu(menu_button, tearoff = False)
        menu.add_radiobutton(label = 'Genişletme uygula',
                             variable = menu_option,
                             command = self.dilation)
        menu.add_radiobutton(label = 'Erozyon uygula',
                             variable = menu_option,
                             command = self.erosion)
        menu.add_radiobutton(label = 'İskelet çıkar',
                             variable = menu_option,
                             command = self.skeletonization_start)
        menu_button['menu'] = menu
        menu_button.pack(pady=round(self.winfo_height()*0.04))
        menu_button['state'] ='disabled'
        
        image_label = ttk.Label(self.image_frame, image=self.image_display)
        image_label.pack(pady=round(self.winfo_height()*0.04))
        
    def create_window6(self, e):
        next_button = self.navigation_frame.winfo_children()[0]
        prev_button = self.navigation_frame.winfo_children()[1]  
        next_button['state'] = 'disabled'
        prev_button.bind("<Button-1>", self.destroy_widgets)
        prev_button.bind("<Button-1>", self.create_window5, add = '+')
        
        label = ttk.Label(self.options_frame, text = 'Hangi Formatta'\
                          'Kaydetmek İstersiniz?')
        label.pack(pady=round(self.winfo_height()*0.04))
        
        menu_button = ttk.Menubutton(self.options_frame, 
                                     text ='Formatı Seç')
        menu = tk.Menu(menu_button, tearoff = False)
        menu.add_radiobutton(label = 'İşlenmiş_resim.jpg',
                             value = 'İşlenmiş_resim.jpg',
                             variable = self.format)
        menu.add_radiobutton(label = 'İşlenmiş_resim.bmp',
                             value = 'İşlenmiş_resim.bmp',
                             variable = self.format)
        menu.add_radiobutton(label = 'İşlenmiş_resim.png',
                             value = 'İşlenmiş_resim.png',
                             variable = self.format)
        menu_button['menu'] = menu
        menu_button.pack()
        
        save_button = ttk.Button(self.options_frame, text = 'RESMİ KAYDET',
                                 command = self.save_image)
        save_button.pack(pady=round(self.winfo_height()*0.04))
        
        image_label = ttk.Label(self.image_frame, image=self.image_display)
        image_label.pack(pady=round(self.winfo_height()*0.04))
    
    def dilation(self, d_filter=[[0,1,0],[1,1,1],[0,1,0]]):
        image_list = list(self.image.getdata())
        size = self.image.size

        filter_size = len(d_filter)
        n = filter_size // 2
        
        image_list_list = self.before_convolution(image_list, size)
        rows = len(image_list_list)
        columns = len(image_list_list[0])
        processed = [[image_list_list[i][j] for j in range(columns)] 
                     for i in range(rows)]
        for row in range(rows):
            for column in range(columns):
                if image_list_list[row][column] == 255:
                    for i in range(-n, n + 1):
                        for j in range(-n, n + 1):
                            if row + i >= 0 and row + i < rows and\
                              column + j >=0 and column + j < columns and\
                              d_filter[n+i][n+j] == True:
                                processed[row+i][column+j] = 255
        
        image_list = self.after_convolution(processed)
                
        dilated_image = Image.new('L', size)
        dilated_image.putdata(image_list)
        self.image = dilated_image
        self.image_display = ImageTk.PhotoImage(self.image)
        self.image_frame.winfo_children()[0].configure(\
                                             image=self.image_display)
        self.update()
        
    
    def erosion(self, e_filter=[[0,1,0],[1,1,1],[0,1,0]]):
        image_list = list(self.image.getdata())
        size = self.image.size

        filter_size = len(e_filter)
        n = filter_size // 2
        
        image_list_list = self.before_convolution(image_list, size)
        rows = len(image_list_list)
        columns = len(image_list_list[0])
        processed = [[0 for j in range(columns)] for i in range(rows)]
        for row in range(rows):
            for column in range(columns):
                fits = True
                for i in range(-n, n + 1):
                    if fits == False:
                        break
                    for j in range(-n, n + 1):
                        if fits == False:
                            break
                        if row + i >= 0 and row + i < rows and\
                          column + j >=0 and column + j < columns and\
                          e_filter[n+i][n+j] == True:
                            if image_list_list[row+i][column+j] != 255:
                                    fits = False
                if fits:
                    processed[row][column] = 255
        image_list = self.after_convolution(processed)
                
        dilated_image = Image.new('L', size)
        dilated_image.putdata(image_list)
        self.image = dilated_image
        self.image_display = ImageTk.PhotoImage(self.image)
        self.image_frame.winfo_children()[0].configure(\
                                             image=self.image_display)
        self.update()
    
    def skeletonization_start(self):
        label = ttk.Label(self.options_frame, text = '+ Şeklindeki'\
                          ' filtrenin boyutu')
        label.pack(side = tk.LEFT, padx = round(self.winfo_width() * 0.02))
        
        treshold = tk.StringVar()
        entry = ttk.Entry(self.options_frame, textvariable = treshold)
        entry.pack(side = tk.LEFT)
        
        button = ttk.Button(self.options_frame, text = 'İskelet çıkar',
                            command = self.skeletonization_end)
        button.pack(side = tk.LEFT, padx = round(self.winfo_width() * 0.02))
    
    def skeletonization_end(self):
        image_list = list(self.image.getdata())

        skeletonized_image_list = [0 for _ in range(len(image_list))]
        
        s_filter_size = int(self.options_frame.winfo_children()[-2].get()) 
        s_filter = [[False for _ in range(s_filter_size)] 
                    for __ in range(s_filter_size)]
        for i in range(s_filter_size):
            s_filter[i][s_filter_size//2] = True
            s_filter[s_filter_size//2][i] = True
        
        all_black = False
        while not all_black:
            all_black = True
            for value in image_list:
                if value == 255:
                    all_black = False
                    break
            self.erosion(s_filter)
            self.dilation(s_filter)
            processed = list(self.image.getdata())
            for i, (value1, value2) in enumerate(zip(image_list, processed)):
                if value1 != value2:
                    skeletonized_image_list[i] = 255
            self.erosion(s_filter)   
            image_list = list(self.image.getdata())
        
        size = self.image.size
        skeletized_image = Image.new('L', size)
        skeletized_image.putdata(skeletonized_image_list)
        self.image = skeletized_image
        self.image_display = ImageTk.PhotoImage(self.image)
        self.image_frame.winfo_children()[0].configure(\
                                             image=self.image_display)
        for i in range(-3,0,1):
            self.options_frame.winfo_children()[i].destroy()    
    
    def save_image(self):
        self.image.save(f'.\\{self.format.get()}')
        
    def convolution(self, image, size, conv, absolute = False):
        """
        full padding with 0's, stride 1, normalizes processed image to 0-255
        range
        image is list of lists of integers with rectangular shape, 
        conv is list of lists of integers with odd x odd rectangular shape
        returns processed image which has the same shape as (original) image
        """
        image = self.before_convolution(image, size)
        rows = len(image)
        columns = len(image[0])
        conv_size = len(conv)
        n = conv_size // 2
        processed = [[] for _ in image]
        for row in range(rows):
            for column in range(columns):
                conv_sum = 0.0
                for i in range(-n, n + 1):
                    for j in range(-n, n + 1):
                        conv_sum += conv[i+n][j+n] * (image[row+i][column+j] if
                                                     (row+i>=0 and row+i<rows
                                                      and column+j>=0 and 
                                                      column+j<columns) else 0)
                if(row == 0 and column == 0):
                    min_intensity = max_intensity = conv_sum
                else:
                    min_intensity = conv_sum if conv_sum<min_intensity\
                                             else min_intensity
                    max_intensity = conv_sum if conv_sum>max_intensity\
                                             else max_intensity                     
                    
                processed[row].append(abs(conv_sum) if absolute else conv_sum)  
        for i, row in enumerate(processed):
            for j, value in enumerate(row):
                if value < 0:
                    processed[i][j] = 0
                elif value > 255:
                    processed[i][j] = 255
                    
        ##aykırı değerleri 0 ve 255'e götüren değil
        ##tüm değerleri 0-255 arasına haritalayan kod
        # intensity_range = max_intensity - min_intensity
        # for row in range(len(processed)):
        #     for column in range(len(processed[0])):
        #         processed[row][column] = (processed[row][column] -\
        #                                   min_intensity)/(intensity_range\
        #                                     if intensity_range!=0 
        #                                     else 1) * 255 // 1
        return self.after_convolution(processed)  
    
    def before_convolution(self, image_list, size):
        Wi, He = size
        image_list_of_lists = list()
        for height in range(He):
            row_list = list()
            for width in range(Wi):
                row_list.append(image_list[height * Wi + width])
            image_list_of_lists.append(row_list)
        return image_list_of_lists
    
    def after_convolution(self, image_list_of_lists):
        return [value for row_list in image_list_of_lists for\
                value in row_list]
            
    def median(self, image, size, size_filter):
        image = self.before_convolution(image, size)
        rows = len(image)
        columns = len(image[0])
        n = size_filter // 2
        processed = [[] for _ in image]
        for row in range(rows):
            for column in range(columns):
                median_list = list()
                for i in range(-n, n + 1):
                    for j in range(-n, n + 1):
                        median_list.append(image[row+i][column+j] if
                                           (row+i>=0 and row+i<rows
                                            and column+j>=0 and 
                                            column+j<columns) else 0)
                median_list.sort()
                processed[row].append(median_list[n])  
        
        ##aykırı değerleri 0 ve 255'e götüren değil
        ##tüm değerleri 0-255 arasına haritalayan kod        
        # intensity_range = max_intensity - min_intensity
        # for row in range(len(processed)):
        #     for column in range(len(processed[0])):
        #         processed[row][column] = (processed[row][column] -\
        #                                   min_intensity)/(intensity_range\
        #                                     if intensity_range!=0 
        #                                     else 1) * 255 // 1
        return self.after_convolution(processed)  
    
    def contra_harmonic(self, image, size, q):
        image = self.before_convolution(image, size)
        rows = len(image)
        columns = len(image[0])
        filter_size = 3
        n = filter_size // 2
        processed = [[] for _ in image]
        for row in range(rows):
            for column in range(columns):
                dividend_sum = 0.0
                divisor_sum = 0.0
                for i in range(-n, n + 1):
                    for j in range(-n, n + 1):
                        if row+i>=0 and row+i<rows and column+j>=0 and\
                           column+j<columns:
                               dividend_sum+=(image[row+i][column+j]+e)**(q+1)
                               divisor_sum+=(image[row+i][column+j]+e)**(q)
                    
                processed[row].append(round(dividend_sum / divisor_sum))  
        for i, row in enumerate(processed):
            for j, value in enumerate(row):
                if value < 0:
                    processed[i][j] = 0
                elif value > 255:
                    processed[i][j] = 255
                    
        ##aykırı değerleri 0 ve 255'e götüren değil
        ##tüm değerleri 0-255 arasına haritalayan kod
        # intensity_range = max_intensity - min_intensity
        # for row in range(len(processed)):
        #     for column in range(len(processed[0])):
        #         processed[row][column] = (processed[row][column] -\
        #                                   min_intensity)/(intensity_range\
        #                                     if intensity_range!=0 
        #                                     else 1) * 255 // 1
        return self.after_convolution(processed)  
        
    def gaussian_probability(self, x, y, sd):
        sdsd2 = sd * sd * 2
        return (1 / (pi * sdsd2)) * (e**(-(x**2 + y**2) / sdsd2))
    
    def gaussian_filter_start(self):
        label = ttk.Label(self.options_frame, text = 'Sigma (standart sapma'\
                          ' değeri')
        label.pack(side = tk.LEFT, padx = round(self.winfo_width() * 0.02))
        
        treshold = tk.StringVar()
        entry = ttk.Entry(self.options_frame, textvariable = treshold)
        entry.pack(side = tk.LEFT)
        
        button = ttk.Button(self.options_frame, text = 'Uygula',
                            command = self.gaussian_filter_end)
        button.pack(side = tk.LEFT, padx = round(self.winfo_width() * 0.02))
    
    def gaussian_filter_end(self):
        sd = float(self.options_frame.winfo_children()[-2].get()) 
        filter_size = 3
        n = filter_size // 2
        area_divisor = 100
        result_filter = [[0 for _ in range(filter_size)] 
                         for __ in range(filter_size)]
        total_prob_area = 0.0
        for row in range(-n, n+1):
            row = row - 0.5
            for column in range(-n, n+1):
                column = column - 0.5
                prob_area = 0.0
                for i in range(area_divisor):
                    i = (i + 0.5) / area_divisor
                    for j in range(area_divisor):
                        j = (j + 0.5) / area_divisor
                        x = row + i
                        y = column + j
                        gaussian_prob = self.gaussian_probability(x, y, sd)
                        prob_area += gaussian_prob
                        total_prob_area += gaussian_prob
                prob_area /= area_divisor**2    
                result_filter[round(row+n+0.5)][round(column+n+0.5)] = prob_area
        total_prob_area /= area_divisor**2
        result_filter =[[value/total_prob_area for value in row] 
                        for row in result_filter]      
        image_list = list(self.image.getdata())
        size = self.image.size
        image_list = self.convolution(image_list, size, result_filter)
        
        convoluted_image = Image.new('L', size)
        convoluted_image.putdata(image_list)
        self.image = convoluted_image
        self.image_display = ImageTk.PhotoImage(self.image)
        self.image_frame.winfo_children()[0].configure(\
                                             image=self.image_display)
        for i in range(-3,0,1):
            self.options_frame.winfo_children()[i].destroy()   
                    
    
    def sharpening_filter(self):
        image_list = list(self.image.getdata())
        size = self.image.size
        sharpening_flter = [[-1,-1,-1],[-1,9,-1],[-1,-1,-1]]
        image_list = self.convolution(image_list, size, sharpening_flter)
        
        convoluted_image = Image.new('L', size)
        convoluted_image.putdata(image_list)
        self.image = convoluted_image
        self.image_display = ImageTk.PhotoImage(self.image)
        self.image_frame.winfo_children()[0].configure(\
                                             image=self.image_display)
    
    
    def edge_detection_filter(self):
        image_list = list(self.image.getdata())
        size = self.image.size
        horizontal_flter = [[1,2,1],[0,0,0],[-1,-2,-1]]
        image_list1 = self.convolution(image_list, size, horizontal_flter,
                                       absolute = True)
        
        vertical_flter = [[-1,0,1],[-2,0,2],[-1,0,1]]
        image_list2 = self.convolution(image_list, size, vertical_flter, 
                                       absolute = True)

        for i, (value1, value2) in enumerate(zip(image_list1, image_list2)):
            image_list[i] = 255 if value1 + value2 > 255 else value1 + value2
        
        convoluted_image = Image.new('L', size)
        convoluted_image.putdata(image_list)
        self.image = convoluted_image
        self.image_display = ImageTk.PhotoImage(self.image)
        self.image_frame.winfo_children()[0].configure(\
                                             image=self.image_display)
    
    def mean_filter(self):
        image_list = list(self.image.getdata())
        size = self.image.size
        mean_flter = [[1/9,1/9,1/9],[1/9,1/9,1/9],[1/9,1/9,1/9]]
        image_list = self.convolution(image_list, size, mean_flter)
        
        convoluted_image = Image.new('L', size)
        convoluted_image.putdata(image_list)
        self.image = convoluted_image
        self.image_display = ImageTk.PhotoImage(self.image)
        self.image_frame.winfo_children()[0].configure(\
                                             image=self.image_display)
    
    def median_filter(self):
        image_list = list(self.image.getdata())
        size = self.image.size
        image_list = self.median(image_list, size, 3)
        
        convoluted_image = Image.new('L', size)
        convoluted_image.putdata(image_list)
        self.image = convoluted_image
        self.image_display = ImageTk.PhotoImage(self.image)
        self.image_frame.winfo_children()[0].configure(\
                                             image=self.image_display)
    
    def contra_harmonic_filter_start(self):
        label = ttk.Label(self.options_frame, text = 'Q değeri')
        label.pack(side = tk.LEFT, padx = round(self.winfo_width() * 0.02))
        
        treshold = tk.StringVar()
        entry = ttk.Entry(self.options_frame, textvariable = treshold)
        entry.pack(side = tk.LEFT)
        
        button = ttk.Button(self.options_frame, text = 'Uygula',
                            command = self.contra_harmonic_filter_end)
        button.pack(side = tk.LEFT, padx = round(self.winfo_width() * 0.02))
        
    def contra_harmonic_filter_end(self):
        image_list = list(self.image.getdata())
        size = self.image.size
        q = int(self.options_frame.winfo_children()[-2].get()) 
        image_list = self.contra_harmonic(image_list, size, q)            
        
        contra_harmonized_image = Image.new('L', size)
        contra_harmonized_image.putdata(image_list)
        self.image = contra_harmonized_image
        self.image_display = ImageTk.PhotoImage(self.image)
        self.image_frame.winfo_children()[0].configure(\
                                             image=self.image_display)
        for i in range(-3,0,1):
            self.options_frame.winfo_children()[i].destroy()
    
    def histogram(self):
        hist_dict = defaultdict(lambda:0)
        image_list = list(self.image.getdata())
        pixel_count = 0
        for intensity in image_list:
            pixel_count += 1
            hist_dict[intensity] += 1
        hist_dict = dict((k, v / pixel_count) for k, v in hist_dict.items())
        hist_dict = dict(sorted(hist_dict.items()))
        plt.rcParams['figure.dpi'] = 75
        plt.bar(hist_dict.keys(), hist_dict.values(), width = 1.0)
        plt.xlim([0,255])
        filepath = ".\\temp_211213105.png"
        plt.savefig(filepath)
        plt.close()
        
        with Image.open(filepath) as im:
            self.image = copy.deepcopy(im)
        remove(filepath)
        self.image_display = ImageTk.PhotoImage(self.image)
        self.image_frame.winfo_children()[0].configure(image =\
                                                       self.image_display)
    
    def histogram_equalization(self):
        hist_dict = defaultdict(lambda:0)
        image_list = list(self.image.getdata())
        pixel_count = 0
        for intensity in image_list:
            pixel_count += 1
            hist_dict[intensity] += 1
        hist_dict = dict((k, v / pixel_count) for k, v in hist_dict.items())
        hist_dict = dict(sorted(hist_dict.items()))
        
        total_probability = 0.0
        equ_dict = dict()
        for key, value in hist_dict.items():
            total_probability += value
            value = round(255 * total_probability)
            equ_dict[key] = value
        
        for i, pixel in enumerate(image_list):
            image_list[i] = equ_dict[pixel]
        size = self.image.size
        equalized_image = Image.new('L', size)
        equalized_image.putdata(image_list)
        self.image = equalized_image
        self.image_display = ImageTk.PhotoImage(self.image)
        self.image_frame.winfo_children()[0].configure(\
                                             image=self.image_display)
            
    
    def quantization_start(self):
        label = ttk.Label(self.options_frame, text = 'Nicemleme değeri')
        label.pack(side = tk.LEFT, padx = round(self.winfo_width() * 0.02))
        
        treshold = tk.StringVar()
        entry = ttk.Entry(self.options_frame, textvariable = treshold)
        entry.pack(side = tk.LEFT)
        
        button = ttk.Button(self.options_frame, text = 'Nicemle',
                            command = self.quantization_end)
        button.pack(side = tk.LEFT, padx = round(self.winfo_width() * 0.02))
    
    def quantization_end(self):
        hist_dict = defaultdict(lambda:0)
        image_list = list(self.image.getdata())
        pixel_count = 0
        for intensity in image_list:
            pixel_count += 1
            hist_dict[intensity] += 1
        hist_dict = dict((k, v / pixel_count) for k, v in hist_dict.items())
        hist_dict = dict(sorted(hist_dict.items()))
        k = int(self.options_frame.winfo_children()[-2].get()) 
        treshold = 1
        quantization_dict = dict()
        key_list = list()
        total_probability = 0.0
        for key, value in hist_dict.items():
            total_probability += value
            key_list.append(key)
            if total_probability >= (treshold / k):
                for key_in_list in key_list:
                    intensity = round((key_list[0] + key_list[-1]) / 2)
                    quantization_dict[key_in_list] = intensity
                key_list = list()
                treshold +=1
                
        for i, pixel in enumerate(image_list):
            image_list[i] = quantization_dict[pixel]    
            
        size = self.image.size
        quantized_image = Image.new('L', size)
        quantized_image.putdata(image_list)
        self.image = quantized_image
        self.image_display = ImageTk.PhotoImage(self.image)
        self.image_frame.winfo_children()[0].configure(\
                                             image=self.image_display)
        for i in range(-3,0,1):
            self.options_frame.winfo_children()[i].destroy()
    
    def gray_scale(self):
        image_list = list(self.image.getdata())
        size = self.image.size
        for i, pixel in enumerate(image_list):
            scale = 0
            for intensity in pixel:
                scale += intensity / 3
            image_list[i] = round(scale)
        gray_scale_image = Image.new('L', size)
        gray_scale_image.putdata(image_list)
        self.image = gray_scale_image
        self.image_display = ImageTk.PhotoImage(self.image)
        self.image_frame.winfo_children()[0].configure(\
                                             image=self.image_display)
    
    def black_and_white_start(self):
        label = ttk.Label(self.options_frame, text = 'Eşik Değer')
        label.pack(side = tk.LEFT, padx = round(self.winfo_width() * 0.02))
        
        treshold = tk.StringVar()
        entry = ttk.Entry(self.options_frame, textvariable = treshold)
        entry.pack(side = tk.LEFT)
        
        button = ttk.Button(self.options_frame, text = 'Dönüştür',
                            command = self.black_and_white_end)
        button.pack(side = tk.LEFT, padx = round(self.winfo_width() * 0.02))
        
        
    def black_and_white_end(self):
        image_list = list(self.image.getdata())
        size = self.image.size
        treshold = int(self.options_frame.winfo_children()[-2].get())
        for i, intensity in enumerate(image_list):
            image_list[i] = 0 if intensity < treshold else 255
        black_and_white_image = Image.new('1', size)
        black_and_white_image.putdata(image_list)
        self.image = black_and_white_image
        self.image_display = ImageTk.PhotoImage(self.image)
        self.image_frame.winfo_children()[0].configure(\
                                             image=self.image_display)
        for i in range(-3,0,1):
            self.options_frame.winfo_children()[i].destroy()
    
    def crop_prepare(self):
        self.image_frame.winfo_children()[0].bind('<Button-1>', 
                                                  self.crop_press)
        self.image_frame.winfo_children()[0].bind('<ButtonRelease-1>', 
                                                  self.crop_release)
    
    def crop_press(self, e):
        self.button_press = (e.x, e.y)
        
    def crop_release(self, e):
        press_x, press_y = self.button_press
        release_x, release_y = e.x, e.y
        image_list = list(self.image.getdata())
        size = self.image.size
        image_list_list = self.before_convolution(image_list, size)
        cropped = list()
        x_nw, x_se = min(press_x, release_x), max(press_x, release_x)
        x_nw, x_se = max(x_nw, 0), min(x_se, size[0])
        y_nw, y_se = min(press_y, release_y), max(press_y, release_y)
        y_nw, y_se = max(y_nw, 0), min(y_se, size[1])
        for row in range(y_nw, y_se):
            cropped.append(list())
            for column in range(x_nw, x_se):
                cropped[-1].append(image_list_list[row][column])
        cropped = self.after_convolution(cropped)
        cropped_image = Image.new(self.image.mode, (x_se-x_nw, y_se-y_nw))
        cropped_image.putdata(cropped)
        self.image = cropped_image
        self.image_display = ImageTk.PhotoImage(self.image)
        
        self.image_frame.winfo_children()[0].destroy()
        image_label = ttk.Label(self.image_frame, image=self.image_display)
        image_label.pack(pady=round(self.winfo_height()*0.04))
        
    def zoom_prepare(self):
        self.image_frame.winfo_children()[0].bind("<MouseWheel>", 
                                                  self.zoom)
    def zoom(self, e):
        e.x *= self.zoom_ratio
        e.y *= self.zoom_ratio
        if e.delta > 0:
            self.zoom_ratio *= self.zoom_ratio_change
        else:
            self.zoom_ratio /= self.zoom_ratio_change
            if self.zoom_ratio > 1:
                self.zoom_ratio = 1.0
        image_list = list(self.image.getdata())
        size = self.image.size             
        x, y = size
        zoom_ratio = self.zoom_ratio
        x_new_half = (x * zoom_ratio) / 2
        y_new_half = (y * zoom_ratio) / 2
        x_west = round(e.x + self.zoom_nw[0] - x_new_half)
        x_east = round(e.x + self.zoom_nw[0] + x_new_half)
        if x_west < 0:
            x_east -= x_west
            x_west = 0
        if x_east > x:
            x_west -= x_east - x
            x_east = x
        if x_west < 0:
            x_west = 0
        y_north = round(e.y + self.zoom_nw[1] - y_new_half)
        y_south = round(e.y + self.zoom_nw[1] + y_new_half)
        if y_north < 0:
            y_south -= y_north
            y_north = 0
        if y_south > y:
            y_north -= y_south - y
            y_south = y   
        if(y_north < 0):
            y_north = 0
        self.zoom_nw = x_west, y_north
        
        image_list_list = self.before_convolution(image_list, self.image.size)
        zoomed = list()
        for row in range(y_north, y_south):
            zoomed.append(list())
            for column in range(x_west, x_east):
                zoomed[-1].append(image_list_list[row][column])
        zoomed = self.after_convolution(zoomed)
        zoomed = self.change_size(zoomed,(x_east-x_west, y_south-y_north),size)
        zoomed_image = Image.new(self.image.mode,  size)
        zoomed_image.putdata(zoomed)
        self.image_zoom = zoomed_image
        self.image_display = ImageTk.PhotoImage(self.image_zoom)
        self.image_frame.winfo_children()[0].configure(\
                                             image=self.image_display)
    
    def zoom_remove(self, e):
        self.zoom_nw = 0, 0
        self.zoom_ratio = 1.0
        self.image_display = ImageTk.PhotoImage(self.image)
        self.image_frame.winfo_children()[0].destroy()
        image_label = ttk.Label(self.image_frame, image=self.image_display)
        image_label.pack(pady=round(self.winfo_height()*0.04))
    
    def change_size(self, image, size_before, size_after):
        new_image = list()
        (y_bef, x_bef), (y_aft, x_aft) = size_before, size_after 
        x_ratio = x_bef / x_aft
        y_ratio = y_bef / y_aft
        for x in range(x_aft):
            for y in range(y_aft):
                x_on_org = int((x+0.5)*x_ratio)
                y_on_org = int((y+0.5)*y_ratio)
                new_image.append(image[x_on_org*y_bef + y_on_org])
        return new_image    
    
    def select_file(self):
        filetypes = (('resim','.bmp .png .jpg'),('tüm dosyalar','.*'))
        filepath = tk.filedialog.askopenfilename(title='Resim aç',
                                                 initialdir=".\\",
                                                 filetypes=filetypes)
        self.options_frame.winfo_children()[-1]['text'] = filepath
        image_label = self.image_frame.winfo_children()[0]
        im = Image.open(filepath)
        Wi, He = im.size
        maxWi = self.winfo_width() * 0.5
        if Wi > maxWi:
            He = round(He * (maxWi / Wi))
            Wi = round(maxWi)
        maxHe = self.winfo_height() * 0.5
        if He > maxHe:
            Wi = round(Wi * (maxHe / He))
            He = round(maxHe)
        image_list1 = list(im.getdata())
        size = (Wi,He)
        image_list2 = self.change_size(image_list1, im.size, size)
        im2 = Image.new(im.mode, size)
        im2.putdata(image_list2)  
        self.image = im2
        self.image_display = ImageTk.PhotoImage(self.image)
        image_label['image'] = self.image_display

if __name__ == "__main__":
    app = App()
    app.mainloop()




