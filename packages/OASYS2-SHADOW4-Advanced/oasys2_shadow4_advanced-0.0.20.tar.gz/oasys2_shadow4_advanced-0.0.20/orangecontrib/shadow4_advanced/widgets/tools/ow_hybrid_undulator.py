#!/usr/bin/env python
# -*- coding: utf-8 -*-
# #########################################################################
# Copyright (c) 2020, UChicago Argonne, LLC. All rights reserved.         #
#                                                                         #
# Copyright 2020. UChicago Argonne, LLC. This software was produced       #
# under U.S. Government contract DE-AC02-06CH11357 for Argonne National   #
# Laboratory (ANL), which is operated by UChicago Argonne, LLC for the    #
# U.S. Department of Energy. The U.S. Government has rights to use,       #
# reproduce, and distribute this software.  NEITHER THE GOVERNMENT NOR    #
# UChicago Argonne, LLC MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR        #
# ASSUMES ANY LIABILITY FOR THE USE OF THIS SOFTWARE.  If software is     #
# modified to produce derivative works, such modified software should     #
# be clearly marked, so as not to confuse it with the version available   #
# from ANL.                                                               #
#                                                                         #
# Additionally, redistribution and use in source and binary forms, with   #
# or without modification, are permitted provided that the following      #
# conditions are met:                                                     #
#                                                                         #
#     * Redistributions of source code must retain the above copyright    #
#       notice, this list of conditions and the following disclaimer.     #
#                                                                         #
#     * Redistributions in binary form must reproduce the above copyright #
#       notice, this list of conditions and the following disclaimer in   #
#       the documentation and/or other materials provided with the        #
#       distribution.                                                     #
#                                                                         #
#     * Neither the name of UChicago Argonne, LLC, Argonne National       #
#       Laboratory, ANL, the U.S. Government, nor the names of its        #
#       contributors may be used to endorse or promote products derived   #
#       from this software without specific prior written permission.     #
#                                                                         #
# THIS SOFTWARE IS PROVIDED BY UChicago Argonne, LLC AND CONTRIBUTORS     #
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT       #
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS       #
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL UChicago     #
# Argonne, LLC OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,        #
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,    #
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;        #
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER        #
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT      #
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN       #
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE         #
# POSSIBILITY OF SUCH DAMAGE.                                             #
# #########################################################################
import os
import sys
import numpy

from silx.gui.plot import Plot2D

from AnyQt.QtWidgets import QMessageBox, QDialog, QVBoxLayout, QLabel, QDialogButtonBox
from AnyQt.QtGui import QPixmap, QPalette, QColor, QFont

import orangecanvas.resources as resources

from orangewidget import gui
from orangewidget.settings import Setting

from oasys2.widget import gui as oasysgui
from oasys2.widget.util import congruence
from oasys2.widget.util.widget_util import EmittingStream
from oasys2.widget.util.widget_objects import TriggerIn
from oasys2.canvas.util.canvas_util import add_widget_parameters_to_module

from syned.beamline.optical_elements.absorbers.slit import Slit
from syned.beamline.shape import Rectangle

try:
    from orangecontrib.shadow4.widgets.gui.ow_synchrotron_source import OWSynchrotronSource
    from orangecontrib.shadow4.util.shadow4_objects import ShadowData
    from orangecontrib.shadow4.util.shadow4_util import ShadowCongruence
except ImportError:
    raise ImportError("OASYS2-SHADOW4 add-on required to run OASYS2-SHADOW4-Advanced")

from shadow4.beamline.s4_beamline import S4Beamline

from shadow4_advanced.sources.hybrid.s4_hybrid_undulator_light_source import (
    S4HybridUndulatorLightSource, HybridUndulatorInputParameters, HybridUndulatorOutputParameters, HybridUndulatorListener,
    gamma, get_default_initial_z, resonance_energy, is_canted_undulator, get_source_slit_data, set_which_waist, K_from_magnetic_field, S4HybridUndulator
)

import scipy.constants as codata

m2ev = codata.c * codata.h / codata.e

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class AutoUndulator:
    VERTICAL   = 1
    HORIZONTAL = 2
    BOTH       = 3

