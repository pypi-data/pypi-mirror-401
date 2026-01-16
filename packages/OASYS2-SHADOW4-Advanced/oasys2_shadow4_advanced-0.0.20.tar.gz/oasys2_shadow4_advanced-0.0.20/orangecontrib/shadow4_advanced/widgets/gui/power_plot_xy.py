#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------- #
# Copyright (c) 2022, UChicago Argonne, LLC. All rights reserved.         #
#                                                                         #
# Copyright 2022. UChicago Argonne, LLC. This software was produced       #
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
# ----------------------------------------------------------------------- #

import os, sys, copy, re
import time
import numpy
import scipy.ndimage.filters as filters
import scipy.ndimage.interpolation as interpolation
import scipy.ndimage.fourier as fourier
from scipy.optimize import least_squares
from numpy.polynomial.polynomial import polyval2d

from AnyQt.QtWidgets import QMessageBox, QInputDialog, QDialog, \
    QLabel, QVBoxLayout, QDialogButtonBox, QSizePolicy, QWidget
from AnyQt.QtGui import QTextCursor, QPixmap, QFont, QColor, QPalette
from AnyQt.QtCore import Qt

from silx.gui.plot import Plot2D

import orangecanvas.resources as resources

from orangewidget import gui
from orangewidget.settings import Setting
from orangewidget.widget import Input

from oasys2.widget import gui as oasysgui
from oasys2.widget.util import congruence
from oasys2.widget.util.widget_util import EmittingStream

from shadow4.beam.s4_beam import S4Beam

try:
    from orangecontrib.shadow4.util.shadow4_objects import ShadowData
    from orangecontrib.shadow4.util.shadow4_util import ShadowCongruence, ShadowPlot, ShadowPhysics
    from orangecontrib.shadow4.widgets.gui.ow_automatic_element import AutomaticElement
except ImportError:
    raise ImportError("OASYS2-SHADOW4 add-on required to run OASYS2-SHADOW4-Advanced")

try:    from mpl_toolkits.mplot3d import Axes3D  # mandatory to load 3D plot
except: pass
from matplotlib.colors import LinearSegmentedColormap, Normalize

cdict_temperature = {'red': ((0.0, 0.0, 0.0),
                             (0.5, 0.0, 0.0),
                             (0.75, 1.0, 1.0),
                             (1.0, 1.0, 1.0)),
                     'green': ((0.0, 0.0, 0.0),
                               (0.25, 1.0, 1.0),
                               (0.75, 1.0, 1.0),
                               (1.0, 0.0, 0.0)),
                     'blue': ((0.0, 1.0, 1.0),
                              (0.25, 1.0, 1.0),
                              (0.5, 0.0, 0.0),
                              (1.0, 0.0, 0.0))}

cmap_temperature = LinearSegmentedColormap('temperature', cdict_temperature, 256)

import scipy.constants as codata

TO_MM = 1e3

