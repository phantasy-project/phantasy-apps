from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget
from phantasy_apps.diag_viewer.ui.ui_device_selection import Ui_Form
from phantasy import build_element


class DeviceSelectionWidget(QWidget, Ui_Form):

    pv_elems_selected = pyqtSignal(list)

    def __init__(self, parent=None):
        super(DeviceSelectionWidget, self).__init__()
        self.parent = parent

        self.setupUi(self)
        self.setWindowTitle("Select Devices")

        self._post_init()

    def _post_init(self):
        self._pvlist = []

    @pyqtSlot()
    def on_add_pv(self):
        # add pv to list
        pv = self.pv_lineEdit.text()
        if pv == '' or pv in self._pvlist:
            return
        print(f"Add {pv} into list")
        self.pv_textEdit.append(pv)
        self._pvlist.append(pv)

    @pyqtSlot()
    def on_del_pv(self):
        # delete pv fro list
        pv = self.pv_lineEdit.text()
        if pv == '':
            return
        print(f"Delete {pv} from list")
        if pv in self._pvlist:
            self._pvlist.remove(pv)
            self.pv_textEdit.clear()
            for i in self._pvlist:
                self.pv_textEdit.append(i)

    @pyqtSlot()
    def on_clear_all_pv(self):
        self.pv_textEdit.clear()
        self._pvlist = []

    @pyqtSlot()
    def on_exit(self):
        self.close()

    @pyqtSlot()
    def on_apply(self):
        # apply pv list as elements
        #for i in self._pvlist:
        #    print(i)
        elem_list = [build_element(pv, pv) for pv in self._pvlist]
        if elem_list:
            self.pv_elems_selected.emit(elem_list)

    @pyqtSlot()
    def on_selection_changed(self):
        cursor = self.sender().textCursor()
        sel = cursor.selection()
        if sel.isEmpty():
            return
        text = sel.toPlainText()
        self.pv_lineEdit.setText(text.strip())

    @pyqtSlot()
    def on_pvlist_changed(self):
        doc = self.pv_textEdit.document()
        if doc.isEmpty():
            cnt = 0
        else:
            cnt = doc.lineCount()
        self.pv_cnt_lbl.setText(str(cnt))


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    w = DeviceSelectionWidget()
    w.show()
    sys.exit(app.exec_())
