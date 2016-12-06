import sys
import numpy
from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui
from oasys.widgets import congruence

from orangecontrib.wpg.util.wpg_objects import WPGOutput
from orangecontrib.wpg.widgets.gui.ow_wpg_widget import WPGWidget

import wpg
from wpg.generators import build_gauss_wavefront
from wpg.beamline import Beamline
from wpg.optical_elements import Drift, Use_PP
from wpg.srwlib import srwl
from wpg.useful_code.wfrutils import plot_wfront

import pylab

class OWGaussianWavefront(WPGWidget):
    name = "GaussianWavefront"
    id = "GaussianWavefront"
    description = "GaussianWavefront"
    icon = "icons/gaussian_wavefront.png"
    priority = 1
    category = ""
    keywords = ["wpg", "gaussian"]

    d2waist = Setting(270)
    # beam parameters:
    qnC = Setting(0.1)  # [nC] e-bunch charge
    thetaOM = Setting(3.6e-3)
    ekev = Setting(5.0)

    propagation_distance = Setting(5.0)

    def build_gui(self):

        main_box = oasysgui.widgetBox(self.controlArea, "Gaussian Source 1D Input Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-5, height=200)

        self.le_d2waist = oasysgui.lineEdit(main_box, self, "d2waist", "d2waist", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(main_box, self, "qnC", "e-bunch charge [nC]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(main_box, self, "thetaOM", "thetaOM", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(main_box, self, "ekev", "Energy [keV]", labelWidth=260, valueType=float, orientation="horizontal")

        gui.separator(main_box, height=5)

        oasysgui.lineEdit(main_box, self, "propagation_distance", "Propagation Distance (plots) [m]", labelWidth=260, valueType=float, orientation="horizontal")

    def after_change_workspace_units(self):
        label = self.le_d2waist.parent().layout().itemAt(0).widget()
        label.setText(label.text() + " [" + self.workspace_units_label + "]")

    def check_fields(self):
        congruence.checkPositiveNumber(self.qnC, "e-bunch charge")
        congruence.checkStrictlyPositiveNumber(self.ekev, "energy")
        congruence.checkPositiveNumber(self.propagation_distance, "Propagation Distance")


    def do_wpg_calculation(self):
        # calculate angular divergence:
        theta_fwhm = (17.2 - 6.4 * numpy.sqrt(self.qnC)) * 1e-6 / self.ekev ** 0.85
        theta_rms = theta_fwhm / 2.35
        sigX = 12.4e-10 / (self.ekev * 4 * numpy.pi * theta_rms)

        # define limits
        xmax = theta_rms * self.d2waist * 3.5
        xmin = - xmax
        ymin = xmin
        ymax = xmax
        nx = 300
        ny = nx
        nz = 3
        tau = 0.12e-15

        srw_wf = build_gauss_wavefront(nx, ny, nz, self.ekev, xmin, xmax, ymin, ymax, tau, sigX, sigX, self.d2waist)

        wf = wpg.Wavefront(srw_wf)

        b = Beamline()
        b.append(Drift(self.propagation_distance), Use_PP())
        b.propagate(wf)

        srwl.ResizeElecField(srw_wf, 'c', [0, 0.25, 1, 0.25, 1])

        return wf


    def extract_plot_data_from_calculation_output(self, calculation_output):
        mwf = calculation_output
        dd =  plot_wfront(mwf, 'at '+str(self.propagation_distance)+' m', False, False, 1e-5,1e-5,'x', True)

        pylab.show()

        return dd


    def extract_wpg_output_from_calculation_output(self, calculation_output):
        return WPGOutput(wavefront=calculation_output, beamline=None)
