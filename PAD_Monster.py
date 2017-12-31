__author__ = 'Aaron'

# Class Description:
#   Our Monster Class where we hold all of the Monster's stats and calculate the values needed with those stats

import os
import json


class PADMonster:
    def __init__(self):

        # initialize the Class's stats
        # _max, _min, and _scale are used for when the monster's level is set to something other than its max level
        # _bonus used for when awakenings add value to the base stat
        self.name = ''
        self.hp = 0
        self.hp_max = 0
        self.hp_min = 0
        self.hp_scale = 0
        self.hp_plus = 0
        self.hp_bonus = 0
        self.hp_base = 0
        self.rcv_base = 0
        self.rcv = 0
        self.rcv_max = 0
        self.rcv_min = 0
        self.rcv_scale = 0
        self.rcv_plus = 0
        self.rcv_bonus = 0
        self.base_base_atk = 0
        self.base_atk = 0
        self.base_atk_max = 0
        self.base_atk_min = 0
        self.base_atk_scale = 0
        self.base_atk_plus = 0
        self.base_atk_bonus = 0
        # Array of Attack: atk[attribute]
        self.atk = [0, 0, 0, 0, 0]
        # Array of Pronged Attack: [attribute][0 = Main, 1 = Sub]
        self.pronged_atk = [0, 0, 0, 0, 0]

        self.max_level = 99
        self.current_level = 99

        # 'fire' = 0, 'water' = 1, 'wood' = 2, 'light' = 3, 'dark' = 4
        self.attr_main = 0
        self.attr_sub = 0
        # check if main attribute = sub attribute
        self.is_same_attr = False
        # save list of attribute types
        self.attributes = ['fire', 'water', 'wood', 'light', 'dark']

        # see list of types for corresponding index number
        self.type_main = 0
        self.type_sub = 0
        self.type_main_name = ''
        self.type_sub_name = ''
        # save list of types
        self.types = ['Evo Material', 'Balanced', 'Physical', 'Healer', 'Dragon', 'God', 'Attacker',
                      'Devil', '', '', '', '', 'Awoken Skill Material', 'Protected', 'Enhance Material']
        # save leader skill multipliers; leader_skill[0 = hp, 1 = atk, 2 = rcv]
        self.leader_skill = [0, 0, 0]

        # store image 60x60 size and file location on padherder.com
        self.image60_size = 0
        self.image60_href = ''

        # save amount of each awoken skill
        # id: 1 -> Enhanced HP, 2 -> Enhanced Attack, 3 -> Enhanced Heal, 4 -> Reduce Fire Damage,
        # 5 -> Reduce Water Damage,
        # 6 -> Reduce Wood Damage, 7 -> Reduce Light Damage, 8 -> Reduce Dark Damage,  9 -> Auto-Recover,
        # 10 -> Resistance-Bind, 11 -> Resistance-Dark, 12 -> Resistance-Jammers, 13 -> Resistance-Poison,
        # 14 -> Enhanced Fire Orbs, 15 -> Enhanced Water Orbs, 16 -> Enhanced Wood Orbs, 17 -> Enhanced Light Orbs,
        # 18 -> Enhanced Dark Orbs, 19 -> Extend Time, 20 -> Recover Bind, 21 -> Skill Boost, 22 -> Enhanced Fire Att.,
        # 23 -> Enhanced Water Att., 24 -> Enhanced Wood Att., 25 -> Enhanced Light Att., 26 -> Enhanced Dark Att.,
        # 27 -> Two-Pronged Attack, 28 -> Resistance-Skill Lock
        self.awakenings = [['', '', 0] for x in range(28)]
        self.awakenings_names = ['Enhanced HP', 'Enhanced Attack', 'Enhanced Heal', 'Reduce Fire Damage',
                                 'Reduce Water Damage', 'Reduce Wood Damage', 'Reduce Light Damage',
                                 'Reduce Dark Damage', 'Auto-Recover', 'Resistance-Bind', 'Resistance-Dark',
                                 'Resistance-Jammers', 'Resistance-Poison', 'Enhanced Fire Orbs', 'Enhanced Water Orbs',
                                 'Enahnced Wood Orbs', 'Enhanced Light Orbs', 'Enhanced Dark Orbs', 'Extend Time',
                                 'Recover Bind', 'Skill Boost', 'Enhanced Fire Att.', 'Enhanced Water Att.',
                                 'Enhanced Wood Att.', 'Enhanced Light Att.', 'Enhanced Dark Att.',
                                 'Two-Pronged Attack', 'Resistance-Skill Lock']

        # open awakenings.txt and load it into a python object using json
        self.json_file = open(os.path.join('awakenings.txt'), 'r')
        self.json_awakenings = json.loads(self.json_file.read())

        # iterate through self.json_awakenings and extract the necessary information into self.awakenings
        # awakenings[id-1][name, desc, count]
        for awakening in self.json_awakenings:
            self.awakenings[awakening['id'] - 1] = [awakening['name'], awakening['desc'], 0]

        # leader skill
        self.leader_skill_name = ''
        self.leader_skill_desc = ''
        # [xhp, xatk, xrcv, ['elem/type?', which elem/type?]]
        self.leader_skill_effect = [1, 1, 1]

        self.json_file = open(os.path.join('leader skills.txt'), 'r')
        self.json_leader_skills = json.loads(self.json_file.read())

    def set_base_stats(self, name, hp, atk, rcv, attr1, attr2, type1, type2, size, href, awakenings, leader_skill,
                       level, hp_min, hp_scale, atk_min, atk_scale, rcv_min, rcv_scale):

        self.name = name
        self.hp = hp
        self.hp_base = hp
        self.hp_max = hp
        self.hp_min = hp_min
        self.hp_scale = hp_scale
        self.base_atk = atk
        self.base_base_atk = atk
        self.base_atk_max = atk
        self.base_atk_min = atk_min
        self.base_atk_scale = atk_scale
        self.rcv = rcv
        self.rcv_base = rcv
        self.rcv_max = rcv
        self.rcv_min = rcv_min
        self.rcv_scale = rcv_scale
        self.max_level = level
        self.current_level = level
        self.attr_main = attr1
        self.attr_sub = attr2
        self.type_main = type1
        self.type_main_name = self.types[type1]
        self.type_sub = type2
        if type2:
            self.type_sub_name = self.types[type2]
        self.image60_size = size
        self.image60_href = href
        self.leader_skill_name = leader_skill

        for awakening in awakenings:
            self.awakenings[awakening - 1][2] += 1

        # sets _bonus stats if awakenings[0-2][2] a.k.a. the stat bonus awakenings are greater than 1
        for x in range(3):
            if self.awakenings[x][2] > 0:
                if x == 0:
                    self.hp_bonus = self.awakenings[x][2] * 200
                    self.hp += self.hp_bonus
                    self.hp_base = self.hp
                if x == 1:
                    self.base_atk_bonus = self.awakenings[x][2] * 100
                    self.base_atk += self.base_atk_bonus
                    self.base_base_atk = self.base_atk
                if x == 2:
                    self.rcv_bonus = self.awakenings[x][2] * 50
                    self.rcv += self.rcv_bonus
                    self.rcv_base = self.rcv
        # find the leader skills' effects and description in the json library according to the name
        for x in range(len(self.json_leader_skills)):
            if leader_skill == self.json_leader_skills[x]['name']:
                self.leader_skill_desc = self.json_leader_skills[x]['effect']
                if 'data' in self.json_leader_skills[x].keys():
                    self.leader_skill_effect = self.json_leader_skills[x]['data']

        self._set_atk_(self.attr_main, self.attr_sub)
        self._set_pronged_atk_(self.attr_main, self.attr_sub)

    def _set_attr_main_(self, attr):
        """
        If the attribute name is valid, set the Class's attr_main value to the value corresponding
        to the attr
        :param attr: attribute name
        """
        if attr.lower() in self.attributes:
            self.attr_main = self.attributes.index(attr.lower())

            # if attribute is changed, check if main and sub attributes are the same
            if self.attr_main == self.attr_sub:
                self.is_same_attr = True
            else:
                self.is_same_attr = False

    def _set_attr_sub_(self, attr):
        """
        If the attribute name is valid, set the Class's attr_sub value to the value corresponding
        to the attr
        :param attr: attribute name
        """
        if attr.lower() in self.attributes:
            self.attr_sub = self.attributes.index(attr.lower())

            # if attribute is changed, check if main and sub attributes are the same
            if self.attr_main == self.attr_sub:
                self.is_same_attr = True
            else:
                self.is_same_attr = False

    def _set_atk_(self, attr1, attr2):
        """
        Calculate and set atk for each attribute
        :param attr1: value corresponding to main attribute
        :param attr2: value corresponding to sub attribute
        """
        if attr1 in [0, 1, 2, 3, 4]:
            if attr1 != attr2:
                self.atk[attr1] = self.base_atk
            else:
                self.atk[attr1] = self.base_atk * 1.1

        if attr2 in [0, 1, 2, 3, 4]:
            if attr1 != attr2:
                self.atk[attr2] = self.base_atk * (1/3)

    def _set_pronged_atk_(self, attr1, attr2):
        """
        Calculate and set pronged atk for each attribute
        :param attr1: value corresponding to main attribute
        :param attr2: value corresponding to sub attribute
        """
        if attr1 in [0, 1, 2, 3, 4]:
            self.pronged_atk[attr1] = self.atk[attr1] * 1.5 ** self.awakenings[26][2]

        if attr2 in [0, 1, 2, 3, 4] and attr1 != attr2:
            self.pronged_atk[attr2] = self.atk[attr2] * 1.5 ** self.awakenings[26][2]

    def _set_stats_at_level_(self, level):
        """
        Modify all stats according to level.
        :param level: Level the monster will be set to.
        """
        self.current_level = level
        self.hp = self._use_growth_formula(self.hp_min, self.hp_max, self.hp_scale)
        self.hp += self.hp_bonus
        self.hp_base = self.hp
        self._set_stats_with_pluses_('hp', self.hp_plus)
        self.base_atk = self._use_growth_formula(self.base_atk_min, self.base_atk_max, self.base_atk_scale)
        self.base_atk += self.base_atk_bonus
        self.base_base_atk = self.base_atk
        self._set_stats_with_pluses_('atk', self.base_atk_plus)
        self.rcv = self._use_growth_formula(self.rcv_min, self.rcv_max, self.rcv_scale)
        self.rcv += self.rcv_bonus
        self.rcv_base = self.rcv
        self._set_stats_with_pluses_('rcv', self.rcv_plus)

    def _use_growth_formula(self, min_value, max_value, scale):
        """
        Applies the growth formula to get the values of the specified stat at the current level.
        :param min_value: the minimum value of the stat
        :param max_value: the maximum value of the stat
        :param scale: the scaling rate of the stat
        :return: the value of the stat at the current level
        """
        value = ((self.current_level - 1) / (self.max_level - 1)) ** scale
        value *= (max_value - min_value)
        value += min_value
        return value

    def _set_stats_with_pluses_(self, type, num):
        """
        Modify the specified stat according to the specified amount of pluses
        :param type: 'hp', 'atk', or 'rcv'
        :param num: 0-99, the number of pluses for the specified stat
        """
        if type == 'hp':
            self.hp_plus = num
            self.hp = self.hp_base + self.hp_plus * 10
        elif type == 'atk':
            self.base_atk_plus = num
            self.base_atk = self.base_base_atk + self.base_atk_plus * 5
            self._set_atk_(self.attr_main, self.attr_sub)
            self._set_pronged_atk_(self.attr_main, self.attr_sub)
        elif type == 'rcv':
            self.rcv_plus = num
            self.rcv = self.rcv_base + self.rcv_plus * 3
