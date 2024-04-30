import sys
import aisolver.card as c
from PyQt5.QtCore import Qt, QRectF
import memory.processMemoryReader as pmr
from concurrent.futures import ThreadPoolExecutor
from aisolver.solver import BFS, DFS, AStar, BestFirst
from PyQt5.QtGui import QImage, QPixmap, QPainterPath, QBrush, QColor, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsPixmapItem, QGraphicsPathItem


class MainWindow(QWidget):
    def __init__(self, start_board):
        super().__init__()
        
        self.setWindowTitle("Solitaire Solver")
        self.model = ""
        self.path = []
        self.count_moves = 0
        self.model_paths = []
        self.menu_items = []
        self.start_board = start_board
        self.models = ["Depth First Search", "A Star Search", "Best First Search"]
        self.setGeometry(100, 100, 800, 600)

        self.arrow_image = None

        self.instruction_label = None

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.run_button = QPushButton('Run')
        self.run_button.clicked.connect(self.run_algorithm)
        self.layout.addWidget(self.run_button)

        self.combo_box = QComboBox()
        self.combo_box.addItems(self.menu_items)
        self.layout.addWidget(self.combo_box)
        
        self.run_button = QPushButton('Select')
        self.run_button.clicked.connect(self.write_solution)
        self.layout.addWidget(self.run_button)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.layout.addWidget(self.view)

        self.next_button = QPushButton('Next')
        self.next_button.clicked.connect(self.next_card)
        self.next_button.hide()
        self.layout.addWidget(self.next_button)

        self.moves_label = QLabel(f'Moves remaining: {self.count_moves}')
        self.layout.addWidget(self.moves_label)


    def single_thread(self, seeker, alg):
        print(f"Running {alg}...")
        try:
            path = next(seeker.search())
        except StopIteration:
            path = []
        
        if path:
            print(f"{alg} Found a solution! Path length: {len(path)}")
        else:
            print(f"No solution found")
            
        return path

    def run_algorithm(self):  
        with ThreadPoolExecutor() as executor:
            self.model_paths = list(executor.map(self.single_thread, [
                                                                 DFS(self.start_board),
                                                                 AStar(self.start_board),
                                                                 BestFirst(self.start_board)], self.models))      
        
        self.menu_items.clear()
        for model, path in zip(self.models, self.model_paths):
            self.menu_items.append(model + " - " + str(len(path)) + " moves")

        self.combo_box.clear()
        self.combo_box.addItems(self.menu_items)
            
    def write_solution(self):
        self.model = self.combo_box.currentText().split(" -")[0]
        self.path = self.model_paths[self.models.index(self.model)]
        
        pmr.processMemoryReader.write_to_file(self.path, "out.txt")
        
        self.moves_label.clear()
        self.count_moves = len(self.path)
        self.moves_label.setText(f'Moves remaining: {self.count_moves}')
        self.next_button.show()

    def next_card(self):

        # Decrease num moves
        self.moves_label.clear()
        self.count_moves -= 1
        self.moves_label.setText(f'Moves remaining: {self.count_moves}')

        if self.count_moves <= 0:
            self.scene.clear()
            self.finish_label = QLabel("BANG!")
            font = QFont()
            self.instruction_label.move(0,0)
            font.setPointSize(40)
            self.scene.addWidget(self.finish_label)
            return

        # Get next instruction
        if self.path:
            instruction = self.path.pop(0).split(" ")
            command = instruction[0]

        if not self.arrow_image:
            self.arrow_image = QPixmap('../data/img/arrow.png').scaled(100, 150, Qt.KeepAspectRatio)
            self.arrow = QGraphicsPixmapItem(self.arrow_image)
            self.arrow.setPos(0, -30)
            self.scene.addItem(self.arrow)
            

        if command == 'stack':
            f1 = c.card_code_to_pic(instruction[1])
            sp1 = QPixmap(f1).scaled(100, 150, Qt.KeepAspectRatio)
            self.card1 = QGraphicsPixmapItem(sp1)
            self.card1.setPos(-150, -75)
            self.scene.addItem(self.card1)

            f2 = c.card_code_to_pic(instruction[-1])
            sp2 = QPixmap(f2).scaled(100, 150, Qt.KeepAspectRatio)
            self.card2 = QGraphicsPixmapItem(sp2)
            self.card2.setPos(150, -75)
            self.scene.addItem(self.card2)

            if self.instruction_label: self.instruction_label.clear()
            self.instruction_label = QLabel(f"Stack the {c.code_to_name(instruction[1])} on the {c.code_to_name(instruction[2])}")
            self.instruction_label.move(-50,-150)
            self.scene.addWidget(self.instruction_label)

        else:
            filename = c.card_code_to_pic(instruction[-1])
            scaled_pixmap = QPixmap(filename).scaled(100, 150, Qt.KeepAspectRatio)
            self.card1 = QGraphicsPixmapItem(scaled_pixmap)
            self.card1.setPos(-150, -75)
            self.scene.addItem(self.card1)

            path = QPainterPath()
            radius = 5
            rect = QRectF(0, 0, 100, 135)
            path.addRoundedRect(rect, radius, radius)

            self.card2 = QGraphicsPathItem(path)
            self.card2.setBrush(QBrush(Qt.green))
            self.card2.setPos(150, -75)
            self.scene.addItem(self.card2)

            self.command_label = QLabel(f'{command.title()}')
            self.command_label.move(198-len(command)*2,-13)
            self.scene.addWidget(self.command_label)


            if self.instruction_label: self.instruction_label.clear()
            self.instruction_label = QLabel(f"Move the {c.code_to_name(instruction[1])} to the {command.title()}")
            self.instruction_label.move(-50,-150)
            self.scene.addWidget(self.instruction_label)






















        # for e in instruction:
        #     filename = c.card_code_to_pic(e)

        




        print(instruction)

        pass


