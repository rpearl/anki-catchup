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
    def add_labeled_widget(self, label, control, small=False):
        if not isinstance(label, QLabel):
            label = QLabel(label)
        self._num_lines += 1
        width = 1 if small else 2
        self.grid.addWidget(  label, self._num_lines, 0, 1, 1)
        self.grid.addWidget(control, self._num_lines, 1, 1, width)
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
                'unsuspend_query': '',
                'tag': 'catchup',
                'numdays': 1,
                'show_stats': False,
            }
            mw.col.setMod()
            mw.reset()

    def display_conf(self):
        config = mw.col.conf['catchup']
        self.ctl_query.setText(config['query'])
        self.ctl_tag.setText(config['tag'])
        self.ctl_numdays.setValue(config['numdays'])
        self.ctl_unsuspend_query.setText(config['unsuspend_query'])
        self.ctl_show_stats.setChecked(config['show_stats'])

    def on_accept(self):
        if not self.ctl_tag.text():
            showInfo('You must specify a tag')
            return
        config = mw.col.conf['catchup']

        old_tag = config['tag']

        config['query'] = self.ctl_query.text()
        config['unsuspend_query'] = self.ctl_unsuspend_query.text()
        config['tag'] = self.ctl_tag.text()
        config['numdays'] = self.ctl_numdays.value()
        config['show_stats'] = self.ctl_show_stats.isChecked()

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
            query += ' (%s)' % (config['query'])

        cids = mw.col.findCards(query)
        for cid in cids:
            card = mw.col.getCard(cid)
            note = card.note()
            note.addTag(config['tag'])
            note.flush()
        mw.col.sched.suspendCards(cids)
        self.update_stats()
        showInfo('%d cards suspended' % len(cids))

    def get_tagged_cids(self, query=None):
        config = mw.col.conf['catchup']
        find_query = 'tag:%s is:suspended' % (config['tag'],)
        if query:
            find_query += ' (%s)' % (query,)
        cids = mw.col.findCards(find_query, order='c.type, c.due')

        return cids

    def _fixup_tags(self, unsuspended):
        config = mw.col.conf['catchup']
        cids = self.get_tagged_cids()
        for cid in cids:
            if cid in unsuspended:
                continue
            card = mw.col.getCard(cid)
            note = card.note()
            note.addTag(config['tag'])
            note.flush()

    def do_unsuspend(self):
        config = mw.col.conf['catchup']

        query = '-is:new '+config['unsuspend_query']

        cids = self.get_tagged_cids(query=query)

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

        self._fixup_tags(unsuspended)

        self.update_stats()
        showInfo('%d cards unsuspended' % len(unsuspended))

    def do_unsuspend_new(self):
        config = mw.col.conf['catchup']
        cids = self.get_tagged_cids(query='is:new')
        unsuspended = []
        for cid in cids:
            card = mw.col.getCard(cid)
            note = card.note()
            note.delTag(config['tag'])
            note.flush()
            unsuspended.append(cid)
        mw.col.sched.unsuspendCards(unsuspended)
        self._fixup_tags(unsuspended)

        self.update_stats()
        showInfo('%d cards unsuspended' % len(unsuspended))


    def set_dirty_config(self):
        self.ctl_suspend.setEnabled(False)
        self.ctl_unsuspend.setEnabled(False)

    def set_clean_config(self):
        self.ctl_suspend.setEnabled(True)
        self.ctl_unsuspend.setEnabled(True)

    def toggle_stats(self):
        config = mw.col.conf['catchup']
        config['show_stats'] = self.ctl_show_stats.isChecked()
        mw.col.setMod()
        mw.reset()
        self.update_stats()

    def update_stats(self):
        config = mw.col.conf['catchup']
        if config['show_stats']:
            days = set()

            all_cids = self.get_tagged_cids()
            new_behind = 0

            for cid in all_cids:
                card = mw.col.getCard(cid)
                if card.type == 2: # review
                    days.add(card.due)
                else:
                    new_behind += 1
            total_behind = len(all_cids)
            review_behind = total_behind - new_behind
            self.days_behind_label.setText("Days behind")
            self.days_behind.setText("%d" % len(days))
            self.cards_behind_label.setText("Cards behind")
            self.cards_behind.setText("New/Learn: %d\t In review: %d\t Total %d" %
                (new_behind, review_behind, total_behind)
            )
        else:
            self.days_behind_label.setText("Intentionally left blank")
            self.days_behind.setText("")
            self.cards_behind_label.setText("")
            self.cards_behind.setText("")

    def __init__(self):
        QDialog.__init__(self, parent=mw)
        self.load_conf()
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self._num_lines = 0

        self.add_label("Settings")
        self.ctl_query   = self.add_labeled_widget("Suspend filter", QLineEdit())
        self.ctl_tag     = self.add_labeled_widget("Catchup tag", QLineEdit())
        self.add_empty()
        self.ctl_unsuspend_query = self.add_labeled_widget("Unsuspend filter", QLineEdit())
        self.ctl_numdays = self.add_labeled_widget("Number of days to unsuspend", QSpinBox(), small=True)
        self.add_empty()
        self.ctl_show_stats = self.add_labeled_widget('Show stats', QCheckBox())

        settings_apply = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.add_widget(settings_apply, left=False)
        settings_apply.accepted.connect(self.on_accept)
        settings_apply.rejected.connect(self.on_reject)

        self.add_rule()
        self.stats_label = self.add_label("Stats")

        self.days_behind_label = QLabel("Days behind")
        self.cards_behind_label = QLabel("Cards behind")

        self.days_behind  = self.add_labeled_widget(self.days_behind_label, QLabel(""))
        self.cards_behind = self.add_labeled_widget(self.cards_behind_label, QLabel(""))
        self.update_stats()

        self.add_rule()

        self.add_label("Actions")
        self.ctl_suspend = self.add_widget(QPushButton("Suspend overdue cards"), small=True)
        self.ctl_unsuspend = self.add_widget(QPushButton("Unsuspend earliest cards"), small=True)
        self.ctl_unsuspend_new = self.add_widget(QPushButton("Unsuspend new/learning cards"), small=True)

        self.ctl_suspend.clicked.connect(self.do_suspend)
        self.ctl_unsuspend.clicked.connect(self.do_unsuspend)
        self.ctl_unsuspend_new.clicked.connect(self.do_unsuspend_new)

        self.add_rule()
        self.add_widget(QLabel('Check the README for instructions and examples'))


        layout_main = QVBoxLayout()
        layout_main.addLayout(self.grid)

        self.display_conf()

        self.ctl_query.textEdited.connect(self.set_dirty_config)
        self.ctl_unsuspend_query.textEdited.connect(self.set_dirty_config)
        self.ctl_tag.textEdited.connect(self.set_dirty_config)
        self.ctl_numdays.valueChanged.connect(self.set_dirty_config)

        self.ctl_show_stats.stateChanged.connect(self.toggle_stats)

        self.setLayout(layout_main)
        self.setMinimumWidth(512)
        self.setWindowTitle('CatchUp')

def on_catchup_settings():
    dialog = CatchupSettings()
    dialog.exec_()

def main():
    action = QAction("&CatchUp", mw)
    action.triggered.connect(on_catchup_settings)
    mw.form.menuTools.addAction(action)
