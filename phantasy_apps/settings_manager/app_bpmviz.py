#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow

from .ui.ui_bpmviz import Ui_MainWindow

DEFAULT_GROUPS = ('BPM-X', 'BPM-Y', 'BPM-PHA', 'BPM_MAG')


def plot_data(ax, dataframe, group_list, color_list, label_list, y_column, yerr_column=None, **kws):
    for (gname, color, label) in zip(group_list, color_list, label_list):
        df = dataframe.xs(gname, level=1)
        df.reset_index(inplace=True)
        df.set_index('D####', inplace=True)
        if yerr_column is None:
            df.plot.bar(y=y_column, ax=ax,
                        fontsize=14, rot=90, alpha=0.6, color=color, label=label)
        else:
            df.plot.bar(y=y_column, yerr=yerr_column, ax=ax,
                        fontsize=14, rot=90, alpha=0.6, color=color, label=label)

    xlabel = kws.get('xlabel', 'BPM')
    ylabel = kws.get('ylabel', 'Centroid Trajectory [mm]')
    fontsize = kws.get('fontsize', 18)
    ax.set_xlabel(xlabel, fontsize=fontsize, fontfamily='monospace')
    ax.set_ylabel(ylabel, fontsize=fontsize, fontfamily='monospace')
    # ax.set_ylim([-1.5, 1.5])
    ax.grid()
    # ax.set_title(df_traj_x.columns[1][:-4], fontsize=16)
    [i.set_family('monospace') for i in ax.get_xticklabels()]
    [i.set_family('monospace') for i in ax.get_yticklabels()]


class BPMVizWidget(QMainWindow, Ui_MainWindow):

    def __init__(self, df1, df2=None, parent=None, **kws):
        super(BPMVizWidget, self).__init__()
        self.parent = parent
        self._df1 = df1
        self._df2 = df2
        self._groups = kws.get('groups', DEFAULT_GROUPS)

        # UI
        self.setupUi(self)
        self.setWindowTitle("BPM Signal Visualization")

        #
        self._post_init()
        #
        if df2 is None:
            self.plot1()
        else:
            self.plot2()

    def _post_init(self):
        #
        self._ax11 = self.mplbase11.axes
        self._ax12 = self.mplbase12.axes
        self._ax21 = self.mplbase21.axes
        self._ax22 = self.mplbase22.axes

    def plot1(self):
        #
        index0 = self._df1.index.get_level_values(0)
        dnum = index0.str.extract(r'.*(D[0-9]{4}).*')
        self._df1['D####'] = dnum[0].to_numpy()
        #
        df = self._df1
        #
        plot_data(self._ax11, df,
                  group_list=self._groups[:2],
                  color_list=['b', 'r'],
                  label_list=['$\\langle x \\rangle$', '$\\langle y \\rangle$'],
                  y_column='avg', yerr_column='std',
                  xlabel='BPMs', ylabel='Trajectory [mm]')
        self.tabWidget.setTabText(0, "Centroid Trajectory")

        #
        plot_data(self._ax12, df,
                  group_list=self._groups[2:3],
                  color_list=['b'],
                  label_list=['$\phi$'],
                  y_column='avg', yerr_column='std',
                  xlabel='BPMs', ylabel='Phase [deg]')
        self.tabWidget.setTabText(1, "Phase Plot")

        #
        plot_data(self._ax21, df,
                  group_list=self._groups[3:4],
                  color_list=['g'],
                  label_list=['Intensity'],
                  y_column='avg', yerr_column='std',
                  xlabel='BPMs', ylabel='Intensity')
        self.tabWidget.setTabText(2, "Intensity")

        #
        self.tabWidget.setTabEnabled(3, False)

    def plot2(self):
        #
        df_saved, df_live = self._df1, self._df2
        df_saved1 = df_saved.loc[:, ('avg',)]
        df_live1 = df_live.loc[:, ('avg',)]
        df_live1.rename(columns={'avg':'avg-live', 'std':'std-live'}, inplace=True)
        df_saved1.rename(columns={'avg':'avg-saved', 'std':'std-saved'}, inplace=True)
        df = df_live1.join(df_saved1)
        df['avg-delta'] = df['avg-live'] - df['avg-saved']

        #
        index0 = df.index.get_level_values(0)
        dnum = index0.str.extract(r'.*(D[0-9]{4}).*')
        df['D####'] = dnum[0].to_numpy()
        #

        plot_data(self._ax11, df,
                  group_list=self._groups[0:1],
                  color_list=['b',],
                  label_list=['$\Delta\\langle x \\rangle$'],
                  y_column='avg-delta',
                  xlabel='BPMs', ylabel='Trajectory Difference [mm]')
        self.tabWidget.setTabText(0, "Delta X")

        plot_data(self._ax12, df,
                  group_list=self._groups[1:2],
                  color_list=['r',],
                  label_list=['$\Delta\\langle y \\rangle$'],
                  y_column='avg-delta',
                  xlabel='BPMs', ylabel='Trajectory Difference [mm]')
        self.tabWidget.setTabText(1, "Delta Y")

        #
        plot_data(self._ax21, df,
                  group_list=self._groups[2:3],
                  color_list=['g',],
                  label_list=['$\Delta\phi$'],
                  y_column='avg-delta',
                  xlabel='BPMs', ylabel='Phase Difference [deg]')
        self.tabWidget.setTabText(2, "Delta Phase")

        #
        plot_data(self._ax22, df,
                  group_list=self._groups[3:4],
                  color_list=['c',],
                  label_list=['$\Delta Intensity$'],
                  y_column='avg-delta',
                  xlabel='BPMs', ylabel='Intensity Difference')
        self.tabWidget.setTabText(3, "Delta Intensity")