class PowerPlotXYWidget(QWidget):
    def __init__(self, parent=None):
        pass

        super(QWidget, self).__init__(parent=parent)

        self.plot_canvas = None
        self.cumulated_power_plot = 0.0
        self.cumulated_previous_power_plot = 0.0

        self.setLayout(QVBoxLayout())

    def manage_empty_beam(self, ticket_to_add, nbins_h, nbins_v, xrange, yrange, var_x, var_y, cumulated_total_power, energy_min, energy_max, energy_step, show_image, cumulated_quantity=0):
        if not ticket_to_add is None:
            ticket = copy.deepcopy(ticket_to_add)
            last_ticket = copy.deepcopy(ticket_to_add)
        else:
            ticket = {}
            ticket["histogram"] = numpy.zeros((nbins_h, nbins_v))
            ticket['intensity'] = numpy.zeros((nbins_h, nbins_v))
            ticket['nrays'] = 0
            ticket['good_rays'] = 0

            if not xrange is None and not yrange is None:
                ticket['bin_h_center'] = numpy.arange(xrange[0], xrange[1], nbins_h) * TO_MM
                ticket['bin_v_center'] = numpy.arange(yrange[0], yrange[1], nbins_v) * TO_MM
            else:
                raise ValueError("Beam is empty and no range has been specified: Calculation is impossible")

        self.plot_power_density_ticket(ticket, var_x, var_y, cumulated_total_power, energy_min, energy_max, energy_step, show_image, cumulated_quantity)

        if not ticket_to_add is None:
            return ticket, last_ticket
        else:
            return ticket, None

    def plot_power_density_BM(self, shadow_data, initial_energy, initial_flux, nbins_interpolation,
                              var_x, var_y, nbins_h=100, nbins_v=100, xrange=None, yrange=None, nolost=1, show_image=True, cumulated_quantity=0):
        n_rays = len(shadow_data.beam.rays[:, 0])  # lost and good!

        if n_rays == 0:
            ticket, _ = self.manage_empty_beam(None,
                                               nbins_h,
                                               nbins_v,
                                               xrange,
                                               yrange,
                                               var_x,
                                               var_y,
                                               0.0,
                                               0.0,
                                               0.0,
                                               0.0,
                                               show_image)
            return ticket
        
        beamline = shadow_data.beamline
        first_oe = beamline.get_beamline_element_at(0)
        last_oe  = beamline.get_beamline_element_at(-1)
        
        source_beam = first_oe.get_input_beam()

        if last_oe.get_input_beam() is None: previous_beam = shadow_data.beam
        else:                                previous_beam = last_oe.get_input_beam().duplicate()

        rays_energy  = ShadowPhysics.getEnergyFromShadowK(shadow_data.beam.rays[:, 10])
        energy_range = [numpy.min(rays_energy), numpy.max(rays_energy)]

        ticket_initial = source_beam.histo1(26, xrange=energy_range, nbins=nbins_interpolation, nolost=1, ref=23)

        energy_bins = ticket_initial["bin_center"]

        energy_min  = energy_bins[0]
        energy_max  = energy_bins[-1]
        energy_step = energy_bins[1] - energy_bins[0]

        initial_flux_shadow  = numpy.interp(energy_bins, initial_energy, initial_flux, left=initial_flux[0], right=initial_flux[-1])
        initial_power_shadow = initial_flux_shadow * 1e3 * codata.e * energy_step

        total_initial_power_shadow = initial_power_shadow.sum()

        print("Total Initial Power from Shadow", total_initial_power_shadow)

        if nolost > 1:  # must be calculating only the rays the become lost in the last object
            current_beam = shadow_data.beam

            if last_oe.get_input_beam() is None: 
                beam = shadow_data.beam
            else:
                if nolost == 2:
                    current_lost_rays_cursor = numpy.where(current_beam.rays[:, 9] != 1)

                    current_lost_rays = current_beam.rays[current_lost_rays_cursor]
                    lost_rays_in_previous_beam = previous_beam.rays[current_lost_rays_cursor]

                    lost_that_were_good_rays_cursor = numpy.where(lost_rays_in_previous_beam[:, 9] == 1)

                    beam = S4Beam()
                    beam.rays = current_lost_rays[lost_that_were_good_rays_cursor]  # lost rays that were good after the previous OE

                    # in case of filters, Shadow computes the absorption for lost rays. This cause an imbalance on the total power.
                    # the lost rays that were good must have the same intensity they had before the optical element.

                    beam.rays[:, 6]  = lost_rays_in_previous_beam[lost_that_were_good_rays_cursor][:, 6]
                    beam.rays[:, 7]  = lost_rays_in_previous_beam[lost_that_were_good_rays_cursor][:, 7]
                    beam.rays[:, 8]  = lost_rays_in_previous_beam[lost_that_were_good_rays_cursor][:, 8]
                    beam.rays[:, 15] = lost_rays_in_previous_beam[lost_that_were_good_rays_cursor][:, 15]
                    beam.rays[:, 16] = lost_rays_in_previous_beam[lost_that_were_good_rays_cursor][:, 16]
                    beam.rays[:, 17] = lost_rays_in_previous_beam[lost_that_were_good_rays_cursor][:, 17]
                    beam.rays[:, 9]  = 1
                else:
                    incident_rays    = previous_beam.rays
                    transmitted_rays = current_beam.rays

                    incident_intensity = incident_rays[:, 6] ** 2 + incident_rays[:, 7] ** 2 + incident_rays[:, 8] ** 2 + \
                                         incident_rays[:, 15] ** 2 + incident_rays[:, 16] ** 2 + incident_rays[:, 17] ** 2
                    transmitted_intensity = transmitted_rays[:, 6] ** 2 + transmitted_rays[:, 7] ** 2 + transmitted_rays[:, 8] ** 2 + \
                                            transmitted_rays[:, 15] ** 2 + transmitted_rays[:, 16] ** 2 + transmitted_rays[:, 17] ** 2

                    electric_field = numpy.sqrt(incident_intensity - transmitted_intensity)
                    electric_field[numpy.where(electric_field == numpy.nan)] = 0.0

                    beam = S4Beam()
                    beam.rays = copy.deepcopy(shadow_data.beam.rays)

                    beam.rays[:, 6] = electric_field
                    beam.rays[:, 7] = 0.0
                    beam.rays[:, 8] = 0.0
                    beam.rays[:, 15] = 0.0
                    beam.rays[:, 16] = 0.0
                    beam.rays[:, 17] = 0.0
        else:
            beam = shadow_data.beam

        if len(beam.rays) == 0:
            ticket, _ = self.manage_empty_beam(None,
                                               nbins_h,
                                               nbins_v,
                                               xrange,
                                               yrange,
                                               var_x,
                                               var_y,
                                               0.0,
                                               energy_min,
                                               energy_max,
                                               energy_step,
                                               show_image)
            return ticket

        ticket_incident = previous_beam.histo1(26, xrange=energy_range, nbins=nbins_interpolation, nolost=1, ref=23)  # intensity of good rays per bin incident
        ticket_final    = beam.histo1(26, xrange=energy_range, nbins=nbins_interpolation, nolost=1, ref=23)  # intensity of good rays per bin

        good = numpy.where(ticket_initial["histogram"] > 0)

        efficiency_incident = numpy.zeros(len(ticket_incident["histogram"]))
        efficiency_incident[good] = ticket_incident["histogram"][good] / ticket_initial["histogram"][good]

        incident_power_shadow = initial_power_shadow * efficiency_incident

        total_incident_power_shadow = incident_power_shadow.sum()
        print("Total Incident Power from Shadow", total_incident_power_shadow)

        efficiency_final = numpy.zeros(len(ticket_final["histogram"]))
        efficiency_final[good] = ticket_final["histogram"][good] / ticket_initial["histogram"][good]

        final_power_shadow = initial_power_shadow * efficiency_final

        total_final_power_shadow = final_power_shadow.sum()
        print("Total Final Power from Shadow", total_final_power_shadow)

        # CALCULATE POWER DENSITY PER EACH RAY -------------------------------------------------------

        ticket = beam.histo1(26, xrange=energy_range, nbins=nbins_interpolation, nolost=1, ref=0)  # number of rays per bin
        good   = numpy.where(ticket["histogram"] > 0)

        final_power_per_ray = numpy.zeros(len(final_power_shadow))
        final_power_per_ray[good] = final_power_shadow[good] / ticket["histogram"][good]

        go = numpy.where(beam.rays[:, 9] == 1)

        rays_energy = ShadowPhysics.getEnergyFromShadowK(beam.rays[go, 10])

        ticket = beam.histo2(var_x, var_y, nbins_h=nbins_h, nbins_v=nbins_v, xrange=xrange, yrange=yrange, nolost=1, ref=0)

        ticket['bin_h_center'] *= TO_MM
        ticket['bin_v_center'] *= TO_MM
        pixel_area = (ticket['bin_h_center'][1] - ticket['bin_h_center'][0]) * (ticket['bin_v_center'][1] - ticket['bin_v_center'][0])

        power_density = numpy.interp(rays_energy, energy_bins, final_power_per_ray, left=0, right=0) / pixel_area

        final_beam = S4Beam()
        final_beam.rays = copy.deepcopy(beam.rays)

        final_beam.rays[go, 6] = numpy.sqrt(power_density)
        final_beam.rays[go, 7] = 0.0
        final_beam.rays[go, 8] = 0.0
        final_beam.rays[go, 15] = 0.0
        final_beam.rays[go, 16] = 0.0
        final_beam.rays[go, 17] = 0.0

        ticket = final_beam.histo2(var_x, var_y,
                                   nbins_h=nbins_h, nbins_v=nbins_v, xrange=xrange, yrange=yrange,
                                   nolost=1, ref=23)

        ticket['histogram'][numpy.where(ticket['histogram'] < 1e-15)] = 0.0

        ticket['h_label'] = var_x
        ticket['v_label'] = var_y

        self.cumulated_previous_power_plot = total_incident_power_shadow
        self.cumulated_power_plot = total_final_power_shadow

        self.plot_power_density_ticket(ticket, var_x, var_y, total_initial_power_shadow, energy_min, energy_max, energy_step, show_image, cumulated_quantity)

        return ticket

    def plot_power_density(self, shadow_data, var_x, var_y, total_power, cumulated_total_power, energy_min, energy_max, energy_step,
                           nbins_h=100, nbins_v=100, xrange=None, yrange=None, nolost=1, ticket_to_add=None, show_image=True,
                           kind_of_calculation=0,
                           replace_poor_statistic=0,
                           good_rays_limit=100,
                           center_x=0.0,
                           center_y=0.0,
                           sigma_x=1.0,
                           sigma_y=1.0,
                           gamma=1.0,
                           cumulated_quantity=0):

        n_rays = shadow_data.beam.get_number_of_rays()  # lost and good!

        if n_rays == 0:
            return self.manage_empty_beam(ticket_to_add,
                                          nbins_h,
                                          nbins_v,
                                          xrange,
                                          yrange,
                                          var_x,
                                          var_y,
                                          cumulated_total_power,
                                          energy_min,
                                          energy_max,
                                          energy_step,
                                          show_image)


        beamline = shadow_data.beamline
        if not beamline is None: last_oe = beamline.get_beamline_element_at(-1)
        else:                    last_oe = None

        previous_beam = None

        if shadow_data.scanning_data and shadow_data.scanning_data.has_additional_parameter("incident_power"):
            self.cumulated_previous_power_plot += shadow_data.scanning_data.get_additional_parameter("incident_power")
        elif not last_oe is None and not last_oe.get_input_beam() is None:
            previous_ticket = last_oe.get_input_beam().histo2(var_x, var_y, nbins_h=nbins_h, nbins_v=nbins_v, xrange=None, yrange=None, nolost=1, ref=23)
            previous_ticket['histogram'] *= (total_power / n_rays)  # power

            self.cumulated_previous_power_plot += previous_ticket['histogram'].sum()

        if nolost > 1:  # must be calculating only the rays the become lost in the last object
            current_beam = shadow_data

            if last_oe is None or last_oe.get_input_beam() is None:
                beam = shadow_data.beam
            else:
                previous_beam = previous_beam if previous_beam else last_oe.get_input_beam().duplicate()

                if nolost == 2:
                    current_lost_rays_cursor = numpy.where(current_beam.rays[:, 9] != 1)

                    current_lost_rays = current_beam.rays[current_lost_rays_cursor]
                    lost_rays_in_previous_beam = previous_beam.rays[current_lost_rays_cursor]

                    lost_that_were_good_rays_cursor = numpy.where(lost_rays_in_previous_beam[:, 9] == 1)

                    beam = S4Beam()
                    beam.rays = current_lost_rays[lost_that_were_good_rays_cursor]  # lost rays that were good after the previous OE

                    # in case of filters, Shadow computes the absorption for lost rays. This cause an imbalance on the total power.
                    # the lost rays that were good must have the same intensity they had before the optical element.

                    beam.rays[:, 6] = lost_rays_in_previous_beam[lost_that_were_good_rays_cursor][:, 6]
                    beam.rays[:, 7] = lost_rays_in_previous_beam[lost_that_were_good_rays_cursor][:, 7]
                    beam.rays[:, 8] = lost_rays_in_previous_beam[lost_that_were_good_rays_cursor][:, 8]
                    beam.rays[:, 15] = lost_rays_in_previous_beam[lost_that_were_good_rays_cursor][:, 15]
                    beam.rays[:, 16] = lost_rays_in_previous_beam[lost_that_were_good_rays_cursor][:, 16]
                    beam.rays[:, 17] = lost_rays_in_previous_beam[lost_that_were_good_rays_cursor][:, 17]
                    beam.rays[:, 9] = 1
                else:
                    incident_rays    = previous_beam.rays
                    transmitted_rays = current_beam.rays

                    incident_intensity = incident_rays[:, 6] ** 2 + incident_rays[:, 7] ** 2 + incident_rays[:, 8] ** 2 + \
                                         incident_rays[:, 15] ** 2 + incident_rays[:, 16] ** 2 + incident_rays[:, 17] ** 2
                    transmitted_intensity = transmitted_rays[:, 6] ** 2 + transmitted_rays[:, 7] ** 2 + transmitted_rays[:, 8] ** 2 + \
                                            transmitted_rays[:, 15] ** 2 + transmitted_rays[:, 16] ** 2 + transmitted_rays[:, 17] ** 2

                    electric_field = numpy.sqrt(incident_intensity - transmitted_intensity)
                    electric_field[numpy.where(electric_field == numpy.nan)] = 0.0

                    beam = S4Beam()
                    beam.rays = copy.deepcopy(shadow_data.beam.rays)

                    beam.rays[:, 6] = electric_field
                    beam.rays[:, 7] = 0.0
                    beam.rays[:, 8] = 0.0
                    beam.rays[:, 15] = 0.0
                    beam.rays[:, 16] = 0.0
                    beam.rays[:, 17] = 0.0
        else:
            beam = shadow_data.beam

        if len(beam.rays) == 0:
            return self.manage_empty_beam(ticket_to_add,
                                          nbins_h,
                                          nbins_v,
                                          xrange,
                                          yrange,
                                          var_x,
                                          var_y,
                                          cumulated_total_power,
                                          energy_min,
                                          energy_max,
                                          energy_step,
                                          show_image)

        ticket = beam.histo2(var_x, var_y, nbins_h=nbins_h, nbins_v=nbins_v, xrange=xrange, yrange=yrange, nolost=1 if nolost != 2 else 2, ref=23)

        ticket['bin_h_center'] *= TO_MM
        ticket['bin_v_center'] *= TO_MM

        bin_h_size = (ticket['bin_h_center'][1] - ticket['bin_h_center'][0])
        bin_v_size = (ticket['bin_v_center'][1] - ticket['bin_v_center'][0])

        if kind_of_calculation > 0:
            if replace_poor_statistic == 0 or (replace_poor_statistic == 1 and ticket['good_rays'] < good_rays_limit):
                if kind_of_calculation == 1:  # FLAT
                    PowerPlotXYWidget.get_flat_2d(ticket['histogram'], ticket['bin_h_center'], ticket['bin_v_center'])
                elif kind_of_calculation == 2:  # GAUSSIAN
                    PowerPlotXYWidget.get_gaussian_2d(ticket['histogram'], ticket['bin_h_center'], ticket['bin_v_center'],
                                                      sigma_x, sigma_y, center_x, center_y)
                elif kind_of_calculation == 3:  # LORENTZIAN
                    PowerPlotXYWidget.get_lorentzian_2d(ticket['histogram'], ticket['bin_h_center'], ticket['bin_v_center'],
                                                        gamma, center_x, center_y)
                # rinormalization
                ticket['histogram'] *= ticket['intensity']

        ticket['histogram'][numpy.where(ticket['histogram'] < 1e-9)] = 0.0
        ticket['histogram'] *= (total_power / n_rays)  # power

        if ticket_to_add == None:
            self.cumulated_power_plot = ticket['histogram'].sum()
        else:
            self.cumulated_power_plot += ticket['histogram'].sum()

        ticket['histogram'] /= (bin_h_size * bin_v_size)  # power density

        if not ticket_to_add is None:
            last_ticket = copy.deepcopy(ticket)

            ticket['histogram'] += ticket_to_add['histogram']
            ticket['intensity'] += ticket_to_add['intensity']
            ticket['nrays'] += ticket_to_add['nrays']
            ticket['good_rays'] += ticket_to_add['good_rays']

        ticket['h_label'] = var_x
        ticket['v_label'] = var_y

        # data for reload of the file
        ticket['energy_min'] = energy_min
        ticket['energy_max'] = energy_max
        ticket['energy_step'] = energy_step
        ticket['plotted_power'] = self.cumulated_power_plot
        ticket['incident_power'] = self.cumulated_previous_power_plot
        ticket['total_power'] = cumulated_total_power

        self.plot_power_density_ticket(ticket, var_x, var_y, cumulated_total_power, energy_min, energy_max, energy_step, show_image, cumulated_quantity)

        if not ticket_to_add is None:
            return ticket, last_ticket
        else:
            return ticket, None

    def plot_power_density_ticket(self, ticket, var_x, var_y, cumulated_total_power, energy_min, energy_max, energy_step, show_image=True, cumulated_quantity=0):
        if show_image:
            histogram = ticket['histogram']

            average_power_density = numpy.average(histogram[numpy.where(histogram > 0.0)])

            if cumulated_quantity == 0:  # Power density
                title = "Power Density [W/mm\u00b2] from " + str(round(energy_min, 2)) + " to " + str(round(energy_max + energy_step, 2)) + " [eV], Current Step: " + str(round(energy_step, 2)) + "\n" + \
                        "Power [W]: Plot=" + str(round(self.cumulated_power_plot, 3)) + \
                        ", Incid.=" + str(round(self.cumulated_previous_power_plot, 3)) + \
                        ", Tot.=" + str(round(cumulated_total_power, 3)) + \
                        ", <PD>=" + str(round(average_power_density, 3)) + " W/mm\u00b2"
            elif cumulated_quantity == 1:  # Intensity
                title = "Intensity [ph/s/mm\u00b2] from " + str(round(energy_min, 2)) + " to " + str(round(energy_max + energy_step, 2)) + " [eV], Current Step: " + str(round(energy_step, 2)) + "\n" + \
                        "Flux [ph/s]: Plot=" + "{:.1e}".format(self.cumulated_power_plot) + \
                        ", Incid.=" + "{:.1e}".format(self.cumulated_previous_power_plot) + \
                        ", Tot.=" + "{:.1e}".format(cumulated_total_power) + \
                        ", <I>=" + "{:.2e}".format(average_power_density) + " ph/s/mm\u00b2"

            xx = ticket['bin_h_center']
            yy = ticket['bin_v_center']

            if not isinstance(var_x, str): var_x = self.get_label(var_x)
            if not isinstance(var_y, str): var_y = self.get_label(var_y)

            self.plot_data2D(histogram, xx, yy, title, var_x, var_y)

    def get_label(self, var):
        if var == 1:
            return "X [mm]"
        elif var == 2:
            return "Y [mm]"
        elif var == 3:
            return "Z [mm]"

    def plot_data2D(self, data2D, dataX, dataY, title="", xtitle="", ytitle=""):
        if self.plot_canvas is None:
            self.plot_canvas = Plot2D()

            self.plot_canvas.resetZoom()
            self.plot_canvas.setXAxisAutoScale(True)
            self.plot_canvas.setYAxisAutoScale(True)
            self.plot_canvas.setGraphGrid(False)
            self.plot_canvas.setKeepDataAspectRatio(False)
            self.plot_canvas.yAxisInvertedAction.setVisible(False)

            self.plot_canvas.setXAxisLogarithmic(False)
            self.plot_canvas.setYAxisLogarithmic(False)
            self.plot_canvas.getMaskAction().setVisible(False)
            self.plot_canvas.getRoiAction().setVisible(False)
            self.plot_canvas.getColormapAction().setVisible(True)

        origin = (dataX[0], dataY[0])
        scale = (dataX[1] - dataX[0], dataY[1] - dataY[0])

        self.plot_canvas.addImage(numpy.array(data2D.T),
                                  legend="power",
                                  scale=scale,
                                  origin=origin,
                                  colormap={"name": "temperature", "normalization": "linear", "autoscale": True, "vmin": 0, "vmax": 0, "colors": 256},
                                  replace=True)

        self.plot_canvas.setActiveImage("power")

        self.plot_canvas.setGraphXLabel(xtitle)
        self.plot_canvas.setGraphYLabel(ytitle)
        self.plot_canvas.setGraphTitle(title)

        self.plot_canvas.resetZoom()
        self.plot_canvas.setXAxisAutoScale(True)
        self.plot_canvas.setYAxisAutoScale(True)

        layout = self.layout()
        layout.addWidget(self.plot_canvas)
        self.setLayout(layout)

    def clear(self):
        if not self.plot_canvas is None:
            self.plot_canvas.clear()
            self.cumulated_power_plot = 0.0
            self.cumulated_previous_power_plot = 0.0

    @classmethod
    def get_flat_2d(cls, z, x, y):
        for i in range(len(x)):
            z[i, :] = 1

        norm = numpy.sum(z)
        z[:, :] /= norm

    @classmethod
    def get_gaussian_2d(cls, z, x, y, sigma_x, sigma_y, center_x=0.0, center_y=0.0):
        for i in range(len(x)):
            z[i, :] = numpy.exp(-1 * (0.5 * ((x[i] - center_x) / sigma_x) ** 2 + 0.5 * ((y - center_y) / sigma_y) ** 2))

        norm = numpy.sum(z)
        z[:, :] /= norm

    @classmethod
    def get_lorentzian_2d(cls, z, x, y, gamma, center_x=0.0, center_y=0.0):
        for i in range(len(x)):
            z[i, :] = gamma / (((x[i] - center_x) ** 2 + (y - center_y) ** 2 + gamma ** 2))

        norm = numpy.sum(z)
        z[:, :] /= norm

