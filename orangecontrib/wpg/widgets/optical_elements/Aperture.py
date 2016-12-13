import numpy
from PyQt4.QtGui import QApplication, QPalette, QColor, QFont, QMessageBox

from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui
from oasys.widgets import congruence

from orangecontrib.wpg.util.wpg_objects import WPGOutput
from orangecontrib.wpg.widgets.gui.ow_wpg_widget import WPGWidget

from wpg.generators import build_gauss_wavefront_xy
from wpg import Wavefront
from wpg.useful_code.wfrutils import plot_wfront
from wpg.optical_elements import Drift, Aperture
from wpg.beamline import Beamline
from wpg.optical_elements import Empty, Use_PP

class OWAperture(WPGWidget):
    name = "Aperture"
    id = "Aperture"
    description = "Aperture"
    icon = "icons/aperture.png"
    priority = 1
    category = ""
    keywords = ["wpg", "gaussian"]

    inputs = [("Input", WPGOutput, "set_input")]

    horApM1 = Setting(2.E-3)
    range_xy = Setting(2.E-3) #CRL wall thickness [m])

    def build_gui(self):

        main_box = oasysgui.widgetBox(self.controlArea, "Aperture Input Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-5, height=200)

        oasysgui.lineEdit(main_box, self, "horApM1", "horApM1", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(main_box, self, "range_xy", "range_xy", labelWidth=260, valueType=float, orientation="horizontal")

    def after_change_workspace_units(self):
        pass

    def check_fields(self):
        congruence.checkPositiveNumber(self.horApM1, "horApM1")
        congruence.checkPositiveNumber(self.range_xy, "range_xy")

    def set_input(self, input_data):
        self.setStatusMessage("")

        if not input_data is None:
            self.input_data = input_data

            self.horApM1=self.input_data.get_thetaOM()* 0.8
            self.range_xy=self.input_data.get_range_xy()

            if self.is_automatic_run: self.compute()

    def do_wpg_calculation(self):
        aperture = Aperture(shape='r',ap_or_ob='a',Dx=self.horApM1, Dy=self.range_xy)

        wavefront = self.input_data.get_wavefront()

        beamline_for_propagation = Beamline()
        beamline_for_propagation.append(aperture, Use_PP())
        beamline_for_propagation.propagate(wavefront)

        return wavefront

    def extract_plot_data_from_calculation_output(self, calculation_output):
        self.reset_plotting()

        plot_wfront(calculation_output, 'at '+ str(self.input_data.get_total_distance()) +' m',False, False, 1e-5,1e-5,'x', False)

        return self.getFigureCanvas(1), \
               self.getFigureCanvas(2), \
               self.getFigureCanvas(3)

    def getTabTitles(self):
        return ["Intensity", "Vertical Cut", "Horizontal Cut"]

    def extract_wpg_output_from_calculation_output(self, calculation_output):
        return WPGOutput(thetaOM=self.input_data.get_thetaOM(),
                         range_xy=self.input_data.get_range_xy(),
                         wavefront=calculation_output, total_distance=self.input_data.get_total_distance())
