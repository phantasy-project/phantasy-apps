#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os
import pandas as pd
from datetime import datetime

from PyQt5.QtWidgets import (
    QWidget,
    QMessageBox,
    QLayout,
    QScrollArea,
)

from PyQt5.QtCore import (
    pyqtSlot,
    QTimer,
    Qt,
    QDate,
    QDateTime,
    QModelIndex,
)

from PyQt5.QtGui import (
    QFont,
    QFontDatabase,
    QPixmap,
    QFontMetrics,
)

from phantasy_ui import delayed_exec
from phantasy_ui import get_open_filename
from phantasy_apps.threshold_manager.ui.ui_mps_diag import Ui_Form as MPSDiagWidgetForm
from phantasy_apps.threshold_manager.ui.ui_snp_widget import Ui_Form as SnapshotWidgetForm
from phantasy_apps.threshold_manager._mps_model import MPSBeamLossDataModel
from phantasy_apps.threshold_manager._mps_model import MPSBeamLossDataDelegateModel
from phantasy_apps.threshold_manager._mps_model import SnapshotModel
from phantasy_apps.threshold_manager._mps_model import SnapshotDelegateModel
from phantasy_apps.threshold_manager.db.utils import ensure_connect_db

DEVICE_TYPE_FULLNAME_MAP = {
    'ND': 'Neutron Detector',
    'IC': 'Ionization Chamber',
    'HMR': 'Halo Monitor Ring',
}

NOW_DT = datetime.now()
NOW_YEAR = NOW_DT.year
NOW_MONTH = NOW_DT.month
NOW_DAY = NOW_DT.day


