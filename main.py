from UI import *
from database import Database
database1=Database()
database1.connect('library.db')
app = QApplication([])
app.setWindowIcon(QIcon('./resources/logo.jpg'))
stats = Stats(database1.conn)
stats.ui_star.show()
app.exec_()
