import json

from Dish import Dish

data = {}

def load_data(path='data.json'):
    '''
    Функция сохраняет все текущие блюда из файла path в приложение
    '''
    try:
        with open(path, 'r') as file:
            loaded_data = json.load(file)
            for date, dishes in loaded_data.items():
                data[date] = [Dish.from_dict(dish) for dish in dishes]
    except FileNotFoundError:
        pass

def save_data(path='data.json'):
    '''
    Функция сохраняет все текущие блюда из приложения в файле path
    '''
    with open(path, 'w') as file:
        json.dump(
            {date: [dish.to_dict() for dish in dishes] for date, dishes in data.items()}, 
            file, 
            indent=2
        )