class MPSDiagWidget(QWidget, MPSDiagWidgetForm):

    def __init__(self, device_type: str, outdata_dir: str, parent=None):
        super(self.__class__, self).__init__()
        self.parent = parent

        self.setupUi(self)
        self.device_type = device_type
        self.outdata_dir = outdata_dir
        self.setWindowTitle(
            f"MPS Configurtions: Beam Loss Threshold ({self.device_type})")

        self._post_init()

    def _post_init(self):
        self.diff_help_btn.setVisible(False)
        self._dt_ms = int(1000.0 / self.refresh_rate_dsbox.value())
        self.dtype_lbl.setText(
            '<html><head/><body><p><span style=" font-size:18pt; font-weight:600; color:#0055ff;">{dtype}</span></p></body></html>'
            .format(dtype=DEVICE_TYPE_FULLNAME_MAP[self.device_type]))
        self.view.setItemDelegate(MPSBeamLossDataDelegateModel(self.view))
        self.set_data()
        self.hide_columns()
        delayed_exec(lambda: self.auto_resize_columns(), 2000)

    def hide_columns(self):
        """Hide columns.
        """
        for i in self.__model.get_hidden_columns():
            self.view.setColumnHidden(i, True)

    def set_data(self):
        self.__model = MPSBeamLossDataModel(self.device_type)
        self.view.setModel(self.__model)
        self.__model.dataRefreshStarted.connect(self.onDataRefreshStarted)
        self.__model.dataRefreshStopped.connect(self.onDataRefreshStopped)
        self._r_tmr = QTimer(self)
        self._r_tmr.timeout.connect(self.__model.refresh_data)

    @pyqtSlot()
    def auto_resize_columns(self):
        for c in range(self.view.model().columnCount()):
            self.view.resizeColumnToContents(c)

    @pyqtSlot(bool)
    def refreshData(self, is_checked: bool):
        """Refresh the data model.
        """
        if is_checked:
            self._dt_ms = int(1000.0 / self.refresh_rate_dsbox.value())
            self._r_tmr.start(self._dt_ms)
        else:
            self._r_tmr.stop()
        for _w in (self.refresh_rate_dsbox, ):
            _w.setDisabled(is_checked)

    @pyqtSlot()
    def onDataRefreshStarted(self):
        pass

    @pyqtSlot()
    def onDataRefreshStopped(self):
        self.refresh_sts_lbl.setPixmap(QPixmap(":/tm-icons/active.png"))
        delayed_exec(
            lambda: self.refresh_sts_lbl.setPixmap(
                QPixmap(":/tm-icons/inactive.png")), int(self._dt_ms * 0.6))

    def closeEvent(self, evt):
        self._r_tmr.stop()

    @pyqtSlot()
    def saveData(self):
        """Save data into a file.
        """
        _auto_filename = datetime.now().strftime(
            "%Y%m%dT%H%M%S") + f"_{self.device_type}.csv"
        outfilepath = os.path.join(self.outdata_dir, _auto_filename)
        self.__model.get_dataframe().to_csv(outfilepath, index=False)
        QMessageBox.information(self, "MPS Diagnostics Threshold Configs",
                                f"Saved data to {outfilepath}", QMessageBox.Ok,
                                QMessageBox.Ok)

    @pyqtSlot()
    def compareData(self):
        """Compare data, highlight the differences.
        """
        filepath, ext = get_open_filename(self, type_filter='CSV File (*.csv)')
        if filepath is None:
            return None
        ref_df = pd.read_csv(filepath)

        self.diff_type_lbl.setText(
            '<p><span style="font-weight:600;color:#007BFF;">[FILE]</span></p>'
        )
        _fulltext = f'''<p><span style="font-weight:600;color:#007BFF;">[FILE]</span> {filepath}</p>'''
        _intext = QFontMetrics(self.ref_datafilepath_lbl.font()).elidedText(
            filepath, Qt.ElideRight, self.ref_datafilepath_lbl.width())
        self.ref_datafilepath_lbl.setText(_intext)
        self.ref_datafilepath_lbl.setToolTip(_fulltext)
        self.__model.highlight_diff(ref_df)
        self.diff_help_btn.setVisible(True)

    @pyqtSlot()
    def clearDiff(self):
        """Clear diff.
        """
        self.ref_datafilepath_lbl.clear()
        self.diff_type_lbl.clear()
        self.__model.update_ref_dataframe(None)
        self.diff_help_btn.setVisible(False)

    @pyqtSlot()
    def takeDiff(self):
        """Take a snapshot of current live readings for diff.
        """
        auto_name = datetime.now().strftime(
            "%Y%m%dT%H%M%S") + f"_{self.device_type}"
        self.__model.highlight_diff(self.__model.get_dataframe())
        self.diff_type_lbl.setText(
            '<p><span style="font-weight:600;color:#DC3545;">[MEM]</span></p>')
        _fulltext = f'''<p><span style="font-weight:600;color:#DC3545;">[MEM]</span> {auto_name}</p>'''
        _intext = QFontMetrics(self.ref_datafilepath_lbl.font()).elidedText(
            auto_name, Qt.ElideRight, self.ref_datafilepath_lbl.width())
        self.ref_datafilepath_lbl.setText(_intext)
        self.ref_datafilepath_lbl.setToolTip(_fulltext)
        self.diff_help_btn.setVisible(True)

    @pyqtSlot()
    def onHelpDiffMode(self):
        """Show the help message for diff mode.
        """
        _help_text = '''<html>
        <p>Diff mode is enabled: Colored cells indicate diff from the reference,
        reference could be loaded from saved data ("Load-Diff") or set through
        "Take-Diff".</p>
        <p><span style="color:#28a745;">Green</span> color indicates the live
        reading is lower than the reference; <span style="color:#dc3545;">red</span>
        color is higher, hover on the cell gives the reference reading and the relative
        difference in percentage.</p></html>
        '''
        QMessageBox.information(self, "Diff Mode Help", _help_text,
                                QMessageBox.Ok, QMessageBox.Ok)


TABLE_NAME_MAP = {
    'ND': 'mps_threshold_nd',
    'IC': 'mps_threshold_ic',
    'HMR': 'mps_threshold_hmr',
}


