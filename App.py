import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt

from Dish import Dish
from Data import load_data, save_data
class App:
    '''
    Класс приложения для учёта ежедневных приемов пищи
    
    Поля класса:
    data - словарь с данными о блюдах (дата: [блюда])
    root - tkinter окно приложения
    entries - словарь с введенными значениями в полях
    analyze_entries - словарь с введенными датами для анализа
    tree - tkinter Treeview для отображения блюд
    '''
    def __init__(self, data):
        self.data = data
        load_data()

        self.root = self.set_window()
        self.entries = self.set_dish_entries(self.root)
        self.analyze_entries = self.set_analyze_entries(self.root)
        self.set_buttons(self.root)
        self.tree = self.set_tree(self.root)
        
        self._update_treeview()
        
        self.root.mainloop()

    def set_window(self):
        root = tk.Tk()
        root.title("Ежедневник приемов пищи.")
        return root

    def set_dish_entries(self, root):
        tk.Label(root, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0)
        date_entry = tk.Entry(root)
        date_entry.grid(row=0, column=1, columnspan=1)

        tk.Label(root, text="Название продукта:").grid(row=1, column=0)
        name_entry = tk.Entry(root)
        name_entry.grid(row=1, column=1, columnspan=1)

        tk.Label(root, text="Вес продукта (гр):").grid(row=2, column=0)
        weight_entry = tk.Entry(root)
        weight_entry.grid(row=2, column=1, columnspan=1)

        tk.Label(root, text="Калории (на 100 гр):").grid(row=3, column=0)
        calories_entry = tk.Entry(root)
        calories_entry.grid(row=3, column=1, columnspan=1)

        tk.Label(root, text="Белки (на 100 гр):").grid(row=4, column=0)
        proteins_entry = tk.Entry(root)
        proteins_entry.grid(row=4, column=1, columnspan=1)

        tk.Label(root, text="Жиры (на 100 гр):").grid(row=5, column=0)
        fats_entry = tk.Entry(root)
        fats_entry.grid(row=5, column=1, columnspan=1)

        tk.Label(root, text="Углеводы (на 100 гр):").grid(row=6, column=0)
        carbs_entry = tk.Entry(root)
        carbs_entry.grid(row=6, column=1, columnspan=1)
        
        return {
            'date_entry': date_entry, 
            'name_entry': name_entry, 
            'weight_entry': weight_entry, 
            'calories_entry': calories_entry, 
            'proteins_entry': proteins_entry, 
            'fats_entry': fats_entry, 
            'carbs_entry': carbs_entry
        }
        
    # Переносим данные блюда из таблицы в окно редактирования
    def _edit_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        date, change_dish = Dish.from_tree(self.tree.item(selected_item, 'values'))

        # Удаляем, если что-то было из окошек
        for entry in self.entries.values():
            entry.delete(0, tk.END)

        # Добавляем данные редактируемого блюда
        self.entries['date_entry'].insert(0, date)
        self.entries['name_entry'].insert(0, change_dish.name)
        self.entries['weight_entry'].insert(0, change_dish.weight)
        self.entries['calories_entry'].insert(0, change_dish.calories)
        self.entries['proteins_entry'].insert(0, change_dish.proteins)
        self.entries['fats_entry'].insert(0, change_dish.fats)
        self.entries['carbs_entry'].insert(0, change_dish.carbs)

        # Удаляем старый объект
        self.tree.delete(selected_item)
        self.data[date].remove(change_dish)

    def _add_product(self):
        date = self.entries['date_entry'].get()
        name = self.entries['name_entry'].get()
        weight = int(self.entries['weight_entry'].get())
        calories = int(self.entries['calories_entry'].get())
        proteins = int(self.entries['proteins_entry'].get())
        fats = int(self.entries['fats_entry'].get())
        carbs = int(self.entries['carbs_entry'].get())
        
        # Удаляем устаревшие данные из окошек
        for entry in self.entries.values():
            entry.delete(0, tk.END)

        self.data[date] = self.data.get(date, []) # Если такой даты еще не было, присваиваем пустое значение
        self.data[date].append(Dish(name, weight, calories, proteins, fats, carbs))
        save_data()
        self._update_treeview()
    
    # Под капотом просто добавление объекта
    def _save_edited_product(self):
        self._add_product()
        
    def _analyze_period(self):
        date1 = self.analyze_entries['analyze_date_entry1'].get()
        date2 = self.analyze_entries['analyze_date_entry2'].get()
        dates = []
        calories = []
        proteins = []
        fats = []
        carbs = []

        for date in self.data:
            if date1 <= date <= date2:
                dates.append(date)
                calories.append(sum(dish.calories * dish.weight / 100 for dish in self.data[date]))
                proteins.append(sum(dish.proteins * dish.weight / 100 for dish in self.data[date]))
                fats.append(sum(dish.fats * dish.weight / 100 for dish in self.data[date]))
                carbs.append(sum(dish.carbs * dish.weight / 100 for dish in self.data[date]))
        
         # Строим график
        plt.figure('Ваш график потребления еды', figsize=(10, 6))
        plt.plot(dates, calories, label='Калории', marker='o')
        plt.plot(dates, proteins, label='Белки', marker='o')
        plt.plot(dates, fats, label='Жиры', marker='o')
        plt.plot(dates, carbs, label='Углеводы', marker='o')
        plt.xlabel('Дата')
        plt.ylabel('Количество')
        plt.title(f'Анализ потребления еды с {date1} по {date2}')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def set_buttons(self, root):
        add_button = tk.Button(root, text="Добавить продукт", command=self._add_product)
        add_button.grid(row=0, column=2)

        edit_button = tk.Button(root, text="Редактировать продукт", command=self._edit_product)
        edit_button.grid(row=1, column=2)

        save_edit_button = tk.Button(root, text="Сохранить изменения", command=self._save_edited_product)
        save_edit_button.grid(row=2, column=2)

        analyze_button = tk.Button(root, text="Анализировать с даты по дату (ГГГГ-ММ-ДД)", command=self._analyze_period)
        analyze_button.grid(row=10, column=0)
    
    def set_analyze_entries(self, root):
        analyze_date_entry1 = tk.Entry(root)
        analyze_date_entry1.grid(row=10, column=1)
        analyze_date_entry2 = tk.Entry(root)
        analyze_date_entry2.grid(row=10, column=2)
        
        return {
            'analyze_date_entry1': analyze_date_entry1,
            'analyze_date_entry2': analyze_date_entry2
        }
    
    def _update_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for date, dishes in self.data.items():
            for dish in dishes:
                self.tree.insert('', 'end', values=(date, dish.name, dish.weight, dish.calories, dish.proteins, dish.fats, dish.carbs))
    
    def set_tree(self, root):
        tree = ttk.Treeview(root, columns=("Дата", "Продукт", "Вес", "Калории", "Белки", "Жиры", "Углеводы"), show="headings", selectmode='browse')
        tree.heading("Дата", text="Дата")
        tree.heading("Продукт", text="Продукт")
        tree.heading("Вес", text="Вес")
        tree.heading("Калории", text="Калории")
        tree.heading("Белки", text="Белки")
        tree.heading("Жиры", text="Жиры")
        tree.heading("Углеводы", text="Углеводы")
        tree.grid(row=9, column=0, columnspan=3)

        vsb = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
        vsb.grid(row=10, column=3)
        tree.configure(yscrollcommand=vsb.set)
        return tree