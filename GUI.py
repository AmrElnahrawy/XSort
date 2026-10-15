from PyQt5 import QtCore, QtGui, QtWidgets
from XSort import XSort

class BarCanvas(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.array = []
        self.highlight = ()
        self.setContentsMargins(40, 40, 40, 40)


    def build(self, array, highlight=()):
        self.array = array
        self.highlight = highlight
        self.update()

    def paintEvent(self, event):
        if not self.array:
            return
        painter = QtGui.QPainter(self)
        rect = self.contentsRect()
        x0, y0 = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        n = len(self.array)
        bar_w = w / n
        max_val = max(self.array)
        for i, value in enumerate(self.array):
            bar_h = value / max_val * h
            color =  QtGui.QColor("#ffffff" if i in self.highlight else "#4caf50")
            gap = 1 if bar_w > 4 else 0
            painter.fillRect(QtCore.QRectF(x0 + i * bar_w, y0 + h - bar_h, bar_w - gap, bar_h), color)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("XSort")
        self.resize(1280, 720)
        self.setMinimumSize(1280, 720)

        navbar = QtWidgets.QToolBar()
        navbar.setMovable(False)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QToolBar {
                background-color: #3c3f41;
                border-bottom: 1px solid #323232;
                spacing: 0.5em;
                padding: 1em;
            }
            QLabel {
                color: #a9b7c6;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 16px;
                font-weight: 500;
            }
            QLineEdit, QComboBox {
                background-color: #2b2b2b;
                color: #a9b7c6;
                font-size: 14px;
                border: 1px solid #646464;
                border-radius: 4px;
                padding: 4px 8px;
                selection-background-color: #214283;
                selection-color: #ffffff;
                min-width: 70px;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #3598ff;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 0px;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QComboBox QAbstractItemView {
                background-color: #3c3f41;
                color: #a9b7c6;
                font-size: 16px;
                selection-background-color: #2f3235;
                selection-color: #ffffff;
                border: 1px solid #646464;
            }
            QPushButton#Start {
                background-color: #36863c;
                color: #ffffff;
                font-size: 16px;
                letter-spacing: 1px;
                border: 1px solid #2e7233;
                border-radius: 4px;
                padding: 5px 16px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QPushButton#Start:hover {
                background-color: #3f9a46;
            }
            QPushButton#Start:pressed {
                background-color: #2b6830;
            }
            QPushButton#Reset {
                background-color: #b33939;
                color: #ffffff;
                font-size: 16px;
                border: 1px solid #8a2b2b;
                border-radius: 4px;
                padding: 5px 16px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QPushButton#Reset:hover {
                background-color: #c44545;
            }
            QPushButton#Reset:pressed {
                background-color: #922b2b;
            }
        """)
        self.addToolBar(navbar)

        navbar.addWidget(QtWidgets.QLabel("Array Size:"))
        self.arr_size_input = QtWidgets.QComboBox()
        sizes = [str(x) for x in range(10, 100, 10)] + [str(x) for x in range(100, 1001, 100)]
        for size in sizes:
            self.arr_size_input.addItem(str(size), size)
        self.arr_size_input.setCurrentIndex(4)
        navbar.addWidget(self.arr_size_input)

        navbar.addWidget(QtWidgets.QLabel("Delay Time:"))
        self.delay_time_input = QtWidgets.QComboBox()
        delays = [1, 5, 10, 20, 50, 100]
        for delay in delays:
            self.delay_time_input.addItem(str(delay) + "ms", delay)
        self.delay_time_input.setCurrentIndex(0)
        navbar.addWidget(self.delay_time_input)

        navbar.addWidget(QtWidgets.QLabel("Shuffling Style:"))
        self.shuffling_input = QtWidgets.QComboBox()
        self.shuffling_input.addItems(["Acceding", "Decreasing", "Randomized"])
        self.shuffling_input.setCurrentIndex(2)
        navbar.addWidget(self.shuffling_input)

        self.seed_input = QtWidgets.QLineEdit()
        self.seed_input.setPlaceholderText("Seed")
        self.seed_input.setValidator(QtGui.QIntValidator())
        self.seed_input.setFixedWidth(80)
        navbar.addWidget(self.seed_input)

        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        navbar.addWidget(spacer)

        navbar.addWidget(QtWidgets.QLabel("Algorithm:"))
        self.sorting_type_input = QtWidgets.QComboBox()
        self.sorting_type_input.addItems(["Selection Sort", "Insertion Sort", "Bubble Sort"])
        navbar.addWidget(self.sorting_type_input)

        navbar.addSeparator()

        self.start_btn = QtWidgets.QPushButton("Start")
        self.start_btn.setObjectName("Start")
        self.start_btn.clicked.connect(self.on_toggle_action)
        navbar.addWidget(self.start_btn)

        self.canvas = BarCanvas()
        self.setCentralWidget(self.canvas)

        self.array = []
        self.steps = None
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.on_tick)

        self.generate_array()

        self.arr_size_input.currentIndexChanged.connect(self.generate_array)
        self.shuffling_input.currentIndexChanged.connect(self.generate_array)
        self.seed_input.textChanged.connect(self.generate_array)

    def set_running(self, running):
        name = "Reset" if running else "Start"
        self.start_btn.setText(name)
        self.start_btn.setObjectName(name)
        self.refresh_stylesheet(self.start_btn)
        for w in (self.arr_size_input, self.delay_time_input, self.shuffling_input,
                  self.seed_input, self.sorting_type_input):
            w.setEnabled(not running)

    def generate_array(self):
        array_size = int(self.arr_size_input.currentData())
        shuffling_style = self.shuffling_input.currentText()
        try:
            seed = int(self.seed_input.text().strip())
        except ValueError:
            seed = None

        self.array = XSort.make_array(array_size, shuffling_style, seed)
        self.canvas.build(self.array)

    def on_toggle_action(self):
        if self.start_btn.text() == "Start":
            self.start_sort()
        else:
            self.reset_sort()

    def start_sort(self):
        algorithm = self.sorting_type_input.currentText()
        delay_time = int(self.delay_time_input.currentData())

        self.steps = XSort.ALGORITHMS[algorithm](self.array)
        self.set_running(True)
        self.timer.start(delay_time)

    def reset_sort(self):
        self.timer.stop()
        self.steps = None
        self.set_running(False)
        self.generate_array()


    def on_tick(self):
        try:
            highlight = next(self.steps)
        except StopIteration:
            self.timer.stop()
            self.canvas.build(self.array)
            return
        self.canvas.build(self.array, highlight)

    def refresh_stylesheet(self, widget):
        widget.style().unpolish(widget)
        widget.style().polish(widget)


