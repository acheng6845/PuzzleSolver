__author__ = 'Aaron'
# Class Description:
#  Create framework for the split screens used in PAD_GUI
# import necessary files
import os
import json
from functools import partial
from PyQt5.QtWidgets import (QLabel, QWidget, QHBoxLayout,
                             QFrame, QSplitter, QStyleFactory,
                             QGridLayout, QLineEdit, QPushButton,
                             QVBoxLayout, QCompleter, QComboBox,
                             QScrollArea, QToolTip)
from PyQt5.QtGui import QPixmap, QColor, QFont
from PyQt5.QtCore import Qt, QStringListModel
from PAD_Monster import PADMonster
from PAD_Team import PADTeam

class CalculatorScreen(QHBoxLayout):
    def __init__(self, gui):
        super().__init__()

        # 0 = lead1, 1 = sub1,..., 5 = lead2
        self.team = [PADMonster() for x in range(6)]
        self.pad_team = PADTeam(self.team)
        # keeps old team stats before modification from leader multipliers
        self.team_base = [PADMonster() for x in range(6)]

        # open monsters.txt and load it into a python object using json
        # self.json_file = requests.get('https://padherder.com/api/monsters')
        self.json_file = open(os.path.join('.\monsters.txt'), 'r')
        self.json_monsters = json.loads(self.json_file.read())
        # print(self.json_monsters[0]["name"])

        self.completer_string_list_model = QStringListModel()
        array_of_monster_names = []
        for x in range(len(self.json_monsters)):
            array_of_monster_names.append(self.json_monsters[x]["name"])
        self.completer_string_list_model.setStringList(array_of_monster_names)

        # checks if the modified button has been pressed so other functions can know which stat to display
        self.is_pressed = False

        QToolTip.setFont(QFont('SansSerif', 10))

        self.init_screen(gui)

    def init_screen(self, gui):

        # add things to top of the screen here (Monitor section)!

        # Create an overarching top widget/layout

        supreme_top_box = QWidget()
        supreme_top_box_layout = QVBoxLayout()
        supreme_top_box.setLayout(supreme_top_box_layout)

        # Monitor section will have labels inside of a grid layout
        top_box = QWidget()
        grid = QGridLayout()
        top_box.setLayout(grid)
        supreme_top_box_layout.addWidget(top_box)

        # Creates lists of labels, initially having only static labels and having
        # the tangible labels substituted with ''
        static_labels = ['', '', '', '', '', '', '', '',
                         '', 'Lead 1', 'Sub 1 ', 'Sub 2 ', 'Sub 3 ', 'Sub 4 ', 'Lead 2', 'Team Totals',
                         'Type:', '', '', '', '', '', '', '',
                         'HP:', 0, 0, 0, 0, 0, 0, 0,
                         'Atk:', 0, 0, 0, 0, 0, 0, 0,
                         'Pronged Atk:', 0, 0, 0, 0, 0, 0, 0,
                         'RCV:', 0, 0, 0, 0, 0, 0, 0,
                         'Awakenings:', '', '', '', '', '', '', '']

        self.display_labels = [QLabel(gui) for x in range(len(static_labels))]

        for s_label, d_label in zip(static_labels, self.display_labels):

            if s_label == '':
                continue
            d_label.setText(str(s_label))

        positions = [(i, j) for i in range(8) for j in range(8)]

        for position, d_label in zip(positions, self.display_labels):
            # why *position? because the array is [(i,j), (i,j),...,(i,j)]
            grid.addWidget(d_label, *position)
            grid.setAlignment(d_label, Qt.AlignHCenter)

        self.leader_skills_labels = [QLabel(gui) for x in range(2)]
        for x in range(2):
            self.leader_skills_labels[x].setText('Leader Skill '+str(x+1)+': ')
            supreme_top_box_layout.addWidget(self.leader_skills_labels[x])

        # Create another row of labels for Awoken Skills Image Lists

        # Create another row of labels to show the Leader Skill Multipliers

        ########################################################################

        # add things to bottom of the screen here (Input section)!

        # Input section will be split in two: have LineEdits in a grid layout and then PushButtons in a separate grid
        # layout
        bottom_box = QWidget()
        grid2 = QGridLayout()
        bottom_box.setLayout(grid2)

        bottom_labels_text = ['Leader 1', 'Sub 1', 'Sub 2', 'Sub 3', 'Sub 4', 'Leader 2']
        bottom_labels = [QLabel(gui) for x in range(6)]
        instruction_labels_text = ['Please enter the name here:', 'Enter level here:', 'Enter pluses here:']
        instruction_labels = [QLabel(gui) for x in range(3)]
        self.line_edits = [QLineEdit(gui) for x in range(6)]
        line_edit_completer = QCompleter()
        line_edit_completer.setCaseSensitivity(Qt.CaseInsensitive)
        line_edit_completer.setFilterMode(Qt.MatchContains)
        line_edit_completer.setModel(self.completer_string_list_model)

        # Combo Boxes for Levels and Pluses
        level_boxes = [QComboBox(gui) for x in range(6)]
        self.plus_boxes_types = [QComboBox(gui) for x in range(6)]
        self.plus_boxes_values = [QComboBox(gui) for x in range(6)]
        for x in range(6):
            for n in range(0,100):
                if n != 0 and n <= self.team[x].max_level:
                    level_boxes[x].addItem(str(n))
                self.plus_boxes_values[x].addItem(str(n))
            self.plus_boxes_types[x].addItem('hp')
            self.plus_boxes_types[x].addItem('atk')
            self.plus_boxes_types[x].addItem('rcv')
            self.plus_boxes_values[x].hide()

        # add the labels and line_edits to the bottom grid
        for x in range(6):
            bottom_labels[x].setText(bottom_labels_text[x])
            bottom_labels[x].adjustSize()
            grid2.addWidget(bottom_labels[x], *(x+1, 0))
            grid2.addWidget(self.line_edits[x], *(x+1, 1))
            grid2.addWidget(level_boxes[x], *(x+1, 2))
            grid2.addWidget(self.plus_boxes_types[x], *(x+1, 3))
            grid2.addWidget(self.plus_boxes_values[x], *(x+1, 3))
            self.line_edits[x].textChanged[str].connect(partial(self._on_changed_, x))
            self.line_edits[x].setCompleter(line_edit_completer)
            self.line_edits[x].setMaxLength(50)
            level_boxes[x].activated[str].connect(partial(self._on_level_activated_, x))
            self.plus_boxes_types[x].activated[str].connect(partial(self._on_plus_type_activated_, x))
        for x in range(3):
            instruction_labels[x].setText(instruction_labels_text[x])
            instruction_labels[x].adjustSize()
            grid2.addWidget(instruction_labels[x], *(0, x+1))

        ###########################################################################

        # create the button widgets in a separate widget below bottom_box
        below_bottom_box = QWidget()
        grid3 = QGridLayout()
        below_bottom_box.setLayout(grid3)

        # create a set of buttons below the line_edits:
        #  White(Base) Red Blue Green Yellow Purple
        buttons = []
        button_labels = ['Fire', 'Water', 'Wood', 'Light', 'Dark', 'Base']
        button_colors = ['red', 'lightskyblue', 'green', 'goldenrod', 'mediumpurple', 'white']
        for x in range(6):
            buttons.append(QPushButton(button_labels[x], gui))
            buttons[x].clicked.connect(partial(self._handle_button_, x))
            buttons[x].setStyleSheet('QPushButton { background-color : %s }' % button_colors[x])
            grid3.addWidget(buttons[x], *(0, x))

        # create a QHBoxLayout widget that holds the page turners and toggle
        page_turner = QWidget()
        page_turner_layout = QHBoxLayout()
        page_turner.setLayout(page_turner_layout)

        # create the page turner and toggle widgets
        page_turner_layout.addStretch()
        self.toggle_button = QPushButton('Toggle On Modified Stats', gui)
        self.toggle_button.setCheckable(True)
        self.toggle_button.clicked[bool].connect(self._handle_toggle_button_)
        page_turner_layout.addWidget(self.toggle_button)
        page_turner_layout.addStretch()

        # Create overarching bottom widget
        supreme_bottom_box = QWidget()
        supreme_bottom_box_layout = QVBoxLayout()
        supreme_bottom_box.setLayout(supreme_bottom_box_layout)
        button_label = QLabel('Select from below the attribute you would like to display.')
        supreme_bottom_box_layout.setAlignment(button_label, Qt.AlignHCenter)
        supreme_bottom_box_layout.addWidget(bottom_box)
        supreme_bottom_box_layout.addWidget(button_label)
        supreme_bottom_box_layout.addWidget(below_bottom_box)
        supreme_bottom_box_layout.addWidget(page_turner)

        # Add the two screens into a split screen
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(supreme_top_box)
        splitter.addWidget(supreme_bottom_box)

        # Add the split screen to our main screen
        self.addWidget(splitter)

    def _create_monster_(self, index, dict_index, name):

        """
        When a valid name has been entered into the line edits, create a PADMonster Class
        using the values stored in the json dictionary and save the PADMonster to the appropriate
        index in the team array and PADTeam Class subsequently.
        :param index: 0 = lead 1, 1 = sub 1, 2 = sub 2, 3 = sub 3, 4 = sub 4, 5 = lead 2
        :param dict_index: the index in the json dictionary containing the monster
        :param name: the monster's name
        """
        self.team[index] = PADMonster()
        self.team_base[index] = PADMonster()

        hp_max = self.json_monsters[dict_index]["hp_max"]
        atk_max = self.json_monsters[dict_index]["atk_max"]
        rcv_max = self.json_monsters[dict_index]["rcv_max"]
        attr1 = self.json_monsters[dict_index]["element"]
        attr2 = self.json_monsters[dict_index]["element2"]
        type1 = self.json_monsters[dict_index]["type"]
        type2 = self.json_monsters[dict_index]["type2"]
        image60_size = self.json_monsters[dict_index]["image60_size"]
        image60_href = self.json_monsters[dict_index]["image60_href"]
        awakenings = self.json_monsters[dict_index]["awoken_skills"]
        leader_skill_name = self.json_monsters[dict_index]["leader_skill"]
        max_level = self.json_monsters[dict_index]["max_level"]
        hp_min = self.json_monsters[dict_index]["hp_min"]
        atk_min = self.json_monsters[dict_index]["atk_min"]
        rcv_min = self.json_monsters[dict_index]["rcv_min"]
        hp_scale = self.json_monsters[dict_index]["hp_scale"]
        atk_scale = self.json_monsters[dict_index]["atk_scale"]
        rcv_scale = self.json_monsters[dict_index]["rcv_scale"]
        # use PAD_Monster's function to set our monster's stats
        self.team[index].set_base_stats(name, hp_max, atk_max, rcv_max, attr1, attr2, type1,
                                        type2, image60_size, image60_href, awakenings,
                                        leader_skill_name, max_level, hp_min, hp_scale,
                                        atk_min, atk_scale, rcv_min, rcv_scale)
        # create a PADTeam Class according to our team of Six PADMonster Classes
        self.pad_team = PADTeam(self.team)
        # set our labels according to our monsters
        self._set_labels_(self.team[index], index)

        # save our team for future modifications:
        self.team_base[index].set_base_stats(name, hp_max, atk_max, rcv_max, attr1, attr2, type1,
                                             type2, image60_size, image60_href, awakenings,
                                             leader_skill_name, max_level, hp_min, hp_scale,
                                             atk_min, atk_scale, rcv_min, rcv_scale)

    def _set_labels_(self, monster, index):
        """
        Set the labels according to the values in the indexed PADMonster Class
        :param monster: the PADMonster associated with the index
        :param index: the index associated with the PADMonster [0-5]
        """
        # extract and display image
        self.display_labels[index + 1].setPixmap(QPixmap(os.path.join('images') + '/' + monster.name + '.png'))
        # display name
        font = QFont()
        font.setPointSize(5)
        type_text = monster.type_main_name+'/'+monster.type_sub_name
        self.display_labels[index + 17].setText(type_text)
        self.display_labels[index + 17].setFont(font)
        self.display_labels[index + 17].adjustSize()
        self.display_labels[index + 17].setToolTip(type_text)
        # display hp
        hp = monster.hp
        # if modified by leader skills button has been pressed, multiply monster's stat by its
        # respective index in the stats modified variable of the PADTeam Class
        if self.is_pressed:
            hp *= self.pad_team.stats_modified_by[index][0]
        # if plus values have been set, display how many
        if monster.hp_plus > 0:
            self.display_labels[index + 25].setText(str(round(hp)) + ' (+' + str(monster.hp_plus) + ')')
        else:
            self.display_labels[index + 25].setText(str(round(hp)))
        self.display_labels[index + 25].adjustSize()
        # display attack and pronged attack of main element
        self._set_attack_labels_(index, 5, monster.atk[monster.attr_main], monster.pronged_atk[monster.attr_main],
                                 monster.base_atk_plus)
        # display rcv
        rcv = monster.rcv
        # if modified by leader skills button has been pressed, multiply monster's stat by its
        # respective index in the stats modified variable of the PADTeam Class
        if self.is_pressed:
            rcv *= self.pad_team.stats_modified_by[index][2]
        # if plus values have been set, display how many
        if monster.rcv_plus > 0:
            self.display_labels[index + 49].setText(str(round(rcv)) + ' (+' + str(monster.rcv_plus) + ')')
        else:
            self.display_labels[index + 49].setText(str(round(rcv)))
        self.display_labels[index + 49].adjustSize()
        # display awakenings
        awakenings_text = ''
        awakenings_font = QFont()
        awakenings_font.setPointSize(6)
        for x in range(len(monster.awakenings)):
            if monster.awakenings[x][2] > 0:
                awakenings_text += monster.awakenings[x][0]+': '+str(monster.awakenings[x][2])+'\n'
        # set awakenings string to a tooltip since it can't fit into the grid
        self.display_labels[index + 57].setText('Hover Me!')
        self.display_labels[index + 57].setFont(awakenings_font)
        self.display_labels[index + 57].adjustSize()
        self.display_labels[index + 57].setToolTip(awakenings_text)
        # calculate and change our display labels for team total values with each change in monster
        self._set_team_labels_()
        # if the monster is in the first or last index, it's considered the leader and its leader skill name
        # and effect are displayed accordingly.
        if index == 0:
            text = 'Leader Skill 1: '+self.team[0].leader_skill_name+' > '+self.team[0].leader_skill_desc
            # if the string is too long, splice it up
            if len(text) > 50:
                divider = len(text)//2
                # separate the string at a part that is a whitespace
                while text[divider] != ' ':
                    divider += 1
                final_text = text[:divider]+'\n'+text[divider:]
            else:
                final_text = text
            self.leader_skills_labels[0].setText(final_text)

        elif index == 5:
            text = 'Leader Skill 1: '+self.team[5].leader_skill_name+' > '+self.team[5].leader_skill_desc
            # if the string is too long, splice it up
            if len(text) > 50:
                divider = len(text)//2
                # separate the string at a part that is a whitespace
                while text[divider] != ' ':
                    divider += 1
                final_text = text[:divider]+'\n'+text[divider:]
            else:
                final_text = text
            self.leader_skills_labels[1].setText(final_text)

    def _set_attack_labels_(self, index, color_num, atk_value, pronged_atk_value, plus_value = 0):
        """
        Set the attack labels according to the values given.
        :param index: the index of the PADMonster [0-5] and 6 = the team total
        :param color_num: 0 = fire, 1 = water, 2 = wood, 3 = light, 4 = dark, 5 = base
        :param atk_value: the value to be displayed in the attack label
        :param pronged_atk_value: the value to be displayed in the pronged attack label
        :param plus_value: the amount of pluses is set to 0 initially
        """
        # an array holding the colors associated with each value of color_num
        colors = ['red', 'blue', 'green', 'goldenrod', 'purple', 'black']

        # if modified by leader skills button has been pressed, multiply monster's stat by its
        # respective index in the stats modified variable of the PADTeam Class
        if self.is_pressed and index != 6:
            atk_value *= self.pad_team.stats_modified_by[index][1]
            pronged_atk_value *= self.pad_team.stats_modified_by[index][1]
        # display attack of main element
        if plus_value > 0:
            self.display_labels[index + 33].setText(str(round(atk_value)) + ' (+' + str(plus_value) + ')')
        else:
            self.display_labels[index + 33].setText(str(round(atk_value)))
        self.display_labels[index + 33].setStyleSheet("QLabel { color : %s }" % colors[color_num])
        self.display_labels[index + 33].adjustSize()
        # display pronged attack of main element
        self.display_labels[index + 41].setText(str(round(pronged_atk_value)))
        self.display_labels[index + 41].setStyleSheet("QLabel {color : %s }" % colors[color_num])
        self.display_labels[index + 41].adjustSize()

    def _set_team_labels_(self):
        """
        Access the PADTeam Class to extract the values to be displayed in the Team Totals Labels
        """
        # initialize objects to store the total values
        hp_total = self.pad_team.hp
        atk_total = self.pad_team.base_atk
        pronged_atk_total = self.pad_team.base_pronged_atk
        rcv_total = self.pad_team.rcv
        total_awakenings = self.pad_team.awakenings

        # if the modified by leader skills button is pressed, use the team's modified stats instead
        if self.is_pressed:
            hp_total = self.pad_team.hp_modified
            atk_total = self.pad_team.base_atk_modified
            pronged_atk_total = self.pad_team.base_pronged_atk_modified
            rcv_total = self.pad_team.rcv_modified

        # display our total value objects on our labels
        self.display_labels[31].setText(str(round(hp_total)))
        self.display_labels[31].adjustSize()
        self._set_attack_labels_(6, 5, atk_total, pronged_atk_total)
        self.display_labels[55].setText(str(round(rcv_total)))
        self.display_labels[55].adjustSize()

        # set the label containing the team's total awakenings to a tooltip since it won't fit
        awakenings_font = QFont()
        awakenings_font.setPointSize(6)
        self.display_labels[63].setText('Hover Me!')
        self.display_labels[63].setFont(awakenings_font)
        self.display_labels[63].adjustSize()
        self.display_labels[63].setToolTip(total_awakenings)

    def _get_total_attr_attack_(self, attr):
        """
        Returns the values stored in PADTeam for the Team's Total Attacks and Pronged Attacks
        for the specified element or the sum of all the element's attacks (BASE)
        :param attr: 0 = fire, 1 = water, 2 = wood, 3 = light, 4 = dark, 5 = base
        :return:
        """
        # if we're not looking for the base values a.k.a. sum of all the values
        if attr != 5:
            if not self.is_pressed:
                atk_total = self.pad_team.atk[attr]
                pronged_atk_total = self.pad_team.pronged_atk[attr]
            else:
                atk_total = self.pad_team.atk_modified[attr]
                pronged_atk_total = self.pad_team.pronged_atk_modified[attr]
        # if we're looking for the base values
        else:
            if not self.is_pressed:
                atk_total = self.pad_team.base_atk
                pronged_atk_total = self.pad_team.base_pronged_atk
            else:
                atk_total = self.pad_team.base_atk_modified
                pronged_atk_total = self.pad_team.base_pronged_atk_modified

        return atk_total, pronged_atk_total

    # when line_edits are altered, activate this line code according to the text in the line
    def _on_changed_(self, index, text):
        """
        When a line edit is altered, check the text entered to see if it matches with any of
        the names in the json dictionary and create a PADMonster at the appropriate index in
        the team array if the name is found.
        :param index: the index of the line edit corresponding to the index of the PADMonster
        in the team array.
        :param text: the text currently inside the line edit
        """
        for x in range(len(self.json_monsters)):
            if text == self.json_monsters[x]["name"]:
                self._create_monster_(index, x, text)
            elif text.title() == self.json_monsters[x]["name"]:
                self._create_monster_(index, x, text.title())

    def _handle_button_(self, color_num, pressed):
        """
        Only show the Attack and Pronged Attack values of the appropriate element or sum of the
        elements if BASE is chosen.
        :param color_num: 0 = fire, 1 = water, 2 = wood, 3 = light, 4 = dark, 5 = base
        :param pressed: useless event input
        """
        for index in range(6):
            if color_num == 5:
                self._set_attack_labels_(index, color_num, self.team[index].atk[self.team[index].attr_main],
                                         self.team[index].pronged_atk[self.team[index].attr_main])
            else:
                self._set_attack_labels_(index, color_num, self.team[index].atk[color_num],
                                         self.team[index].pronged_atk[color_num])

        atk_total, pronged_atk_total = self._get_total_attr_attack_(color_num)

        self._set_attack_labels_(6, color_num, atk_total, pronged_atk_total)

    def _handle_toggle_button_(self, pressed):
        """
        If the modify stats by leader skills button is pressed, modify the button's text, set
        the Class Variable is_pressed to True/False accordingly, and reset the labels now that
        is_pressed has been changed.
        :param pressed: Useless event input.
        """
        if pressed:
            self.is_pressed = True
            self.toggle_button.setText('Toggle Off Modified Stats')
        else:
            self.is_pressed = False
            self.toggle_button.setText('Toggle On Modified Stats')

        for monster in range(6):
            self._set_labels_(self.team[monster], monster)

    def _on_level_activated_(self, index, level):
        """
        If a level for the PADMonster has been selected, change the monster's base stats
        according to that level, reset pad_team according to these new values and reset
        labels accordingly.
        :param index: PADMonster's index in the team array. [0-5]
        :param level: the level the PADMonster will be set to
        """
        self.team[index]._set_stats_at_level_(int(level))
        self.team_base[index]._set_stats_at_level_(int(level))
        self.pad_team = PADTeam(self.team)

        for monster in range(6):
            self._set_labels_(self.team[monster], monster)

    def _on_plus_type_activated_(self, index, text):
        """
        If hp, atk, or rcv has been selected in the drop down menu, hide the menu asking for the
        type and show the menu asking for the value of pluses between 0-99.
        :param index: PADMonster's index in the team array. [0-5]
        :param text: 'hp', 'atk', or 'rcv'
        """
        self.plus_boxes_types[index].hide()
        self.plus_boxes_values[index].show()
        try: self.plus_boxes_values[index].activated[str].disconnect()
        except Exception: pass
        self.plus_boxes_values[index].activated[str].connect(partial(self._on_plus_value_activated_, index, text))
        self.plus_boxes_types[index].disconnect()
    def _on_plus_value_activated_(self, index, type, value):
        """
        If the value pertaining to the specified type has been selected, modify the appropriate
        stat of the indexed PADMonster according the specified amount of pluses, reset the
        pad_team according to the modified stats, and redisplay the new values
        :param index: PADMonster's index in the team array. [0-5]
        :param type: 'hp', 'atk', or 'rcv'
        :param value: the value, 0-99, of pluses the PADMonster has for the specified type
        """
        self.plus_boxes_types[index].show()
        self.plus_boxes_types[index].activated[str].connect(partial(self._on_plus_type_activated_, index))
        self.plus_boxes_values[index].hide()
        self.team[index]._set_stats_with_pluses_(type, int(value))
        self.team_base[index]._set_stats_with_pluses_(type, int(value))
        self.pad_team = PADTeam(self.team)

        for monster in range(6):
            self._set_labels_(self.team[monster], monster)

# class mouselistener(QLabel):
#     def __init__(self):
#         super().__init__()
#
#         self.setMouseTracking(True)
#         self.widget_location = self.rect()
#
#     def mouseMoveEvent(self, event):
#         posMouse = event.pos()
#         font = QFont()
#         if self.widget_location.contains(posMouse):
#             font.setPointSize(8)
#
#             QToolTip.setFont(font)
#             self.setToolTip(self.text())
#
#         return super().mouseReleaseEvent(event)
