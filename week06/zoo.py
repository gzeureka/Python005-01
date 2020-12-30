#!/usr/bin/env python
#
# 背景：在使用 Python 进行《我是动物饲养员》这个游戏的开发过程中，有一个代码片段要求定义动物园、动物、猫、狗四个类。
#
# 这个类可以使用如下形式为动物园增加一只猫：
#
# if __name__ == '__main__':
#     # 实例化动物园
#     z = Zoo('时间动物园')
#     # 实例化一只猫，属性包括名字、类型、体型、性格
#     cat1 = Cat('大花猫 1', '食肉', '小', '温顺')
#     # 增加一只猫到动物园
#     z.add_animal(cat1)
#     # 动物园是否有猫这种动物
#     have_cat = hasattr(z, 'Cat')
#
# 具体要求：
#   定义“动物”、“猫”、“狗”、“动物园”四个类，动物类不允许被实例化。
#   动物类要求定义“类型”、“体型”、“性格”、“是否属于凶猛动物”四个属性，是否属于凶猛动物的判断标准是：“体型 >= 中等”并且是“食肉类型”同时“性格凶猛”。
#   猫类要求有“叫声”、“是否适合作为宠物”以及“名字”三个属性，其中“叫声”作为类属性，除凶猛动物外都适合作为宠物，猫类继承自动物类。狗类属性与猫类相同，继承自动物类。
#   动物园类要求有“名字”属性和“添加动物”的方法，“添加动物”方法要实现同一只动物（同一个动物实例）不能被重复添加的功能。

from abc import ABC


class Zoo(object):
    def __init__(self, name):
        self.name = name
        self.animals = []

    def add_animal(self, animal):
        # 是否已有同一只动物
        for a in self.animals:
            if animal is a:
                return
        # 添加动物
        self.animals.append(animal)

    # 动物园里是否有某种类型的动物
    def has_animal_of_type(self, type_name):
        for a in self.animals:
            if type_name == type(a).__name__:
                return True
        return False


def hasattr(zoo, type_name):
    return zoo.has_animal_of_type(type_name)


# diet '食草'，'食肉'，'杂食'
# body_type '小'，'中'，'大'
# character '性格'，'温顺'，'凶猛'
class Animal(ABC):
    def __init__(self, diet, body_type, character):
        self.diet = diet
        self.body_type = body_type
        self.character = character

    # 是否凶猛动物
    @property
    def is_fierce(self):
        return self.body_type in ['中', '大'] and self.diet == '食肉' and self.character == '凶猛'


class Cat(Animal):
    voice = 'Meow'

    def __init__(self, name, diet, body_type, character):
        super().__init__(diet, body_type, character)
        self.name = name


class Dog(Animal):
    voice = 'Woof'

    def __init__(self, name, diet, body_type, character):
        super().__init__(diet, body_type, character)
        self.name = name


if __name__ == '__main__':
    # 实例化动物园
    z = Zoo('时间动物园')
    # 动物园是否有猫这种动物
    print('动物园是否有猫这种动物', hasattr(z, 'Cat'))
    # 实例化一只猫，属性包括名字、类型、体型、性格
    cat1 = Cat('大花猫 1', '食肉', '小', '温顺')
    # 增加一只猫到动物园
    z.add_animal(cat1)
    print(z.animals)
    # 增加一只到动物园
    dog1 = Dog('大黄狗 1', '食肉', '中', '凶猛')
    z.add_animal(dog1)
    print(z.animals)
    # 同一只猫不会被重复添加
    z.add_animal(cat1)
    print(z.animals)
    # 动物园是否有猫这种动物 True
    print('动物园是否有猫这种动物？', hasattr(z, 'Cat'))

