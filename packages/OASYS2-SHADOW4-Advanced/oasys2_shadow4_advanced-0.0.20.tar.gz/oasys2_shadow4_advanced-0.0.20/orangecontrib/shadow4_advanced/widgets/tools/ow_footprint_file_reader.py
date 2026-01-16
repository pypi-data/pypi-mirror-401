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

import numpy

from AnyQt.QtWidgets import QMessageBox

from orangewidget import gui
from orangewidget.settings import Setting
from orangewidget.widget import Input, Output

from oasys2.widget import gui as oasysgui
from oasys2.widget.widget import OWWidget
from oasys2.canvas.util.canvas_util import add_widget_parameters_to_module

try:
    from orangecontrib.shadow4.util.shadow4_objects import ShadowData
    from orangecontrib.shadow4.util.shadow4_util import ShadowCongruence
except ImportError:
    raise ImportError("OASYS2-SHADOW4 add-on required to run OASYS2-SHADOW4-Advanced")

from shadow4.beam.s4_beam import S4Beam
from shadow4.beamline.s4_beamline import S4Beamline
from shadow4.beamline.s4_beamline_element import S4BeamlineElement


class FootprintFileReader(OWWidget):
    name = "Footprint Reader"
    description = "Utility: Footprint Reader"
    icon = "icons/footprint_reader.png"
    maintainer = "Luca Rebuffi"
    maintainer_email = "lrebuffi(@at@)anl.gov"
    priority = 6.2
    category = "Utility"
    keywords = ["data", "file", "load", "read"]

    want_main_area = 0

    input_data = None
    
    class Inputs:
        shadow_data = Input("Shadow Data", ShadowData, default=True, auto_summary=False)

    class Outputs:
        shadow_data = Output("Shadow Data", ShadowData, default=True, auto_summary=False)
        
    kind_of_power = Setting(0)

    def __init__(self):
        super().__init__()

        self.setFixedWidth(585)
        self.setFixedHeight(180)

        left_box_1 = oasysgui.widgetBox(self.controlArea, "Footprint Settings", addSpace=False, orientation="vertical", width=570, height=130)

        gui.comboBox(left_box_1, self, "kind_of_power", label="Kind Of Power",
                     items=["Incident", "Absorbed", "Transmitted"],
                     labelWidth=260, sendSelectedValue=False, orientation="horizontal")

        gui.separator(left_box_1)

        gui.button(left_box_1, self, "Send Footprint", callback=self.manage_footprint, height=45, width=555)

        gui.rubber(self.controlArea)
    
    @Inputs.shadow_data
    def set_shadow_data(self, shadow_data):
        if ShadowCongruence.check_empty_data(shadow_data):
            if ShadowCongruence.check_good_beam(shadow_data.beam):
                self.input_data = shadow_data

                self.manage_footprint()
        else:
            self.input_data = None

    def manage_footprint(self):
        self.setStatusMessage("")

        try:
            if ShadowCongruence.check_empty_data(self.input_data):
                if ShadowCongruence.check_good_beam(self.input_data.beam) and not self.input_data.footprint is None:
                    beamline: S4Beamline = self.input_data.beamline
                    output_beam: S4Beam  = self.input_data.footprint.duplicate()
    
                    is_scanning = self.input_data.scanning_data and self.input_data.scanning_data.has_additional_parameter("total_power")
    
                    additional_parameters = {}
                    if is_scanning:
                        total_power = self.input_data.scanning_data.get_additional_parameter("total_power")
    
                        additional_parameters["total_power"]        = total_power
                        additional_parameters["current_step"]       = self.input_data.scanning_data.get_additional_parameter("current_step")
                        additional_parameters["total_steps"]        = self.input_data.scanning_data.get_additional_parameter("total_steps")
                        additional_parameters["photon_energy_step"] = self.input_data.scanning_data.get_additional_parameter("photon_energy_step")
                    additional_parameters["is_footprint"] = True
                    
                    last_oe: S4BeamlineElement = beamline.get_beamline_element_at(-1)
                    
                    incident_beam    = last_oe.get_input_beam()
                    transmitted_beam = self.input_data.beam
    
                    if is_scanning:
                        n_rays = incident_beam.get_number_of_rays() # lost and good!
    
                        ticket = incident_beam.histo2(1, 3, nbins=100, xrange=None, yrange=None, nolost=1, ref=23)
                        ticket['histogram'] *= (total_power/n_rays) # power
    
                        additional_parameters["incident_power"] = ticket['histogram'].sum()
    
                    if self.kind_of_power == 0: # incident
                        output_beam.rays[:, 6]  = incident_beam.rays[:, 6]
                        output_beam.rays[:, 7]  = incident_beam.rays[:, 7]
                        output_beam.rays[:, 8]  = incident_beam.rays[:, 8]
                        output_beam.rays[:, 15] = incident_beam.rays[:, 15]
                        output_beam.rays[:, 16] = incident_beam.rays[:, 16]
                        output_beam.rays[:, 17] = incident_beam.rays[:, 17]
                    elif self.kind_of_power == 1: # absorbed
                        # need a trick: put the whole intensity of one single component
                        incident_intensity = incident_beam.rays[:, 6]**2 + \
                                             incident_beam.rays[:, 7]**2 + \
                                             incident_beam.rays[:, 8]**2 +\
                                             incident_beam.rays[:, 15]**2 + \
                                             incident_beam.rays[:, 16]**2 + \
                                             incident_beam.rays[:, 17]**2
                        transmitted_intensity = transmitted_beam.rays[:, 6]**2 + \
                                                transmitted_beam.rays[:, 7]**2 + \
                                                transmitted_beam.rays[:, 8]**2 +\
                                                transmitted_beam.rays[:, 15]**2 + \
                                                transmitted_beam.rays[:, 16]**2 + \
                                                transmitted_beam.rays[:, 17]**2
    
                        electric_field = numpy.sqrt(incident_intensity - transmitted_intensity)
                        electric_field[numpy.where(numpy.isnan(electric_field))] = 0.0
    
                        output_beam.rays[:, 6]  = electric_field
                        output_beam.rays[:, 7]  = 0.0
                        output_beam.rays[:, 8]  = 0.0
                        output_beam.rays[:, 15] = 0.0
                        output_beam.rays[:, 16] = 0.0
                        output_beam.rays[:, 17] = 0.0
                    elif self.kind_of_power == 2: # transmitted
                        output_beam.rays[:, 6]  = transmitted_beam.rays[:, 6]
                        output_beam.rays[:, 7]  = transmitted_beam.rays[:, 7]
                        output_beam.rays[:, 8]  = transmitted_beam.rays[:, 8]
                        output_beam.rays[:, 15] = transmitted_beam.rays[:, 15]
                        output_beam.rays[:, 16] = transmitted_beam.rays[:, 16]
                        output_beam.rays[:, 17] = transmitted_beam.rays[:, 17]

                    output_data = ShadowData(beamline=beamline,
                                             beam=output_beam,
                                             footprint=output_beam)
                    if is_scanning:
                        output_data.scanning_data = ShadowData.ScanningData(self.input_data.scanning_data.scanned_variable_name,
                                                                            self.input_data.scanning_data.scanned_variable_value,
                                                                            self.input_data.scanning_data.scanned_variable_display_name,
                                                                            self.input_data.scanning_data.scanned_variable_um,
                                                                            additional_parameters=additional_parameters)
                    else:
                        output_data.scanning_data = ShadowData.ScanningData(None, None, None, None,
                                                                            additional_parameters=additional_parameters)
    
                    self.Outputs.shadow_data.send(output_data)
        except Exception as exception:
            QMessageBox.critical(self, "Error", str(exception), QMessageBox.Ok)

            if self.IS_DEVELOP: raise exception

add_widget_parameters_to_module(__name__)