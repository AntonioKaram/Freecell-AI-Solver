import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
import memory.processMemoryReader as pmr
from concurrent.futures import ThreadPoolExecutor
from aisolver.solver import BFS, DFS, AStar, BestFirst
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsPixmapItem


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
        self.combo_box.addItems(self.menu_items)
        layout.addWidget(self.combo_box)
        
        self.run_button = QPushButton('Select')
        self.run_button.clicked.connect(self.write_solution)
        layout.addWidget(self.run_button)


        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        layout.addWidget(self.view)






        # self.card1 = QGraphicsPixmapItem(QPixmap())
        # self.card1.setBrush(QBrush(Qt.green))
        # self.card1.setPos(-150, -75)
        # self.scene.addItem(self.card1)

        # self.card2 = QGraphicsPixmapItem(0, 0, 100, 150)
        # self.card2.setBrush(QBrush(Qt.green))
        # self.card2.setPos(150, -75)
        # self.scene.addItem(self.card2)

        # Load the original image into a QImage
        image = QImage('../data/img/01c.png')

        # Create the mirrored image
        mirrored_image = image.mirrored(False, True)

        # Create QPixmaps from the images
        original_pixmap = QPixmap.fromImage(image)
        mirrored_pixmap = QPixmap.fromImage(mirrored_image)

        # Create QGraphicsPixmapItems for the cards
        self.card1_item = QGraphicsPixmapItem(original_pixmap)
        self.card2_item = QGraphicsPixmapItem(mirrored_pixmap)

        # Scale the QGraphicsPixmapItems to fit the slots
        self.card1_item.setScale(100 / original_pixmap.width())
        self.card2_item.setScale(100 / mirrored_pixmap.width())

        # Position the QGraphicsPixmapItems on the slots
        self.card1_item.setPos(-150, -75)
        self.card2_item.setPos(-150, 75)

        # Add the QGraphicsPixmapItems to the scene
        self.scene.addItem(self.card1_item)
        self.scene.addItem(self.card2_item)


        self.next_button = QPushButton('Next')
        self.next_button.clicked.connect(self.next_card)
        self.next_button.hide()
        layout.addWidget(self.next_button)

        self.moves_label = QLabel(f'Moves remaining: {self.count_moves}')
        layout.addWidget(self.moves_label)


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
            self.model_paths = list(executor.map(self.single_thread, [AStar(self.start_board), DFS(self.start_board), BestFirst(self.start_board)], ["A Star Search", "DFS", "Best"]))  
            # self.model_paths = list(executor.map(self.single_thread, [BFS(self.start_board),
            #                                                      DFS(self.start_board),
            #                                                      AStar(self.start_board),
            #                                                      BestFirst(self.start_board)], self.models))      
        
        self.menu_items.clear()
        for model, path in zip(self.models, self.model_paths):
            self.menu_items.append(model + " - " + str(len(path)) + " moves")

        self.combo_box.clear()  # Clear the combo box
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
        instruction = self.path.pop(0)

        self.moves_label.clear()
        self.count_moves -= 1
        self.moves_label.setText(f'Moves remaining: {self.count_moves}')


        print(instruction)

        pass


