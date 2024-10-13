import json

from Dish import Dish

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
        json.dump(
            {date: [dish.to_dict() for dish in dishes] for date, dishes in data.items()}, 
            file, 
            indent=2
        )