class SnapshotWidget(QWidget, SnapshotWidgetForm):

    def __init__(self, device_type, parent=None):
        super(self.__class__, self).__init__()
        self.parent = parent
        self.device_type = device_type
        self.__table_name = TABLE_NAME_MAP[self.device_type]

        self.setupUi(self)
        self.setWindowTitle("Snapshots of MPS Configurations")

        self.__set_up_post_init_vars()
        self.__set_up_post_init_0()
        self.__set_up_events()
        self.__set_up_post_init_1()

    def __set_up_post_init_vars(self):
        # post initial
        self.__default_font: QFont = QFontDatabase.systemFont(
            QFontDatabase.FixedFont)
        self.__default_font_size: int = self.__default_font.pointSize()
        self.__model: SnapshotModel = None
        self.__db_con: sqlite3.Connection = None
        self.__df: pd.Dataframe = None
        self.__max_init_nitems: int = None
        self.__total_item_cnt: int = 0
        self.__irow: int = 0
        self.__current_tag_filter_dict: dict = dict(
        )  # {tag_name (str): is_checked? (bool)}
        self.__current_ion_filter_dict: dict = dict(
        )  # {ion_name (str): is_checked? (bool)}
        self.__current_user_filter_dict: dict = dict(
        )  # {user (str): is_checked? (bool)}
        self.__user_list: list = None
        self.__ion_list: list = None
        self.__tag_list: list = None
        self.__note_filter_enabled: bool = False
        self.__daterange_filter_enabled: bool = False
        self.__daterange_date1_s: float = None
        self.__daterange_date2_s: float = None

    def __set_up_post_init_0(self):
        # prior events setup
        self.view.setItemDelegate(SnapshotDelegateModel(self.view))
        #
        self.filter_note_lineEdit.setVisible(False)
        [
            o.setVisible(False) for o in (
                self.filter_daterange_dateEdit1,
                self.daterange_lbl,
                self.filter_daterange_dateEdit2,
            )
        ]
        self.filter_daterange_dateEdit1.setDate(
            QDate(NOW_YEAR, NOW_MONTH, NOW_DAY).addMonths(-3))
        self.filter_daterange_dateEdit2.setDate(
            QDate(NOW_YEAR, NOW_MONTH, NOW_DAY))
        __date1 = self.filter_daterange_dateEdit1.date()
        self.__daterange_date1_s = qdate2epochs(__date1)
        self.filter_daterange_dateEdit1.setToolTip(
            f"{__date1.toString()} 00:00:00")
        __date2 = self.filter_daterange_dateEdit2.date()
        self.__daterange_date2_s = qdate2epochs(__date2, True)
        self.filter_daterange_dateEdit2.setToolTip(
            f"{__date2.toString()} 23:59:59")

    def __set_up_events(self):
        #        # note filter
        #        self.filter_note_btn.toggled.connect(
        #            self.filter_note_lineEdit.setVisible)
        #        self.filter_note_lineEdit.returnPressed.connect(self.activate_filters)
        #        # daterange filter
        #        self.filter_daterange_btn.toggled.connect(
        #            self.on_enable_daterange_filter)
        #        self.filter_daterange_dateEdit1.dateChanged.connect(
        #            self.onFilterDateRangeUpdated1)
        #        self.filter_daterange_dateEdit2.dateChanged.connect(
        #            self.onFilterDateRangeUpdated2)
        #        [
        #            self.filter_daterange_btn.toggled.connect(o.setVisible) for o in (
        #                self.filter_daterange_dateEdit1,
        #                self.daterange_lbl,
        #                self.filter_daterange_dateEdit2,
        #            )
        #        ]
        # initial max nitems
        self.init_nitem_sbox.valueChanged.connect(
            self.onInitialMaxNItemsChanged)
        # open db file
        self.db_open_btn.clicked.connect(self.onOpenDatabase)
        #        # check ion/tag filter buttons
        #        self.select_all_ions_btn.clicked.connect(
        #            partial(self.on_check_snp_filters, "ion", "all"))
        #        self.select_none_ions_btn.clicked.connect(
        #            partial(self.on_check_snp_filters, "ion", "none"))
        #        self.select_invert_ions_btn.clicked.connect(
        #            partial(self.on_check_snp_filters, "ion", "invert"))
        #        self.select_all_tags_btn.clicked.connect(
        #            partial(self.on_check_snp_filters, "tag", "all"))
        #        self.select_none_tags_btn.clicked.connect(
        #            partial(self.on_check_snp_filters, "tag", "none"))
        #        self.select_invert_tags_btn.clicked.connect(
        #            partial(self.on_check_snp_filters, "tag", "invert"))
        #        # note filter button
        #        self.filter_note_btn.toggled.connect(self.on_enable_note_filter)

        # dblclick row
        self.view.doubleClicked.connect(self.onDblClickedItem)

    @pyqtSlot()
    def auto_resize_columns(self):
        for c in range(self.view.model().columnCount()):
            self.view.resizeColumnToContents(c)

    def __set_up_post_init_1(self):
        pass

    def hide_columns(self):
        """Hide columns.
        """
        for i in self.__model.get_hidden_columns():
            self.view.setColumnHidden(i, True)

    @pyqtSlot(QModelIndex)
    def onDblClickedItem(self, idx: QModelIndex):
        pass
