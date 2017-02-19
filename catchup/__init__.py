from aqt import mw
from aqt.qt import *

# list of functions that this exposes:

#1) suspend all overdue cards (tag them)
#2) unsuspend oldest n days

#configuration
# 
# chosen tag for overdue cards controlled by this app
# list of tags to ignore

class CatchupSettings(QDialog):
    def __init__(self):
        QDialog.__init__(self, parent=mw)
        grid = QGridLayout()
        grid.setSpacing(10)


        lbl_numdays = QLabel("Number of days to unsuspend")
        ctl_numdays = QSpinBox()
        grid.addWidget(lbl_numdays, 1, 0, 1, 1)
        grid.addWidget(ctl_numdays, 1, 1, 1, 2)

        lbl_tag = QLabel("Catchup tag")
        ctl_tag = QLineEdit()
        grid.addWidget(lbl_tag, 2, 0, 1, 1)
        grid.addWidget(ctl_tag, 2, 1, 1, 2)

        lbl_query = QLabel("Cards to ignore (search query)")
        ctl_query = QLineEdit()
        grid.addWidget(lbl_query, 3, 0, 1, 1)
        grid.addWidget(ctl_query, 3, 1, 1, 2)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout_main = QVBoxLayout()
        layout_main.addLayout(grid)
        layout_main.addWidget(button_box)

        self.setLayout(layout_main)
        self.setMinimumWidth(512)
        self.setWindowTitle('Catchup Settings')

def on_catchup_settings():
    dialog = CatchupSettings()
    dialog.exec_()

def main():
    action = QAction("&Catchup Settings", mw)
    action.triggered.connect(on_catchup_settings)
    mw.form.menuTools.addAction(action)
