class Dish:
    '''
    Класс, описывающий блюдо в нашем приложении
    
    Поля класса:
    name - название
    weight - вес блюда в граммах
    calories - количество калорий на 100 грамм
    proteins - количество белков на 100 грамм
    fats - количество жиров на 100 грамм
    carbs - количество углеводов на 100 грамм
    '''
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