class AbstractPowerPlotXY(AutomaticElement):

    maintainer = "Luca Rebuffi"
    maintainer_email = "lrebuffi(@at@)anl.gov"
    category = "Display Data Tools"
    keywords = ["data", "file", "load", "read"]

    class Inputs:
        shadow_data = Input("Shadow Data", ShadowData, default=True, auto_summary=False)

    IMAGE_WIDTH = 878
    IMAGE_HEIGHT = 570

    want_main_area=1
    plot_canvas=None
    input_data=None

    image_plane=Setting(0)
    image_plane_new_position=Setting(10.0)
    image_plane_rel_abs_position=Setting(0)

    x_column_index=Setting(0)
    y_column_index=Setting(2)

    x_range=Setting(0)
    x_range_min=Setting(0.0)
    x_range_max=Setting(0.0)

    y_range=Setting(0)
    y_range_min=Setting(0.0)
    y_range_max=Setting(0.0)

    rays=Setting(1)
    number_of_bins=Setting(100) # for retrocompatibility: I don't change the name
    number_of_bins_v=Setting(100)

    title=Setting("X,Z")

    kind_of_calculation = Setting(0)
    replace_poor_statistic = Setting(0)
    good_rays_limit = Setting(100)
    center_x = Setting(0.0)
    center_y = Setting(0.0)
    sigma_x = Setting(0.0)
    sigma_y = Setting(0.0)
    gamma = Setting(0.0)

    loaded_plot_file_name = "<load hdf5 file>"

    new_nbins_h = Setting(25)
    new_nbins_v = Setting(25)

    new_range_h_from = Setting(0.0)
    new_range_h_to   = Setting(0.0)
    new_range_v_from = Setting(0.0)
    new_range_v_to   = Setting(0.0)

    filter = Setting(3)
    filter_sigma_h = Setting(1.0)
    filter_sigma_v = Setting(1.0)
    filter_mode = Setting(0)
    filter_cval = Setting(0.0)
    filter_spline_order = Setting(2)
    scaling_factor = Setting(1.0)

    masking = Setting(0)
    masking_type = Setting(0)
    masking_level = Setting(1e-3)
    masking_width = Setting(0.0)
    masking_height = Setting(0.0)
    masking_diameter = Setting(0.0)

    fit_algorithm = Setting(0)
    show_fit_plot = Setting(1)

    gauss_c = 0.0
    gauss_c_fixed = 0
    gauss_A = 0.0
    gauss_x0 = 0.0
    gauss_y0 = 0.0
    gauss_fx = 0.0
    gauss_fy = 0.0
    gauss_chisquare = 0.0

    pv_c = 0.0
    pv_c_fixed = 0
    pv_A = 0.0
    pv_x0 = 0.0
    pv_y0 = 0.0
    pv_fx = 0.0
    pv_fy = 0.0
    pv_mx = 0.0
    pv_my = 0.0
    pv_chisquare = 0.0

    poly_degree = Setting(4)
    poly_coefficients = []
    poly_chisquare = 0.0

    cumulated_ticket=None
    plotted_ticket   = None
    energy_min = None
    energy_max = None
    energy_step = None
    total_power = None
    current_step = None
    total_steps = None
    cumulated_total_power = None

    plotted_ticket_original = None

    view_type=Setting(1)

    cumulated_quantity = Setting(0)

    autosave_file = None

    def __init__(self):
        super().__init__(show_automatic_box=False)

        button_box = oasysgui.widgetBox(self.controlArea, "", addSpace=False, orientation="horizontal", width=self.CONTROL_AREA_WIDTH-5)

        gui.button(button_box, self, "Plot Data", callback=self.plot_cumulated_data, height=45)
        gui.button(button_box, self, "Save Plot", callback=self.save_cumulated_data, height=45)

        gui.separator(self.controlArea, 10)

        self.tabs_setting = oasysgui.tabWidget(self.controlArea)
        self.tabs_setting.setFixedWidth(self.CONTROL_AREA_WIDTH-5)

        # graph tab
        tab_set = oasysgui.createTabPage(self.tabs_setting, "Plot Settings")
        tab_gen = oasysgui.createTabPage(self.tabs_setting, "Histogram Settings")
        tab_post = oasysgui.createTabPage(self.tabs_setting, "Post Processing")

        screen_box = oasysgui.widgetBox(tab_set, "Screen Position Settings", addSpace=True, orientation="vertical", height=120)

        self.image_plane_combo = gui.comboBox(screen_box, self, "image_plane", label="Position of the Image",
                                              items=["On Image Plane", "Retraced"], labelWidth=260,
                                              callback=self.set_image_plane, sendSelectedValue=False, orientation="horizontal")

        self.image_plane_box = oasysgui.widgetBox(screen_box, "", addSpace=False, orientation="vertical", height=50)
        self.image_plane_box_empty = oasysgui.widgetBox(screen_box, "", addSpace=False, orientation="vertical", height=50)

        oasysgui.lineEdit(self.image_plane_box, self, "image_plane_new_position", "Image Plane new Position", labelWidth=220, valueType=float, orientation="horizontal")

        gui.comboBox(self.image_plane_box, self, "image_plane_rel_abs_position", label="Position Type", labelWidth=250,
                     items=["Absolute", "Relative"], sendSelectedValue=False, orientation="horizontal")

        self.set_image_plane()

        general_box = oasysgui.widgetBox(tab_set, "Variables Settings", addSpace=True, orientation="vertical", height=395)

        self.cb_cumulated_quantity = gui.comboBox(general_box, self, "cumulated_quantity", label="Cumulated Quantity", labelWidth=250,
                                    items=["Power Density [W/mm\u00b2]", "Intensity [ph/s/mm\u00b2]"],
                                    sendSelectedValue=False, orientation="horizontal")

        self.cb_rays = gui.comboBox(general_box, self, "rays", label="Rays", labelWidth=250,
                                    items=["Transmitted", "Absorbed (Lost)", "Absorbed (Still Good)"],
                                    sendSelectedValue=False, orientation="horizontal")

        gui.separator(general_box, height=10)

        self.x_column = gui.comboBox(general_box, self, "x_column_index", label="X Column", labelWidth=70,
                                     items=["1: X",
                                            "2: Y",
                                            "3: Z",
                                     ],
                                     sendSelectedValue=False, orientation="horizontal")

        gui.comboBox(general_box, self, "x_range", label="X Range", labelWidth=250,
                     items=["<Default>",
                                            "Set.."],
                     callback=self.set_x_range, sendSelectedValue=False, orientation="horizontal")

        self.xrange_box = oasysgui.widgetBox(general_box, "", addSpace=True, orientation="vertical", height=70)
        self.xrange_box_empty = oasysgui.widgetBox(general_box, "", addSpace=True, orientation="vertical", height=70)

        oasysgui.lineEdit(self.xrange_box, self, "x_range_min", "X min", labelWidth=220, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.xrange_box, self, "x_range_max", "X max", labelWidth=220, valueType=float, orientation="horizontal")

        self.set_x_range()

        self.y_column = gui.comboBox(general_box, self, "y_column_index", label="Y Column",labelWidth=70,
                                     items=["1: X",
                                            "2: Y",
                                            "3: Z",
                                     ],

                                     sendSelectedValue=False, orientation="horizontal")

        gui.comboBox(general_box, self, "y_range", label="Y Range", labelWidth=250,
                     items=["<Default>",
                                            "Set.."],
                     callback=self.set_y_range, sendSelectedValue=False, orientation="horizontal")

        self.yrange_box = oasysgui.widgetBox(general_box, "", addSpace=True, orientation="vertical", height=70)
        self.yrange_box_empty = oasysgui.widgetBox(general_box, "", addSpace=True, orientation="vertical", height=70)

        oasysgui.lineEdit(self.yrange_box, self, "y_range_min", "Y min", labelWidth=220, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.yrange_box, self, "y_range_max", "Y max", labelWidth=220, valueType=float, orientation="horizontal")

        self.set_y_range()

        ### TAB GEN

        self._set_additional_boxes(tab_gen)

        histograms_box = oasysgui.widgetBox(tab_gen, "Histograms settings", addSpace=True, orientation="vertical", height=300)

        oasysgui.lineEdit(histograms_box, self, "number_of_bins", "Number of Bins H", labelWidth=250, valueType=int, orientation="horizontal")
        oasysgui.lineEdit(histograms_box, self, "number_of_bins_v", "Number of Bins V", labelWidth=250, valueType=int, orientation="horizontal")

        gui.separator(histograms_box)

        gui.comboBox(histograms_box, self, "kind_of_calculation", label="Kind of Calculation", labelWidth=200,
                     items=["From Rays", "Flat Distribution", "Gaussian Distribution", "Lorentzian Distribution"], sendSelectedValue=False, orientation="horizontal", callback=self.set_kind_of_calculation)

        self.poor_statics_cb = gui.comboBox(histograms_box, self, "replace_poor_statistic", label="Activate on Poor Statistics", labelWidth=250,
                                            items=["No", "Yes"], sendSelectedValue=False, orientation="horizontal", callback=self.set_manage_poor_statistics)

        self.poor_statistics_box_1 = oasysgui.widgetBox(histograms_box, "", addSpace=False, orientation="vertical", height=30)
        self.poor_statistics_box_2 = oasysgui.widgetBox(histograms_box, "", addSpace=False, orientation="vertical", height=30)

        oasysgui.lineEdit(self.poor_statistics_box_1, self, "good_rays_limit", "Good Rays Limit", labelWidth=100,  valueType=int, orientation="horizontal")

        self.kind_of_calculation_box_1 = oasysgui.widgetBox(histograms_box, "", addSpace=False, orientation="vertical", height=110)
        self.kind_of_calculation_box_2 = oasysgui.widgetBox(histograms_box, "", addSpace=False, orientation="vertical", height=110)
        self.kind_of_calculation_box_3 = oasysgui.widgetBox(histograms_box, "", addSpace=False, orientation="vertical", height=110)

        self.le_g_sigma_x = oasysgui.lineEdit(self.kind_of_calculation_box_2, self, "sigma_x", "Sigma H", labelWidth=100,  valueType=float, orientation="horizontal")
        self.le_g_sigma_y = oasysgui.lineEdit(self.kind_of_calculation_box_2, self, "sigma_y", "Sigma V", labelWidth=100,  valueType=float, orientation="horizontal")
        self.le_g_center_x = oasysgui.lineEdit(self.kind_of_calculation_box_2, self, "center_x", "Center H", labelWidth=100,  valueType=float, orientation="horizontal")
        self.le_g_center_y = oasysgui.lineEdit(self.kind_of_calculation_box_2, self, "center_y", "Center V", labelWidth=100,  valueType=float, orientation="horizontal")

        self.le_l_gamma = oasysgui.lineEdit(self.kind_of_calculation_box_3, self, "gamma", "Gamma", labelWidth=100,  valueType=float, orientation="horizontal")
        self.le_l_center_x = oasysgui.lineEdit(self.kind_of_calculation_box_3, self, "center_x", "Center H", labelWidth=100,  valueType=float, orientation="horizontal")
        self.le_l_center_y = oasysgui.lineEdit(self.kind_of_calculation_box_3, self, "center_y", "Center V", labelWidth=100,  valueType=float, orientation="horizontal")

        self.set_kind_of_calculation()

        # post processing

        gui.separator(tab_post)

        post_box_1 = oasysgui.widgetBox(tab_post, "", addSpace=False, orientation="horizontal", height=25)
        self.le_loaded_plot_file_name = oasysgui.lineEdit(post_box_1, self, "loaded_plot_file_name", "Loaded File", labelWidth=100,  valueType=str, orientation="horizontal")
        gui.button(post_box_1, self, "...", callback=self.select_plot_file)

        tabs_post = oasysgui.tabWidget(tab_post)
        tabs_post.setFixedWidth(self.CONTROL_AREA_WIDTH-20)

        # graph tab
        tab_post_basic  = oasysgui.createTabPage(tabs_post, "Basic")
        tab_post_smooth = oasysgui.createTabPage(tabs_post, "Smoothing")
        tab_post_fit    = oasysgui.createTabPage(tabs_post, "Fit")

        post_box = oasysgui.widgetBox(tab_post_basic, "Post Processing", addSpace=False, orientation="vertical", height=460)

        button_box = oasysgui.widgetBox(post_box, "", addSpace=False, orientation="vertical")
        button = gui.button(button_box, self, "Reset", callback=self.reload_plot, height=25, width=352)
        gui.separator(button_box, height=10)

        font = QFont(button.font())
        font.setItalic(True)
        button.setFont(font)
        palette = QPalette(button.palette())
        palette.setColor(QPalette.ButtonText, QColor('dark red'))
        button.setPalette(palette)

        button_box = oasysgui.widgetBox(post_box, "", addSpace=False, orientation="horizontal")

        gui.button(button_box, self, "Invert H,V", callback=self.invert_plot, height=25)
        gui.button(button_box, self, "Flip H", callback=self.flip_H, height=25)
        gui.button(button_box, self, "Flip V", callback=self.flip_V, height=25)

        button_box = oasysgui.widgetBox(post_box, "", addSpace=False, orientation="vertical")
        gui.button(button_box, self, "Rescale Plot", callback=self.rescale_plot, height=25)
        oasysgui.lineEdit(post_box, self, "scaling_factor", "Scaling factor", labelWidth=250,  valueType=float, orientation="horizontal")

        button_box = oasysgui.widgetBox(post_box, "", addSpace=False, orientation="horizontal")
        gui.button(button_box, self, "Rebin Plot", callback=self.rebin_plot, height=25)

        post_box_0 = oasysgui.widgetBox(post_box, "", addSpace=False, orientation="horizontal", height=25)
        oasysgui.lineEdit(post_box_0, self, "new_nbins_h", "Nr. Bins H x V", labelWidth=150,  valueType=int, orientation="horizontal")
        oasysgui.lineEdit(post_box_0, self, "new_nbins_v", "x", labelWidth=10,  valueType=int, orientation="horizontal")

        button_box = oasysgui.widgetBox(post_box, "", addSpace=False, orientation="horizontal")
        gui.button(button_box, self, "Cut Plot", callback=self.cut_plot, height=25)
        post_box_0 = oasysgui.widgetBox(post_box, "", addSpace=False, orientation="horizontal", height=25)
        oasysgui.lineEdit(post_box_0, self, "new_range_h_from", "New Range H (from, to)", labelWidth=150,  valueType=float, orientation="horizontal")
        oasysgui.lineEdit(post_box_0, self, "new_range_h_to", "x", labelWidth=10,  valueType=float, orientation="horizontal")
        post_box_0 = oasysgui.widgetBox(post_box, "", addSpace=False, orientation="horizontal", height=25)
        oasysgui.lineEdit(post_box_0, self, "new_range_v_from", "New Range V (from, to)", labelWidth=150,  valueType=float, orientation="horizontal")
        oasysgui.lineEdit(post_box_0, self, "new_range_v_to", "x", labelWidth=10,  valueType=float, orientation="horizontal")

        gui.separator(post_box)

        button_box = oasysgui.widgetBox(post_box, "", addSpace=False, orientation="horizontal")
        gui.button(button_box, self, "Mask", callback=self.mask_plot, height=25)

        gui.comboBox(post_box, self, "masking", label="Mask", labelWidth=200,
                     items=["Level", "Rectangular", "Circular"], sendSelectedValue=False, orientation="horizontal", callback=self.set_masking)

        gui.comboBox(post_box, self, "masking_type", label="Mask Type", labelWidth=100,
                     items=["Aperture or < Level", "Obstruction or > Level"], sendSelectedValue=False, orientation="horizontal")

        self.mask_box_1 = oasysgui.widgetBox(post_box, "", addSpace=False, orientation="vertical", height=50)
        self.mask_box_2 = oasysgui.widgetBox(post_box, "", addSpace=False, orientation="vertical", height=50)
        self.mask_box_3 = oasysgui.widgetBox(post_box, "", addSpace=False, orientation="vertical", height=50)

        oasysgui.lineEdit(self.mask_box_1, self, "masking_level", "Mask Level (W/mm\u00B2)", labelWidth=250,  valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.mask_box_2, self, "masking_width", "Mask Width ", labelWidth=250,  valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.mask_box_2, self, "masking_height", "Mask Height", labelWidth=250,  valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.mask_box_3, self, "masking_diameter", "Mask Diameter ", labelWidth=250,  valueType=float, orientation="horizontal")

        self.set_masking()

        post_box = oasysgui.widgetBox(tab_post_smooth, "Smoothing", addSpace=False, orientation="vertical", height=220)

        button_box = oasysgui.widgetBox(post_box, "", addSpace=False, orientation="vertical")
        button = gui.button(button_box, self, "Reset", callback=self.reload_plot, height=25, width=352)
        gui.separator(button_box, height=10)

        font = QFont(button.font())
        font.setItalic(True)
        button.setFont(font)
        palette = QPalette(button.palette())
        palette.setColor(QPalette.ButtonText, QColor('dark red'))
        button.setPalette(palette)

        button_box = oasysgui.widgetBox(post_box, "", addSpace=False, orientation="horizontal")
        gui.button(button_box, self, "Smooth Plot", callback=self.smooth_plot, height=25)

        gui.separator(post_box)

        gui.comboBox(post_box, self, "filter", label="Filter", labelWidth=200,
                     items=["Gaussian",
                            "Spline",
                            "Uniform",
                            "Fourier-Gaussian",
                            "Fourier-Ellipsoid",
                            "Fourier-Uniform",
                            "Fill Holes"
                            ], sendSelectedValue=False, orientation="horizontal", callback=self.set_filter)

        self.post_box_1 = oasysgui.widgetBox(post_box, "", addSpace=False, orientation="vertical", height=110)
        self.post_box_2 = oasysgui.widgetBox(post_box, "", addSpace=False, orientation="vertical", height=110)
        self.post_box_3 = oasysgui.widgetBox(post_box, "", addSpace=False, orientation="vertical", height=110)
        self.post_box_4 = oasysgui.widgetBox(post_box, "", addSpace=False, orientation="vertical", height=110)

        oasysgui.lineEdit(self.post_box_1, self, "filter_sigma_h", "Sigma/Size H", labelWidth=200,  valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.post_box_1, self, "filter_sigma_v", "Sigma/Size V", labelWidth=200,  valueType=float, orientation="horizontal")

        oasysgui.lineEdit(self.post_box_2, self, "filter_sigma_h", "Sigma/Size H", labelWidth=200,  valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.post_box_2, self, "filter_sigma_v", "Sigma/Size V", labelWidth=200,  valueType=float, orientation="horizontal")

        self.cb_filter_mode = gui.comboBox(self.post_box_2, self, "filter_mode", label="Mode", labelWidth=200,
                                           items=["reflect", "constant", "nearest", "mirror", "wrap"],
                                           sendSelectedValue=False, orientation="horizontal", callback=self.set_filter_mode)

        self.le_filter_cval = oasysgui.lineEdit(self.post_box_2, self, "filter_cval", "Constant Value", labelWidth=250,  valueType=float, orientation="horizontal")

        oasysgui.lineEdit(self.post_box_3, self, "filter_spline_order", "Spline Order", labelWidth=250,  valueType=int, orientation="horizontal")

        self.set_filter()

        post_box = oasysgui.widgetBox(tab_post_fit, "Fit", addSpace=False, orientation="vertical", height=460)

        gui.comboBox(post_box, self, "fit_algorithm", label="Fit Algorithm",
                     items=["Gaussian", "Pseudo-Voigt", "Polynomial"], labelWidth=200,
                     callback=self.set_fit_algorithm, sendSelectedValue=False, orientation="horizontal")

        gui.comboBox(post_box, self, "show_fit_plot", label="Show Fit Plot",
                     items=["No", "Yes"], labelWidth=260,
                     sendSelectedValue=False, orientation="horizontal")

        self.fit_box_1 = oasysgui.widgetBox(post_box, "", addSpace=False, orientation="vertical", height=340)
        self.fit_box_2 = oasysgui.widgetBox(post_box, "", addSpace=False, orientation="vertical", height=340)
        self.fit_box_3 = oasysgui.widgetBox(post_box, "", addSpace=False, orientation="vertical", height=340)

        gauss_c_box = oasysgui.widgetBox(self.fit_box_1, "", addSpace=False, orientation="horizontal")

        le_gauss_c  = oasysgui.lineEdit(gauss_c_box, self, "gauss_c", "c [W/mm\u00b2]", labelWidth=200,  valueType=float, orientation="horizontal")
        gui.checkBox(gauss_c_box, self, "gauss_c_fixed", label="c=0")

        le_gauss_A  = oasysgui.lineEdit(self.fit_box_1, self, "gauss_A", "A [W/mm\u00b2]", labelWidth=200,  valueType=float, orientation="horizontal")
        self.le_gauss_x0 = oasysgui.lineEdit(self.fit_box_1, self, "gauss_x0", "x0 [m] ", labelWidth=200,  valueType=float, orientation="horizontal")
        self.le_gauss_y0 = oasysgui.lineEdit(self.fit_box_1, self, "gauss_y0", "y0 [m]", labelWidth=200,  valueType=float, orientation="horizontal")
        self.le_gauss_fx = oasysgui.lineEdit(self.fit_box_1, self, "gauss_fx", "fx [m]", labelWidth=200,  valueType=float, orientation="horizontal")
        self.le_gauss_fy = oasysgui.lineEdit(self.fit_box_1, self, "gauss_fy", "fy [m]", labelWidth=200,  valueType=float, orientation="horizontal")
        self.le_gauss_chisquare = oasysgui.lineEdit(self.fit_box_1, self, "gauss_chisquare", "\u03c7\u00b2 (RSS/\u03bd)", labelWidth=200,  valueType=float, orientation="horizontal")

        le_gauss_c.setReadOnly(True)
        le_gauss_A.setReadOnly(True)
        self.le_gauss_x0.setReadOnly(True)
        self.le_gauss_y0.setReadOnly(True)
        self.le_gauss_fx.setReadOnly(True)
        self.le_gauss_fy.setReadOnly(True)
        self.le_gauss_chisquare.setReadOnly(True)

        pv_c_box = oasysgui.widgetBox(self.fit_box_2, "", addSpace=False, orientation="horizontal")

        le_pv_c  = oasysgui.lineEdit(pv_c_box, self, "pv_c", "c [W/mm\u00b2]", labelWidth=200,  valueType=float, orientation="horizontal")
        gui.checkBox(pv_c_box, self, "pv_c_fixed", label="c=0")

        le_pv_A  = oasysgui.lineEdit(self.fit_box_2, self, "pv_A", "A [W/mm\u00b2]", labelWidth=200,  valueType=float, orientation="horizontal")
        self.le_pv_x0 = oasysgui.lineEdit(self.fit_box_2, self, "pv_x0", "x0 [m]", labelWidth=200,  valueType=float, orientation="horizontal")
        self.le_pv_y0 = oasysgui.lineEdit(self.fit_box_2, self, "pv_y0", "y0 [m]", labelWidth=200,  valueType=float, orientation="horizontal")
        self.le_pv_fx = oasysgui.lineEdit(self.fit_box_2, self, "pv_fx", "fx [m]", labelWidth=200,  valueType=float, orientation="horizontal")
        self.le_pv_fy = oasysgui.lineEdit(self.fit_box_2, self, "pv_fy", "fy [m]", labelWidth=200,  valueType=float, orientation="horizontal")
        le_pv_mx = oasysgui.lineEdit(self.fit_box_2, self, "pv_mx", "mx", labelWidth=200,  valueType=float, orientation="horizontal")
        le_pv_my = oasysgui.lineEdit(self.fit_box_2, self, "pv_my", "my", labelWidth=200,  valueType=float, orientation="horizontal")
        self.le_pv_chisquare = oasysgui.lineEdit(self.fit_box_2, self, "pv_chisquare", "\u03c7\u00b2 (RSS/\u03bd)", labelWidth=200,  valueType=float, orientation="horizontal")

        le_pv_c.setReadOnly(True)
        le_pv_A.setReadOnly(True)
        self.le_pv_x0.setReadOnly(True)
        self.le_pv_y0.setReadOnly(True)
        self.le_pv_fx.setReadOnly(True)
        self.le_pv_fy.setReadOnly(True)
        le_pv_mx.setReadOnly(True)
        le_pv_my.setReadOnly(True)
        self.le_pv_chisquare.setReadOnly(True)

        oasysgui.lineEdit(self.fit_box_3, self, "poly_degree", "Degree", labelWidth=260, valueType=int, orientation="horizontal")
        oasysgui.widgetLabel(self.fit_box_3, "Polynomial Coefficients")

        text_box = oasysgui.widgetBox(self.fit_box_3, "", addSpace=False, orientation="vertical", height=205)

        self.poly_coefficients_text = oasysgui.textArea(205, 350, readOnly=True)
        text_box.layout().addWidget(self.poly_coefficients_text)
        self.le_poly_chisquare = oasysgui.lineEdit(self.fit_box_3, self, "poly_chisquare", "\u03c7\u00b2 (RSS/\u03bd)", labelWidth=200,  valueType=float, orientation="horizontal")

        self.le_poly_chisquare.setReadOnly(True)

        button_box = oasysgui.widgetBox(post_box, "", addSpace=False, orientation="horizontal")
        gui.button(button_box, self, "Do Fit", callback=self.do_fit, height=25)
        button = gui.button(button_box, self, "Show Fit Formulas", callback=self.show_fit_formulas, height=25)

        font = QFont(button.font())
        font.setItalic(True)
        button.setFont(font)
        palette = QPalette(button.palette())
        palette.setColor(QPalette.ButtonText, QColor('dark blue'))
        button.setPalette(palette)

        self.set_fit_algorithm()

        #######################################################
        # MAIN TAB

        self.main_tabs = oasysgui.tabWidget(self.mainArea)
        plot_tab = oasysgui.createTabPage(self.main_tabs, "Plots")
        out_tab = oasysgui.createTabPage(self.main_tabs, "Output")

        view_box = oasysgui.widgetBox(plot_tab, "Plotting", addSpace=False, orientation="vertical", width=self.IMAGE_WIDTH)
        view_box_1 = oasysgui.widgetBox(view_box, "", addSpace=False, orientation="vertical", width=350)

        gui.comboBox(view_box_1, self, "view_type", label="Plot Accumulated Results", labelWidth=320,
                     items=["No", "Yes"],  sendSelectedValue=False, orientation="horizontal")

        self.image_box = gui.widgetBox(plot_tab, "Plot Result", addSpace=True, orientation="vertical")
        self.image_box.setFixedHeight(self.IMAGE_HEIGHT)
        self.image_box.setFixedWidth(self.IMAGE_WIDTH)

        self.shadow_output = oasysgui.textArea(height=580, width=800)

        out_box = gui.widgetBox(out_tab, "System Output", addSpace=True, orientation="horizontal")
        out_box.layout().addWidget(self.shadow_output)

    def _set_additional_boxes(self, tab_gen): raise NotImplementedError()

    def set_kind_of_calculation(self):
        self.kind_of_calculation_box_1.setVisible(self.kind_of_calculation<=1)
        self.kind_of_calculation_box_2.setVisible(self.kind_of_calculation==2)
        self.kind_of_calculation_box_3.setVisible(self.kind_of_calculation==3)

        if self.kind_of_calculation > 0:
            self.poor_statics_cb.setEnabled(True)
        else:
            self.poor_statics_cb.setEnabled(False)
            self.replace_poor_statistic = 0

        self.set_manage_poor_statistics()

    def set_manage_poor_statistics(self):
        self.poor_statistics_box_1.setVisible(self.replace_poor_statistic==1)
        self.poor_statistics_box_2.setVisible(self.replace_poor_statistic==0)

    def set_image_plane(self):
        self.image_plane_box.setVisible(self.image_plane==1)
        self.image_plane_box_empty.setVisible(self.image_plane==0)

    def set_x_range(self):
        self.xrange_box.setVisible(self.x_range == 1)
        self.xrange_box_empty.setVisible(self.x_range == 0)

    def set_y_range(self):
        self.yrange_box.setVisible(self.y_range == 1)
        self.yrange_box_empty.setVisible(self.y_range == 0)

    def set_filter(self):
        self.post_box_1.setVisible(3<=self.filter<=5)
        self.post_box_2.setVisible(self.filter==0 or self.filter==2)
        self.post_box_3.setVisible(self.filter==1 )
        self.post_box_4.setVisible(self.filter==6)

        if self.filter==0 or self.filter==2: self.set_filter_mode()

    def set_masking(self):
        self.mask_box_1.setVisible(self.masking==0)
        self.mask_box_2.setVisible(self.masking==1)
        self.mask_box_3.setVisible(self.masking==2)

    def set_filter_mode(self):
        self.le_filter_cval.setEnabled(self.filter_mode==1)

    def set_fit_algorithm(self):
        self.fit_box_1.setVisible(self.fit_algorithm==0)
        self.fit_box_2.setVisible(self.fit_algorithm==1)
        self.fit_box_3.setVisible(self.fit_algorithm==2)

    #########################################################
    # I/O
    
    @Inputs.shadow_data
    def set_shadow_data(self, input_data):
        self.cb_rays.setEnabled(True)

        if not input_data is None:
            if self._analyze_input_data(input_data):
                if self._can_be_plotted(input_data):
                    self.plot_results()

    def _analyze_input_data(self, input_data): raise NotImplementedError()

    def _can_be_plotted(self, input_data):
        if ShadowCongruence.check_empty_data(input_data): return ShadowCongruence.check_good_beam(input_data.beam)
        else: return False

    def _write_std_out(self, text):
        cursor = self.shadow_output.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.shadow_output.setTextCursor(cursor)
        self.shadow_output.ensureCursorVisible()

    #########################################################
    # PLOTTING

    def replace_fig(self, shadow_data, var_x, var_y, xrange, yrange, nbins_h, nbins_v, nolost):
        if self.plot_canvas is None:
            self.plot_canvas = PowerPlotXYWidget()
            self.image_box.layout().addWidget(self.plot_canvas)

        try:
            if self.autosave == 1:
                if self.autosave_file is None:
                    self.autosave_file = ShadowPlot.PlotXYHdf5File(congruence.checkDir(self.autosave_file_name))
                elif self.autosave_file.filename != congruence.checkFileName(self.autosave_file_name):
                    self.autosave_file.close()
                    self.autosave_file = ShadowPlot.PlotXYHdf5File(congruence.checkDir(self.autosave_file_name))

                self.autosave_file.add_attribute("current_step", self.current_step, dataset_name="additional_data")
                self.autosave_file.add_attribute("total_steps", self.total_steps, dataset_name="additional_data")
                self.autosave_file.add_attribute("last_energy_value", self.energy_max, dataset_name="additional_data")
                self.autosave_file.add_attribute("last_power_value", self.total_power, dataset_name="additional_data")

            if self.keep_result == 1:
                self.cumulated_ticket, last_ticket = self.plot_canvas.plot_power_density(shadow_data, var_x, var_y,
                                                                                         self.total_power, self.cumulated_total_power,
                                                                                         self.energy_min, self.energy_max, self.energy_step,
                                                                                         nbins_h=nbins_h, nbins_v=nbins_v, xrange=xrange, yrange=yrange, nolost=nolost,
                                                                                         ticket_to_add=self.cumulated_ticket,
                                                                                         show_image=self.view_type==1,
                                                                                         kind_of_calculation=self.kind_of_calculation,
                                                                                         replace_poor_statistic=self.replace_poor_statistic,
                                                                                         good_rays_limit=self.good_rays_limit,
                                                                                         center_x=self.center_x,
                                                                                         center_y=self.center_y,
                                                                                         sigma_x=self.sigma_x,
                                                                                         sigma_y=self.sigma_y,
                                                                                         gamma=self.gamma,
                                                                                         cumulated_quantity=self.cumulated_quantity)

                if self.autosave == 1:
                    self.autosave_file.add_attribute("last_plotted_power",  self.cumulated_ticket['plotted_power'],  dataset_name="additional_data")
                    self.autosave_file.add_attribute("last_incident_power", self.cumulated_ticket['incident_power'], dataset_name="additional_data")
                    self.autosave_file.add_attribute("last_total_power",    self.cumulated_ticket['total_power'],    dataset_name="additional_data")
                    self.autosave_file.add_attribute("last_energy_min",     self.cumulated_ticket['energy_min'],     dataset_name="additional_data")
                    self.autosave_file.add_attribute("last_energy_max",     self.cumulated_ticket['energy_max'],     dataset_name="additional_data")
                    self.autosave_file.add_attribute("last_energy_step",    self.cumulated_ticket['energy_step'],    dataset_name="additional_data")

                self.plotted_ticket          = self.cumulated_ticket
                self.plotted_ticket_original = self.plotted_ticket.copy()

                if self.autosave == 1:
                    self.autosave_file.write_coordinates(self.cumulated_ticket)
                    dataset_name = "power_density"

                    self.autosave_file.add_plot_xy(self.cumulated_ticket, dataset_name=dataset_name)

                    if self.autosave_partial_results == 1:
                        if last_ticket is None:
                            self.autosave_file.add_plot_xy(self.cumulated_ticket,
                                                           plot_name="Energy Range: " + str(round(self.energy_max-self.energy_step, 2)) + "-" + str(round(self.energy_max, 2)),
                                                           dataset_name=dataset_name)
                        else:
                            self.autosave_file.add_plot_xy(last_ticket,
                                                           plot_name="Energy Range: " + str(round(self.energy_max-self.energy_step, 2)) + "-" + str(round(self.energy_max, 2)),
                                                           dataset_name=dataset_name)

                    self.autosave_file.flush()
            else:
                ticket, _ = self.plot_canvas.plot_power_density(shadow_data, var_x, var_y,
                                                                self.total_power, self.cumulated_total_power,
                                                                self.energy_min, self.energy_max, self.energy_step,
                                                                nbins_h=nbins_h, nbins_v=nbins_v, xrange=xrange, yrange=yrange, nolost=nolost,
                                                                show_image=self.view_type==1,
                                                                kind_of_calculation=self.kind_of_calculation,
                                                                replace_poor_statistic=self.replace_poor_statistic,
                                                                good_rays_limit=self.good_rays_limit,
                                                                center_x=self.center_x,
                                                                center_y=self.center_y,
                                                                sigma_x=self.sigma_x,
                                                                sigma_y=self.sigma_y,
                                                                gamma=self.gamma,
                                                                cumulated_quantity=self.cumulated_quantity)

                self.cumulated_ticket = None
                self.plotted_ticket = ticket
                self.plotted_ticket_original = self.plotted_ticket.copy()

                if self.autosave == 1:
                    self.autosave_file.write_coordinates(ticket)
                    self.autosave_file.add_plot_xy(ticket, dataset_name="power_density")
                    self.autosave_file.flush()

        except Exception as e:
            if not self.IS_DEVELOP:
                raise Exception("Data not plottable: " + str(e))
            else:
                raise e

    def plot_xy(self, var_x, var_y):
        data_to_plot = self.input_data

        if ShadowCongruence.check_good_beam(data_to_plot.beam):
            if self.image_plane == 1:
                new_shadow_data = self.input_data.duplicate(copy_beamline=False)

                if self.image_plane_rel_abs_position == 1:  # relative
                    dist = self.image_plane_new_position
                else:  # absolute
                    beamline = self.input_data.beamline

                    if beamline is None: image_plane = 0.0
                    else:                image_plane = beamline.get_beamline_element_at(-1).get_coordinates().q()

                    dist = self.image_plane_new_position - image_plane

                new_shadow_data.beam.retrace(dist)

                data_to_plot = new_shadow_data
        else:
            # no good rays in the region of interest: creates a 0 power step with 1 good ray
            data_to_plot.beam.rays[0, 9] = 1 # convert to good rays

            data_to_plot.beam.rays[:, 6] = 0.0
            data_to_plot.beam.rays[:, 7] = 0.0
            data_to_plot.beam.rays[:, 8] = 0.0
            data_to_plot.beam.rays[:, 15] = 0.0
            data_to_plot.beam.rays[:, 16] = 0.0
            data_to_plot.beam.rays[:, 17] = 0.0

        xrange, yrange = self.get_ranges()

        self.replace_fig(data_to_plot, var_x, var_y,
                         xrange=xrange,
                         yrange=yrange,
                         nbins_h=int(self.number_of_bins),
                         nbins_v=int(self.number_of_bins_v),
                         nolost=self.rays+1)

    def plot_cumulated_data(self):
        if not self.cumulated_ticket is None:
            self.plot_canvas.plot_power_density_ticket(ticket=self.cumulated_ticket,
                                                       var_x=self.x_column_index+1,
                                                       var_y=self.y_column_index+1,
                                                       cumulated_total_power=self.cumulated_total_power,
                                                       energy_min=self.energy_min,
                                                       energy_max=self.energy_max,
                                                       energy_step=self.energy_step,
                                                       show_image=self.view_type==1,
                                                       cumulated_quantity=self.cumulated_quantity)

            self.plotted_ticket_original = self.cumulated_ticket.copy()

    def plot_results(self):
        try:
            sys.stdout = EmittingStream(textWritten=self._write_std_out)

            if ShadowCongruence.check_empty_data(self.input_data):
                self.number_of_bins   = congruence.checkStrictlyPositiveNumber(self.number_of_bins, "Number of Bins")
                self.number_of_bins_v = congruence.checkStrictlyPositiveNumber(self.number_of_bins_v, "Number of Bins V")
                self._check_other_fields()

                self.plot_xy(self.x_column_index+1, self.y_column_index+1)

            time.sleep(0.1)  # prevents a misterious dead lock in the Orange cycle when refreshing the histogram
        except Exception as exception:
            QMessageBox.critical(self, "Error",
                                       str(exception),
                                       QMessageBox.Ok)

            if self.IS_DEVELOP: raise exception

    def _check_other_fields(self): pass

    def get_ranges(self):
        xrange  = None
        yrange  = None

        if self.x_range == 1:
            congruence.checkLessThan(self.x_range_min, self.x_range_max, "X range min", "X range max")

            xrange = [self.x_range_min / TO_MM, self.x_range_max / TO_MM]

        if self.y_range == 1:
            congruence.checkLessThan(self.y_range_min, self.y_range_max, "Y range min", "Y range max")

            yrange = [self.y_range_min / TO_MM, self.y_range_max / TO_MM]

        return xrange, yrange

    ##################################################
    # SAVE

    def save_cumulated_data(self):
        file_name = oasysgui.selectSaveFileFromDialog(self, "Save Current Plot", default_file_name=("" if (not hasattr(self, "autosave") or self.autosave==0) else self.autosave_file_name),
                                                      file_extension_filter="HDF5 Files (*.hdf5 *.h5 *.hdf);;Text Files (*.dat *.txt);;Ansys Files (*.csv)")

        if not file_name is None and not file_name.strip()=="":
            format, ok = QInputDialog.getItem(self, "Select Output Format", "Formats: ", ("Hdf5", "Text", "Ansys", "Image", "Hdf5 & Image", "All"), 4, False)

            if ok and format:
                if format == "Hdf5" or format == "All":  self.save_cumulated_data_hdf5(file_name)
                if format == "Text" or format == "All":  self.save_cumulated_data_txt(file_name)
                if format == "Ansys" or format == "All": self.save_cumulated_data_ansys(file_name)
                if format == "Image" or format == "All": self.save_cumulated_data_image(file_name)
                if format == "Hdf5 & Image":
                    self.save_cumulated_data_hdf5(file_name)
                    self.save_cumulated_data_image(file_name)

    def save_cumulated_data_hdf5(self, file_name):
        if not self.plotted_ticket is None:
            try:
                save_file = ShadowPlot.PlotXYHdf5File(congruence.checkDir(os.path.splitext(file_name)[0] + ".hdf5"))

                save_file.write_coordinates(self.plotted_ticket)
                save_file.add_plot_xy(self.plotted_ticket, dataset_name="power_density")

                save_file.add_attribute("last_plotted_power", self.plot_canvas.cumulated_power_plot, dataset_name="additional_data")
                save_file.add_attribute("last_incident_power", self.plot_canvas.cumulated_previous_power_plot, dataset_name="additional_data")
                save_file.add_attribute("last_total_power", 0.0, dataset_name="additional_data")
                save_file.add_attribute("last_energy_min", 0.0, dataset_name="additional_data")
                save_file.add_attribute("last_energy_max", 0.0, dataset_name="additional_data")
                save_file.add_attribute("last_energy_step", 0.0, dataset_name="additional_data")

                save_file.close()
            except Exception as exception:
                QMessageBox.critical(self, "Error", str(exception), QMessageBox.Ok)

                if self.IS_DEVELOP: raise exception

    def save_cumulated_data_txt(self, file_name):
        if not self.plotted_ticket is None:
            try:
                save_file = open(os.path.splitext(file_name)[0] + ".dat", "w")

                x_values = self.plotted_ticket["bin_h_center"]
                y_values = self.plotted_ticket["bin_v_center"]
                z_values = self.plotted_ticket["histogram"]

                for i in range(len(x_values)):
                    for j in range(len(y_values)):
                        row = str(x_values[i]) + " " + str(y_values[j]) + " " + str(z_values[i, j])

                        if i+j > 0: row = "\n" + row

                        save_file.write(row)

                save_file.flush()
                save_file.close()
            except Exception as exception:
                QMessageBox.critical(self, "Error", str(exception), QMessageBox.Ok)

                if self.IS_DEVELOP: raise exception

    def save_cumulated_data_image(self, file_name):
        if not self.plotted_ticket is None:
            try:
                def duplicate(obj):
                    import io, pickle
                    buf = io.BytesIO()
                    pickle.dump(obj, buf)
                    buf.seek(0)
                    return pickle.load(buf)

                fig = duplicate(self.plot_canvas.plot_canvas._backend.fig)

                vmin = numpy.min(self.plotted_ticket["histogram"])
                vmax = numpy.max(self.plotted_ticket["histogram"])

                cbar = fig.colorbar(cm.ScalarMappable(norm=Normalize(vmin=vmin, vmax=vmax), cmap=cmap_temperature), ax=fig.gca())
                cbar.ax.set_ylabel('Power Density [W/mm\u00b2]')
                ticks = cbar.get_ticks()
                cbar.set_ticks([vmax] + list(ticks))

                def format_number(number):
                    order_of_magnitude = int(numpy.floor(numpy.log10(numpy.abs(number))))

                    if order_of_magnitude > 3:
                        return str(round(number, 1))
                    elif order_of_magnitude >= 0:
                        return str(round(number, 4 - order_of_magnitude))
                    else:
                        return ("{:.1e}").format(round(number, abs(order_of_magnitude)+1))

                cbar.set_ticklabels([format_number(vmax)] + ["{:.1e}".format(t) for t in ticks])

                fig.savefig(os.path.splitext(file_name)[0] + ".png")

            except Exception as exception:
                QMessageBox.critical(self, "Error", str(exception), QMessageBox.Ok)

                if self.IS_DEVELOP: raise exception

    def save_cumulated_data_ansys(self, file_name):
        if not self.plotted_ticket is None:
            try:
                column, ok = QInputDialog.getItem(self, "Ansys File", "Empty column in Ansys axes system", ("x", "y", "z"), 2, False)

                if ok and column:
                    save_file = open(os.path.splitext(file_name)[0] + ".csv", "w")

                    x_values = self.plotted_ticket["bin_h_center"]
                    y_values = self.plotted_ticket["bin_v_center"]
                    z_values = self.plotted_ticket["histogram"]

                    for i in range(x_values.shape[0]):
                        for j in range(y_values.shape[0]):
                            if column == "x":   row = "0.0,"                              + str(x_values[i]) + ","  + str(y_values[j]) + "," + str(z_values[i, j])
                            elif column == "y": row = str(x_values[i])                    + ",0.0,"                 + str(y_values[j]) + "," + str(z_values[i, j])
                            elif column == "z": row = str(x_values[i]) + ","              + str(y_values[j])        + ",0.0,"                + str(z_values[i, j])

                            if i+j > 0: row = "\n" + row

                            save_file.write(row)

                    save_file.flush()
                    save_file.close()
            except Exception as exception:
                QMessageBox.critical(self, "Error", str(exception), QMessageBox.Ok)

                if self.IS_DEVELOP: raise exception

    ##################################################
    # POST EDITING

    def select_plot_file(self):
        file_name = oasysgui.selectFileFromDialog(self, None, "Select File", file_extension_filter="HDF5 Files (*.hdf5 *.h5 *.hdf)")

        if not file_name is None:
            self.le_loaded_plot_file_name.setText(os.path.basename(os.path.normpath(file_name)))

            plot_file = ShadowPlot.PlotXYHdf5File(congruence.checkDir(file_name), mode="r")

            ticket = {}

            ticket["histogram"], ticket["histogram_h"], ticket["histogram_v"], attributes = plot_file.get_last_plot(dataset_name="power_density")
            ticket["bin_h_center"], ticket["bin_v_center"], ticket["h_label"], ticket["v_label"] = plot_file.get_coordinates()
            ticket["intensity"] = attributes["intensity"]
            ticket["nrays"] = attributes["total_rays"]
            ticket["good_rays"] = attributes["good_rays"]

            is_merged = False

            if self.plot_canvas is None:
                self.plot_canvas = PowerPlotXYWidget()
                self.image_box.layout().addWidget(self.plot_canvas)
            else:
                if not self.plotted_ticket is None:
                    if QMessageBox.question(self, "Load Plot", "Merge with current Plot?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes:
                        if ticket["histogram"].shape == self.plotted_ticket["histogram"].shape and \
                                ticket["bin_h_center"].shape == self.plotted_ticket["bin_h_center"].shape and \
                                ticket["bin_v_center"].shape == self.plotted_ticket["bin_v_center"].shape and \
                                ticket["bin_h_center"][0] == self.plotted_ticket["bin_h_center"][0] and \
                                ticket["bin_h_center"][-1] == self.plotted_ticket["bin_h_center"][-1] and \
                                ticket["bin_v_center"][0] == self.plotted_ticket["bin_v_center"][0] and \
                                ticket["bin_v_center"][-1] == self.plotted_ticket["bin_v_center"][-1]:
                            ticket["histogram"] += self.plotted_ticket["histogram"]
                            is_merged = True

                            if QMessageBox.question(self, "Load Plot", "Average with current Plot?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes:
                                ticket["histogram"] *= 0.5
                        else:
                            raise ValueError("The plots cannot be merged: the should have same dimensions and ranges")

            try:
                last_plotted_power = plot_file.get_attribute("last_plotted_power", dataset_name="additional_data")
                last_incident_power = plot_file.get_attribute("last_incident_power", dataset_name="additional_data")
                last_total_power = plot_file.get_attribute("last_total_power", dataset_name="additional_data")
                energy_min = plot_file.get_attribute("last_energy_min", dataset_name="additional_data")
                energy_max = plot_file.get_attribute("last_energy_max", dataset_name="additional_data")
                energy_step = plot_file.get_attribute("last_energy_step", dataset_name="additional_data")
            except:
                last_plotted_power = numpy.sum(ticket["histogram"]) * (ticket["bin_h_center"][1] - ticket["bin_h_center"][0]) * (ticket["bin_v_center"][1] - ticket["bin_v_center"][0])
                last_incident_power = 0.0
                last_total_power = 0.0
                energy_min = 0.0
                energy_max = 0.0
                energy_step = 0.0

            try:
                if is_merged:
                    self.plot_canvas.cumulated_power_plot += last_plotted_power
                    self.plot_canvas.cumulated_previous_power_plot += last_incident_power
                    last_total_power = 0.0
                else:
                    self.plot_canvas.cumulated_power_plot = last_plotted_power
                    self.plot_canvas.cumulated_previous_power_plot = last_incident_power

                self.plot_canvas.plot_power_density_ticket(ticket,
                                                           ticket["h_label"],
                                                           ticket["v_label"],
                                                           cumulated_total_power=last_total_power,
                                                           energy_min=energy_min,
                                                           energy_max=energy_max,
                                                           energy_step=energy_step,
                                                           cumulated_quantity=self.cumulated_quantity)

                self.cumulated_ticket = ticket
                self.plotted_ticket = ticket
                self.plotted_ticket_original = ticket.copy()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e), QMessageBox.Ok)

                if self.IS_DEVELOP: raise e

    def reload_plot(self):
        if not self.plotted_ticket_original is None:
            ticket = self.plotted_ticket_original.copy()

            if self.plot_canvas is None:
                self.plot_canvas = PowerPlotXYWidget()
                self.image_box.layout().addWidget(self.plot_canvas)

            cumulated_power_plot = numpy.sum(ticket["histogram"]) * (ticket["bin_h_center"][1] - ticket["bin_h_center"][0]) * (ticket["bin_v_center"][1] - ticket["bin_v_center"][0])

            try:
                try:
                    energy_min = ticket["energy_min"]
                    energy_max = ticket["energy_max"]
                    energy_step = ticket["energy_step"]
                except:
                    energy_min = 0.0
                    energy_max = 0.0
                    energy_step = 0.0

                self.plot_canvas.cumulated_power_plot = cumulated_power_plot
                self.plot_canvas.plot_power_density_ticket(ticket,
                                                           ticket["h_label"],
                                                           ticket["v_label"],
                                                           cumulated_total_power=0.0,
                                                           energy_min=energy_min,
                                                           energy_max=energy_max,
                                                           energy_step=energy_step,
                                                           cumulated_quantity=self.cumulated_quantity)

                self.plotted_ticket = ticket
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e), QMessageBox.Ok)

                if self.IS_DEVELOP: raise e

    def __flip(self, axis=0):
        if not self.plotted_ticket is None:
            try:
                ticket = self.plotted_ticket.copy()

                histogram = ticket["histogram"]
                h_coord = ticket["bin_h_center"]
                v_coord = ticket["bin_v_center"]

                h_coord, v_coord, histogram = flip(h_coord, v_coord, histogram, axis=axis)

                ticket["histogram"] = histogram
                ticket["bin_h_center"] = h_coord
                ticket["bin_v_center"] = v_coord

                pixel_area = (h_coord[1] - h_coord[0]) * (v_coord[1] - v_coord[0])

                if self.plot_canvas is None:
                    self.plot_canvas = PowerPlotXYWidget()
                    self.image_box.layout().addWidget(self.plot_canvas)

                cumulated_power_plot = numpy.sum(histogram) * pixel_area

                try:
                    energy_min = ticket["energy_min"]
                    energy_max = ticket["energy_max"]
                    energy_step = ticket["energy_step"]
                except:
                    energy_min = 0.0
                    energy_max = 0.0
                    energy_step = 0.0

                self.plot_canvas.cumulated_power_plot = cumulated_power_plot
                self.plot_canvas.plot_power_density_ticket(ticket,
                                                           ticket["v_label"],
                                                           ticket["h_label"],
                                                           cumulated_total_power=0.0,
                                                           energy_min=energy_min,
                                                           energy_max=energy_max,
                                                           energy_step=energy_step,
                                                           cumulated_quantity=self.cumulated_quantity)

                self.plotted_ticket = ticket
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e), QMessageBox.Ok)

                if self.IS_DEVELOP: raise e

    def flip_H(self):
        self.__flip(0)

    def flip_V(self):
        self.__flip(1)

    def invert_plot(self):
        if not self.plotted_ticket is None:
            try:
                ticket = self.plotted_ticket.copy()

                histogram = ticket["histogram"]
                h_coord = ticket["bin_h_center"]
                v_coord = ticket["bin_v_center"]

                h_coord, v_coord, histogram = invert(h_coord, v_coord, histogram)

                ticket["histogram"] = histogram
                ticket["bin_h_center"] = h_coord
                ticket["bin_v_center"] = v_coord

                pixel_area = (h_coord[1] - h_coord[0]) * (v_coord[1] - v_coord[0])

                if self.plot_canvas is None:
                    self.plot_canvas = PowerPlotXYWidget()
                    self.image_box.layout().addWidget(self.plot_canvas)

                cumulated_power_plot = numpy.sum(histogram) * pixel_area

                try:
                    energy_min = ticket["energy_min"]
                    energy_max = ticket["energy_max"]
                    energy_step = ticket["energy_step"]
                except:
                    energy_min = 0.0
                    energy_max = 0.0
                    energy_step = 0.0

                self.plot_canvas.cumulated_power_plot = cumulated_power_plot
                self.plot_canvas.plot_power_density_ticket(ticket,
                                                           ticket["v_label"],
                                                           ticket["h_label"],
                                                           cumulated_total_power=0.0,
                                                           energy_min=energy_min,
                                                           energy_max=energy_max,
                                                           energy_step=energy_step,
                                                           cumulated_quantity=self.cumulated_quantity)

                self.plotted_ticket = ticket
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e), QMessageBox.Ok)

                if self.IS_DEVELOP: raise e

    def rescale_plot(self):
        if not self.plotted_ticket is None:
            try:
                congruence.checkStrictlyPositiveNumber(self.scaling_factor, "Scaling Factor")

                ticket = self.plotted_ticket.copy()

                histogram = ticket["histogram"] * self.scaling_factor
                h_coord = ticket["bin_h_center"]
                v_coord = ticket["bin_v_center"]

                pixel_area = (h_coord[1] - h_coord[0]) * (v_coord[1] - v_coord[0])

                ticket["histogram"] = histogram

                if self.plot_canvas is None:
                    self.plot_canvas = PowerPlotXYWidget()
                    self.image_box.layout().addWidget(self.plot_canvas)

                cumulated_power_plot = numpy.sum(histogram) * pixel_area

                try:
                    energy_min = ticket["energy_min"]
                    energy_max = ticket["energy_max"]
                    energy_step = ticket["energy_step"]
                except:
                    energy_min = 0.0
                    energy_max = 0.0
                    energy_step = 0.0

                if not self.plot_canvas.cumulated_previous_power_plot is None:
                    self.plot_canvas.cumulated_previous_power_plot *= self.scaling_factor
                self.plot_canvas.cumulated_power_plot = cumulated_power_plot
                self.plot_canvas.plot_power_density_ticket(ticket,
                                                           ticket["v_label"],
                                                           ticket["h_label"],
                                                           cumulated_total_power=0.0,
                                                           energy_min=energy_min,
                                                           energy_max=energy_max,
                                                           energy_step=energy_step,
                                                           cumulated_quantity=self.cumulated_quantity)

                self.plotted_ticket = ticket
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e), QMessageBox.Ok)

                if self.IS_DEVELOP: raise e

    def rebin_plot(self):
        if not self.plotted_ticket is None:
            try:
                congruence.checkStrictlyPositiveNumber(self.new_nbins_h, "Nr. Bins H")
                congruence.checkStrictlyPositiveNumber(self.new_nbins_v, "Nr. Bins V")

                ticket = self.plotted_ticket.copy()

                histogram = ticket["histogram"]
                h_coord = ticket["bin_h_center"]
                v_coord = ticket["bin_v_center"]

                pixel_area_original = (h_coord[1] - h_coord[0]) * (v_coord[1] - v_coord[0])
                integral_original   = numpy.sum(histogram)

                h_coord, v_coord, histogram = rebin(h_coord, v_coord, histogram, (int(self.new_nbins_h), int(self.new_nbins_v)))

                pixel_area_rebin = (h_coord[1] - h_coord[0]) * (v_coord[1] - v_coord[0])

                if self.plot_canvas is None:
                    self.plot_canvas = PowerPlotXYWidget()
                    self.image_box.layout().addWidget(self.plot_canvas)

                integral_rebin = numpy.sum(histogram)

                histogram *= (integral_original * pixel_area_original) / (integral_rebin * pixel_area_rebin) # rinormalization

                cumulated_power_plot = numpy.sum(histogram) * pixel_area_rebin

                ticket["histogram"] = histogram
                ticket["bin_h_center"] = h_coord
                ticket["bin_v_center"] = v_coord

                try:
                    energy_min = ticket["energy_min"]
                    energy_max = ticket["energy_max"]
                    energy_step = ticket["energy_step"]
                except:
                    energy_min = 0.0
                    energy_max = 0.0
                    energy_step = 0.0

                self.plot_canvas.cumulated_power_plot = cumulated_power_plot
                self.plot_canvas.plot_power_density_ticket(ticket,
                                                           ticket["h_label"],
                                                           ticket["v_label"],
                                                           cumulated_total_power=0.0,
                                                           energy_min=energy_min,
                                                           energy_max=energy_max,
                                                           energy_step=energy_step,
                                                           cumulated_quantity=self.cumulated_quantity)

                self.plotted_ticket = ticket
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e), QMessageBox.Ok)

                if self.IS_DEVELOP: raise e

    def cut_plot(self):
        if not self.plotted_ticket is None:
            try:
                congruence.checkLessThan(self.new_range_h_from, self.new_range_h_to, "New Range H from", "New Range H to")
                congruence.checkLessThan(self.new_range_v_from, self.new_range_v_to, "New Range V from", "New Range V to")

                ticket = self.plotted_ticket.copy()

                histogram = ticket["histogram"]
                h_coord = ticket["bin_h_center"]
                v_coord = ticket["bin_v_center"]

                congruence.checkGreaterOrEqualThan(self.new_range_h_from, h_coord[0], "New Range H from", "Original Min(H)")
                congruence.checkLessOrEqualThan(self.new_range_h_to, h_coord[-1], "New Range H to", "Original Max(H)")
                congruence.checkGreaterOrEqualThan(self.new_range_v_from, v_coord[0], "New Range V from", "Original Min(V)")
                congruence.checkLessOrEqualThan(self.new_range_v_to, v_coord[-1], "New Range V to", "Original Max(V)")

                h_coord, v_coord, histogram = cut(h_coord, v_coord, histogram,
                                                  range_x=[self.new_range_h_from, self.new_range_h_to],
                                                  range_y=[self.new_range_v_from, self.new_range_v_to])

                ticket["histogram"] = histogram
                ticket["bin_h_center"] = h_coord
                ticket["bin_v_center"] = v_coord

                pixel_area = (h_coord[1] - h_coord[0]) * (v_coord[1] - v_coord[0])

                if self.plot_canvas is None:
                    self.plot_canvas = PowerPlotXYWidget()
                    self.image_box.layout().addWidget(self.plot_canvas)

                cumulated_power_plot = numpy.sum(histogram) * pixel_area

                try:
                    energy_min = ticket["energy_min"]
                    energy_max = ticket["energy_max"]
                    energy_step = ticket["energy_step"]
                except:
                    energy_min = 0.0
                    energy_max = 0.0
                    energy_step = 0.0

                self.plot_canvas.cumulated_power_plot = cumulated_power_plot
                self.plot_canvas.plot_power_density_ticket(ticket,
                                                           ticket["h_label"],
                                                           ticket["v_label"],
                                                           cumulated_total_power=0.0,
                                                           energy_min=energy_min,
                                                           energy_max=energy_max,
                                                           energy_step=energy_step,
                                                           cumulated_quantity=self.cumulated_quantity)

                self.plotted_ticket = ticket
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e), QMessageBox.Ok)

                if self.IS_DEVELOP: raise e

    def mask_plot(self):
        if not self.plotted_ticket is None:
            try:
                if self.masking == 0:
                    congruence.checkPositiveNumber(self.masking_level, "Masking Level")
                if self.masking == 1:
                    congruence.checkPositiveNumber(self.masking_width, "Masking Width")
                    congruence.checkPositiveNumber(self.masking_height, "Masking height")
                if self.masking == 2:
                    congruence.checkPositiveNumber(self.masking_diameter, "Masking Radius")

                ticket = copy.deepcopy(self.plotted_ticket)

                histogram = ticket["histogram"]
                h_coord = ticket["bin_h_center"]
                v_coord = ticket["bin_v_center"]

                if self.masking == 0:
                    if self.masking_type == 0:
                        mask = numpy.where(histogram <= self.masking_level)
                    else:
                        mask = numpy.where(histogram >= self.masking_level)
                    histogram[mask] = 0.0
                elif self.masking == 1:
                    if self.masking_type == 0:
                        mask_h = numpy.where(numpy.logical_or(h_coord < -self.masking_width / 2, h_coord > self.masking_width / 2))
                        mask_v = numpy.where(numpy.logical_or(v_coord < -self.masking_height / 2, v_coord > self.masking_height / 2))

                        histogram[mask_h, :] = 0.0
                        histogram[:, mask_v] = 0.0
                    else:
                        mask_h = numpy.where(numpy.logical_and(h_coord >= -self.masking_width / 2, h_coord <= self.masking_width / 2))
                        mask_v = numpy.where(numpy.logical_and(v_coord >= -self.masking_height / 2, v_coord <= self.masking_height / 2))

                        histogram[numpy.meshgrid(mask_h, mask_v)] = 0.0
                elif self.masking == 2:
                    h, v = numpy.meshgrid(v_coord, h_coord)
                    r = numpy.sqrt(h ** 2 + v ** 2)

                    if self.masking_type == 0: mask = numpy.where(r > self.masking_diameter * 0.5)
                    else:                      mask = numpy.where(r <= self.masking_diameter * 0.5)

                    histogram[mask] = 0.0

                pixel_area = (h_coord[1] - h_coord[0]) * (v_coord[1] - v_coord[0])

                ticket["histogram"] = histogram

                if self.plot_canvas is None:
                    self.plot_canvas = PowerPlotXYWidget()
                    self.image_box.layout().addWidget(self.plot_canvas)

                cumulated_power_plot = numpy.sum(ticket["histogram"]) * pixel_area

                try:
                    energy_min = ticket["energy_min"]
                    energy_max = ticket["energy_max"]
                    energy_step = ticket["energy_step"]
                except:
                    energy_min = 0.0
                    energy_max = 0.0
                    energy_step = 0.0

                self.plot_canvas.cumulated_power_plot = cumulated_power_plot
                self.plot_canvas.plot_power_density_ticket(ticket,
                                                           ticket["h_label"],
                                                           ticket["v_label"],
                                                           cumulated_total_power=0.0,
                                                           energy_min=energy_min,
                                                           energy_max=energy_max,
                                                           energy_step=energy_step,
                                                           cumulated_quantity=self.cumulated_quantity)

                self.plotted_ticket = ticket
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e), QMessageBox.Ok)

                if self.IS_DEVELOP: raise e

    def smooth_plot(self):
        if not self.plotted_ticket is None:
            try:
                if self.filter == 0 or 2 <= self.filter <= 5:
                    congruence.checkStrictlyPositiveNumber(self.filter_sigma_h, "Sigma/Size H")
                    congruence.checkStrictlyPositiveNumber(self.filter_sigma_v, "Sigma/Size V")

                if self.filter == 1: congruence.checkStrictlyPositiveNumber(self.filter_spline_order, "Spline Order")

                ticket = self.plotted_ticket.copy()

                histogram = ticket["histogram"]
                h_coord = ticket["bin_h_center"]
                v_coord = ticket["bin_v_center"]

                norm = histogram.sum()

                pixel_area = (h_coord[1] - h_coord[0]) * (v_coord[1] - v_coord[0])

                filter_mode = self.cb_filter_mode.currentText()

                if self.filter == 0:
                    histogram = filters.gaussian_filter(histogram, sigma=(self.filter_sigma_h, self.filter_sigma_v), mode=filter_mode, cval=self.filter_cval)
                elif self.filter == 1:
                    histogram = interpolation.spline_filter(histogram, order=int(self.filter_spline_order))
                elif self.filter == 2:
                    histogram = filters.uniform_filter(histogram, size=(int(self.filter_sigma_h), int(self.filter_sigma_v)), mode=filter_mode, cval=self.filter_cval)
                elif self.filter == 3:
                    histogram = numpy.real(numpy.fft.ifft2(fourier.fourier_gaussian(numpy.fft.fft2(histogram), sigma=(self.filter_sigma_h, self.filter_sigma_v))))
                elif self.filter == 4:
                    histogram = numpy.real(numpy.fft.ifft2(fourier.fourier_ellipsoid(numpy.fft.fft2(histogram), size=(self.filter_sigma_h, self.filter_sigma_v))))
                elif self.filter == 5:
                    histogram = numpy.real(numpy.fft.ifft2(fourier.fourier_uniform(numpy.fft.fft2(histogram), size=(self.filter_sigma_h, self.filter_sigma_v))))
                elif self.filter == 6:
                    histogram = apply_fill_holes(histogram)

                norm /= histogram.sum()

                ticket["histogram"] = histogram * norm

                if self.plot_canvas is None:
                    self.plot_canvas = PowerPlotXYWidget()
                    self.image_box.layout().addWidget(self.plot_canvas)

                cumulated_power_plot = numpy.sum(ticket["histogram"]) * pixel_area

                energy_min = 0.0
                energy_max = 0.0
                energy_step = 0.0

                self.plot_canvas.cumulated_power_plot = cumulated_power_plot
                self.plot_canvas.plot_power_density_ticket(ticket,
                                                           ticket["h_label"],
                                                           ticket["v_label"],
                                                           cumulated_total_power=0.0,
                                                           energy_min=energy_min,
                                                           energy_max=energy_max,
                                                           energy_step=energy_step,
                                                           cumulated_quantity=self.cumulated_quantity)

                self.plotted_ticket = ticket
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e), QMessageBox.Ok)

                if self.IS_DEVELOP: raise e

    def show_fit_formulas(self):
        dialog = ShowFitFormulasDialog(parent=self)
        dialog.show()

    def do_fit(self):
        if not self.plotted_ticket is None:
            try:
                ticket = self.plotted_ticket.copy()

                # NB, matplotlib inverts....
                histogram = ticket["histogram"].T
                h_coord = ticket["bin_h_center"]
                v_coord = ticket["bin_v_center"]

                def chisquare(pd, pd_fit, n):
                    N = pd.shape[0]*pd.shape[1]
                    squared_deviations = (pd-pd_fit)**2

                    return squared_deviations.sum()/(N-n)

                show = self.show_fit_plot == 1

                if self.fit_algorithm == 0:
                    if self.gauss_c_fixed == 1: bounds = bounds_gaussian(c=[-1e-12, 1e-12])
                    else:                       bounds = None

                    pd_fit_g, params_g = get_fitted_data_gaussian(h_coord, v_coord, histogram, bounds=bounds)

                    self.gauss_c =  round(params_g[0], 4)
                    self.gauss_A =  round(params_g[1], 4)
                    self.gauss_x0 = round(params_g[2], 4)
                    self.gauss_y0 = round(params_g[3], 4)
                    self.gauss_fx = round(params_g[4], 6)
                    self.gauss_fy = round(params_g[5], 6)
                    self.gauss_chisquare = round(chisquare(histogram, pd_fit_g, 6), 4)

                    params_string = '\n'.join((
                        r'$c=%.4f$' %   (self.gauss_c,),
                        r'$A=%.4f$' %   (self.gauss_A,),
                        r'$x_0=%.4f$' % (self.gauss_x0,),
                        r'$y_0=%.4f$' % (self.gauss_y0,),
                        r'$f_x=%.6f$' % (self.gauss_fx,),
                        r'$f_y=%.6f$' % (self.gauss_fy,),
                    ))

                    if show: self.plot_fit(h_coord, v_coord, histogram, pd_fit_g, "Gaussian", "gauss", self.gauss_chisquare, params_string,
                                           formula_img_file=gauss_formula_path, zoom=0.5, xybox=(85, -20))

                elif self.fit_algorithm == 1:
                    if self.pv_c_fixed == 1: bounds = bounds_pv(c=[-1e-12, 1e-12])
                    else:                    bounds = None

                    pd_fit_pv, params_pv = get_fitted_data_pv(h_coord, v_coord, histogram, bounds=bounds)

                    self.pv_c =  round(params_pv[0], 4)
                    self.pv_A =  round(params_pv[1], 4)
                    self.pv_x0 = round(params_pv[2], 4)
                    self.pv_y0 = round(params_pv[3], 4)
                    self.pv_fx = round(params_pv[4], 6)
                    self.pv_fy = round(params_pv[5], 6)
                    self.pv_mx = round(params_pv[6], 4)
                    self.pv_my = round(params_pv[7], 4)
                    self.pv_chisquare = round(chisquare(histogram, pd_fit_pv, 8), 4)

                    params_string = '\n'.join((
                        r'$c=%.4f$' %   (self.pv_c,),
                        r'$A=%.4f$' %   (self.pv_A,),
                        r'$x_0=%.4f$' % (self.pv_x0,),
                        r'$y_0=%.4f$' % (self.pv_y0,),
                        r'$f_x=%.6f$' % (self.pv_fx,),
                        r'$f_y=%.6f$' % (self.pv_fy,),
                        r'$m_x=%.4f$' % (self.pv_mx,),
                        r'$m_y=%.4f$' % (self.pv_my,),
                    ))

                    if show: self.plot_fit(h_coord, v_coord, histogram, pd_fit_pv, "Pseudo-Voigt", "p-v", self.pv_chisquare, params_string,
                                           formula_img_file=pv_formula_path, zoom=0.42, xybox=(215, -15))

                elif self.fit_algorithm == 2:
                    congruence.checkStrictlyPositiveNumber(self.poly_degree, "Degree")

                    pd_fit_poly, params_poly = get_fitted_data_poly(h_coord, v_coord, histogram, self.poly_degree)

                    params_poly = numpy.reshape(params_poly, (self.poly_degree + 1, self.poly_degree + 1))
                    params_string     = []
                    params_string_mpl = []
                    for i in range(params_poly.shape[0]):
                        for j in range(params_poly.shape[1]):
                            param = params_poly[i, j]
                            params_string.append(r'c%d,%d=%.4f' % (i, j, param,))
                            params_string_mpl.append(r'c_{%d,%d}=%.4f' % (i, j, param,))

                    params_string     = '\n'.join(params_string)
                    params_string_mpl = '\n'.join(params_string_mpl)

                    self.poly_coefficients_text.setText(params_string)
                    self.poly_chisquare = round(chisquare(histogram, pd_fit_poly, len(params_poly)), 4)

                    if show: self.plot_fit(h_coord, v_coord, histogram, pd_fit_poly, "Polynomial", "poly", self.poly_chisquare, params_string_mpl, fontsize=10,
                                           formula_img_file=poly_formula_path, zoom=0.5, xybox=(25, -20))

            except Exception as e:
                QMessageBox.critical(self, "Error", str(e), QMessageBox.Ok)

                if self.IS_DEVELOP: raise e

    def plot_fit(self, xx, yy, pd, pd_fit, algorithm, suffix, chisquare, params, fontsize=14,
                 formula_img_file=None, zoom=0.5, xybox=(85, -20)):
        dialog = ShowFitResultDialog(xx, yy, pd, pd_fit, algorithm, chisquare, params,
                                     file_name=None if self.autosave==0 else self.autosave_file_name,
                                     suffix=suffix,
                                     fontsize=fontsize,
                                     formula_img_file=formula_img_file,
                                     zoom=zoom,
                                     xybox=xybox,
                                     parent=self)
        dialog.show()

    def load_partial_results(self):
        file_name = None if self.autosave==0 else self.autosave_file_name

        if not file_name is None:
            plot_file = ShadowPlot.PlotXYHdf5File(congruence.checkDir(file_name), mode="r")

            ticket = {}

            ticket["histogram"], ticket["histogram_h"], ticket["histogram_v"], attributes = plot_file.get_last_plot(dataset_name="power_density")
            ticket["bin_h_center"], ticket["bin_v_center"], ticket["h_label"], ticket["v_label"] = plot_file.get_coordinates()
            ticket["intensity"] = attributes["intensity"]
            ticket["nrays"] = attributes["total_rays"]
            ticket["good_rays"] = attributes["good_rays"]

            if self.plot_canvas is None:
                self.plot_canvas = PowerPlotXYWidget()
                self.image_box.layout().addWidget(self.plot_canvas)

            try:
                last_plotted_power = plot_file.get_attribute("last_plotted_power", dataset_name="additional_data")
                last_incident_power = plot_file.get_attribute("last_incident_power", dataset_name="additional_data")
                last_total_power = plot_file.get_attribute("last_total_power", dataset_name="additional_data")
                energy_min = plot_file.get_attribute("last_energy_min", dataset_name="additional_data")
                energy_max = plot_file.get_attribute("last_energy_max", dataset_name="additional_data")
                energy_step = plot_file.get_attribute("last_energy_step", dataset_name="additional_data")
            except:
                last_plotted_power = numpy.sum(ticket["histogram"]) * (ticket["bin_h_center"][1] - ticket["bin_h_center"][0]) * (ticket["bin_v_center"][1] - ticket["bin_v_center"][0])
                last_incident_power = 0.0
                last_total_power = 0.0
                energy_min = 0.0
                energy_max = 0.0
                energy_step = 0.0

            try:
                self.plot_canvas.cumulated_power_plot = last_plotted_power
                self.plot_canvas.cumulated_previous_power_plot = last_incident_power
                self.plot_canvas.plot_power_density_ticket(ticket,
                                                           ticket["h_label"],
                                                           ticket["v_label"],
                                                           cumulated_total_power=last_total_power,
                                                           energy_min=energy_min,
                                                           energy_max=energy_max,
                                                           energy_step=energy_step,
                                                           cumulated_quantity=self.cumulated_quantity)

                self.cumulated_ticket = ticket
                self.plotted_ticket = ticket
                self.plotted_ticket_original = ticket.copy()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e), QMessageBox.Ok)

                if self.IS_DEVELOP: raise e


