from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QGraphicsScene, QGraphicsView, QGraphicsRectItem
from PyQt5.QtGui import QBrush
from PyQt5.QtCore import Qt
from aisolver.solver import BFS, DFS, AStar, BestFirst
import sys
import memory.processMemoryReader as pmr

class MainWindow(QWidget):
    def __init__(self, start_board):
        super().__init__()
        
        self.model = ""
        self.path = []
        self.count_moves = 0
        self.model_paths = []
        self.menu_items = []
        self.start_board = start_board
        self.models = ["Breadth First Search", "Depth First Search", "A Star Search", "Best First Search"]
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.run_button = QPushButton('Run')
        self.run_button.clicked.connect(self.run_algorithm)
        layout.addWidget(self.run_button)

        self.combo_box = QComboBox()
        self.combo_box.addItems(self.models)
        layout.addWidget(self.combo_box)
        
        self.run_button = QPushButton('Select')
        self.run_button.clicked.connect(self.write_solution)
        layout.addWidget(self.run_button)


        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        layout.addWidget(self.view)

        self.card1 = QGraphicsRectItem(0, 0, 100, 150)
        self.card1.setBrush(QBrush(Qt.green))
        self.card1.setPos(-150, -75)
        self.scene.addItem(self.card1)

        self.card2 = QGraphicsRectItem(0, 0, 100, 150)
        self.card2.setBrush(QBrush(Qt.green))
        self.card2.setPos(150, -75)
        self.scene.addItem(self.card2)

        self.next_button = QPushButton('Next')
        self.next_button.clicked.connect(self.next_card)
        self.next_button.hide()
        layout.addWidget(self.next_button)

        self.moves_label = QLabel(f'Moves remaining: {self.count_moves}')
        layout.addWidget(self.moves_label)

    def run_algorithm(self):        
        for seeker, alg in zip([BFS(self.start_board), DFS(self.start_board), AStar(self.start_board), BestFirst(self.start_board)], self.models):
            print(f"Running {alg}...")
            try:
                path = next(seeker.search())
            except StopIteration:
                path = []
            
            if path:
                print(f"Found a solution! Path length: {path}")
            else:
                print(f"No solution found")
                
            self.model_paths.append(path)
        
        for model, path in zip(self.models, self.model_paths):
            self.menu_options.append(model + " - " + str(len(path)) + " moves")
            
    def write_solution(self):
        self.model = self.selected_option.get().split(" -")
        self.path = self.model_paths[self.models.index(self.model)]
        
        pmr.write_to_file(self.path, "out.txt")
        
        self.count_moves = len(self.path)

    def next_card(self):
        pass


