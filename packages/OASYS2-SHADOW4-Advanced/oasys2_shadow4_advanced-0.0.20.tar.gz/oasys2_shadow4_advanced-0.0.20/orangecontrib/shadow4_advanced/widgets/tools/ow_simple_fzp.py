import sys, numpy

from AnyQt.QtWidgets import QMessageBox

from orangewidget import gui
from orangewidget.settings import Setting
from orangewidget.widget import Input, Output

from oasys2.widget.widget import OWAction
from oasys2.widget import gui as oasysgui
from oasys2.widget.util import congruence
from oasys2.widget.util.widget_util import EmittingStream
from oasys2.widget.gui import Styles
from oasys2.widget.util.widget_objects import TriggerIn
from oasys2.canvas.util.canvas_util import add_widget_parameters_to_module

from syned.beamline.element_coordinates import ElementCoordinates

try:
    from orangecontrib.shadow4.util.shadow4_objects import ShadowData
    from orangecontrib.shadow4.util.shadow4_util import ShadowCongruence, TriggerToolsDecorator
    from orangecontrib.shadow4.widgets.gui.ow_generic_element import GenericElement
except ImportError:
    raise ImportError("OASYS2-SHADOW4 add-on required to run OASYS2-SHADOW4-Advanced")

from shadow4_advanced.beamline.optical_elements.gratings.s4_simple_fzp import (
    S4SimpleFZP, S4SimpleFZPElement, FZPType, W2E
)

