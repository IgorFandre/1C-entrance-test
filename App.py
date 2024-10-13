import tkinter as tk
from tkinter import ttk
import json

# Класс блюда
class Dish:
    def __init__(self, name, weight, calories, proteins, fats, carbs):
        self.name = name
        self.weight = weight
        self.calories = calories
        self.proteins = proteins
        self.fats = fats
        self.carbs = carbs
    
    def __eq__(self, other):
        return self.name == other.name and\
            self.weight == other.weight and\
            self.calories == other.calories and\
            self.proteins == other.proteins and\
            self.fats == other.fats and\
            self.carbs == other.carbs

    def __repr__(self) -> str:
        return str(self.to_dict())

    # Для перевода в json и обратно
    def to_dict(self):
        return {
            'name': self.name,
            'weight': self.weight,
            'calories': self.calories,
            'proteins': self.proteins,
            'fats': self.fats,
            'carbs': self.carbs
        }

    @staticmethod
    def from_dict(data):
        return Dish(data['name'], data['weight'], data['calories'], data['proteins'], data['fats'], data['carbs'])

    # Для получения объекта класса из приложения
    @staticmethod
    def from_tree(lst):
        return lst[0], Dish(lst[1], int(lst[2]), int(lst[3]), int(lst[4]), int(lst[5]), int(lst[6]))

# Текущее хранилище блюд
data = {}

def load_data():
    try:
        with open('data.json', 'r') as file:
            loaded_data = json.load(file)
            for date, dishes in loaded_data.items():
                data[date] = [Dish.from_dict(dish) for dish in dishes]
    except FileNotFoundError:
        pass

def save_data():
    with open('data.json', 'w') as file:
        json.dump({date: [dish.to_dict() for dish in dishes] for date, dishes in data.items()}, file, indent=2)


def add_product():
    date = date_entry.get()
    name = name_entry.get()
    weight = int(weight_entry.get())
    calories = int(calories_entry.get())
    proteins = int(proteins_entry.get())
    fats = int(fats_entry.get())
    carbs = int(carbs_entry.get())

    data[date] = data.get(date, []) # Если такой даты еще не было, присваиваем пустое значение
    data[date].append(Dish(name, weight, calories, proteins, fats, carbs))
    save_data()
    update_treeview()

def update_treeview():
    for item in tree.get_children():
        tree.delete(item)

    for date, dishes in data.items():
        for dish in dishes:
            tree.insert('', 'end', values=(date, dish.name, dish.weight, dish.calories, dish.proteins, dish.fats, dish.carbs))

def analyze_period():
    date = analyze_date_entry.get()
    pass # TODO

# Переносим данные блюда из таблицы в окно редактирования
def edit_product():
    selected_item = tree.selection()
    if not selected_item:
        return

    date, change_dish = Dish.from_tree(tree.item(selected_item, 'values'))

    # Удаляем, если что-то было из окошек
    name_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    weight_entry.delete(0, tk.END)
    calories_entry.delete(0, tk.END)
    proteins_entry.delete(0, tk.END)
    fats_entry.delete(0, tk.END)
    carbs_entry.delete(0, tk.END)

    # Добавляем данные редактируемого блюда
    date_entry.insert(0, date)
    name_entry.insert(0, change_dish.name)
    weight_entry.insert(0, change_dish.weight)
    calories_entry.insert(0, change_dish.calories)
    proteins_entry.insert(0, change_dish.proteins)
    fats_entry.insert(0, change_dish.fats)
    carbs_entry.insert(0, change_dish.carbs)

    # Удаляем старый объект
    tree.delete(selected_item)
    data[date].remove(change_dish)

# Под капотом просто добавление объекта
def save_edited_product():
    add_product()

if __name__ == '__main__':
    load_data()

    root = tk.Tk()
    root.title("Ежедневник приемов пищи.")

    # Виджеты для ввода данных
    tk.Label(root, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0)
    date_entry = tk.Entry(root)
    date_entry.grid(row=0, column=1)

    tk.Label(root, text="Название продукта:").grid(row=1, column=0)
    name_entry = tk.Entry(root)
    name_entry.grid(row=1, column=1)

    tk.Label(root, text="Вес продукта (гр):").grid(row=2, column=0)
    weight_entry = tk.Entry(root)
    weight_entry.grid(row=2, column=1)

    tk.Label(root, text="Калории (на 100 гр):").grid(row=3, column=0)
    calories_entry = tk.Entry(root)
    calories_entry.grid(row=3, column=1)

    tk.Label(root, text="Белки (на 100 гр):").grid(row=4, column=0)
    proteins_entry = tk.Entry(root)
    proteins_entry.grid(row=4, column=1)

    tk.Label(root, text="Жиры (на 100 гр):").grid(row=5, column=0)
    fats_entry = tk.Entry(root)
    fats_entry.grid(row=5, column=1)

    tk.Label(root, text="Углеводы (на 100 гр):").grid(row=6, column=0)
    carbs_entry = tk.Entry(root)
    carbs_entry.grid(row=6, column=1)

    add_button = tk.Button(root, text="Добавить продукт", command=add_product)
    add_button.grid(row=7, column=0, columnspan=2)

    edit_button = tk.Button(root, text="Редактировать продукт", command=edit_product)
    edit_button.grid(row=8, column=0, columnspan=2)

    save_edit_button = tk.Button(root, text="Сохранить изменения", command=save_edited_product)
    save_edit_button.grid(row=9, column=0, columnspan=2)

    tree = ttk.Treeview(root, columns=("Дата", "Продукт", "Вес", "Калории", "Белки", "Жиры", "Углеводы"), show="headings", selectmode='browse')
    tree.heading("Дата", text="Дата")
    tree.heading("Продукт", text="Продукт")
    tree.heading("Вес", text="Вес")
    tree.heading("Калории", text="Калории")
    tree.heading("Белки", text="Белки")
    tree.heading("Жиры", text="Жиры")
    tree.heading("Углеводы", text="Углеводы")
    tree.grid(row=10, column=0, columnspan=2)

    vsb = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    vsb.grid(row=10, column=2)
    tree.configure(yscrollcommand=vsb.set)

    update_treeview()

    tk.Label(root, text="Анализ с даты (ГГГГ-ММ-ДД):").grid(row=11, column=0)
    analyze_date_entry = tk.Entry(root)
    analyze_date_entry.grid(row=11, column=1)
    
    tk.Label(root, text="По дату (ГГГГ-ММ-ДД):").grid(row=12, column=0)
    analyze_date_entry = tk.Entry(root)
    analyze_date_entry.grid(row=12, column=1)

    analyze_button = tk.Button(root, text="Анализировать", command=analyze_period)
    analyze_button.grid(row=13, column=0, columnspan=2)

    #result_graphic = tk.Label(root, text="") # TODO matplotlib plot
    #result_graphic.grid(row=14, column=0, columnspan=2)

    root.mainloop()