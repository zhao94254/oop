#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 18/1/25 下午3:26
# @Author  : zpy
# @Software: PyCharm


# 一个类植物大战僵尸的游戏，用来练习oop


class Place:
    """ 每一个place相关的属性，方法在这里
    主要用来添加，删除 insect
    """
    def __init__(self, name, exit=None):
        self.name = name
        self.exit = exit
        self.bees = []  # 一个位置可以放多个
        self.ant = None
        self.entrance = None

    def add_insect(self, insect):
        if insect.is_ant:
            if self.ant is None:
                self.ant = insect
            else:
                assert self.ant is None, "两个 ant 无法在同一个地方。"
        else:
            self.bees.append(insect)

        insect.place = self

    def remove_insect(self, insect):
        """ 将insect 从当前位置移走"""
        if insect.is_ant:
            self.ant = None
        else:
            self.bees.remove(insect)

        insect.place = None


    def __str__(self):
        return self.name

    __repr__ = __str__


class Insect:
    """ ant bee 的基类"""

    is_ant = False
    damage = 0


    def __init__(self, armor, place=None):
        self.armor = armor
        self.place = place

    def reduce_armor(self, amount):
        """ 攻击掉血。小于等于零移走"""
        self.armor -= amount
        if self.armor <= 0:
            self.place.remove_insect(self)

    def __str__(self):
        name = type(self).__name__
        return name

    __repr__ = __str__


class Ant(Insect):
    """ 守的一方"""
    is_ant = True
    food_cost = 0


class Bee(Insect):
    """ 攻的一方"""
    damage = 1
    name = 'Bee'



class AssaultPlan(dict):
    """ 将bee 部署出来。"""

    def add_wave(self, bee_type, bee_armor, time, count):
        """ 将bee 放在字典中"""
        bees = [bee_type(bee_armor) for _ in range(count)]
        self.setdefault(time, []).extend(bees)
        return self

    @property
    def all_bees(self):
        """ 返回所有的蜂巢，和蜜蜂"""
        return [bee for wave in self.values() for bee in wave]

    def __str__(self):
        pass

if __name__ == '__main__':
    a = Ant(2)
    b = Bee(3)
    p = Place('x')
    p.add_insect(a)
    print(p.ant)
    a.reduce_armor(1)
    print(p.ant)