#################################################
# UTILITIES

def rebin(x, y, z, new_shape):
    shape = (new_shape[0], z.shape[0] // new_shape[0], new_shape[1], z.shape[1] // new_shape[1])

    return numpy.linspace(x[0], x[-1], new_shape[0]), \
           numpy.linspace(y[0], y[-1], new_shape[1]), \
           z.reshape(shape).mean(-1).mean(1)


def invert(x, y, data):
    return y, x, data.T


def flip(x, y, data, axis=0):
    return x, y, numpy.flip(data, axis=axis)


def cut(x, y, data, range_x, range_y):
    zoom_x = numpy.where(numpy.logical_and(x >= range_x[0], x <= range_x[1]))
    zoom_y = numpy.where(numpy.logical_and(y >= range_y[0], y <= range_y[1]))

    return x[zoom_x], y[zoom_y], data[numpy.meshgrid(zoom_x, zoom_y)].T


def apply_fill_holes(histogram):
    from skimage.morphology import reconstruction

    seed = numpy.copy(histogram)
    seed[1:-1, 1:-1] = histogram.max()

    filled = reconstruction(seed=seed, mask=histogram, method='erosion')

    return filled * (histogram.sum() / filled.sum())


####################################################
# FIT FUNCTIONS

def gaussian(c, height, center_x, center_y, fwhm_x, fwhm_y):
    sigma_x = float(fwhm_x / 2.355)
    sigma_y = float(fwhm_y / 2.355)

    return lambda x, y: c + height * numpy.exp(-((0.5 * ((x - center_x) / sigma_x) ** 2) + (0.5 * ((y - center_y) / sigma_y) ** 2)))


def pseudovoigt(c, height, center_x, center_y, fwhm_x, fwhm_y, mixing_x, mixing_y):
    sigma_x = fwhm_x / 2.355
    gamma_x = fwhm_x / 2
    sigma_y = fwhm_y / 2.355
    gamma_y = fwhm_y / 2

    def pv(x, center, sigma, gamma, mixing):
        return mixing * numpy.exp(-0.5 * (x - center) ** 2 / (sigma ** 2)) + (1 - mixing) * ((gamma ** 2) / ((x - center) ** 2 + gamma ** 2))

    return lambda x, y: c + height * pv(x, center_x, sigma_x, gamma_x, mixing_x) * pv(y, center_y, sigma_y, gamma_y, mixing_y)


def polynomial(coefficients):
    size = int(numpy.sqrt(len(coefficients)))
    coefficients = numpy.array(coefficients).reshape((size, size))

    return lambda x, y: polyval2d(x, y, coefficients)


from srxraylib.util.histograms import get_sigma, get_average


# Returns (x, y, width_x, width_y) the gaussian parameters of a 2D distribution by calculating its moments
def guess_params_gaussian(xx, yy, data):
    h_histo = data.sum(axis=0)
    v_histo = data.sum(axis=1)
    center_x = get_average(h_histo, xx)
    center_y = get_average(v_histo, yy)
    sigma_x = get_sigma(h_histo, xx)
    sigma_y = get_sigma(v_histo, yy)

    return 0.0, data.max(), center_x, center_y, sigma_x * 2.355, sigma_y * 2.355


def bounds_gaussian(c=None, height=None, center_x=None, center_y=None, fwhm_x=None, fwhm_y=None):
    bounds = [[0, 0, -numpy.inf, -numpy.inf, 0, 0],
              [numpy.inf, numpy.inf, numpy.inf, numpy.inf, numpy.inf, numpy.inf]]

    if not c is None:
        bounds[0][0] = c[0]
        bounds[1][0] = c[1]

    if not height is None:
        bounds[0][1] = height[0]
        bounds[1][1] = height[1]

    if not center_x is None:
        bounds[0][2] = center_x[0]
        bounds[1][2] = center_x[1]

    if not center_y is None:
        bounds[0][3] = center_y[0]
        bounds[1][3] = center_y[1]

    if not fwhm_x is None:
        bounds[0][4] = fwhm_x[0]
        bounds[1][4] = fwhm_x[1]

    if not fwhm_y is None:
        bounds[0][5] = fwhm_y[0]
        bounds[1][5] = fwhm_y[1]

    return bounds


def guess_params_pv(xx, yy, data):
    c, height, center_x, center_y, fwhm_x, fwhm_y = guess_params_gaussian(xx, yy, data)

    return c, height, center_x, center_y, fwhm_x, fwhm_y, 0.5, 0.5


def bounds_pv(c=None, height=None, center_x=None, center_y=None, fwhm_x=None, fwhm_y=None, mixing_x=None, mixing_y=None):
    bounds = [[0, 0, -numpy.inf, -numpy.inf, 0, 0, 0, 0],
              [numpy.inf, numpy.inf, numpy.inf, numpy.inf, numpy.inf, numpy.inf, 1, 1]]

    if not c is None:
        bounds[0][0] = c[0]
        bounds[1][0] = c[1]

    if not height is None:
        bounds[0][1] = height[0]
        bounds[1][1] = height[1]

    if not center_x is None:
        bounds[0][2] = center_x[0]
        bounds[1][2] = center_x[1]

    if not center_y is None:
        bounds[0][3] = center_y[0]
        bounds[1][3] = center_y[1]

    if not fwhm_x is None:
        bounds[0][4] = fwhm_x[0]
        bounds[1][4] = fwhm_x[1]

    if not fwhm_y is None:
        bounds[0][5] = fwhm_y[0]
        bounds[1][5] = fwhm_y[1]

    if not mixing_x is None:
        bounds[0][6] = mixing_x[0]
        bounds[1][6] = mixing_x[1]

    if not mixing_y is None:
        bounds[0][7] = mixing_y[0]
        bounds[1][7] = mixing_y[1]

    return bounds


def guess_params_poly(degree):
    return numpy.ones(int(degree + 1) ** 2).tolist()


def fit_gaussian(xx, yy, pd, guess_params=None, bounds=None):
    error_function = lambda p: numpy.ravel(gaussian(*p)(*numpy.meshgrid(xx, yy)) - pd)

    if guess_params is None: guess_params = guess_params_gaussian(xx, yy, pd)
    if bounds is None:       bounds = bounds_gaussian()

    optimized_result = least_squares(fun=error_function, x0=guess_params, bounds=bounds)

    return optimized_result.x


def fit_pseudovoigt(xx, yy, pd, guess_params=None, bounds=None):
    error_function = lambda p: numpy.ravel(pseudovoigt(*p)(*numpy.meshgrid(xx, yy)) - pd)

    if guess_params is None: guess_params = guess_params_pv(xx, yy, pd)
    if bounds is None:       bounds = bounds_pv()

    optimized_result = least_squares(fun=error_function, x0=guess_params, bounds=bounds)

    return optimized_result.x


def fit_polynomial(xx, yy, pd, degree=4, guess_params=None):
    error_function = lambda p: numpy.ravel(polynomial(p)(*numpy.meshgrid(xx, yy)) - pd)

    bounds = [numpy.full(int(degree + 1) ** 2, -numpy.inf).tolist(),
              numpy.full(int(degree + 1) ** 2, numpy.inf).tolist()]
    bounds[0][0] = 0.0

    optimized_result = least_squares(fun=error_function,
                                     x0=guess_params_poly(degree) if guess_params is None else guess_params,
                                     bounds=bounds)

    return optimized_result.x


def get_fitted_data_gaussian(xx, yy, pd, guess_params=None, bounds=None):
    params = fit_gaussian(xx, yy, pd, guess_params, bounds)
    fit = gaussian(*params)

    return fit(*numpy.meshgrid(xx, yy)), params


def get_fitted_data_pv(xx, yy, pd, guess_params=None, bounds=None):
    params = fit_pseudovoigt(xx, yy, pd, guess_params, bounds)
    fit = pseudovoigt(*params)

    return fit(*numpy.meshgrid(xx, yy)), params


def get_fitted_data_poly(xx, yy, pd, degree=4, guess_params=None):
    params = fit_polynomial(xx, yy, pd, degree, guess_params)
    fit = polynomial(params)

    return fit(*numpy.meshgrid(xx, yy)), params


formulas_path = os.path.join(resources.package_dirname("orangecontrib.shadow4_advanced.widgets.tools"), "misc", "fit_formulas.png")


class ShowFitFormulasDialog(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle('Fit Formulas')
        layout = QVBoxLayout(self)

        label = QLabel("")
        label.setAlignment(Qt.AlignCenter)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label.setPixmap(QPixmap(formulas_path))

        bbox = QDialogButtonBox(QDialogButtonBox.Ok)

        bbox.accepted.connect(self.accept)
        layout.addWidget(label)
        layout.addWidget(bbox)


from matplotlib import cm
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from matplotlib import gridspec

gauss_formula_path = os.path.join(resources.package_dirname("orangecontrib.shadow4_advanced.widgets.tools"), "misc", "gauss_formula.png")
pv_formula_path    = os.path.join(resources.package_dirname("orangecontrib.shadow4_advanced.widgets.tools"), "misc", "pv_formula.png")
poly_formula_path  = os.path.join(resources.package_dirname("orangecontrib.shadow4_advanced.widgets.tools"), "misc", "poly_formula.png")


class ShowFitResultDialog(QDialog):

    def __init__(self, xx, yy, pd, pd_fit, algorithm, chisquare, params_string, file_name=None, suffix=None,
                 fontsize=14, formula_img_file=None, zoom=0.5, xybox=(85, -20), parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle('Fit Result')
        layout = QVBoxLayout(self)

        self.file_name = None if file_name is None else \
            congruence.checkDir(os.path.splitext(file_name)[0] + "_fit" + ("" if suffix is None else ("_" + suffix)) + ".png")

        figure = Figure(figsize=(4, 8))
        figure.patch.set_facecolor('white')

        gs = gridspec.GridSpec(1, 2, width_ratios=[1, 3])
        ax = [None, None]
        ax[0] = figure.add_subplot(gs[0])
        ax[1] = figure.add_subplot(gs[1], projection='3d')

        ax[0].axis('off')
        ax[0].set_title("Fit Parameters")
        ax[0].text(-0.2, 0.95, params_string,
                   transform=ax[0].transAxes,
                   fontsize=fontsize,
                   verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        x_to_plot, y_to_plot = numpy.meshgrid(xx, yy)

        ax[1].plot_surface(x_to_plot, y_to_plot, pd,
                           rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0.5, antialiased=True, alpha=0.25)

        ax[1].plot_surface(x_to_plot, y_to_plot, pd_fit,
                           rstride=1, cstride=1, cmap=cm.Blues, linewidth=0.5, antialiased=True, alpha=0.75)

        ax[1].set_title(algorithm + " Fit\n\u03c7\u00b2 (RSS/\u03bd): " + str(chisquare))
        ax[1].set_xlabel("H [mm]")
        ax[1].set_ylabel("V [mm]")
        ax[1].set_zlabel("Power Density [W/mm\u00b2]")
        ax[1].axes.mouse_init()

        if not formula_img_file is None:
            from matplotlib.cbook import get_sample_data
            from matplotlib.pyplot import imread
            from matplotlib.offsetbox import AnnotationBbox, OffsetImage

            fn = get_sample_data(formula_img_file, asfileobj=False)
            arr_img = imread(fn, format='png')

            imagebox = OffsetImage(arr_img, zoom=zoom)
            imagebox.image.axes = ax[0]

            ab = AnnotationBbox(imagebox, (0.0, 0.0),
                                xybox=xybox,
                                xycoords='data',
                                boxcoords="offset points",
                                arrowprops=dict(arrowstyle="->"))
            ax[0].add_artist(ab)

        figure_canvas = FigureCanvasQTAgg(figure)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Save)
        self.buttonBox.accepted.connect(self.save)
        self.buttonBox.rejected.connect(self.reject)

        layout.addWidget(figure_canvas)
        layout.addWidget(self.buttonBox)

        self.figure = figure

    def save(self):
        file_name = oasysgui.selectSaveFileFromDialog(self, "Select File", default_file_name=("" if self.file_name is None else self.file_name), file_extension_filter="PNG Files (*.png)")

        if not file_name is None and not file_name.strip() == "":
            try:
                self.figure.savefig(file_name)
                QMessageBox.information(self, "Save", "Fit plot saved on file " + file_name, QMessageBox.Ok)
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e), QMessageBox.Ok)

