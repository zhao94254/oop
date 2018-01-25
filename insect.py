#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 18/1/25 下午3:26
# @Author  : zpy
# @Software: PyCharm


# 一个类植物大战僵尸的游戏，用来练习oop
import random

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

    def action(self, colony):
        pass

    def __str__(self):
        name = type(self).__name__
        return name

    __repr__ = __str__


class Ant(Insect):
    """ 守的一方"""
    is_ant = True
    food_cost = 0

    def __init__(self, armor=1):
        Insect.__init__(self, armor)


class HarvesterAnt(Ant):
    name = 'Harvester'
    food_cost = 2

    def action(self, colony):
        """ 产生食物。"""
        colony.food += 1


class FireAnt(Ant):

    name = 'Fire'
    food_cost = 3
    damage = 3

    def reduce_armor(self, amount):
        """
        如果这个ant死掉，会对当前位置的所有bee产生伤害
        :param amount:
        :return:
        """

        self.armor -= amount
        if self.armor <= 0:
            for b in self.place.bees[:]:
                b.reduce_armor(self.damage)
            self.place.remove_insect(self)


def random_or_none(s):
    if s:
        return random.choice(s)

class ThrowerAnt(Ant):

    name = 'Thrower'
    food_cost = 1
    damage = 1
    max_range = 1 # 最大的攻击范围


    def nearest_bee(self, hive):
        """ 获取攻击范围内的bee。 """
        i = 0
        place = self.place
        bee = random_or_none(self.place.bees)
        # 这里的思路就是从当前的位置向攻击范围可以达到的
        # 位置进行搜索，如果搜索到目标就停止。
        # 并且这个位置不能是hive, 并且位置需要是存在的。
        while bee is None and place is not hive and\
                i <= self.max_range and place.entrance:
            place = place.entrance
            i += 1
            bee = random_or_none(place.bees)
        return bee

    def throw_at(self, target):
        """ 对目标范围内的进行攻击"""
        if target is not None:
            target.reduce_armor(self.damage)

    def action(self, colony):
        self.throw_at(self.nearest_bee(colony))


class LongThrower(ThrowerAnt):
    name = 'Long'
    food_cost = 2
    max_range = 5  # 最大的攻击范围


class ShortThrower(ThrowerAnt):
    name = 'Short'
    food_cost = 2
    max_range = 3  # 最大的攻击范围


class WallAnt(Ant):
    """ 防御性的 。"""
    name = 'Short'
    food_cost = 4

    def __init__(self):
        Ant.__init__(self, 5)


class HungryAnt(Ant):

    name = 'Hungry'
    food_cost = 4
    time_to_digest = 3 # 冷却时间



class Bee(Insect):
    """ 攻的一方"""
    damage = 1
    name = 'Bee'

    def sting(self, ant):
        """ 攻击 ant， 减掉相应的血"""
        ant.reduce_armor(self.damage)

    def move_to(self, place):
        """ 移动到一个新的地方"""
        self.place.remove_insect(self)
        place.add_insect(self)



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