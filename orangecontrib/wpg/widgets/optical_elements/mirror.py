import os

from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui
from oasys.widgets import congruence

from orangecontrib.wpg.util.wpg_objects import WPGOutput
from orangecontrib.wpg.widgets.gui.ow_wpg_widget import WPGWidget

from wpg.useful_code.wfrutils import plot_wfront
from wpg.optical_elements import Drift, calculateOPD, Use_PP, WF_dist
from wpg.beamline import Beamline

class OWMirror(WPGWidget):
    name = "Mirror"
    id = "Mirror"
    description = "Mirror"
    icon = "icons/crl.png"
    priority = 3
    category = ""
    keywords = ["wpg", "gaussian"]

    inputs = [("Input", WPGOutput, "set_input")]


    file_name = Setting("/Users/labx/Desktop/Alexey/OASYS/mirror2.dat")

    # beam parameters:
    distance = Setting(641.0)

    horApM1 = 0.0
    range_xy = 0.0
    thetaOM = 0.0

    def build_gui(self):

        main_box = oasysgui.widgetBox(self.controlArea, "Mirror Input Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-5, height=200)

        oasysgui.lineEdit(main_box, self, "file_name", "CRL file", labelWidth=160, valueType=str, orientation="horizontal")

        gui.separator(main_box, height=5)

        oasysgui.lineEdit(main_box, self, "distance", "Distance to next [m]", labelWidth=260, valueType=float, orientation="horizontal")

    def after_change_workspace_units(self):
        pass

    def check_fields(self):
        congruence.checkPositiveNumber(self.distance, "Distance to next")

    def set_input(self, input_data):
        self.setStatusMessage("")

        if not input_data is None:
            self.input_data = input_data

            self.thetaOM = self.input_data.get_thetaOM()
            self.horApM1=self.input_data.get_thetaOM()* 0.8
            self.range_xy=self.input_data.get_range_xy()

            if self.is_automatic_run: self.compute()

    def do_wpg_calculation(self):

        opOPD_M = calculateOPD(WF_dist(nx=1500, ny=100, Dx=self.horApM1,Dy=self.range_xy),
                               '/Users/labx/Desktop/Alexey/OASYS/mirror2.dat',
                               2, ' ', 'x', self.thetaOM, scale=1)


        wavefront = self.input_data.get_wavefront()

        beamline_for_propagation = Beamline()
        beamline_for_propagation.append(opOPD_M, Use_PP())
        beamline_for_propagation.append(Drift(self.distance), Use_PP(semi_analytical_treatment=1, zoom=2.4, sampling=1.8))

        beamline_for_propagation.propagate(wavefront)

        return wavefront

    def extract_plot_data_from_calculation_output(self, calculation_output):
        self.reset_plotting()

        plot_wfront(calculation_output, 'at '+ str(self.distance + self.input_data.get_total_distance()) +' m',False, False, 1e-5,1e-5,'x', False)

        return self.getFigureCanvas(1), \
               self.getFigureCanvas(2), \
               self.getFigureCanvas(3)

    def getTabTitles(self):
        return ["Intensity", "Vertical Cut", "Horizontal Cut"]

    def extract_wpg_output_from_calculation_output(self, calculation_output):
        return WPGOutput(wavefront=calculation_output, distance_to_previous=self.distance, total_distance=(self.distance + self.input_data.get_total_distance()))
