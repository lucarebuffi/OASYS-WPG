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
from wpg.optical_elements import Drift, create_CRL_from_file
from wpg.beamline import Beamline
from wpg.optical_elements import Empty, Use_PP

class OWCRL(WPGWidget):
    name = "CRL"
    id = "CRL"
    description = "CRL"
    icon = "icons/crl.png"
    priority = 2
    category = ""
    keywords = ["wpg", "gaussian"]

    inputs = [("Input", WPGOutput, "set_input")]

    nCRL = Setting(1) #number of lenses, collimating
    delta = Setting(7.511e-06)
    attenLen = Setting(3.88E-3)
    diamCRL = 3.58e-03 #CRL diameter
    wallThickCRL = Setting(30e-06) #CRL wall thickness [m])

    file_name = Setting("opd_CRL1.pkl")

    # beam parameters:
    distance = Setting(55.0)

    def build_gui(self):

        main_box = oasysgui.widgetBox(self.controlArea, "CRL Input Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-5, height=200)

        oasysgui.lineEdit(main_box, self, "nCRL", "Number of Lenses", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(main_box, self, "delta", "Delta", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(main_box, self, "attenLen", "Attenuation length", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(main_box, self, "diamCRL", "CRL diameter", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(main_box, self, "wallThickCRL", "CRL wall Thickness", labelWidth=260, valueType=float, orientation="horizontal")

        oasysgui.lineEdit(main_box, self, "file_name", "CRL file", labelWidth=160, valueType=str, orientation="horizontal")

        gui.separator(main_box, height=5)

        oasysgui.lineEdit(main_box, self, "distance", "Distance to next [m]", labelWidth=260, valueType=float, orientation="horizontal")

    def after_change_workspace_units(self):
        pass

    def check_fields(self):
        congruence.checkStrictlyPositiveNumber(self.nCRL, "Number of Lenses")
        congruence.checkPositiveNumber(self.delta, "delta")
        congruence.checkPositiveNumber(self.attenLen, "Attenuation length")
        congruence.checkPositiveNumber(self.diamCRL, "CRL diameter")

        congruence.checkPositiveNumber(self.distance, "Distance to next")

    def set_input(self, input_data):
        self.setStatusMessage("")

        if not input_data is None:
            self.input_data = input_data

            if self.is_automatic_run: self.compute()

    def do_wpg_calculation(self):
        rMinCRL = 2*self.delta*self.input_data.get_distance_to_previous()/self.nCRL #CRL radius at the tip of parabola [m]

        opCRL = create_CRL_from_file(self.working_directory,
                                     self.file_name,
                                     3,
                                     self.delta,
                                     self.attenLen,
                                     1,
                                     self.diamCRL,
                                     self.diamCRL,
                                     rMinCRL,
                                     self.nCRL,
                                     self.wallThickCRL,
                                     0,
                                     0,
                                     None)

        wavefront = self.input_data.get_wavefront()

        beamline_for_propagation = Beamline()
        beamline_for_propagation.append(opCRL, Use_PP())
        beamline_for_propagation.append(Drift(self.distance), Use_PP(semi_analytical_treatment=1))

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
        return WPGOutput(thetaOM=self.input_data.get_thetaOM(),
                         range_xy=self.input_data.get_range_xy(),
                         wavefront=calculation_output,
                         distance_to_previous=self.distance,
                         total_distance=(self.distance + self.input_data.get_total_distance()))