#        m = self.view.model()
#        item = m.getItem(idx)
#        if isinstance(item, SnapshotItem) and \
#                idx.column() not in (COLUMN_IDX_TAGS, COLUMN_IDX_NOTE):
#            self.onLoadData(item._itemData[-1])
#
#    @pyqtSlot(bool)
#    def on_enable_note_filter(self, is_checked: bool):
#        """Enable note filter if checked.
#        """
#        self.__note_filter_enabled = is_checked
#        self.activate_filters()
#
#    @pyqtSlot(bool)
#    def on_enable_daterange_filter(self, is_checked: bool):
#        """Enable daterange filter if checked.
#        """
#        self.__daterange_filter_enabled = is_checked
#        self.activate_filters()
#
#    @pyqtSlot()
#    def on_check_snp_filters(self, filter_type: Literal['ion', 'tag'],
#                             check_type: Literal['all', 'none', 'invert',
#                                                 'apply']):
#        area = getattr(self, f"{filter_type}_filter_area")
#        _slot = getattr(self, f"on_update_{filter_type}_filters")
#        btn_list = area.findChildren(QToolButton)
#        # rewire slot
#        for btn in btn_list:
#            btn.toggled.disconnect()
#            btn.toggled.connect(partial(_slot, btn.text(), False))
#
#        if check_type == 'all':
#            [i.setChecked(True) for i in btn_list]
#        elif check_type == 'none':
#            [i.setChecked(False) for i in btn_list]
#        elif check_type == 'invert':
#            [i.setChecked(not i.isChecked()) for i in btn_list]
#        else:
#            print(f"Apply {filter_type} filter buttons.")
#
#        # rewire slot
#        for btn in btn_list:
#            btn.toggled.disconnect()
#            btn.toggled.connect(partial(_slot, btn.text(), True))
#        #
#        self.activate_filters()
#
#    def activate_filters(self):
#        # activate filters
#        df = self.filter_dataframe()
#        #
#        self.total_nitem_lbl.setText(f"{df.shape[0]}")
#        self.fetched_nitem_lbl.setText("0")
#        self.__total_item_cnt = 0
#        self.__irow = 0
#        self.__max_init_nitems = self.init_nitem_sbox.value()
#        self.__model.setDataSource(df)
#        self.post_style_view(self.view)
#
#    def filter_dataframe(self):
#        # refresh the internal dataframe as the response of all filter changes.
#        # tag
#        _idx_by_tag = self.__filter_df_by_tag()
#        self.tag_filter_nitem_lbl.setText(f"{_idx_by_tag.size}")
#
#        # ion
#        _idx_by_ion = self.__filter_df_by_ion()
#        self.ion_filter_nitem_lbl.setText(f"{_idx_by_ion.size}")
#
#        idx = _idx_by_tag.intersection(_idx_by_ion)
#
#        # user
#        btn = self.findChild(QToolButton, 'user_filter_btn')
#        if btn is not None and btn.isChecked():
#            _idx_by_user = self.__filter_df_by_user()
#            btn.setToolTip(
#                f"Filter by User, reset when reloading data.\nHit {_idx_by_user.size} snapshots."
#            )
#            idx = idx.intersection(_idx_by_user)
#
#        # note
#        if self.__note_filter_enabled:
#            s = self.filter_note_lineEdit.text()
#            if s != '':
#                _idx_by_note = self.__filter_df_by_note(s)
#                idx = idx.intersection(_idx_by_note)
#
#        # daterange
#        if self.__daterange_filter_enabled:
#            _idx_by_daterange = self.__filter_df_by_daterange()
#            idx = idx.intersection(_idx_by_daterange)
#        #
#        return self.__df.loc[idx].sort_values('timestamp', ascending=False)
#
#    def __filter_df_by_tag(self):
#        checked_tag_list = [
#            f'\\b{k}\\b' for k, v in self.__current_tag_filter_dict.items()
#            if v
#        ]
#        _notag_idx = pd.Int64Index([])
#        if '\\bNOTAG\\b' in checked_tag_list:
#            r = self.__df.tags == ''
#            _notag_idx = r[r].index
#            checked_tag_list.remove('\\bNOTAG\\b')
#        re_str = '|'.join(checked_tag_list)
#        if re_str == '':
#            return pd.Int64Index([]).union(_notag_idx)
#        else:
#            r = self.__df.tags.str.contains(fr'{re_str}', case=False)
#            return r[r].index.union(_notag_idx)
#
#    def __filter_df_by_ion(self):
#        checked_ion_list = [
#            k for k, v in self.__current_ion_filter_dict.items() if v
#        ]
#        re_str = '|'.join(checked_ion_list)
#        if re_str == '':
#            return pd.Int64Index([])
#        else:
#            r = self.__df.ion_name.str.contains(fr'{re_str}', case=False)
#        return r[r].index
#
#    def __filter_df_by_user(self):
#        checked_user_list = [
#            f'\\b{k}\\b' for k, v in self.__current_user_filter_dict.items()
#            if v
#        ]
#        re_str = '|'.join(checked_user_list)
#        if re_str == '':
#            return pd.Int64Index([])
#        else:
#            r = self.__df.user.str.contains(fr'{re_str}', case=False)
#        return r[r].index
#
#    def __filter_df_by_note(self, s: str):
#        r = self.__df.note.str.contains(fr'{s}', case=False)
#        return r[r].index
#
#    def __filter_df_by_daterange(self):
#        r = (self.__df.timestamp >= self.__daterange_date1_s) & \
#                (self.__df.timestamp <= self.__daterange_date2_s)
#        return r[r].index
#

    @pyqtSlot(int)
    def onInitialMaxNItemsChanged(self, i: int):
        # Max initial number of SnapshotItems is changed.
        self.__max_init_nitems = i

    @pyqtSlot()
    def onOpenDatabase(self):
        ## Open and read data from a database file.
        # 1. Read data from a database file as a dataframe
        # 2. Update the model and view
        ##
        # close the existing db connection if any
        if self.__db_con is not None:
            self.__db_con.close()
        # get the database file path
        _db_path = self.db_path_lineEdit.text()
        # self.__df, self.__db_con = read_dataframe(_db_path)
        self.__db_con = ensure_connect_db(_db_path)
        if self.__model is None:
            self.__initial_model()
        else:
            self.__refresh_model()


