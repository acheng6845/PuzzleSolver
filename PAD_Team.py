__author__ = 'Aaron'
import os
from PAD_Monster import PADMonster

class PADTeam:

    def __init__(self, team):
        """
        Initializes the PADTeam Class.
        :param team: an array containing 6 PADMonster Classes
        """
        # self.team = [PADMonster() for monster in range(6)] -> how the team should look
        self.team = team
        # below we initialize the variables that will be containing the team stats.
        self.hp = 0
        # for all atk arrays: [fire atk, water atk, wood atk, light atk, dark atk]
        self.atk = [0, 0, 0, 0, 0]
        # for all base atks, it's the sum of each value in the array
        self.base_atk = 0
        self.pronged_atk = [0, 0, 0, 0, 0]
        self.base_pronged_atk = 0
        self.rcv = 0

        # below we initialize the modified stats, the team's total stats after being
        # multiplied by the effects of the two leader skills
        self.hp_modified = 0
        self.atk_modified = [0, 0, 0, 0, 0]
        self.base_atk_modified = 0
        self.pronged_atk_modified = [0, 0, 0, 0, 0]
        self.base_pronged_atk_modified = 0
        self.rcv_modified = 0

        # a string that will contain all our the teams' awakenings
        self.awakenings = ''

        # the leader skills effects: [hp multiplied by, atk multiplied by, rcv multiplied by]
        self.leader1_effects = [1, 1, 1]
        self.leader2_effects = [1, 1, 1]
        # store how each monster's stats will be modified as in if the monster satisfies the
        # leader skill's conditions
        self.stats_modified_by = [[1, 1, 1] for monster in range(6)]

        # set all the variables according to the team input
        self.__set__team__hp()
        self.__set__team__rcv()
        self.__set__team__atk()
        self.__set__team__base__atk()
        self.__set__team__awakenings()
        self.__set__modified__stats__()

    def __set__team__hp(self):
        self.hp = 0
        for monster in range(6):
            self.hp += self.team[monster].hp
    def __set__team__rcv(self):
        self.rcv = 0
        for monster in range(6):
            self.rcv += self.team[monster].rcv
    def __set__team__awakenings(self):
        self.awakenings = ''
        for awakening in range(len(self.team[0].awakenings)):
            # count stores how many instances of a specific awakening are contained in the team
            count = 0
            for monster in range(6):
                if self.team[monster].awakenings[awakening][2] > 0:
                    count += self.team[monster].awakenings[awakening][2]
            if count > 0:
                # if the team has an awakening, save it to the string and add the count number
                self.awakenings += self.team[0].awakenings[awakening][0]+': '+str(count)+'\n'
    def __set__team__atk(self):
        self.atk = [0, 0, 0, 0, 0]
        self.pronged_atk = [0, 0, 0, 0, 0]
        for attr in range(5):
            for monster in self.team:
                self.atk[attr] += monster.atk[attr]
                self.pronged_atk[attr] += monster.pronged_atk[attr]
    def __set__team__base__atk(self):
        self.base_atk = 0
        self.base_pronged_atk = 0
        for monster in self.team:
            self.base_atk += monster.atk[monster.attr_main]
            self.base_pronged_atk += monster.pronged_atk[monster.attr_main]
    def __set__modified__stats__(self):

        self.stats_modified_by = [[1, 1, 1] for monster in range(6)]

        # the first and last team members of the team are considered the leaders and we use
        # their respective leader skills.
        for index in [0, 5]:
            # if the leader skill isn't ""
            if self.team[index].leader_skill_name:
                # the skill effect will look [hp modified by, atk modified by, rcv modified by]
                # an additional 4th index exists if there's a conditional which will look like:
                # [hp * by, atk * by, rcv * by, ['elem' or 'type', # associated with elem or type]]
                if len(self.team[index].leader_skill_effect) > 3:
                    # if fourth array exists, save whether the conditional asks for an element
                    # or type in attribute variable
                    # and save the # associated in the num variable
                    attribute = self.team[index].leader_skill_effect[3][0]
                    num = self.team[index].leader_skill_effect[3][1]

                    # check if each monster in the team satisfies the elem or type conditional
                    # if true, the stats modified index for that monster will be multiplied appropriately
                    if attribute == "elem":
                        for monster in range(6):
                            if self.team[monster].attr_main == num or self.team[monster].attr_sub == num:
                                self.stats_modified_by[monster][0] *= self.team[index].leader_skill_effect[0]
                                self.stats_modified_by[monster][1] *= self.team[index].leader_skill_effect[1]
                                self.stats_modified_by[monster][2] *= self.team[index].leader_skill_effect[2]

                    elif attribute == "type":
                        for monster in range(6):
                            if self.team[monster].type_main == num or self.team[monster].type_sub == num:
                                self.stats_modified_by[monster][0] *= self.team[index].leader_skill_effect[0]
                                self.stats_modified_by[monster][1] *= self.team[index].leader_skill_effect[1]
                                self.stats_modified_by[monster][2] *= self.team[index].leader_skill_effect[2]

                # if there isn't a 4th index conditional, just multiply all of the stats modified indexes
                # by the appropriate skill effect amounts
                else:
                    for monster in range(6):
                        self.stats_modified_by[monster][0] *= self.team[index].leader_skill_effect[0]
                        self.stats_modified_by[monster][1] *= self.team[index].leader_skill_effect[1]
                        self.stats_modified_by[monster][2] *= self.team[index].leader_skill_effect[2]

        hp = 0
        base_atk = 0
        atk = [0, 0, 0, 0, 0]
        base_pronged_attack = 0
        pronged_atk = [0, 0, 0, 0, 0]
        rcv = 0

        # modify each team stat according to the leader skills' effects and save them to their respective
        # variables.
        for monster in range(6):
            hp += self.team[monster].hp * self.stats_modified_by[monster][0]
            rcv += self.team[monster].rcv * self.stats_modified_by[monster][2]
            main_attr = self.team[monster].attr_main
            base_atk += self.team[monster].atk[main_attr] * self.stats_modified_by[monster][1]
            base_pronged_attack += self.team[monster].pronged_atk[main_attr] * self.stats_modified_by[monster][1]
            for attr in range(5):
                atk[attr] += self.team[monster].atk[attr] * self.stats_modified_by[monster][1]
                pronged_atk[attr] += self.team[monster].pronged_atk[attr] * self.stats_modified_by[monster][1]
        self.hp_modified = hp
        self.atk_modified = atk
        self.base_atk_modified = base_atk
        self.pronged_atk_modified = pronged_atk
        self.base_pronged_atk_modified = base_pronged_attack
        self.rcv_modified = rcv
