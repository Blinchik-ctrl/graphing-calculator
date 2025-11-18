import sys
import numpy as np
from PyQt6.QtWidgets import *
import pyqtgraph as pg
from math import *


class FunctionWidget(QWidget):
    def __init__(self, color, on_change, on_remove):
        super().__init__()

        self.color = color

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(QLabel("y ="))

        self.color_label = QLabel("█")
        self.color_label.setStyleSheet(f"color: {color}; font-size: 20px;")
        layout.addWidget(self.color_label)

        self.input = QLineEdit()
        self.input.setPlaceholderText("например: x**2")
        self.input.textChanged.connect(on_change)
        layout.addWidget(self.input)

        btn_remove = QPushButton("✕")
        btn_remove.setMaximumWidth(30)
        btn_remove.clicked.connect(on_remove)
        layout.addWidget(btn_remove)

        self.setLayout(layout)


class Graficator(QWidget):
    def __init__(self):
        super().__init__()

        self.colors = ['#0000FF', '#FF0000', '#00AA00', '#FF8800', '#AA00FF',
                       '#00AAAA', '#FF00FF', '#808000', '#008080', '#800080']
        self.function_widgets = []

        main_layout = QHBoxLayout()

        left_panel = QVBoxLayout()
        left_panel.addWidget(QLabel("Функции:"))

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMaximumWidth(350)
        scroll.setMinimumWidth(300)

        scroll_content = QWidget()
        self.functions_layout = QVBoxLayout(scroll_content)
        self.functions_layout.addStretch()
        scroll.setWidget(scroll_content)

        left_panel.addWidget(scroll)

        btn_add = QPushButton("+ Добавить функцию")
        btn_add.clicked.connect(self.add_function)
        left_panel.addWidget(btn_add)

        main_layout.addLayout(left_panel)

        right_panel = QVBoxLayout()

        self.graph = pg.PlotWidget()
        self.graph.showGrid(x=True, y=True)
        self.graph.setBackground('w')
        self.graph.setLabel('left', 'y')
        self.graph.setLabel('bottom', 'x')
        self.graph.setAspectLocked(False)

        self.graph.setMouseEnabled(x=True, y=True)
        self.graph.getViewBox().setMouseMode(pg.ViewBox.PanMode)
        self.graph.wheelEvent = lambda event: None

        right_panel.addWidget(self.graph)

        buttons = QHBoxLayout()
        buttons.addStretch()

        btn_zoom_in = QPushButton("Zoom In")
        btn_zoom_in.clicked.connect(self.zoom_in)
        buttons.addWidget(btn_zoom_in)

        btn_zoom_out = QPushButton("Zoom Out")
        btn_zoom_out.clicked.connect(self.zoom_out)
        buttons.addWidget(btn_zoom_out)

        btn_center = QPushButton("Центрировать")
        btn_center.clicked.connect(self.center_view)
        buttons.addWidget(btn_center)

        btn_clear = QPushButton("Очистить всё")
        btn_clear.clicked.connect(self.clear_all)
        buttons.addWidget(btn_clear)

        buttons.addStretch()
        right_panel.addLayout(buttons)

        main_layout.addLayout(right_panel, 1)
        self.setLayout(main_layout)
        self.setWindowTitle("Графический калькулятор")
        self.resize(1200, 700)

        self.add_function()
        self.function_widgets[0].input.setText("x**2")
        self.graph.setXRange(-50, 50)
        self.graph.setYRange(-50, 50)

    def add_function(self):
        color = self.colors[len(self.function_widgets) % len(self.colors)]
        widget = FunctionWidget(color, self.update_graphs, lambda: self.remove_function(widget))
        self.function_widgets.append(widget)
        self.functions_layout.insertWidget(len(self.function_widgets) - 1, widget)
        self.update_graphs()

    def remove_function(self, widget):
        if len(self.function_widgets) > 1:
            self.function_widgets.remove(widget)
            widget.deleteLater()
            self.update_graphs()

    def update_graphs(self):
        self.graph.clear()

        x_vals = np.linspace(-500, 500, 20000)

        for widget in self.function_widgets:
            func_text = widget.input.text().strip()
            if not func_text:
                continue

            y_vals = []
            for x in x_vals:
                try:
                    y_vals.append(eval(func_text))
                except:
                    y_vals.append(np.nan)

            pen = pg.mkPen(color=widget.color, width=2)
            self.graph.plot(x_vals, y_vals, pen=pen, name=func_text[:30])

        self.graph.addLegend(offset=(10, 10))

    def zoom_in(self):
        view = self.graph.getViewBox()
        current_range = view.viewRange()
        x_range = current_range[0][1] - current_range[0][0]

        if x_range * 0.8 > 2:
            view.scaleBy(x=0.8, y=0.8)

    def zoom_out(self):
        view = self.graph.getViewBox()
        current_range = view.viewRange()
        x_range = current_range[0][1] - current_range[0][0]

        if x_range * 1.25 < 1000:
            view.scaleBy(x=1.25, y=1.25)

    def center_view(self):
        self.graph.setXRange(-50, 50)
        self.graph.setYRange(-50, 50)

    def clear_all(self):
        for widget in self.function_widgets[1:]:
            widget.deleteLater()
        self.function_widgets = [self.function_widgets[0]]
        self.function_widgets[0].input.clear()
        self.graph.clear()
        self.center_view()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Graficator()
    window.show()
    sys.exit(app.exec())