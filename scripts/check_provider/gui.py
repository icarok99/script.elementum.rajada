
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import center, pyqtSlot
from PyQt5.QtGui import QBrush, QColor

from search import make_rules, test_all_providers, test_site, read_json, sim_min, sim_mid, sim_max

class SearchApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        # Create a search input text
        layout.addWidget(QLabel("Query", self))
        self.search_input = QLineEdit("avatar", self)
        layout.addWidget(self.search_input)

        layout.addWidget(QLabel("Site", self))
        self.site = QLineEdit("https://www.cinetorrent.com.br/search?q=QUERY", self)
        layout.addWidget(self.site)
		
        layout.addWidget(QLabel("Pattern Eval", self))
        self.pattern_input = QLineEdit("make_rules('b',2,'article', \"'blog-post'\",2)", self)
        layout.addWidget(self.pattern_input)

        # Create a search button
        self.search_button = QPushButton('Search', self)
        layout.addWidget(self.search_button)
        self.search_button.clicked.connect(self.on_search)

		# Create a search all button
        self.search_button_all = QPushButton('Search all', self)
        layout.addWidget(self.search_button_all)
        self.search_button_all.clicked.connect(self.on_search_all)

        # Create a table with columns
        self.table = QTableWidget(self)
        self.table.setColumnCount(3)  # Three columns
        self.table.setHorizontalHeaderLabels(['Column 1', 'Column 2', 'Column 3'])
        layout.addWidget(self.table)

        self.central_widget.setLayout(layout)

    @pyqtSlot()
    def on_search(self):
        # This is a placeholder for search functionality.
        q = self.search_input.text()
        search_text = self.site.text().replace('QUERY', q)

        # You can implement your search logic here.
        # For demonstration purposes, let's populate the table with some data.
        #self.populate_table()

        print('pp from gui')
        pp = eval(self.pattern_input.text())
        print(pp)

        print('data from gui')
        data = test_site(q, search_text, pp['parsing_name'], pp['parsing_row'], pp['parsing_torrent'], False)

        self.feed_table(data)
		
        

    @pyqtSlot()
    def on_search_all(self):
        q = self.search_input.text()
        for data in list(test_all_providers(q, read_json(), 10)):
            #print('yield', data)
            self.feed_table(data)

    def feed_table(self, data, clear = True):
        # Placeholder data for demonstration
        #data = [
        #    ['Data 1', 'Info 1', 'Detail 1'],
        #    ['Data 2', 'Info 2', 'Detail 2'],
        #    ['Data 3', 'Info 3', 'Detail 3']
        #]

        if clear: self.table.clear()
        self.table.setRowCount(len(data))
        self.table.setColumnCount(5)

        for row, row_data in enumerate(data):
            for col, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                #if col == 2 and float(cell_data) < sim_min: item.setForeground(QBrush(QColor(255, 255, 0)))
                if col == 2 and float(cell_data) >= sim_min and float(cell_data) < sim_mid: item.setForeground(QBrush(QColor(255, 0, 0)))
                if col == 2 and float(cell_data) >= sim_mid and float(cell_data) < sim_max: item.setForeground(QBrush(QColor(0, 0, 255)))
                if col == 2 and float(cell_data) >= sim_max: item.setForeground(QBrush(QColor(0, 255, 0)))
                self.table.setItem(row, col, item)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.update()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = SearchApp()
	window.setWindowTitle('Search Application')
	window.setGeometry(100, 100, 1600, 800)
	window.show()
	sys.exit(app.exec_())