class HybridUndulator(OWSynchrotronSource, HybridUndulatorListener):
    name = "Shadow4/SRW Undulator"
    description = "Advanced Tools: Hybrid Shadow/SRW Undulator"
    icon = "icons/hybrid_undulator.png"
    priority = 5
    maintainer = "Luca Rebuffi"
    maintainer_email = "lrebuffi(@at@)anl.gov"
    category = "Sources"
    keywords = ["data", "file", "load", "read"]

    distribution_source = Setting(0)
    cumulated_view_type = Setting(0)

    # Shadow
    number_of_rays  = Setting(5000)
    seed            = Setting(6775431)
    use_harmonic    = Setting(0)
    harmonic_number = Setting(1)
    harmonic_energy = 0.0
    energy          = Setting(10000.0)
    energy_to       = Setting(10100.0)
    energy_points   = Setting(10)

    #SRW -> Undulator
    number_of_periods                            = Setting(184)
    undulator_period                             = Setting(0.025)
    Kv                                           = Setting(0.857)
    Kh                                           = Setting(0)
    Bh                                           = Setting(0.0)
    Bv                                           = Setting(1.5)
    magnetic_field_from                          = Setting(0)
    initial_phase_vertical                       = Setting(0.0)
    initial_phase_horizontal                     = Setting(0.0)
    symmetry_vs_longitudinal_position_vertical   = Setting(1)
    symmetry_vs_longitudinal_position_horizontal = Setting(0)
    horizontal_central_position                  = Setting(0.0)
    vertical_central_position                    = Setting(0.0)
    longitudinal_central_position                = Setting(0.0)

    auto_expand = Setting(0)
    auto_expand_rays = Setting(0)

    type_of_initialization = Setting(0)

    moment_x = Setting(0.0)
    moment_y = Setting(0.0)
    moment_z = Setting(0.0)
    moment_xp = Setting(0.0)
    moment_yp = Setting(0.0)

    source_dimension_wf_h_slit_gap = Setting(0.0015)
    source_dimension_wf_v_slit_gap = Setting(0.0015)
    source_dimension_wf_h_slit_c = Setting(0.0)
    source_dimension_wf_v_slit_c =Setting( 0.0)
    source_dimension_wf_h_slit_points = Setting(301)
    source_dimension_wf_v_slit_points = Setting(301)
    source_dimension_wf_distance = Setting(28.0)

    horizontal_range_modification_factor_at_resizing = Setting(0.5)
    horizontal_resolution_modification_factor_at_resizing = Setting(5.0)
    vertical_range_modification_factor_at_resizing = Setting(0.5)
    vertical_resolution_modification_factor_at_resizing = Setting(5.0)

    waist_position_calculation = Setting(0)
    waist_position = Setting(0.0)

    waist_position_auto = Setting(0)
    waist_position_auto_h = Setting(0.0)
    waist_position_auto_v = Setting(0.0)
    waist_back_propagation_parameters = Setting(1)
    waist_horizontal_range_modification_factor_at_resizing = Setting(0.5)
    waist_horizontal_resolution_modification_factor_at_resizing = Setting(5.0)
    waist_vertical_range_modification_factor_at_resizing = Setting(0.5)
    waist_vertical_resolution_modification_factor_at_resizing = Setting(5.0)
    which_waist = Setting(2)
    number_of_waist_fit_points = Setting(10)
    degree_of_waist_fit = Setting(3)
    use_sigma_or_fwhm = Setting(0)

    waist_position_user_defined = Setting(0.0)

    kind_of_sampler = Setting(1)
    save_srw_result = Setting(0)

    # SRW FILE INPUT

    source_dimension_srw_file = Setting("intensity_source_dimension.dat")
    angular_distribution_srw_file = Setting("intensity_angular_distribution.dat")

    # ASCII FILE INPUT

    x_positions_file = Setting("x_positions.txt")
    z_positions_file = Setting("z_positions.txt")
    x_positions_factor = Setting(0.01)
    z_positions_factor = Setting(0.01)
    x_divergences_file = Setting("x_divergences.txt")
    z_divergences_file = Setting("z_divergences.txt")
    x_divergences_factor = Setting(1.0)
    z_divergences_factor = Setting(1.0)

    combine_strategy = Setting(0)

    # Utility

    auto_energy          = Setting(0.0)
    auto_harmonic_number = Setting(1)

    # Advanced
    use_stokes = Setting(1)

    energy_step     = None
    power_step      = None
    current_step    = None
    total_steps     = None
    start_event     = True
    compute_power   = False
    integrated_flux = None
    power_density   = None

    cumulated_energies = None
    cumulated_integrated_flux = None
    cumulated_power_density = None
    cumulated_power = None

    do_cumulated_calculations = False

    def __init__(self):
        super().__init__(show_energy_spread=True)

        tab_shadow = oasysgui.createTabPage(self.tabs_control_area, "Shadow4")
        tab_spdiv  = oasysgui.createTabPage(self.tabs_control_area, "Position/Divergence")
        tab_util   = oasysgui.createTabPage(self.tabs_control_area, "Utility")

        ####################################################################################
        # SHADOW

        left_box_1 = oasysgui.widgetBox(tab_shadow, "Monte Carlo and Energy Spectrum", addSpace=False, orientation="vertical")

        oasysgui.lineEdit(left_box_1, self, "number_of_rays", "Number of Rays", tooltip="Number of Rays", labelWidth=250, valueType=int, orientation="horizontal")
        oasysgui.lineEdit(left_box_1, self, "seed", "Seed", tooltip="Seed (0=clock)", labelWidth=250, valueType=int, orientation="horizontal")

        gui.comboBox(left_box_1, self, "use_harmonic", label="Photon Energy",
                     items=["Harmonic", "Other", "Range"], labelWidth=260,
                     callback=self.set_wf_use_harmonic, sendSelectedValue=False, orientation="horizontal")

        self.use_harmonic_box_1 = oasysgui.widgetBox(left_box_1, "", addSpace=False, orientation="vertical", height=80)
        oasysgui.lineEdit(self.use_harmonic_box_1, self, "harmonic_number", "Harmonic #", labelWidth=260, valueType=int, orientation="horizontal", callback=self.set_harmonic_energy)
        le_he = oasysgui.lineEdit(self.use_harmonic_box_1, self, "harmonic_energy", "Harmonic Energy", labelWidth=260, valueType=float, orientation="horizontal")
        le_he.setReadOnly(True)
        font = QFont(le_he.font())
        font.setBold(True)
        le_he.setFont(font)
        palette = QPalette(le_he.palette())
        palette.setColor(QPalette.Text, QColor('dark blue'))
        palette.setColor(QPalette.Base, QColor(243, 240, 160))
        le_he.setPalette(palette)

        self.use_harmonic_box_2 = oasysgui.widgetBox(left_box_1, "", addSpace=False, orientation="vertical", height=80)
        oasysgui.lineEdit(self.use_harmonic_box_2, self, "energy", "Photon Energy [eV]", labelWidth=260, valueType=float, orientation="horizontal")

        self.use_harmonic_box_3 = oasysgui.widgetBox(left_box_1, "", addSpace=False, orientation="vertical", height=80)
        oasysgui.lineEdit(self.use_harmonic_box_3, self, "energy", "Photon Energy from [eV]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.use_harmonic_box_3, self, "energy_to", "Photon Energy to [eV]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.use_harmonic_box_3, self, "energy_points", "Nr. of Energy values", labelWidth=260, valueType=int, orientation="horizontal")

        self.set_wf_use_harmonic()

        gui.comboBox(tab_spdiv, self, "distribution_source", label="Distribution Source", labelWidth=310,
                     items=["SRW Calculation", "SRW Files", "ASCII Files"], orientation="horizontal", callback=self.set_distribution_source)

        self.srw_box       = oasysgui.widgetBox(tab_spdiv, "", addSpace=False, orientation="vertical", height=550)
        self.srw_files_box = oasysgui.widgetBox(tab_spdiv, "", addSpace=False, orientation="vertical", height=550)
        self.ascii_box     = oasysgui.widgetBox(tab_spdiv, "", addSpace=False, orientation="vertical", height=550)

    
        ####################################################################################
        # SRW

        tabs_srw = oasysgui.tabWidget(self.srw_box)

        if self.IS_DEVELOP:
            gui.comboBox(self.srw_box, self, "kind_of_sampler", label="Random Generator", labelWidth=250,
                         items=["Simple", "Accurate", "Accurate (SRIO)", ], orientation="horizontal")
        else:
            gui.comboBox(self.srw_box, self, "kind_of_sampler", label="Random Generator", labelWidth=250,
                         items=["Simple", "Accurate"], orientation="horizontal")

        gui.comboBox(self.srw_box, self, "save_srw_result", label="Save SRW results", labelWidth=310,
                     items=["No", "Yes"], orientation="horizontal", callback=self.set_save_file_srw)

        self.save_file_box = oasysgui.widgetBox(self.srw_box, "", addSpace=False, orientation="vertical")
        self.save_file_box_empty = oasysgui.widgetBox(self.srw_box, "", addSpace=False, orientation="vertical", height=55)

        file_box = oasysgui.widgetBox(self.save_file_box, "", addSpace=False, orientation="horizontal", height=25)

        self.le_source_dimension_srw_file = oasysgui.lineEdit(file_box, self, "source_dimension_srw_file", "Source Dimension File", labelWidth=140,  valueType=str, orientation="horizontal")

        gui.button(file_box, self, "...", callback=self.select_source_dimension_file)

        file_box = oasysgui.widgetBox(self.save_file_box, "", addSpace=False, orientation="horizontal", height=25)

        self.le_angular_distribution_srw_file = oasysgui.lineEdit(file_box, self, "angular_distribution_srw_file", "Angular Distribution File", labelWidth=140,  valueType=str, orientation="horizontal")

        gui.button(file_box, self, "...", callback=self.select_angular_distribution_file)

        self.set_save_file_srw()

        tab_ls = oasysgui.createTabPage(tabs_srw, "Undulator Setting")
        tab_wf = oasysgui.createTabPage(tabs_srw, "Wavefront Setting")
        tab_fl = oasysgui.createTabPage(tabs_srw, "Advanced Setting")

        ####################################

        box = oasysgui.widgetBox(tab_fl, "Flux Calculation", addSpace=False, orientation="vertical")

        gui.comboBox(box, self, "use_stokes", label="Integrated Flux", labelWidth=300,
                     items=["From Wavefront", "From Stokes"],
                     sendSelectedValue=False, orientation="horizontal")

        ####################################

        tab_und = oasysgui.tabWidget(tab_ls)

        tab_id   = oasysgui.createTabPage(tab_und, "ID Parameters")
        tab_traj = oasysgui.createTabPage(tab_und, "Trajectory")

        self.tab_pos = oasysgui.tabWidget(tab_id)

        tab_dim   = oasysgui.createTabPage(self.tab_pos, "ID")

        oasysgui.lineEdit(tab_dim, self, "undulator_period", "Period Length [m]", labelWidth=260, valueType=float, orientation="horizontal", callback=self.set_harmonic_energy)
        oasysgui.lineEdit(tab_dim, self, "number_of_periods", "Number of Periods", labelWidth=260, valueType=int, orientation="horizontal")
        oasysgui.lineEdit(tab_dim, self, "horizontal_central_position", "Horizontal Central Position [m]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(tab_dim, self, "vertical_central_position", "Vertical Central Position [m]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(tab_dim, self, "longitudinal_central_position", "Longitudinal Central Position [m]", labelWidth=260, valueType=float, orientation="horizontal", callback=self.manage_waist_position)

        self.warning_label = oasysgui.widgetLabel(tab_dim, "  Warning: The source will be positioned at the center\n" +
                                                  "  of the ID: the relative distance of the first optical\n" +
                                                  "  element has to be longitudinally shifted accordingly")
        self.warning_label.setStyleSheet("color: red; font: bold")

        gui.comboBox(tab_dim, self, "magnetic_field_from", label="Magnetic Field", labelWidth=350,
                     items=["From K", "From B"],
                     callback=self.set_magnetic_field,
                     sendSelectedValue=False, orientation="horizontal")

        container = oasysgui.widgetBox(tab_dim, "", addSpace=False, orientation="horizontal")

        horizontal_box = oasysgui.widgetBox(container, "", addSpace=False, orientation="vertical", width=195)
        vertical_box = oasysgui.widgetBox(container,  "", addSpace=False, orientation="vertical", width=155)

        gui.label(horizontal_box, self, "                     Horizontal")
        gui.label(vertical_box, self, "  Vertical")

        self.magnetic_field_box_1_h = oasysgui.widgetBox(horizontal_box, "", addSpace=False, orientation="vertical")
        self.magnetic_field_box_2_h = oasysgui.widgetBox(horizontal_box, "", addSpace=False, orientation="vertical")
        self.magnetic_field_box_1_v = oasysgui.widgetBox(vertical_box, "", addSpace=False, orientation="vertical")
        self.magnetic_field_box_2_v = oasysgui.widgetBox(vertical_box, "", addSpace=False, orientation="vertical")

        oasysgui.lineEdit(self.magnetic_field_box_1_h, self, "Kh", "K", labelWidth=70, valueType=float, orientation="horizontal", callback=self.set_harmonic_energy)
        oasysgui.lineEdit(self.magnetic_field_box_1_v, self, "Kv", " ", labelWidth=2, valueType=float, orientation="horizontal", callback=self.set_harmonic_energy)
        oasysgui.lineEdit(self.magnetic_field_box_2_h, self, "Bh", "B [T]", labelWidth=70, valueType=float, orientation="horizontal", callback=self.set_harmonic_energy)
        oasysgui.lineEdit(self.magnetic_field_box_2_v, self, "Bv", " ", labelWidth=2, valueType=float, orientation="horizontal", callback=self.set_harmonic_energy)

        self.set_magnetic_field()

        oasysgui.lineEdit(horizontal_box, self, "initial_phase_horizontal", "\u03c6\u2080 [rad]", labelWidth=70, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(vertical_box, self, "initial_phase_vertical", " ", labelWidth=2, valueType=float, orientation="horizontal")

        gui.comboBox(horizontal_box, self, "symmetry_vs_longitudinal_position_horizontal", label="Symmetry", labelWidth=70,
                     items=["Symmetrical", "Anti-Symmetrical"],
                     sendSelectedValue=False, orientation="horizontal")

        symmetry_v_box =  oasysgui.widgetBox(vertical_box, "", addSpace=False, orientation="horizontal")
        gui.comboBox(symmetry_v_box, self, "symmetry_vs_longitudinal_position_vertical", label=" ", labelWidth=2,
                     items=["Symmetrical", "Anti-Symmetrical"],
                     sendSelectedValue=False, orientation="horizontal")
        gui.button(symmetry_v_box, self, "?", callback=self.open_help, width=12)

        gui.comboBox(tab_traj, self, "type_of_initialization", label="Trajectory Initialization", labelWidth=140,
                     items=["Automatic", "At Fixed Position", "Sampled from Phase Space"],
                     callback=self.set_type_of_initialization,
                     sendSelectedValue=False, orientation="horizontal")

        self.left_box_3_1 = oasysgui.widgetBox(tab_traj, "", addSpace=False, orientation="vertical", height=160)
        self.left_box_3_2 = oasysgui.widgetBox(tab_traj, "", addSpace=False, orientation="vertical", height=160)

        oasysgui.lineEdit(self.left_box_3_1, self, "moment_x", "x\u2080 [m]", labelWidth=200, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.left_box_3_1, self, "moment_y", "y\u2080 [m]", labelWidth=200, valueType=float, orientation="horizontal")

        box = oasysgui.widgetBox(self.left_box_3_1, "", addSpace=False, orientation="horizontal")

        oasysgui.lineEdit(box, self, "moment_z", "z\u2080 [m]", labelWidth=160, valueType=float, orientation="horizontal")
        gui.button(box, self, "Auto", width=35, callback=self.set_z0_default)

        oasysgui.lineEdit(self.left_box_3_1, self, "moment_xp", "x'\u2080 [rad]", labelWidth=200, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.left_box_3_1, self, "moment_yp", "y'\u2080 [rad]", labelWidth=200, valueType=float, orientation="horizontal")

        self.set_type_of_initialization()

        left_box_3 = oasysgui.widgetBox(tab_wf, "Divergence Distribution Propagation Parameters", addSpace=False, orientation="vertical")

        box = oasysgui.widgetBox(left_box_3, "", addSpace=False, orientation="horizontal")
        oasysgui.lineEdit(box, self, "source_dimension_wf_h_slit_gap", "H Slit Gap [m]", labelWidth=130, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(box, self, "source_dimension_wf_h_slit_c", "  Center [m]", labelWidth=50, valueType=float, orientation="horizontal")
        box = oasysgui.widgetBox(left_box_3, "", addSpace=False, orientation="horizontal")
        oasysgui.lineEdit(box, self, "source_dimension_wf_v_slit_gap", "V Slit Gap [m]", labelWidth=130, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(box, self, "source_dimension_wf_v_slit_c", "  Center [m]", labelWidth=50, valueType=float, orientation="horizontal")

        oasysgui.lineEdit(left_box_3, self, "source_dimension_wf_h_slit_points", "H Slit Points", labelWidth=250, valueType=int, orientation="horizontal", callback=self.set_data_x)
        oasysgui.lineEdit(left_box_3, self, "source_dimension_wf_v_slit_points", "V Slit Points", labelWidth=250, valueType=int, orientation="horizontal", callback=self.set_data_y)
        oasysgui.lineEdit(left_box_3, self, "source_dimension_wf_distance", "Propagation Distance [m]\n(relative to the center of the ID)", labelWidth=250, valueType=float, orientation="horizontal")

        left_box_4 = oasysgui.widgetBox(tab_wf, "Size Distribution (Back) Propagation Parameters", addSpace=False, orientation="vertical")

        oasysgui.lineEdit(left_box_4, self, "horizontal_range_modification_factor_at_resizing", "H range modification factor at resizing", labelWidth=290, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(left_box_4, self, "horizontal_resolution_modification_factor_at_resizing", "H resolution modification factor at resizing", labelWidth=290, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(left_box_4, self, "vertical_range_modification_factor_at_resizing", "V range modification factor at resizing", labelWidth=290, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(left_box_4, self, "vertical_resolution_modification_factor_at_resizing", "V resolution modification factor at resizing", labelWidth=290, valueType=float, orientation="horizontal")

        gui.comboBox(tab_wf, self, "auto_expand", label="Auto Expand Slit to Compensate Random Generator", labelWidth=310,
                     items=["No", "Yes"], orientation="horizontal", callback=self.set_auto_expand)

        self.cb_auto_expand_rays = gui.comboBox(tab_wf, self, "auto_expand_rays", label="Auto Increase Number of Rays", labelWidth=310,
                                                items=["No", "Yes"], orientation="horizontal")

        self.set_auto_expand()

        ####################################################################################
        # SRW FILES

        gui.separator(self.srw_files_box)

        file_box = oasysgui.widgetBox(self.srw_files_box, "", addSpace=True, orientation="horizontal", height=45)

        self.le_source_dimension_srw_file = oasysgui.lineEdit(file_box, self, "source_dimension_srw_file", "Source Dimension File", labelWidth=180,  valueType=str, orientation="vertical")

        gui.button(file_box, self, "...", height=45, callback=self.select_source_dimension_file)

        file_box = oasysgui.widgetBox(self.srw_files_box, "", addSpace=True, orientation="horizontal", height=45)

        self.le_angular_distribution_srw_file = oasysgui.lineEdit(file_box, self, "angular_distribution_srw_file", "Angular Distribution File", labelWidth=180,  valueType=str, orientation="vertical")

        gui.button(file_box, self, "...", height=45, callback=self.select_angular_distribution_file)


        ####################################################################################
        # ASCII FILES

        gui.separator(self.ascii_box)

        file_box = oasysgui.widgetBox(self.ascii_box, "", addSpace=True, orientation="horizontal", height=45)

        self.le_x_positions_file = oasysgui.lineEdit(file_box, self, "x_positions_file", "X Positions File", labelWidth=180,  valueType=str, orientation="vertical")

        gui.button(file_box, self, "...", height=45, callback=self.select_x_positions_file)

        file_box = oasysgui.widgetBox(self.ascii_box, "", addSpace=True, orientation="horizontal", height=45)

        self.le_z_positions_file = oasysgui.lineEdit(file_box, self, "z_positions_file", "Z Positions File", labelWidth=180,  valueType=str, orientation="vertical")

        gui.button(file_box, self, "...", height=45, callback=self.select_z_positions_file)

        file_box = oasysgui.widgetBox(self.ascii_box, "", addSpace=True, orientation="horizontal", height=45)

        self.le_x_divergences_file = oasysgui.lineEdit(file_box, self, "x_divergences_file", "X Divergences File", labelWidth=180,  valueType=str, orientation="vertical")

        gui.button(file_box, self, "...", height=45, callback=self.select_x_divergences_file)

        file_box = oasysgui.widgetBox(self.ascii_box, "", addSpace=True, orientation="horizontal", height=45)

        self.le_z_divergences_file = oasysgui.lineEdit(file_box, self, "z_divergences_file", "Z Divergences File", labelWidth=180,  valueType=str, orientation="vertical")

        gui.button(file_box, self, "...", height=45, callback=self.select_z_divergences_file)

        gui.separator(self.ascii_box)

        oasysgui.lineEdit(self.ascii_box, self, "x_positions_factor",   "X Positions UM to Workspace UM", labelWidth=230, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.ascii_box, self, "z_positions_factor",   "Z Positions UM to Workspace UM",  labelWidth=230, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.ascii_box, self, "x_divergences_factor", "X Divergences UM to rad", labelWidth=230, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.ascii_box, self, "z_divergences_factor", "X Divergences UM to rad", labelWidth=230, valueType=float, orientation="horizontal")

        gui.separator(self.ascii_box)

        gui.comboBox(self.ascii_box, self, "combine_strategy", label="2D Distribution Creation Strategy", labelWidth=310,
                     items=["Sqrt(Product)", "Sqrt(Quadratic Sum)", "Convolution", "Average"], orientation="horizontal", callback=self.set_save_file_srw)

        ####################################################################################
        # Utility

        left_box_1 = oasysgui.widgetBox(tab_util, "Auto Setting of Undulator", addSpace=False, orientation="vertical")

        oasysgui.lineEdit(left_box_1, self, "auto_energy", "Set Undulator at Energy [eV]", labelWidth=250, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(left_box_1, self, "auto_harmonic_number", "As Harmonic #",  labelWidth=250, valueType=int, orientation="horizontal")

        button_box = oasysgui.widgetBox(left_box_1, "", addSpace=False, orientation="horizontal")

        gui.button(button_box, self, "Set Kv value", callback=self.auto_set_undulator_V)
        gui.button(button_box, self, "Set Kh value", callback=self.auto_set_undulator_H)
        gui.button(button_box, self, "Set Both K values", callback=self.auto_set_undulator_B)

        gui.rubber(self.controlArea)

        cumulated_plot_tab = oasysgui.createTabPage(self.main_tabs, "Cumulated Plots")

        view_box = oasysgui.widgetBox(cumulated_plot_tab, "Plotting Style", addSpace=False, orientation="horizontal")
        view_box_1 = oasysgui.widgetBox(view_box, "", addSpace=False, orientation="vertical", width=350)

        self.cumulated_view_type_combo = gui.comboBox(view_box_1, self, "cumulated_view_type", label="Show Plots",
                                                      labelWidth=220,
                                                      items=["No", "Yes"],
                                                      callback=self.set_cumulated_plot_quality, sendSelectedValue=False, orientation="horizontal")


        self.cumulated_tabs = oasysgui.tabWidget(cumulated_plot_tab)

        self.initialize_cumulated_tabs()
        self.set_distribution_source()

        gui.rubber(self.mainArea)


    ###################################################################################
    # Listener from HybridCalculator
    ###################################################################################

    def receive_message(self, message: str, data: dict):
        if not message is None:
            print(message)
            self.setStatusMessage(message)

        progress = data.get("progress", None)
        if not progress is None:
            print(f"Progress: {progress}%")
            self.progressBarSet(progress)

    ###################################################################################
    # Utils from HybridCalculator
    ###################################################################################

    def _gamma(self):
        return gamma(electron_beam=self.get_electron_beam())

    def _resonance_energy(self):
        return resonance_energy(electron_beam=self.get_electron_beam(),
                                magnetic_structure=self.get_magnetic_structure(),
                                harmonic=self.harmonic_number)

    def _get_default_initial_z(self):
        return get_default_initial_z(magnetic_structure=self.get_magnetic_structure(), longitudinal_central_position=self.longitudinal_central_position)

    def _is_canted_undulator(self):
        return is_canted_undulator(longitudinal_central_position=self.longitudinal_central_position)

    def _get_source_slit_data(self, direction):
        return get_source_slit_data(HybridUndulatorInputParameters(
                                        auto_expand=self.auto_expand,
                                        source_dimension_wf_h_slit_points = self.source_dimension_wf_h_slit_points,
                                        source_dimension_wf_v_slit_points = self.source_dimension_wf_v_slit_points,
                                        source_dimension_wf_h_slit_gap = self.source_dimension_wf_h_slit_gap,
                                        source_dimension_wf_v_slit_gap = self.source_dimension_wf_v_slit_gap),
                                    direction)

    def _get_which_waist_position_auto(self):
        input_parameters = HybridUndulatorInputParameters(
                                which_waist=self.which_waist,
                                waist_position_auto_h=self.waist_position_auto_h,
                                waist_position_auto_v=self.waist_position_auto_v )
        set_which_waist(input_parameters)

        return input_parameters.waist_position_auto

    #######################################################################################

    def initialize_cumulated_tabs(self):
        current_tab = self.cumulated_tabs.currentIndex()

        self.cumulated_tabs.removeTab(2)
        self.cumulated_tabs.removeTab(1)
        self.cumulated_tabs.removeTab(0)

        self.cumulated_plot_canvas = [None]*3
        self.cumulated_tab = []
        self.cumulated_tab.append(oasysgui.createTabPage(self.cumulated_tabs, "Spectral Flux"))
        self.cumulated_tab.append(oasysgui.createTabPage(self.cumulated_tabs, "Cumulated Power"))
        self.cumulated_tab.append(oasysgui.createTabPage(self.cumulated_tabs, "Power Density"))

        for tab in self.cumulated_tab:
            tab.setFixedHeight(self.IMAGE_HEIGHT)
            tab.setFixedWidth(self.IMAGE_WIDTH)

        self.cumulated_tabs.setCurrentIndex(current_tab)

    def manage_waist_position(self):
        is_canted = self._is_canted_undulator()

        self.warning_label.setVisible(is_canted)
        self.initialize_waist_position_tab(show=is_canted)
        self.initialize_waist_position_plot_tab(show=(is_canted and self.waist_position_calculation == 1))

    def initialize_waist_position_tab(self, show=True):
        if show and self.tab_pos.count() == 1:
            tab_waist   = oasysgui.createTabPage(self.tab_pos, "Waist Position")

            gui.comboBox(tab_waist, self, "waist_position_calculation", label="Waist Position Calculation", labelWidth=310,
                         items=["None", "Automatic", "User Defined"], orientation="horizontal", callback=self.set_waist_position_calculation)

            self.box_none     = oasysgui.widgetBox(tab_waist, "", addSpace=False, orientation="vertical", height=350)
            self.box_auto     = oasysgui.widgetBox(tab_waist, "", addSpace=False, orientation="vertical", height=350)

            gui.comboBox(self.box_auto, self, "waist_back_propagation_parameters", label="Propagation Parameters", labelWidth=250,
                         items=["Same as Source", "Different"], orientation="horizontal", callback=self.set_waist_back_propagation_parameters)

            self.waist_param_box_1 = oasysgui.widgetBox(self.box_auto, "", addSpace=False, orientation="vertical", height=110)
            self.waist_param_box_2 = oasysgui.widgetBox(self.box_auto, "", addSpace=False, orientation="vertical", height=110)

            gui.separator(self.box_auto, height=5)

            oasysgui.lineEdit(self.waist_param_box_2, self, "waist_horizontal_range_modification_factor_at_resizing", "H range modification factor at resizing", labelWidth=290, valueType=float, orientation="horizontal")
            oasysgui.lineEdit(self.waist_param_box_2, self, "waist_horizontal_resolution_modification_factor_at_resizing", "H resolution modification factor at resizing", labelWidth=290, valueType=float, orientation="horizontal")
            oasysgui.lineEdit(self.waist_param_box_2, self, "waist_vertical_range_modification_factor_at_resizing", "V range modification factor at resizing", labelWidth=290, valueType=float, orientation="horizontal")
            oasysgui.lineEdit(self.waist_param_box_2, self, "waist_vertical_resolution_modification_factor_at_resizing", "V resolution modification factor at resizing", labelWidth=290, valueType=float, orientation="horizontal")

            oasysgui.lineEdit(self.box_auto, self, "number_of_waist_fit_points", "Number of Fit Points", labelWidth=290, valueType=int, orientation="horizontal")
            oasysgui.lineEdit(self.box_auto, self, "degree_of_waist_fit", "Degree of Polynomial Fit", labelWidth=290, valueType=int, orientation="horizontal")

            gui.comboBox(self.box_auto, self, "use_sigma_or_fwhm", label="Gaussian size from", labelWidth=250,
                         items=["Sigma", "FWHM"], orientation="horizontal")

            gui.comboBox(self.box_auto, self, "which_waist", label="Use Direction", labelWidth=150,
                         items=["Horizontal", "Vertical", "Both (middle point)"], orientation="horizontal",
                         callback=self.set_which_waist)

            self.set_waist_back_propagation_parameters()

            le = oasysgui.lineEdit(self.box_auto, self, "waist_position_auto", "Waist Position (relative to ID center) [m]", labelWidth=265, valueType=float, orientation="horizontal")
            le.setReadOnly(True)
            font = QFont(le.font())
            font.setBold(True)
            le.setFont(font)
            palette = QPalette(le.palette())
            palette.setColor(QPalette.Text, QColor('dark blue'))
            palette.setColor(QPalette.Base, QColor(243, 240, 160))
            le.setPalette(palette)

            self.box_user_def = oasysgui.widgetBox(tab_waist, "", addSpace=False, orientation="vertical", height=250)

            oasysgui.lineEdit(self.box_user_def, self, "waist_position_user_defined", "Waist Position (relative to ID center) [m]", labelWidth=265, valueType=float, orientation="horizontal")

            self.set_waist_position_calculation()

        elif not show and self.tab_pos.count() == 2:
            self.tab_pos.removeTab(1)

    def initialize_waist_position_plot_tab(self, show=True):
        if show and self.main_tabs.count() == 4:
            waist_tab = oasysgui.createTabPage(self.main_tabs, "Waist Position for Canted Undulator")

            figure = Figure(figsize=(700, 500))

            self.waist_axes = figure.subplots(1, 2)
            self.waist_axes[0].set_title("Horizontal Direction", fontdict={'horizontalalignment': 'right'})
            self.waist_axes[1].set_title("Vertical Direction", fontdict={'horizontalalignment': 'right'})
            self.waist_axes[0].set_xlabel("Position relative to ID center [mm]")
            self.waist_axes[0].set_ylabel("Sigma [um]")
            self.waist_axes[1].set_xlabel("Position relative to ID center [mm]")
            self.waist_axes[1].set_ylabel("Sigma [um]")

            self.waist_figure = FigureCanvas(figure)

            waist_tab.layout().addWidget(self.waist_figure)

        elif not show and self.main_tabs.count() == 5:
            self.main_tabs.removeTab(4)
            self.waist_axes = None

    def set_waist_position_calculation(self):
        self.box_none.setVisible(self.waist_position_calculation==0)
        self.box_auto.setVisible(self.waist_position_calculation==1)
        self.box_user_def.setVisible(self.waist_position_calculation==2)

        self.initialize_waist_position_plot_tab(show=(self.waist_position_calculation == 1))

    def set_waist_back_propagation_parameters(self):
        self.waist_param_box_1.setVisible(self.waist_back_propagation_parameters==0)
        self.waist_param_box_2.setVisible(self.waist_back_propagation_parameters==1)

    def set_cumulated_plot_quality(self):
        if not self.cumulated_power is None:
            self.initialize_cumulated_tabs()

            self._plot_cumulated_results(True)

    def set_auto_expand(self):
        self.cb_auto_expand_rays.setEnabled(self.auto_expand==1)

        self.set_data_xy()

    def set_data_xy(self):
        self.set_data_x()
        self.set_data_y()

    def set_data_x(self):
        source_dimension_wf_h_slit_points, \
        source_dimension_wf_h_slit_gap = self._get_source_slit_data(direction="h")

        x2 = 0.5 * source_dimension_wf_h_slit_gap
        x1 = -x2

        x1 += self.source_dimension_wf_h_slit_c
        x2 += self.source_dimension_wf_h_slit_c

        self.dataX = 1e3 * numpy.linspace(x1, x2, source_dimension_wf_h_slit_points)

    def set_data_y(self):
        source_dimension_wf_v_slit_points, \
        source_dimension_wf_v_slit_gap = self._get_source_slit_data(direction="v")

        y2 = 0.5 * source_dimension_wf_v_slit_gap
        y1 = -y2

        y1 += self.source_dimension_wf_h_slit_c
        y2 += self.source_dimension_wf_h_slit_c

        self.dataY = 1e3*numpy.linspace(y1, y2, source_dimension_wf_v_slit_points)


    ####################################################################################
    # GRAPHICS
    ####################################################################################

    def set_type_of_initialization(self):
        self.left_box_3_1.setVisible(self.type_of_initialization==1)
        self.left_box_3_2.setVisible(self.type_of_initialization!=1)

    def set_z0_default(self):
        self.moment_z = self._get_default_initial_z()

    def auto_set_undulator_V(self):
        self.auto_set_undulator(AutoUndulator.VERTICAL)

    def auto_set_undulator_H(self):
        self.auto_set_undulator(AutoUndulator.HORIZONTAL)

    def auto_set_undulator_B(self):
        self.auto_set_undulator(AutoUndulator.BOTH)

    def auto_set_undulator(self, which=AutoUndulator.VERTICAL):
        if not self.distribution_source == 0: raise Exception("This calculation can be performed only for explicit SRW Calculation")
        congruence.checkStrictlyPositiveNumber(self.auto_energy, "Set Undulator at Energy")
        congruence.checkStrictlyPositiveNumber(self.auto_harmonic_number, "As Harmonic #")
        congruence.checkStrictlyPositiveNumber(self.electron_energy_in_GeV, "Energy")
        congruence.checkStrictlyPositiveNumber(self.undulator_period, "Period Length")

        wavelength = self.auto_harmonic_number*m2ev/self.auto_energy
        K = round(numpy.sqrt(2*(((wavelength*2*self._gamma()**2)/self.undulator_period)-1)), 6)

        if which == AutoUndulator.VERTICAL:
            self.Kv = K
            self.Kh = 0.0

        if which == AutoUndulator.BOTH:
            Kboth = round(K / numpy.sqrt(2), 6)
            self.Kv = Kboth
            self.Kh = Kboth

        if which == AutoUndulator.HORIZONTAL:
            self.Kh = K
            self.Kv = 0.0

        self.set_wf_use_harmonic()

    class ShowHelpDialog(QDialog):

        def __init__(self, parent=None):
            QDialog.__init__(self, parent)
            self.setWindowTitle('Symmetry vs Longitudinal Position')
            layout = QVBoxLayout(self)
            label = QLabel("")

            file = os.path.join(resources.package_dirname("orangecontrib.shadow4_advanced.widgets.tools"), "misc", "symmetry.png")

            label.setPixmap(QPixmap(file))

            bbox = QDialogButtonBox(QDialogButtonBox.Ok)

            bbox.accepted.connect(self.accept)
            layout.addWidget(label)
            layout.addWidget(bbox)

    def open_help(self):
        dialog = HybridUndulator.ShowHelpDialog(parent=self)
        dialog.show()

    def set_magnetic_field(self):
        self.magnetic_field_box_1_h.setVisible(self.magnetic_field_from==0)
        self.magnetic_field_box_2_h.setVisible(self.magnetic_field_from==1)
        self.magnetic_field_box_1_v.setVisible(self.magnetic_field_from==0)
        self.magnetic_field_box_2_v.setVisible(self.magnetic_field_from==1)

        self.set_harmonic_energy()

    def set_harmonic_energy(self):
        if self.distribution_source==0 and self.use_harmonic==0:
            self.harmonic_energy = round(self._resonance_energy(), 2)
        else:
            self.harmonic_energy = numpy.nan

    def set_wf_use_harmonic(self):
        self.use_harmonic_box_1.setVisible(self.use_harmonic==0)
        self.use_harmonic_box_2.setVisible(self.use_harmonic==1)
        self.use_harmonic_box_3.setVisible(self.use_harmonic==2)

        self.set_harmonic_energy()

    def set_distribution_source(self):
        self.srw_box.setVisible(self.distribution_source == 0)
        self.srw_files_box.setVisible(self.distribution_source == 1)
        self.ascii_box.setVisible(self.distribution_source == 2)

        self.set_harmonic_energy()

        if self.distribution_source == 0: self.manage_waist_position()
        else:                             self.initialize_waist_position_plot_tab(show=False)

    def set_save_file_srw(self):
        self.save_file_box.setVisible(self.save_srw_result == 1)
        self.save_file_box_empty.setVisible(self.save_srw_result == 0)

    def select_optimize_file(self):
        self.le_optimize_file_name.setText(oasysgui.selectFileFromDialog(self, self.optimize_file_name, "Open Optimize Source Parameters File"))

    def select_source_dimension_file(self):
        self.le_source_dimension_srw_file.setText(oasysgui.selectFileFromDialog(self, self.source_dimension_srw_file, "Open Source Dimension File"))

    def select_angular_distribution_file(self):
        self.le_angular_distribution_srw_file.setText(oasysgui.selectFileFromDialog(self, self.angular_distribution_srw_file, "Open Angular Distribution File"))

    def select_x_positions_file(self):
        self.le_x_positions_file.setText(oasysgui.selectFileFromDialog(self, self.x_positions_file, "Open X Positions File", file_extension_filter="*.dat, *.txt"))

    def select_z_positions_file(self):
        self.le_z_positions_file.setText(oasysgui.selectFileFromDialog(self, self.z_positions_file, "Open Z Positions File", file_extension_filter="*.dat, *.txt"))

    def select_x_divergences_file(self):
        self.le_x_divergences_file.setText(oasysgui.selectFileFromDialog(self, self.x_divergences_file, "Open X Divergences File", file_extension_filter="*.dat, *.txt"))

    def select_z_divergences_file(self):
        self.le_z_divergences_file.setText(oasysgui.selectFileFromDialog(self, self.z_divergences_file, "Open Z Divergences File", file_extension_filter="*.dat, *.txt"))

    def set_which_waist(self):
        self.waist_position_auto = self._get_which_waist_position_auto()

    ####################################################################################
    # SYNED
    ####################################################################################

    def receive_syned_data(self, data):
        if not data is None:
            try:
                OWSynchrotronSource.receive_syned_data(self, data)

                if data.get_beamline_elements_number() > 0:
                    slit_element = data.get_beamline_element_at(0)
                    slit         = slit_element.get_optical_element()
                    coordinates  = slit_element.get_coordinates()

                    if isinstance(slit, Slit) and isinstance(slit.get_boundary_shape(), Rectangle):
                        rectangle = slit.get_boundary_shape()

                        self.source_dimension_wf_h_slit_gap = numpy.abs(rectangle._x_right - rectangle._x_left)
                        self.source_dimension_wf_h_slit_c = 0.5*(rectangle._x_right + rectangle._x_left)
                        self.source_dimension_wf_v_slit_gap = numpy.abs(rectangle._y_top - rectangle._y_bottom)
                        self.source_dimension_wf_v_slit_c = 0.5 * (rectangle._y_top + rectangle._y_bottom)
                        self.source_dimension_wf_distance = coordinates.p()
            except Exception as exception:
                QMessageBox.critical(self, "Error", str(exception), QMessageBox.Ok)

    def receive_specific_syned_data(self, data): pass

    def populate_fields_from_magnetic_structure(self, magnetic_structure, electron_beam):
        self.Kh                  = magnetic_structure._K_horizontal
        self.Kv                  = magnetic_structure._K_vertical
        self.undulator_period    = magnetic_structure._period_length
        self.number_of_periods   = int(magnetic_structure._number_of_periods)  # SRW needs int
        self.magnetic_field_from = 0

        self.set_magnetic_field()
        self.set_harmonic_energy()

    def check_data(self):
        OWSynchrotronSource.check_data(self)

        if self.use_harmonic == 0:
            if self.distribution_source != 0: raise Exception("Harmonic Energy can be computed only for explicit SRW Calculation")

            self.harmonic_number = congruence.checkStrictlyPositiveNumber(self.harmonic_number, "Harmonic Number")
        elif self.use_harmonic == 2:
            if self.distribution_source != 0: raise Exception("Energy Range can be computed only for explicit SRW Calculation")

            self.energy        = congruence.checkStrictlyPositiveNumber(self.energy, "Photon Energy From")
            self.energy_to     = congruence.checkStrictlyPositiveNumber(self.energy_to, "Photon Energy To")
            self.energy_points = congruence.checkStrictlyPositiveNumber(self.energy_points, "Nr. Energy Values")
            congruence.checkGreaterThan(self.energy_to, self.energy, "Photon Energy To", "Photon Energy From")
        else:
            self.energy = congruence.checkStrictlyPositiveNumber(self.energy, "Photon Energy")

    def check_magnetic_structure(self):
        if self.magnetic_field_from == 0:
            self.Kh = congruence.checkPositiveNumber(self.Kh, "K Horizontal")
            self.Kv = congruence.checkPositiveNumber(self.Kv, "K Vertical")
        else:
            self.Bh = congruence.checkPositiveNumber(self.Bh, "B Horizontal")
            self.Bv = congruence.checkPositiveNumber(self.Bv, "B Vertical")

        self.undulator_period  = congruence.checkStrictlyPositiveNumber(self.undulator_period , "Undulator Period")
        self.number_of_periods = congruence.checkStrictlyPositiveNumber(self.number_of_periods, "Number of Periods")

    def get_magnetic_structure(self):
        return S4HybridUndulator(
            K_vertical=self.Kv if self.magnetic_field_from == 0 else K_from_magnetic_field(self.Bv),
            K_horizontal=self.Kh if self.magnetic_field_from == 0 else K_from_magnetic_field(self.Bh),
            number_of_periods=self.number_of_periods,
            period_length=self.undulator_period
        )

    ####################################################################################
    # LOOPS - TRIGGER
    ####################################################################################

    def set_trigger_parameters_for_sources(self, trigger):
        self.compute_power             = False
        self.energy_step               = None
        self.do_cumulated_calculations = False

        if trigger and trigger.new_object == True:
            if not trigger.has_additional_parameter("start_event"):
                self.cumulated_energies        = None
                self.cumulated_integrated_flux = None
                self.cumulated_power_density   = None
                self.cumulated_power           = None

            if trigger.has_additional_parameter("energy_value") and trigger.has_additional_parameter("energy_step"):
                self.compute_power             = True
                self.use_harmonic              = 1
                self.distribution_source       = 0
                self.save_srw_result           = 0
                self.do_cumulated_calculations = True

                if trigger.has_additional_parameter("start_event") and trigger.get_additional_parameter("start_event") == True:
                    self.cumulated_energies        = None
                    self.cumulated_integrated_flux = None
                    self.cumulated_power_density   = None
                    self.cumulated_power           = None

                self.energy       = trigger.get_additional_parameter("energy_value")
                self.energy_step  = trigger.get_additional_parameter("energy_step")
                self.power_step   = trigger.get_additional_parameter("power_step")
                self.current_step = trigger.get_additional_parameter("current_step")
                self.total_steps  = trigger.get_additional_parameter("total_steps")
                self.start_event  = trigger.get_additional_parameter("start_event")

                self.set_wf_use_harmonic()
                self.set_distribution_source()
                self.set_save_file_srw()

        OWSynchrotronSource.set_trigger_parameters_for_sources(self, trigger)

    ####################################################################################
    # SHADOW
    ####################################################################################

    def run_shadow4(self, scanning_data = None):
        if not scanning_data: scanning_data = None

        self.setStatusMessage("")
        self.progressBarInit()

        sys.stdout = EmittingStream(textWritten=self._write_stdout)

        try:
            self.check_data()

            hybrid_input_parameters = HybridUndulatorInputParameters(
                electron_beam                                               = self.get_electron_beam(),
                magnetic_structure                                          = self.get_magnetic_structure(),
                number_of_rays                                              = self.number_of_rays,
                seed                                                        = self.seed,
                use_harmonic                                                = self.use_harmonic,
                harmonic_number                                             = self.harmonic_number,
                energy                                                      = self.energy,
                energy_to                                                   = self.energy_to,
                energy_points                                               = self.energy_points,
                initial_phase_vertical                                      = self.initial_phase_vertical,
                initial_phase_horizontal                                    = self.initial_phase_horizontal,
                symmetry_vs_longitudinal_position_vertical                  = self.symmetry_vs_longitudinal_position_vertical,
                symmetry_vs_longitudinal_position_horizontal                = self.symmetry_vs_longitudinal_position_horizontal,
                horizontal_central_position                                 = self.horizontal_central_position,
                vertical_central_position                                   = self.vertical_central_position,
                longitudinal_central_position                               = self.longitudinal_central_position,
                type_of_initialization                                      = self.type_of_initialization,
                use_stokes                                                  = self.use_stokes,
                auto_expand                                                 = self.auto_expand,
                auto_expand_rays                                            = self.auto_expand_rays,
                source_dimension_wf_h_slit_gap                              = self.source_dimension_wf_h_slit_gap,
                source_dimension_wf_v_slit_gap                              = self.source_dimension_wf_v_slit_gap,
                source_dimension_wf_h_slit_c                                = self.source_dimension_wf_h_slit_c,
                source_dimension_wf_v_slit_c                                = self.source_dimension_wf_v_slit_c,
                source_dimension_wf_h_slit_points                           = self.source_dimension_wf_h_slit_points,
                source_dimension_wf_v_slit_points                           = self.source_dimension_wf_v_slit_points,
                source_dimension_wf_distance                                = self.source_dimension_wf_distance,
                horizontal_range_modification_factor_at_resizing            = self.horizontal_range_modification_factor_at_resizing,
                horizontal_resolution_modification_factor_at_resizing       = self.horizontal_resolution_modification_factor_at_resizing,
                vertical_range_modification_factor_at_resizing              = self.vertical_range_modification_factor_at_resizing,
                vertical_resolution_modification_factor_at_resizing         = self.vertical_resolution_modification_factor_at_resizing,
                waist_position_calculation                                  = self.waist_position_calculation,
                waist_position                                              = self.waist_position,
                waist_position_auto                                         = self.waist_position_auto,
                waist_position_auto_h                                       = self.waist_position_auto_h,
                waist_position_auto_v                                       = self.waist_position_auto_v,
                waist_back_propagation_parameters                           = self.waist_back_propagation_parameters,
                waist_horizontal_range_modification_factor_at_resizing      = self.waist_horizontal_range_modification_factor_at_resizing,
                waist_horizontal_resolution_modification_factor_at_resizing = self.waist_horizontal_resolution_modification_factor_at_resizing,
                waist_vertical_range_modification_factor_at_resizing        = self.waist_vertical_range_modification_factor_at_resizing,
                waist_vertical_resolution_modification_factor_at_resizing   = self.waist_vertical_resolution_modification_factor_at_resizing,
                which_waist                                                 = self.which_waist,
                number_of_waist_fit_points                                  = self.number_of_waist_fit_points,
                degree_of_waist_fit                                         = self.degree_of_waist_fit,
                use_sigma_or_fwhm                                           = self.use_sigma_or_fwhm,
                waist_position_user_defined                                 = self.waist_position_user_defined,
                kind_of_sampler                                             = self.kind_of_sampler,
                save_srw_result                                             = self.save_srw_result,
                source_dimension_srw_file                                   = self.source_dimension_srw_file,
                angular_distribution_srw_file                               = self.angular_distribution_srw_file,
                x_positions_file                                            = self.x_positions_file,
                z_positions_file                                            = self.z_positions_file,
                x_positions_factor                                          = self.x_positions_factor,
                z_positions_factor                                          = self.z_positions_factor,
                x_divergences_file                                          = self.x_divergences_file,
                z_divergences_file                                          = self.z_divergences_file,
                x_divergences_factor                                        = self.x_divergences_factor,
                z_divergences_factor                                        = self.z_divergences_factor,
                combine_strategy                                            = self.combine_strategy,
                distribution_source                                         = self.distribution_source,
                energy_step                                                 = self.energy_step,
                power_step                                                  = self.power_step,
                compute_power                                               = self.compute_power,
                integrated_flux                                             = self.integrated_flux,
                power_density                                               = self.power_density)

            light_source = S4HybridUndulatorLightSource(name="Shadow4/SRW Undulator Source",
                                                        hybrid_input_parameters=hybrid_input_parameters,
                                                        calculation_listener=self)

            # script
            script = light_source.to_python_code()
            script += "\n\n# test plot\nfrom srxraylib.plot.gol import plot_scatter"
            script += "\nrays = beam.get_rays()"
            script += "\nplot_scatter(1e6 * rays[:, 0], 1e6 * rays[:, 2], title='(X,Z) in microns')"
            self.shadow4_script.set_code(script)

            params = {"do_cumulated_calculations" : self.do_cumulated_calculations}
            output_beam              = light_source.get_beam(**params)
            hybrid_output_parameters = light_source.get_output_parameters()

            self.cumulated_energies        = hybrid_output_parameters.cumulated_energies
            self.cumulated_integrated_flux = hybrid_output_parameters.cumulated_integrated_flux
            self.cumulated_power_density   = hybrid_output_parameters.cumulated_power_density
            self.cumulated_power           = hybrid_output_parameters.cumulated_power

            self.moment_x        = hybrid_output_parameters.moment_x
            self.moment_y        = hybrid_output_parameters.moment_y
            self.moment_z        = hybrid_output_parameters.moment_z
            self.moment_xp       = hybrid_output_parameters.moment_xp
            self.moment_yp       = hybrid_output_parameters.moment_yp

            #
            # send beam and trigger
            #
            output_data = ShadowData(beam=output_beam,
                                     number_of_rays=self.number_of_rays,
                                     beamline=S4Beamline(light_source=light_source))

            self.setStatusMessage("Plotting Results")

            self.progressBarSet(80)

            self._plot_results(output_beam, None, progressBarValue=80)

            if self.distribution_source == 0 and \
                    is_canted_undulator(hybrid_input_parameters) and \
                    self.waist_position_calculation == 1:

                    self.waist_position_auto_h = hybrid_input_parameters.waist_position_auto_h
                    self.waist_position_auto_v = hybrid_input_parameters.waist_position_auto_v
                    self.waist_position_auto   = hybrid_input_parameters.waist_position_auto
                    self.waist_position        = hybrid_input_parameters.waist_position

                    self._plot_waist(hybrid_output_parameters)

            self._plot_cumulated_results(self.do_cumulated_calculations)

            self.setStatusMessage("")

            if self.compute_power and self.energy_step and hybrid_output_parameters.total_power:
                additional_parameters = {}
                additional_parameters["total_power"]        = hybrid_output_parameters.total_power
                additional_parameters["photon_energy_step"] = self.energy_step
                additional_parameters["current_step"]       = self.current_step
                additional_parameters["total_steps"]        = self.total_steps

                output_data.scanning_data = ShadowData.ScanningData("photon_energy", self.energy, "Energy for Power Calculation", "eV", additional_parameters)

            self.Outputs.shadow_data.send(output_data)
            self.Outputs.trigger.send(TriggerIn(new_object=True))
        except Exception as exception:
            QMessageBox.critical(self, "Error", str(exception), QMessageBox.Ok)

            if self.IS_DEVELOP: raise exception

        self.progressBarFinished()

    def _cumulated_plot_data1D(self, dataX, dataY, plot_canvas_index, title="", xtitle="", ytitle=""):
        if self.cumulated_plot_canvas[plot_canvas_index] is None:
            self.cumulated_plot_canvas[plot_canvas_index] = oasysgui.plotWindow()
            self.cumulated_tab[plot_canvas_index].layout().addWidget(self.cumulated_plot_canvas[plot_canvas_index])

        self.cumulated_plot_canvas[plot_canvas_index].addCurve(dataX, dataY,)

        self.cumulated_plot_canvas[plot_canvas_index].resetZoom()
        self.cumulated_plot_canvas[plot_canvas_index].setXAxisAutoScale(True)
        self.cumulated_plot_canvas[plot_canvas_index].setYAxisAutoScale(True)
        self.cumulated_plot_canvas[plot_canvas_index].setGraphGrid(False)

        self.cumulated_plot_canvas[plot_canvas_index].setXAxisLogarithmic(False)
        self.cumulated_plot_canvas[plot_canvas_index].setYAxisLogarithmic(False)
        self.cumulated_plot_canvas[plot_canvas_index].setGraphXLabel(xtitle)
        self.cumulated_plot_canvas[plot_canvas_index].setGraphYLabel(ytitle)
        self.cumulated_plot_canvas[plot_canvas_index].setGraphTitle(title)

    def _cumulated_plot_data2D(self, data2D, dataX, dataY, plot_canvas_index, title="", xtitle="", ytitle=""):

        if self.cumulated_plot_canvas[plot_canvas_index] is None:
            self.cumulated_plot_canvas[plot_canvas_index] = Plot2D()
            self.cumulated_tab[plot_canvas_index].layout().addWidget(self.cumulated_plot_canvas[plot_canvas_index])

        origin = (dataX[0],dataY[0])
        scale = (dataX[1]-dataX[0], dataY[1]-dataY[0])

        data_to_plot = data2D.T

        colormap = {"name":"temperature", "normalization":"linear", "autoscale":True, "vmin":0, "vmax":0, "colors":256}

        self.cumulated_plot_canvas[plot_canvas_index].resetZoom()
        self.cumulated_plot_canvas[plot_canvas_index].setXAxisAutoScale(True)
        self.cumulated_plot_canvas[plot_canvas_index].setYAxisAutoScale(True)
        self.cumulated_plot_canvas[plot_canvas_index].setGraphGrid(False)
        self.cumulated_plot_canvas[plot_canvas_index].setKeepDataAspectRatio(True)
        self.cumulated_plot_canvas[plot_canvas_index].yAxisInvertedAction.setVisible(False)

        self.cumulated_plot_canvas[plot_canvas_index].setXAxisLogarithmic(False)
        self.cumulated_plot_canvas[plot_canvas_index].setYAxisLogarithmic(False)
        self.cumulated_plot_canvas[plot_canvas_index].getMaskAction().setVisible(False)
        self.cumulated_plot_canvas[plot_canvas_index].getRoiAction().setVisible(False)
        self.cumulated_plot_canvas[plot_canvas_index].getColormapAction().setVisible(False)
        self.cumulated_plot_canvas[plot_canvas_index].setKeepDataAspectRatio(False)



        self.cumulated_plot_canvas[plot_canvas_index].addImage(numpy.array(data_to_plot),
                                                     legend="active",
                                                     scale=scale,
                                                     origin=origin,
                                                     colormap=colormap,
                                                     replace=True)

        self.cumulated_plot_canvas[plot_canvas_index].setActiveImage("active")
        self.cumulated_plot_canvas[plot_canvas_index].setGraphXLabel(xtitle)
        self.cumulated_plot_canvas[plot_canvas_index].setGraphYLabel(ytitle)
        self.cumulated_plot_canvas[plot_canvas_index].setGraphTitle(title)

    def _plot_cumulated_results(self, do_cumulated_calculations):
        if not self.cumulated_view_type == 0 and do_cumulated_calculations==True:
            try:
                self.cumulated_view_type_combo.setEnabled(False)

                total_power = str(round(self.cumulated_power[-1], 2))

                self._cumulated_plot_data1D(self.cumulated_energies, self.cumulated_integrated_flux, 0, "Spectral Flux", "Energy [eV]", "Flux [ph/s/0.1%BW]")
                self._cumulated_plot_data1D(self.cumulated_energies, self.cumulated_power, 1,
                                           "Cumulated Power (Total = " + total_power + " W)", "Energy [eV]", "Power [W]")
                self._cumulated_plot_data2D(self.cumulated_power_density, self.dataX, self.dataY, 2,
                                           "Power Density [W/mm^2] (Total Power = " + total_power + " W)", "X [mm]", "Y [mm]")

                self.cumulated_view_type_combo.setEnabled(True)
            except Exception as e:
                self.cumulated_view_type_combo.setEnabled(True)

                raise Exception("Data not plottable: exception: " + str(e))


    def _plot_waist(self, hybrid_output_parameters: HybridUndulatorOutputParameters):
        def plot(direction, positions, sizes_e, sizes_ph, size_ph_an, sizes_tot, waist_position, waist_size):
            self.waist_axes[direction].clear()
            self.waist_axes[direction].set_title(("Horizontal" if direction == 0 else "Vertical") + " Direction\n" +
                                                   "Source size: " + str(round(waist_size * 1e6, 2)) + " " + r'$\mu$' + "m \n" +
                                                   "at " + str(round(waist_position * 1e3, 1)) + " mm from the ID center")

            self.waist_axes[direction].plot(positions * 1e3, sizes_e * 1e6, label='electron', color='g')
            self.waist_axes[direction].plot(positions * 1e3, sizes_ph * 1e6, label='photon', color='b')
            self.waist_axes[direction].plot(positions * 1e3, size_ph_an * 1e6, '--', label='photon (analytical)', color='b')
            self.waist_axes[direction].plot(positions * 1e3, sizes_tot * 1e6, label='total', color='r')
            self.waist_axes[direction].plot([waist_position * 1e3], [waist_size * 1e6], 'bo', label="waist")
            self.waist_axes[direction].set_xlabel("Position relative to ID center [mm]")
            self.waist_axes[direction].set_ylabel("Sigma [um]")
            self.waist_axes[direction].legend()

        plot(0,
             hybrid_output_parameters.positions,
             hybrid_output_parameters.sizes_e_x,
             hybrid_output_parameters.sizes_ph_x,
             hybrid_output_parameters.sizes_ph_an_x,
             hybrid_output_parameters.sizes_tot_x,
             hybrid_output_parameters.waist_position_x,
             hybrid_output_parameters.waist_size_x)
        plot(1,
             hybrid_output_parameters.positions,
             hybrid_output_parameters.sizes_e_y,
             hybrid_output_parameters.sizes_ph_y,
             hybrid_output_parameters.sizes_ph_an_y,
             hybrid_output_parameters.sizes_tot_y,
             hybrid_output_parameters.waist_position_y,
             hybrid_output_parameters.waist_size_y)

        try: self.waist_figure.draw()
        except Exception as e: print(e)

add_widget_parameters_to_module(__name__)