class OWSimpleFZP(GenericElement, TriggerToolsDecorator):
    name = "Simple FZP"
    description = "Advanced: Simple Fresnel Zone Plate"
    icon = "icons/simple_fzp.png"
    maintainer = "Luca Rebuffi"
    maintainer_email = "lrebuffi(@at@)anl.gov"
    priority = 4.0
    category = "Optical Elements"
    keywords = ["data", "file", "load", "read"]

    class Inputs:
        shadow_data = Input("Shadow Data", ShadowData, default=True, auto_summary=False)
        trigger = TriggerToolsDecorator.get_trigger_input()

    class Outputs:
        shadow_data = Output("Shadow Data", ShadowData, default=True, auto_summary=False)
        trigger = TriggerToolsDecorator.get_trigger_output()

    input_data  = None
    output_data = None

    NONE_SPECIFIED = "NONE SPECIFIED"

    ONE_ROW_HEIGHT = 65
    TWO_ROW_HEIGHT = 110
    THREE_ROW_HEIGHT = 170

    INNER_BOX_WIDTH_L3 = 322
    INNER_BOX_WIDTH_L2 = 335
    INNER_BOX_WIDTH_L1 = 358
    INNER_BOX_WIDTH_L0 = 375

    source_plane_distance = Setting(10.0)
    image_plane_distance = Setting(20.0)

    delta_rn = Setting(25) # nm
    diameter = Setting(618) # micron

    source_distance_flag = Setting(0)
    source_distance = Setting(0.0)

    type_of_zp = Setting(1)

    zone_plate_material = Setting("Au")
    zone_plate_thickness = Setting(200) # nm
    substrate_material = Setting("Si3N4")
    substrate_thickness = Setting(50) # nm

    avg_wavelength = 0.0
    number_of_zones = 0
    focal_distance = 0.0
    image_position = 0.0
    magnification = 0.0
    efficiency = 0.0
    max_efficiency = 0.0
    thickness_max_efficiency = 0.0
    predicted_focal_size_zp = 0.0
    predicted_focal_size_ss = 0.0
    predicted_focal_size_de = 0.0
    predicted_focal_size_total = 0.0

    automatically_set_image_plane = Setting(0)

    energy_plot = Setting(0)
    thickness_plot = Setting(0)
    energy_from = Setting(0)
    energy_to = Setting(0)
    thickness_from = Setting(0)
    thickness_to = Setting(0)

    ##################################################

    not_interactive = False

    def __init__(self):
        super(OWSimpleFZP, self).__init__(show_automatic_box=True, has_footprint=False)

        self.runaction = OWAction("Run Shadow4/Trace", self)
        self.runaction.triggered.connect(self.run_shadow4)
        self.addAction(self.runaction)

        button_box = oasysgui.widgetBox(self.controlArea, "", addSpace=False, orientation="horizontal")

        button = gui.button(button_box, self, "Run Shadow4/Trace", callback=self.run_shadow4)
        button.setStyleSheet(Styles.button_blue)

        button = gui.button(button_box, self, "Reset Fields", callback=self.callResetSettings)
        button.setStyleSheet(Styles.button_red)

        gui.separator(self.controlArea)

        tabs_setting = oasysgui.tabWidget(self.controlArea)
        tabs_setting.setFixedHeight(self.TABS_AREA_HEIGHT)
        tabs_setting.setFixedWidth(self.CONTROL_AREA_WIDTH - 5)

        tab_pos = oasysgui.createTabPage(tabs_setting, "Position")

        upper_box = oasysgui.widgetBox(tab_pos, "Optical Element Orientation", addSpace=True, orientation="vertical")

        self.le_source_plane_distance = oasysgui.lineEdit(upper_box, self, "source_plane_distance", "Source Plane Distance [m]", labelWidth=260, valueType=float, orientation="horizontal")
        self.le_image_plane_distance = oasysgui.lineEdit(upper_box, self, "image_plane_distance", "Image Plane Distance [m]", labelWidth=260, valueType=float, orientation="horizontal")

        tab_bas = oasysgui.createTabPage(tabs_setting, "Fresnel Zone Plate")

        ##########################################
        ##########################################
        # BASIC SETTINGS
        ##########################################
        ##########################################

        tabs_basic_setting = oasysgui.tabWidget(tab_bas)
        tabs_setting.setFixedHeight(self.TABS_AREA_HEIGHT-5)
        tabs_setting.setFixedWidth(self.CONTROL_AREA_WIDTH-5)

        tab_zone_plate_1 = oasysgui.createTabPage(tabs_basic_setting, "Zone Plate Input Parameters")
        tab_zone_plate_2 = oasysgui.createTabPage(tabs_basic_setting, "Zone Plate Output Parameters")

        zp_box = oasysgui.widgetBox(tab_zone_plate_1, "Input Parameters", addSpace=False, orientation="vertical", height=290)

        oasysgui.lineEdit(zp_box, self, "delta_rn",  u"\u03B4" + "rn [nm]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(zp_box, self, "diameter", "Z.P. Diameter [" + u"\u03BC" + "m]", labelWidth=260, valueType=float, orientation="horizontal")

        gui.comboBox(zp_box, self, "source_distance_flag", label="Source Distance", labelWidth=350,
                     items=["Same as Source Plane", "Different"],
                     callback=self.set_source_distance_flag, sendSelectedValue=False, orientation="horizontal")

        self.zp_box_1 = oasysgui.widgetBox(zp_box, "", addSpace=False, orientation="vertical", height=30)
        self.zp_box_2 = oasysgui.widgetBox(zp_box, "", addSpace=False, orientation="vertical", height=30)

        self.le_source_distance = oasysgui.lineEdit(self.zp_box_1, self, "source_distance", "Source Distance", labelWidth=260, valueType=float, orientation="horizontal")

        self.set_source_distance_flag()

        gui.comboBox(zp_box, self, "type_of_zp", label="Type of Zone Plate", labelWidth=350,
                     items=["Amplitude", "Phase"],
                     callback=self.set_type_of_zp, sendSelectedValue=False, orientation="horizontal")

        gui.separator(zp_box, height=5)

        self.zp_box_3 = oasysgui.widgetBox(zp_box, "", addSpace=False, orientation="vertical")

        oasysgui.lineEdit(self.zp_box_3, self, "zone_plate_material",  "Zone Plate Material", labelWidth=260, valueType=str, orientation="horizontal")
        oasysgui.lineEdit(self.zp_box_3, self, "zone_plate_thickness",  "Zone Plate Thickness [nm]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.zp_box_3, self, "substrate_material", "Substrate Material", labelWidth=260, valueType=str, orientation="horizontal")
        oasysgui.lineEdit(self.zp_box_3, self, "substrate_thickness",  "Substrate Thickness [nm]", labelWidth=260, valueType=float, orientation="horizontal")

        self.set_type_of_zp()

        zp_out_box = oasysgui.widgetBox(tab_zone_plate_2, "Output Parameters", addSpace=False, orientation="vertical", height=270)

        read_only_style = Styles.line_edit_read_only

        self.le_avg_wavelength = oasysgui.lineEdit(zp_out_box, self, "avg_wavelength", "Average Wavelength [nm]", labelWidth=260, valueType=float, orientation="horizontal")
        self.le_avg_wavelength.setReadOnly(True)
        self.le_avg_wavelength.setStyleSheet(read_only_style)

        self.le_number_of_zones = oasysgui.lineEdit(zp_out_box, self, "number_of_zones", "Number of Zones", labelWidth=260, valueType=float, orientation="horizontal")
        self.le_number_of_zones.setReadOnly(True)
        self.le_number_of_zones.setStyleSheet(read_only_style)

        self.le_focal_distance = oasysgui.lineEdit(zp_out_box, self, "focal_distance", "Focal Distance", labelWidth=260, valueType=float, orientation="horizontal")
        self.le_focal_distance.setReadOnly(True)
        self.le_focal_distance.setStyleSheet(read_only_style)

        self.le_image_position = oasysgui.lineEdit(zp_out_box, self, "image_position", "Image Position (Q)", labelWidth=260, valueType=float, orientation="horizontal")
        self.le_image_position.setReadOnly(True)
        self.le_image_position.setStyleSheet(read_only_style)

        self.le_magnification = oasysgui.lineEdit(zp_out_box, self, "magnification", "Magnification", labelWidth=260, valueType=float, orientation="horizontal")
        self.le_magnification.setReadOnly(True)
        self.le_magnification.setStyleSheet(read_only_style)

        self.le_efficiency = oasysgui.lineEdit(zp_out_box, self, "efficiency", "Efficiency % (Avg. Wavelength)", labelWidth=260, valueType=float, orientation="horizontal")
        self.le_efficiency.setReadOnly(True)
        self.le_efficiency.setStyleSheet(read_only_style)

        self.le_max_efficiency = oasysgui.lineEdit(zp_out_box, self, "max_efficiency", "Max Possible Efficiency %", labelWidth=260, valueType=float, orientation="horizontal")
        self.le_max_efficiency.setReadOnly(True)
        self.le_max_efficiency.setStyleSheet(read_only_style)

        self.le_thickness_max_efficiency = oasysgui.lineEdit(zp_out_box, self, "thickness_max_efficiency", "Max Efficiency Thickness [nm]", labelWidth=260, valueType=float, orientation="horizontal")
        self.le_thickness_max_efficiency.setReadOnly(True)
        self.le_thickness_max_efficiency.setStyleSheet(read_only_style)

        gui.comboBox(zp_out_box, self, "automatically_set_image_plane", label="Automatically set Image Plane Distance", labelWidth=350,
                     items=["No", "Yes"], sendSelectedValue=False, orientation="horizontal")

        zp_out_box_2 = oasysgui.widgetBox(tab_zone_plate_2, "Efficiency Plot", addSpace=False, orientation="vertical", height=200)

        gui.comboBox(zp_out_box_2, self, "energy_plot", label="Plot Efficiency vs. Energy", labelWidth=350,
                     items=["No", "Yes"],
                     sendSelectedValue=False, orientation="horizontal", callback=self.set_energy_plot)

        self.zp_out_box_2_1 = oasysgui.widgetBox(zp_out_box_2, "", addSpace=False, orientation="vertical", height=50)
        self.zp_out_box_2_2 = oasysgui.widgetBox(zp_out_box_2, "", addSpace=False, orientation="vertical", height=50)

        oasysgui.lineEdit(self.zp_out_box_2_1, self, "energy_from",  "Energy From [eV]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.zp_out_box_2_1, self, "energy_to",  "Energy To [eV]", labelWidth=260, valueType=float, orientation="horizontal")

        gui.comboBox(zp_out_box_2, self, "thickness_plot", label="Plot Efficiency vs. Thickness", labelWidth=350,
                     items=["No", "Yes"],
                     sendSelectedValue=False, orientation="horizontal", callback=self.set_thickness_plot)

        self.zp_out_box_2_3 = oasysgui.widgetBox(zp_out_box_2, "", addSpace=False, orientation="vertical", height=50)
        self.zp_out_box_2_4 = oasysgui.widgetBox(zp_out_box_2, "", addSpace=False, orientation="vertical", height=50)

        oasysgui.lineEdit(self.zp_out_box_2_3, self, "thickness_from",  "Thickness From [nm]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.zp_out_box_2_3, self, "thickness_to",  "Thickness To [nm]", labelWidth=260, valueType=float, orientation="horizontal")

        self.set_energy_plot()
        self.set_thickness_plot()

        gui.rubber(self.controlArea)
        gui.rubber(self.mainArea)

    def set_energy_plot(self):

        self.zp_out_box_2_1.setVisible(self.energy_plot==1)
        self.zp_out_box_2_2.setVisible(self.energy_plot==0)

    def set_thickness_plot(self):
        self.zp_out_box_2_3.setVisible(self.thickness_plot==1)
        self.zp_out_box_2_4.setVisible(self.thickness_plot==0)

    def run_shadow4(self, scanning_data: ShadowData.ScanningData = None):
        if self.input_data is None:
            self.prompt_exception(ValueError("No input beam"))
            return
        if not scanning_data: scanning_data = None

        try:
            self.setStatusMessage("")
            self.progressBarInit()

            if ShadowCongruence.check_empty_data(self.input_data):
                if ShadowCongruence.check_good_beam(self.input_data.beam):
                    self.checkFields()

                    sys.stdout = EmittingStream(textWritten=self._write_stdout)

                    beamline = self.input_data.beamline.duplicate()

                    self.progressBarSet(10)

                    if self.source_distance_flag == 0: self.source_distance = self.source_plane_distance

                    element = S4SimpleFZPElement(optical_element=S4SimpleFZP(name="Simple FZP",
                                                                             diameter=self.diameter*1e-6,
                                                                             delta_rn=self.delta_rn*1e-9,
                                                                             source_distance=self.source_distance,
                                                                             type_of_zp=self.type_of_zp,
                                                                             zone_plate_material=self.zone_plate_material,
                                                                             zone_plate_thickness=self.zone_plate_thickness*1e-9,
                                                                             substrate_material=self.substrate_material,
                                                                             substrate_thickness=self.substrate_thickness*1e-9),
                                                 coordinates=ElementCoordinates(p=self.source_distance, q=self.image_plane_distance),
                                                 input_beam=self.input_data.beam)
                    # element.set_movements(self.get_movements_instance()) for the future

                    print(element.info())

                    output_beam, footprint, calculation_result = element.trace_beam()

                    self.progressBarSet(60)

                    simple_fzp_out: S4SimpleFZP = element.get_optical_element()
                    avg_wavelength = numpy.average(output_beam.get_photon_wavelength(nolost=1))*1e9

                    self.number_of_zones = calculation_result.get('number_of_zones', -1)

                    self.avg_wavelength = avg_wavelength
                    self.focal_distance = simple_fzp_out.focal_distance(avg_wavelength)
                    self.image_position = simple_fzp_out.image_position(self.focal_distance)
                    self.magnification  = simple_fzp_out.magnification(self.image_position)

                    self.avg_wavelength = numpy.round(self.avg_wavelength, 3)  # nm
                    self.focal_distance = numpy.round(self.focal_distance, 6)
                    self.image_position = numpy.round(self.image_position, 6)
                    self.magnification  = numpy.round(self.magnification, 6)

                    if self.automatically_set_image_plane == 1: self.image_plane_distance = self.image_position

                    self.progressBarSet(80)

                    self.setStatusMessage("Plotting Results")

                    self._plot_efficiency(simple_fzp_out, avg_wavelength)
                    self._plot_results(output_beam, None)

                    self.setStatusMessage("")

                    beamline.append_beamline_element(element)

                    script = beamline.to_python_code()
                    script += "\n\n\n# test plot"
                    script += "\nif True:"
                    script += "\n   from srxraylib.plot.gol import plot_scatter"
                    script += "\n   plot_scatter(beam.get_photon_energy_eV(nolost=1), beam.get_column(23, nolost=1), title='(Intensity,Photon Energy)', plot_histograms=0)"
                    script += "\n   plot_scatter(1e6 * beam.get_column(1, nolost=1), 1e6 * beam.get_column(3, nolost=1), title='(X,Z) in microns')"
                    self.shadow4_script.set_code(script)

                    #
                    # send beam and trigger
                    #
                    output_data = ShadowData(beam=output_beam, footprint=footprint, beamline=beamline)
                    output_data.scanning_data = scanning_data

                    self.Outputs.shadow_data.send(output_data)
                    self.Outputs.trigger.send(TriggerIn(new_object=True))
                else:
                    raise Exception("Input Beam with no good rays")
            else:
                raise Exception("Empty Input Beam")

        except Exception as exception:
            QMessageBox.critical(self, "Error", str(exception), QMessageBox.Ok)

            if self.IS_DEVELOP: raise exception

        self.progressBarFinished()

    @Inputs.trigger
    def set_trigger_parameters_for_optics(self, trigger):
        super(OWSimpleFZP, self).set_trigger_parameters_for_optics(trigger)

    @Inputs.shadow_data
    def set_shadow_data(self, shadow_data):
        if ShadowCongruence.check_empty_data(shadow_data):
            self.input_data = shadow_data

            if self.is_automatic_run:
                self.run_shadow4()

    def checkFields(self):
        self.source_plane_distance = congruence.checkNumber(self.source_plane_distance, "Source plane distance")
        self.image_plane_distance = congruence.checkNumber(self.image_plane_distance, "Image plane distance")

        congruence.checkStrictlyPositiveNumber(self.delta_rn, u"\u03B4" + "rn" )
        congruence.checkStrictlyPositiveNumber(self.diameter, "Z.P. Diameter")
        if (self.source_distance_flag == 1):
            congruence.checkPositiveNumber(self.source_distance, "Source Distance" )

        if self.type_of_zp == FZPType.PHASE_ZP:
            congruence.checkEmptyString(self.zone_plate_material, "Zone Plate Material")
            congruence.checkStrictlyPositiveNumber(self.zone_plate_thickness, "Zone Plate Thickness")
            congruence.checkEmptyString(self.substrate_material, "Substrate Material")
            congruence.checkStrictlyPositiveNumber(self.substrate_thickness, "Substrate Thickness")


    def callResetSettings(self):
        super()._call_reset_settings()

    def set_type_of_zp(self):
        self.zp_box_3.setVisible(self.type_of_zp == FZPType.PHASE_ZP)

    def set_source_distance_flag(self):
        self.zp_box_1.setVisible(self.source_distance_flag == 1)
        self.zp_box_2.setVisible(self.source_distance_flag == 0)

    def _plot_efficiency(self, simple_fzp_out: S4SimpleFZP, avg_wavelength: float):
        if self.type_of_zp == FZPType.PHASE_ZP:
            if self.energy_plot == 1:
                if self.plot_canvas[5] is None:
                    self.plot_canvas[5] = oasysgui.plotWindow(roi=False, control=False, position=True, logScale=False)
                    self.tab[5].layout().addWidget(self.plot_canvas[5])

                self.plot_canvas[5].clear()

                self.plot_canvas[5].setDefaultPlotLines(True)
                self.plot_canvas[5].setActiveCurveStyle(color='blue')

                self.plot_canvas[5].setGraphTitle('Thickness: ' + str(self.zone_plate_thickness) + " nm")
                self.plot_canvas[5].getXAxis().setLabel('Energy [eV]')
                self.plot_canvas[5].getYAxis().setLabel('Efficiency [%]')

                x_values = numpy.linspace(self.energy_from, self.energy_to, 100)
                y_values = numpy.round(100.0 * simple_fzp_out.get_efficiency_by_energy(energies=x_values), 3)

                self.plot_canvas[5].addCurve(x_values, y_values, "Efficiency vs Energy", symbol='', color='blue', replace=True)
            else:
                if not self.plot_canvas[5] is None: self.plot_canvas[5].clear()

            if self.thickness_plot == 1:
                if self.plot_canvas[6] is None:
                    self.plot_canvas[6] = oasysgui.plotWindow(roi=False, control=False, position=True, logScale=False)
                    self.tab[6].layout().addWidget(self.plot_canvas[6])

                self.plot_canvas[6].setDefaultPlotLines(True)
                self.plot_canvas[6].setActiveCurveStyle(color='blue')

                self.plot_canvas[6].setGraphTitle('Energy: ' + str(round((W2E / avg_wavelength) * 1e9, 3)) + " eV")
                self.plot_canvas[6].getXAxis().setLabel('Thickness [nm]')
                self.plot_canvas[6].getYAxis().setLabel('Efficiency [%]')

                x_values = numpy.linspace(self.thickness_from, self.thickness_to, 100)
                y_values = numpy.round(100 * simple_fzp_out.get_efficiency_by_thickness(avg_wavelength, x_values), 3)

                self.plot_canvas[6].addCurve(x_values, y_values, "Efficiency vs Thickness", symbol='', color='blue', replace=True)
            else:
                if not self.plot_canvas[6] is None: self.plot_canvas[6].clear()

        else:
            if not self.plot_canvas[5] is None: self.plot_canvas[5].clear()
            if not self.plot_canvas[6] is None: self.plot_canvas[6].clear()

    def _get_titles(self):
        titles = super(OWSimpleFZP, self)._get_titles()
        titles.append("Efficiency vs. Energy")
        titles.append("Efficiency vs. Thickness")

        return titles


add_widget_parameters_to_module(__name__)