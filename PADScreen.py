__author__ = 'Aaron'

from Calculator_Screen import CalculatorScreen
from Board_Screen import BoardScreen
from PAD_Monster import PADMonster
from PAD_Team import PADTeam
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QSplitter, QAction,
                             QFileDialog, QMainWindow, QStackedWidget, QSplitter)
from PyQt5.QtCore import Qt
import os
import json
from functools import partial


class PADScreen(QStackedWidget):

    def __init__(self, main_window):

        """
        Initialize the PADScreen Class
        :param gui: the main interface which will hold all of our widgets
        :param main_window: the main window widget which will hold our menu bar
        """
        super().__init__()

        # create an open file and save file action for our menu bar and connects them to their
        # respective functions
        open_file = QAction('Load Team...', main_window)
        open_file.setShortcut('Ctrl+O')
        open_file.triggered.connect(partial(self._show_dialog_box_, 'Open', main_window))
        save_file = QAction('Save Team...', main_window)
        save_file.setShortcut('Ctrl+S')
        save_file.triggered.connect(partial(self._show_dialog_box_, 'Save', main_window))

        clear_team = QAction('New Team', main_window)
        clear_team.setShortcut('Ctrl+N')
        clear_team.triggered.connect(self.__clear__team__)

        # create our menu bar, attach it to our main window and add to it our open and save actions
        menubar = main_window.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(open_file)
        file_menu.addAction(save_file)
        file_menu.addAction(clear_team)

        # create the widget containing the first page of the GUI, the calculator page
        self.calculator_screen = QWidget(self)
        # use custom calculator layout for the widget's layout
        self.calculator_screen_layout = CalculatorScreen(self)
        self.calculator_screen.setLayout(self.calculator_screen_layout)

        # initialize a variable to hold the PADTeam
        self.pad_team = self.calculator_screen_layout.pad_team
        self.team = self.calculator_screen_layout.team

        # create the widget containing the second page of the GUI, the board page
        self.board_screen = QWidget(self)
        # use custom board layout for the widget's layout
        self.board_screen_layout = BoardScreen(self, self.team, self.pad_team)
        self.board_screen.setLayout(self.board_screen_layout)
        # initially hide this page until the next page button is pressed
        #self.board_screen.hide()

        # create the bottom widget for the GUI which will contain the page turning buttons
        self.page_turner = QWidget(main_window)
        page_turner_layout = QHBoxLayout(main_window)
        self.page_turner.setLayout(page_turner_layout)
        self.turn_left = QPushButton('<', main_window)
        page_turner_layout.addWidget(self.turn_left)
        page_turner_layout.addStretch()
        page_turner_layout.addStretch()
        self.turn_right = QPushButton('>', main_window)
        page_turner_layout.addWidget(self.turn_right)
        # initially hide the button to turn left as the GUI initializes on page 1
        self.turn_left.hide()

        self.page_one_splitter = QSplitter(Qt.Vertical)
        self.page_one_splitter.addWidget(self.calculator_screen)
        self.page_one_splitter.addWidget(self.page_turner)
        self.addWidget(self.page_one_splitter)
        #self.setCurrentWidget(self.page_one_splitter)

        self.page_two_splitter = QSplitter(Qt.Vertical)
        self.page_two_splitter.addWidget(self.board_screen)
        #self.page_two_splitter.addWidget(page_turner)
        self.addWidget(self.page_two_splitter)
        #self.setCurrentWidget(self.page_two_splitter)

        self._init_screen_()

    def _init_screen_(self):

        """
        Set right click button to connect to the second page
        :param gui: the main interface all the widgets will be attached to
        """
        self.turn_right.clicked.connect(self._go_to_board_screen_)
        
    def _go_to_board_screen_(self, clicked):

        """
        Set the active screen to the second page and hide the first page when the respective
        button is clicked. Also hide the right button, show the left button and connect the
        left button to the first page.
        :param gui: same.
        :param clicked: the clicking event, useless.
        """
        self.board_screen_layout.team = self.calculator_screen_layout.team
        self.board_screen_layout.team_totals = self.calculator_screen_layout.pad_team
        self.board_screen_layout.set__team(self.board_screen_layout.team)
        self.setCurrentWidget(self.page_two_splitter)
        self.page_two_splitter.addWidget(self.page_turner)
        #self.board_screen.show()
        #self.calculator_screen.hide()

        self.turn_right.hide()
        self.turn_left.show()
        self.turn_left.clicked.connect(self._go_to_calculator_screen_)

    def _go_to_calculator_screen_(self, clicked):

        """
        Set the active screen to the first page and hide the second page when the respective
        button is clicked. Also hide the left button, show the right button and connect the
        right button to the second page.
        :param gui: same.
        :param clicked: useless clicking event.
        """
        self._init_screen_()
        self.turn_left.hide()
        self.turn_right.show()
        self.turn_right.clicked.connect(self._go_to_board_screen_)

        self.page_one_splitter.addWidget(self.page_turner)
        self.setCurrentWidget(self.page_one_splitter)
        #self.board_screen.hide()
        #self.calculator_screen.show()

    def _show_dialog_box_(self, stringname, gui):

        """
        If the stringname is 'Open', open a dialog where the user can select a team to load
        into the line edits.
        If the stringname is 'Save', open a dialog where the user can save the names of the
        team members into a txt file.
        :param stringname: 'Open' or 'Save', the corresponding menu action will contain the
        key stringname.
        :param gui: same.
        """
        if stringname == 'Open':
            filename = QFileDialog.getOpenFileName(gui, 'Load Team...', os.path.join('saved teams'),
                                                   'Text files (*.txt)')
            # if not empty string and has the appropriate subscript
            if filename[0] and filename[0].endswith('txt'):
                with open(os.path.realpath(filename[0]), 'r') as file:
                    json_content = json.loads(file.read())
                # decode the names in case of unicode strings like the infinity sign
                #content_decoded = content.decode('utf-8')
                #monster_names = content_decoded.splitlines()
                for monster in range(6):
                    # decode the name in case of unicode strings like the infinity sign
                    # name = json_content[monster]['name'].decode('utf-8')
                    name = json_content[monster]['name']
                    hp_plus = json_content[monster]['hp plus']
                    atk_plus = json_content[monster]['atk plus']
                    rcv_plus = json_content[monster]['rcv plus']
                    level = json_content[monster]['level']
                    # enter the names into the line edits
                    self.calculator_screen_layout.line_edits[monster].setText(name)
                    self.calculator_screen_layout._on_plus_value_activated_(monster, 'hp', hp_plus)
                    self.calculator_screen_layout._on_plus_value_activated_(monster, 'atk', atk_plus)
                    self.calculator_screen_layout._on_plus_value_activated_(monster, 'rcv', rcv_plus)
                    self.calculator_screen_layout._on_level_activated_(monster, level)


        if stringname == 'Save':
            filename = QFileDialog.getSaveFileName(gui, 'Save Team...', os.path.join('saved teams'),
                                                   'Text files (*.txt')
            # if not empty string
            if filename[0]:
                # create json file
                json_file = [{} for monster in range(6)]
                #monster_names = ''
                for monster in range(6):
                    # copy the team member's name to a variable
                    monster_name = self.calculator_screen_layout.team[monster].name
                    # copy the team member's pluses to variables
                    hp_plus = self.calculator_screen_layout.team[monster].hp_plus
                    atk_plus = self.calculator_screen_layout.team[monster].base_atk_plus
                    rcv_plus = self.calculator_screen_layout.team[monster].rcv_plus
                    # copy the team member's current level to a variable
                    current_level = self.calculator_screen_layout.team[monster].current_level
                    #monster_names += monster_name+'\n'
                    # encode the string to be saved for symbols like the infinity sign
                    #monster_name_encoded = monster_name.encode('utf8', 'replace')
                    json_file[monster]['name'] = monster_name
                    json_file[monster]['hp plus'] = hp_plus
                    json_file[monster]['atk plus'] = atk_plus
                    json_file[monster]['rcv plus'] = rcv_plus
                    json_file[monster]['level'] = current_level
                with open(os.path.realpath(filename[0]+'.txt'), 'w') as file:
                    json.dump(json_file, file)

    def __clear__team__(self):
        for index in range(6):
            self.calculator_screen_layout.line_edits[index].clear()
        self.calculator_screen_layout.team = [PADMonster() for monster in range(6)]
        self.calculator_screen_layout.pad_team = PADTeam(self.calculator_screen_layout.team)
        for index in range(6):
            self.calculator_screen_layout._set_labels_(self.calculator_screen_layout.team[index], index)
        # self.calculator_screen = QWidget(gui)
        # self.calculator_screen_layout = CalculatorScreen(gui)
        # self.calculator_screen.setLayout(self.calculator_screen_layout)
        # self.active_screen = self.calculator_screen