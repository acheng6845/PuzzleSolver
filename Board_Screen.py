__author__ = 'Aaron'
from PyQt5.QtWidgets import (QVBoxLayout, QWidget, QLabel, QGridLayout, QSplitter,
                             QPushButton, QHBoxLayout)
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QPixmap, QDrag
import os
from PAD_Monster import PADMonster
from PAD_Team import PADTeam
from functools import partial
class BoardScreen(QVBoxLayout):
    default_team = [PADMonster() for monster in range(6)]
    default_team_totals = PADTeam(default_team)
    def __init__(self, gui, team=default_team, team_totals=default_team_totals):
        super().__init__()

        self.team = team
        self.team_totals = team_totals
        self.damage_array = [[{'main attribute': 0, 'sub attribute': 0} for col in range(2)] for row in range(6)]

        self.__init__screen__(gui, self.team, self.team_totals)

    def __init__screen__(self, gui, team, team_totals):
        # DAMAGE SCREEN
        damage_screen = QWidget()
        damage_screen_layout = QGridLayout()
        damage_screen.setLayout(damage_screen_layout)
        self.addWidget(damage_screen)
        self.damage_labels = [[QLabel(gui) for column in range(2)] for row in range(6)]
        for row in range(6):
            for column in range(2):
                damage_screen_layout.addWidget(self.damage_labels[row][column], row, column)
        # RECOVERY LABEL
        self.hp_recovered = QLabel(gui)
        self.addWidget(self.hp_recovered)
        # BOARD
        board = QWidget()
        board_layout = QGridLayout()
        board.setLayout(board_layout)
        self.addWidget(board)
        # TEAM IMAGES
        self.team_labels = []
        for index in range(6):
            label = QLabel(gui)
            self.team_labels.append(label)
            board_layout.addWidget(label, 0, index)
            board_layout.setAlignment(label, Qt.AlignHCenter)
        self.set__team(team)
        # BOARD
        self.board_labels = [[PADLabel(gui) for column in range(8)] for row in range(8)]
        # positions = [(i+1, j) for i in range(8) for j in range(8)]
        light_brown = 'rgb(120, 73, 4)'
        dark_brown = 'rgb(54, 35, 7)'
        color = dark_brown
        for row in self.board_labels:
            for column in row:
                row_index = self.board_labels.index(row)
                col_index = row.index(column)
                column.setStyleSheet("QLabel { background-color: %s }" % color)
                if color == dark_brown and (col_index+1) % 8 != 0:
                    color = light_brown
                elif color == light_brown and (col_index+1) % 8 != 0:
                    color = dark_brown
                board_layout.addWidget(column, row_index+1, col_index)
        #for position, label in zip(positions, self.board_labels):
        #    board_layout.addWidget(label, *position)
        for row in range(9):
            board_layout.setRowStretch(row, 1)
        for column in range(8):
            board_layout.setColumnStretch(column, 1)

        self.board_array = []
        self.__create__board___(5, 6)

        # CALCULATE DAMAGE BUTTON
        calculate_damage_button = QPushButton('Calculate Damage', gui)
        calculate_damage_button.clicked.connect(partial(self.calculate_damage, team, team_totals))
        self.addWidget(calculate_damage_button)
        # ORBS
        # orb_wrapper = QWidget(gui)
        # orb_wrapper_layout = QHBoxLayout()
        # orb_wrapper.setLayout(orb_wrapper_layout)

        # elements = ['fire', 'water', 'wood', 'light', 'dark']
        # for element in elements:
        #     orb = PADIcon(gui)
        #     orb.setPixmap(QPixmap(os.path.join('icons')+'\\'+element+'.png'))
        #     orb_wrapper_layout.addWidget(orb)
        #
        # self.addWidget(orb_wrapper)

    def __create__board___(self, row, column):
        self.board_array = [['' for column in range(column)] for row in range(row)]

        for row_index in self.board_labels:
            for col_label in row_index:
                col_label.hide()
        for x in range(row):
            for y in range(column):
                self.board_labels[x][y].show()

    def calculate_damage(self, team=default_team, team_totals=default_team_totals):
        for row in range(len(self.board_array)):
            for column in range(len(self.board_array[0])):
                self.board_array[row][column] = self.board_labels[row][column].element
        all_positions = set()
        # 0 = fire, 1 = water, 2 = wood, 3 = light, 4 = dark, 5 = heart
        elemental_damage = [{'fire': 0, 'water': 0, 'wood': 0, 'light': 0, 'dark': 0}
                            for monster in range(6)]
        total_hp_recovered = 0
        combo_count = 0
        colors = ['red', 'blue', 'green', 'goldenrod', 'purple', 'pink']
        attribute_translator = ['fire', 'water', 'wood', 'light', 'dark', 'heart']
        for row in range(len(self.board_array)):
            for column in range(len(self.board_array[0])):
                combo_length, positions = self.__find__combos__recursively__(self.board_array, row, column)
                if combo_length >= 3 and not next(iter(positions)) in all_positions and self.board_array[row][column]:
                    print(str(self.board_array[row][column])+":",combo_length,'orb combo.')

                    attribute = attribute_translator.index(self.board_array[row][column])
                    if attribute != 5:
                        for monster in range(6):
                            if combo_length == 4:
                                damage = team[monster].pronged_atk[attribute] * 1.25
                            else:
                                damage = team[monster].atk[attribute] * (1+0.25*(combo_length-3))
                            elemental_damage[monster][self.board_array[row][column]] += damage
                    else:
                        total_rcv = 0
                        for monster in range(6):
                            total_rcv += team[monster].rcv
                        total_hp_recovered += total_rcv * (1+0.25*(combo_length-3))
                        print(total_hp_recovered)
                        print(total_rcv)
                    all_positions |= positions
                    combo_count += 1
        combo_multiplier = 1+0.25*(combo_count-1)
        for monster in range(6):
            main_attribute = attribute_translator[team[monster].attr_main]
            sub_attribute = ''
            if team[monster].attr_sub or team[monster].attr_sub == 0:
                sub_attribute = attribute_translator[team[monster].attr_sub]
            if sub_attribute:
                if main_attribute != sub_attribute:
                    main_damage = elemental_damage[monster][main_attribute] * combo_multiplier
                    sub_damage = elemental_damage[monster][sub_attribute] * combo_multiplier
                else:
                    main_damage = elemental_damage[monster][main_attribute] * combo_multiplier * (10/11)
                    sub_damage = elemental_damage[monster][sub_attribute] * combo_multiplier * (1/11)
            else:
                main_damage = elemental_damage[monster][main_attribute] * combo_multiplier
                sub_damage = 0
            self.damage_labels[monster][0].setText(str(main_damage))
            self.damage_labels[monster][0].setStyleSheet("QLabel { color : %s }" % colors[team[monster].attr_main])
            self.damage_labels[monster][1].setText(str(sub_damage))
            if team[monster].attr_sub or team[monster].attr_sub == 0:
                self.damage_labels[monster][1].setStyleSheet("QLabel { color : %s }" % colors[team[monster].attr_sub])

        total_hp_recovered *= combo_multiplier
        self.hp_recovered.setText(str(total_hp_recovered))
        self.hp_recovered.setStyleSheet("QLabel { color : %s }" % colors[5])

    def set__team(self, team):
        for label, member in zip(self.team_labels, team):
            try:
                image = QPixmap(os.path.join('images')+'/'+member.name+'.png')
                image.scaled(75, 75)
                label.setPixmap(image)
            except Exception: pass

    def __find__combos__recursively__(self, array, row, column):
        combo_length = 0
        positions = set()
        row_length = self.checkIndexInRow(array, row, column)
        if row_length >= 3:
            more_length, more_positions = self.__find__combos__recursively__(array, row, column+row_length-1)
            combo_length += row_length + more_length - 1
            positions |= more_positions
            for col_index in range(row_length):
                positions.add((row, column+col_index))
        column_length = self.checkIndexInColumn(array, row, column)
        if column_length >= 3:
            more_length, more_positions = self.__find__combos__recursively__(array, row+column_length-1, column)
            combo_length += column_length + more_length - 1
            positions |= more_positions
            for row_index in range(column_length):
                positions.add((row+row_index, column))
        if row_length >= 3 and column_length >= 3:
            return combo_length - 1, positions
        elif row_length < 3 and column_length < 3:
            return 1, positions
        return combo_length, positions

    def checkIndexInRow(self, array, row, col_index):
        combo_length = 0
        if array[row].count(array[row][col_index]) >= 3:
            if col_index > 0:
                if array[row][col_index - 1] != array[row][col_index]:
                    combo_length += self.recurseThroughRow(array, row, col_index)
            else:
                combo_length += self.recurseThroughRow(array, row, col_index)
        return combo_length

    def recurseThroughRow(self, array, row, col_index, count=1):
        if array[row][col_index + count] == array[row][col_index]:
            count += 1
            if col_index + count < len(array[row]):
                return self.recurseThroughRow(array, row, col_index, count)
            else:
                return count
        else:
            return count

    def checkIndexInColumn(self, array, row_index, col):
        elements_in_column = []
        combo_length = 0
        for index in range(row_index, len(array)):
            elements_in_column.append(array[index][col])
        if elements_in_column.count(array[row_index][col]) >= 3:
            if row_index > 0:
                if array[row_index][col] != array[row_index - 1][col]:
                    combo_length += self.recurseThroughCol(array, row_index, col)
            else:
                combo_length += self.recurseThroughCol(array, row_index, col)
        return combo_length

    def recurseThroughCol(self, array, row_index, col, count=1):
        if array[row_index + count][col] == array[row_index][col]:
            count += 1
            if row_index + count < len(array):
                return self.recurseThroughCol(array, row_index, col, count)
            else:
                return count
        else:
            return count

