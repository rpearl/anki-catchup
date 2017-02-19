from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo

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

    def load_conf(self):
        if 'catchup' not in mw.col.conf:
            mw.col.conf['catchup'] = {
                'query': '',
                'tag': 'catchup',
                'numdays': 1
            }
            mw.col.setMod()
            mw.reset()

    def display_conf(self):
        config = mw.col.conf['catchup']
        self.ctl_query.setText(config['query'])
        self.ctl_tag.setText(config['tag'])
        self.ctl_numdays.setValue(config['numdays'])

    def on_accept(self):
        if not self.ctl_tag.text():
            showInfo('You must specify a tag')
            return
        config = mw.col.conf['catchup']

        old_tag = config['tag']

        config['query'] = self.ctl_query.text()
        config['tag'] = self.ctl_tag.text()
        config['numdays'] = self.ctl_numdays.value()

        cids = mw.col.findCards('tag:%s' % (old_tag,))
        for cid in cids:
            card = mw.col.getCard(cid)
            note = card.note()
            note.delTag(old_tag)
            note.addTag(config['tag'])
            note.flush()

        mw.col.setMod()
        mw.reset()
        self.set_clean_config()

    def on_reject(self):
        self.display_conf()
        self.set_clean_config()
        mw.reset()

    def do_suspend(self):
        config = mw.col.conf['catchup']
        query = 'is:due'
        if config['query']:
            query += ' -(%s)' % (config['query'])

        cids = mw.col.findCards(query)
        for cid in cids:
            card = mw.col.getCard(cid)
            note = card.note()
            note.addTag(config['tag'])
            note.flush()
        mw.col.sched.suspendCards(cids)
        self.update_stats()
        showInfo('%d cards suspended' % len(cids))

    def get_tagged_cids(self):
        config = mw.col.conf['catchup']
        cids = mw.col.findCards('tag:%s' % config['tag'], order='c.type, c.due')

        return cids

    def do_unsuspend(self):
        config = mw.col.conf['catchup']

        cids = self.get_tagged_cids()

        unsuspended = []

        days = set()

        for cid in cids:
            card = mw.col.getCard(cid)
            days.add(card.due)
            if len(days) > config['numdays']:
                break
            note = card.note()
            note.delTag(config['tag'])
            note.flush()
            unsuspended.append(cid)
        mw.col.sched.unsuspendCards(unsuspended)
        self.update_stats()
        showInfo('%d cards unsuspended' % len(unsuspended))

    def set_dirty_config(self):
        self.ctl_suspend.setEnabled(False)
        self.ctl_unsuspend.setEnabled(False)

    def set_clean_config(self):
        self.ctl_suspend.setEnabled(True)
        self.ctl_unsuspend.setEnabled(True)

    def update_stats(self):
        days = set()

        cids = self.get_tagged_cids()

        for cid in cids:
            card = mw.col.getCard(cid)
            days.add(card.due)

        self.days_behind.setText("%d" % len(days))
        self.cards_behind.setText("%d" % len(cids))

    def __init__(self):
        QDialog.__init__(self, parent=mw)
        self.load_conf()
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self._num_lines = 0

        self.add_label("Settings")
        self.ctl_query   = self.append_config("Cards to ignore (search query)", QLineEdit())
        self.ctl_tag     = self.append_config("Catchup tag", QLineEdit())
        self.add_empty()
        self.ctl_numdays = self.append_config("Number of days to unsuspend", QSpinBox(), small=True)


        self.display_conf()

        settings_apply = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.add_widget(settings_apply, left=False)
        settings_apply.accepted.connect(self.on_accept)
        settings_apply.rejected.connect(self.on_reject)

        self.add_rule()
        self.add_label("Stats")

        self.days_behind = self.append_config("Days behind", QLabel(""))
        self.cards_behind = self.append_config("Cards behind", QLabel(""))
        self.update_stats()

        self.add_rule()

        self.add_label("Actions")
        self.ctl_suspend = self.add_widget(QPushButton("Suspend overdue cards"), small=True)
        self.ctl_unsuspend = self.add_widget(QPushButton("Unsuspend oldest cards"), small=True)

        self.ctl_suspend.clicked.connect(self.do_suspend)
        self.ctl_unsuspend.clicked.connect(self.do_unsuspend)


        layout_main = QVBoxLayout()
        layout_main.addLayout(self.grid)

        self.ctl_query.textEdited.connect(self.set_dirty_config)
        self.ctl_tag.textEdited.connect(self.set_dirty_config)
        self.ctl_numdays.valueChanged.connect(self.set_dirty_config)

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
