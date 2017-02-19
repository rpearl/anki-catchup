from aqt import mw
from aqt.qt import *

# list of functions that this exposes:

#1) suspend all overdue cards (tag them)
#2) unsuspend oldest n days

#configuration
#
# chosen tag for overdue cards controlled by this app

class CatchupSettings(QDialog):
    def append_config(self, label, control, small=False):
        self._num_lines += 1
        width = 1 if small else 2
        self.grid.addWidget(QLabel(label), self._num_lines, 0, 1, 1)
        self.grid.addWidget(      control, self._num_lines, 1, 1, width)
        return control

    def add_rule(self, start=0, width=3):
        frame = QFrame()
        frame.setFrameShape(QFrame.HLine)
        frame.setFrameShadow(QFrame.Sunken)
        self._num_lines += 1
        self.grid.addWidget(frame, self._num_lines, start, 1, width)

    def add_empty(self):
        self.add_label("")

    def add_widget(self, control, left=True, small=False):
        start = 0 if left else 1
        width = 1 if small else 3-start
        self._num_lines += 1
        self.grid.addWidget(control, self._num_lines, start, 1, width)
        return control

    def add_label(self, label):
        ql = QLabel(label)
        font = QFont()
        font.setBold(True)
        ql.setFont(font)
        return self.add_widget(ql)

    def on_accept(self):
        config = mw.col.conf.setdefault('catchup', dict())
        config['query'] = self.ctl_query.currentText()
        config['tag'] = self.ctl_tag.currentText()
        mw.col.setMod()
        mw.reset()

    def on_reject(self):
        config = mw.col.conf.setdefault('catchup', dict())
        self.ctl_query.setText(config.get('query', ''))
        self.ctl_tag.setText(config.get('tag', ''))
        mw.reset()

    def __init__(self):
        QDialog.__init__(self, parent=mw)
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self._num_lines = 0

        self.add_label("Settings")
        self.ctl_query   = self.append_config("Cards to ignore (search query)", QLineEdit())
        self.ctl_tag     = self.append_config("Catchup tag", QLineEdit())
        self.add_empty()
        self.ctl_numdays = self.append_config("Number of days to unsuspend", QSpinBox(), small=True)

        settings_apply = QDialogButtonBox(QDialogButtonBox.Apply | QDialogButtonBox.Reset)
        self.add_widget(settings_apply, left=False)
        settings_apply.accepted.connect(self.on_accept)
        settings_apply.rejected.connect(self.on_reject)

        self.add_rule()

        self.add_label("Actions")
        ctl_suspend = self.add_widget(QPushButton("Suspend overdue cards"), small=True)
        ctl_unsuspend = self.add_widget(QPushButton("Unsuspend oldest cards"), small=True)

        layout_main = QVBoxLayout()
        layout_main.addLayout(self.grid)

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