class PADLabel(QLabel):

    def __init__(self, gui):
        super().__init__(gui)
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
        self.setScaledContents(True)

        self.color_counter = -1
        self.colors = ['fire', 'water', 'wood', 'light', 'dark', 'heart']
        self.element = ''

        self.setFixedSize(75, 75)

    def mousePressEvent(self, click):
        if click.button() == Qt.LeftButton and self.rect().contains(click.pos()):
            if self.color_counter != 5:
                self.color_counter += 1
            else:
                self.color_counter = 0
            self.element = self.colors[self.color_counter]
            icon = QPixmap(os.path.join('icons')+'/'+self.element+'.png')
            icon.scaled(75, 75)
            self.setPixmap(icon)
    def dragEnterEvent(self, event):
        if event.mimeData().hasImage():
            event.accept()
        else:
            event.ignore()
    def dropEvent(self, event):
        image = event.mimeData().imageData().value<QImage>()
        self.setPixmap(image)

class PADIcon(QLabel):
    def __init__(self, gui):
        super().__init__()

        self.gui = gui

        self.setMouseTracking(True)
        self.location = self.rect()

    def mousePressEvent(self, click):
        if click.button() == Qt.LeftButton and self.rect().contains(click.pos()):
            print('On it!')
            drag = QDrag(self.gui)
            mimeData = QMimeData()

            mimeData.setImageData(self.pixmap().toImage())
            drag.setMimeData(mimeData)
            drag.setPixmap(self.pixmap())

            dropAction = drag.exec()