#        t0 = time.perf_counter()
#        # Update tag/ion filter
#        self.__ion_list = self.__get_ion_list()
#        self.__tag_list = self.__get_tag_list()
#        self.__user_list = self.__get_user_list()
#        self.__build_tag_filter_btns(self.tag_filter_area, self.__tag_list)
#        self.__build_ion_filter_btns(self.ion_filter_area, self.__ion_list)
#        self.__build_user_filter_btns(self.user_filter_hbox, self.__user_list)
#        print(f"Building filter buttons: {time.perf_counter() - t0:.1f}s")

#        # apply ion/tag filter buttons
#        self.on_check_snp_filters('ion', 'apply')
#        self.on_check_snp_filters('tag', 'apply')

    def __get_tag_list(self):
        # Return a list of sorted unique tag list, replace empty to 'NOTAG'.
        _a = sorted(
            set(','.join(self.__df.tags.str.upper().unique()).split(',')))
        if '' in _a:
            return ['NOTAG'] + _a[1:]
        else:
            return _a

    def __get_ion_list(self):
        # Return a list of sorted unique ion name list, put NAN to the end if any
        return sorted(self.__df.ion_name.unique(), key=lambda i: sym2z(i))

    def __get_user_list(self):
        # Return a list of sorted unique user list
        return sorted(self.__df.user.unique())

    def __build_user_filter_btns(self, container: QLayout, user_list: list):
        # dropdown menu with checkable user names
        #
        child = container.takeAt(0)
        while child:
            w = child.widget()
            if w is not None:
                w.setParent(None)
            del w
            del child
            child = container.takeAt(0)
        #
        _d = {i: True for i in user_list}

        #
        def _on_update_filter_string(k, btn, is_toggled):
            if k == 'All':  # update checkstates for other actions
                btn.toggled.disconnect()
                for obj in self.sender().parent().findChildren(QCheckBox):
                    obj.setChecked(is_toggled)
                btn.toggled.connect(partial(_on_toggle_filter_btn, btn))
            else:
                _d[k] = is_toggled
                obj = self.sender().parent().findChild(QCheckBox,
                                                       "sel_user_act")
                obj.toggled.disconnect()
                obj.setChecked(all(_d.values()))
                obj.toggled.connect(
                    partial(_on_update_filter_string, 'All', btn))

            btn.setToolTip(
                "Check to enable filtering by {}\nChecked: {}".format(
                    'User', ','.join([k for k, v in _d.items() if v])))
            btn.toggled.emit(btn.isChecked())

        #
        def _on_toggle_filter_btn(btn, is_checked: bool):
            self.__current_user_filter_dict.update(_d)
            if is_checked:
                self.activate_filters()

        def _create_widgetaction(text, parent):
            _chkbox = QCheckBox(text, parent)
            _chkbox.setChecked(True)
            _wa = QWidgetAction(parent)
            _wa.setDefaultWidget(_chkbox)
            _chkbox.setStyleSheet("""QCheckBox{padding-left:10px;}""")
            return _chkbox, _wa

        def _build_actions(btn):
            menu = QMenu(self)
            for i in user_list:
                _chkbox, _wa = _create_widgetaction(i, menu)
                _chkbox.toggled.connect(
                    partial(_on_update_filter_string, i, btn))
                menu.addAction(_wa)
            menu.addSeparator()
            _chkbox_all, _wa_all = _create_widgetaction('All', menu)
            _chkbox_all.setObjectName("sel_user_act")
            _chkbox_all.toggled.connect(
                partial(_on_update_filter_string, 'All', btn))
            menu.addAction(_wa_all)
            btn.setMenu(menu)

        #
        _btn = QToolButton(self)
        _btn.setObjectName('user_filter_btn')
        _btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        _btn.setText("User")
        _btn.setIcon(QIcon(QPixmap(":/sm_icons/icons/person.png")))
        _btn.setIconSize(QSize(ICON_SIZE, ICON_SIZE))
        _btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        _btn.setCheckable(True)
        _btn.setToolTip("Filter by User, reset when reloading data.")
        _btn.setPopupMode(QToolButton.MenuButtonPopup)
        _btn.toggled.connect(partial(_on_toggle_filter_btn, _btn))
        #
        container.addWidget(_btn)
        _build_actions(_btn)

    @pyqtSlot(QDate)
    def onFilterDateRangeUpdated1(self, d: QDate):
        self.__daterange_date1_s = qdate2epochs(d)
        self.sender().setToolTip(f"{d.toString()} 00:00:00")
        if self.__daterange_date1_s < self.__daterange_date2_s:
            self.activate_filters()
        else:
            print("date1 !< date2")

    @pyqtSlot(QDate)
    def onFilterDateRangeUpdated2(self, d: QDate):
        self.__daterange_date2_s = qdate2epochs(d, True)
        self.sender().setToolTip(f"{d.toString()} 23:59:59")
        if self.__daterange_date1_s < self.__daterange_date2_s:
            self.activate_filters()
        else:
            print("date1 !< date2")

    @pyqtSlot(int)
    def onFetchedNItemsChanged(self, i: int):
        self.__total_item_cnt = i
        self.fetched_nitem_lbl.setText(str(i))
        if self.__total_item_cnt < self.__max_init_nitems:
            self.expand_view()

    def onDataChanged(self, tl: QModelIndex, br: QModelIndex, roles: list):
        """The data of SnapshotModel is changed via editting.
        """
        m = self.view.model()
        item = m.getItem(tl)
        column = tl.column()
        column_name = COLUMN_NAME_LIST[column].lower()
        snp_name = item.name  # 'timestamp' in database
        edited_result = item.data(column, Qt.EditRole)

        # update dataframe
        _idx = self.__df[self.__df['timestamp'] == snp_name].index
        val0 = self.__df.loc[_idx, column_name].to_list()[0]
        if edited_result != val0:
            # update only if the new value is different from the current one
            db_update(self.__db_con, snp_name, column_name, edited_result)
            self.__df.loc[_idx, column_name] = edited_result
            print(
                f"Changed '{column_name}' of '{snp_name}' row from {val0} to {edited_result}"
            )

    def post_style_view(self, v):
        self.hide_columns()
        delayed_exec(lambda: self.auto_resize_columns(), 500)
        # style the view after set model.
        #
        # expand the first row
        #if v.model().rowCount(QModelIndex()) == 0:
        #    return
        #[v.resizeColumnToContents(i) for i in range(len(COLUMN_NAME_LIST))]

    def __initial_model(self):
        # self.total_nitem_lbl.setText(f"{self.__df.shape[0]}")
        # self.__total_item_cnt = 0
        # self.__irow = 0
        # self.__max_init_nitems = self.init_nitem_sbox.value()
        #
        self.__model = SnapshotModel(self.__db_con, self.__table_name)
        self.view.setModel(self.__model)
        #self.__model.fetchedItemNumChanged.connect(self.onFetchedNItemsChanged)
        #self.__model.dataChanged.connect(self.onDataChanged)
        self.post_style_view(self.view)

    def __refresh_model(self):
        #self.total_nitem_lbl.setText(f"{self.__df.shape[0]}")
        #self.__total_item_cnt = 0
        #self.__irow = 0
        #self.__max_init_nitems = self.init_nitem_sbox.value()
        #
        self.__model.setDataSource(self.__db_con, self.__table_name)
        self.post_style_view(self.view)

    def __build_ion_filter_btns(self, area: QScrollArea, ion_list: list):
        w = area.takeWidget()
        w.setParent(None)
        w = QWidget(self)
        w.setContentsMargins(0, 4, 0, 0)
        layout = FlowLayout()
        for ion in ion_list:
            btn = QToolButton(self)
            btn.setText(ion)
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(5)
            shadow.setOffset(2)
            btn.setGraphicsEffect(shadow)
            px_tuple = get_pixmap_element(ion, 'on'), get_pixmap_element(
                ion, 'off')
            icon = QIcon()
            for _px, _st in zip(px_tuple, (QIcon.On, QIcon.Off)):
                icon.addPixmap(QPixmap(_px), QIcon.Normal, _st)
            btn.setIcon(icon)
            btn.setIconSize(QSize(ION_ICON_SIZE, ION_ICON_SIZE))
            btn.setCheckable(True)
            btn.toggled.connect(partial(self.on_update_ion_filters, ion,
                                        False))
            layout.addWidget(btn)
            btn.setChecked(self.__current_ion_filter_dict.get(ion, True))
        w.setLayout(layout)
        area.setWidget(w)

    def __build_tag_filter_btns(self, area: QScrollArea, tag_list: list):
        w = area.takeWidget()
        w.setParent(None)
        w = QWidget(self)
        w.setContentsMargins(0, 4, 0, 0)
        layout = FlowLayout()
        for tag in tag_list:
            o = QToolButton(self)
            o.setText(tag)
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(5)
            shadow.setOffset(2)
            o.setGraphicsEffect(shadow)
            o.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            o.setStyleSheet(TAG_BTN_STY.format(fs=self.__default_font_size -
                                               1))
            o.setCheckable(True)
            o.toggled.connect(partial(self.on_update_tag_filters, tag, False))
            layout.addWidget(o)
            # initially set checked
            o.setChecked(self.__current_tag_filter_dict.get(tag, True))
        w.setLayout(layout)
        area.setWidget(w)

    @pyqtSlot(bool)
    def on_update_ion_filters(self, ion: str, activate_filter: bool,
                              is_checked: bool):
        self.__current_ion_filter_dict[ion] = is_checked
        if activate_filter:
            self.activate_filters()

    @pyqtSlot(bool)
    def on_update_tag_filters(self, tag: str, activate_filter: bool,
                              is_checked: bool):
        self.__current_tag_filter_dict[tag] = is_checked
        if activate_filter:
            self.activate_filters()

    def onLoadData(self, dat: bytes):
        # parse the binary data blob
        # emit the settings table
        _df = pd.read_excel(dat, sheet_name='settings')
        self.dataLoaded.emit(_df)


def qdate2epochs(d: QDate, is_end: bool = False):
    """Return seconds since epoch from a given QDate object.

    Parameters
    ----------
    d : QDate
        QDate object obtained from QDateEdit widget.
    is_end : bool
        If the given *d* is the end of the daterange, if so, add 24 * 60 - 1 seconds.

    Returns
    -------
    r : float
        Seconds since epoch.
    """
    if is_end:
        dt = QDateTime(d).addSecs(62399)
    else:
        dt = QDateTime(d)
    return dt.toMSecsSinceEpoch() / 1000.0


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    w1 = MPSDiagWidget('ND', '/tmp/')
    # w2 = MPSDiagWidget('IC')
    # w3 = MPSDiagWidget('HMR')
    w1.show()
    # w2.show()
    # w3.show()

    sys.exit(app.exec_())
