import numpy
from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui
from oasys.widgets import congruence

from orangecontrib.wpg.util.wpg_objects import WPGOutput
from orangecontrib.wpg.widgets.gui.ow_wpg_widget import WPGWidget

from wpg.generators import build_gauss_wavefront_xy

from wpg import Wavefront

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

    # beam parameters:
    qnC = Setting(0.1)  # [nC] e-bunch charge
    thetaOM = Setting(2.5e-3)
    ekev = Setting(6.742)

    pulse_duration = Setting(9.e-15)
    pulseEnergy = Setting(0.5e-3)  # total pulse energy, J
    coh_time = Setting(0.24e-15)

    distance = Setting(235.0)

    def build_gui(self):

        main_box = oasysgui.widgetBox(self.controlArea, "Gaussian Source 1D Input Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-5, height=200)

        oasysgui.lineEdit(main_box, self, "qnC", "e-bunch charge [nC]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(main_box, self, "thetaOM", "thetaOM", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(main_box, self, "ekev", "Energy [keV]", labelWidth=260, valueType=float, orientation="horizontal")

        gui.separator(main_box, height=5)

        oasysgui.lineEdit(main_box, self, "pulse_duration", "Pulse Duration", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(main_box, self, "pulseEnergy", "Pulse Energy", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(main_box, self, "coh_time", "Coherence time", labelWidth=260, valueType=float, orientation="horizontal")

        gui.separator(main_box, height=5)

        oasysgui.lineEdit(main_box, self, "distance", "Distance (plots) [m]", labelWidth=260, valueType=float, orientation="horizontal")

    def after_change_workspace_units(self):
        pass

    def check_fields(self):
        congruence.checkPositiveNumber(self.qnC, "e-bunch charge")
        congruence.checkStrictlyPositiveNumber(self.ekev, "energy")
        congruence.checkPositiveNumber(self.distance, "Distance")

    def do_wpg_calculation(self):

        theta_fwhm = self.calculate_theta_fwhm_cdr(self.ekev, self.qnC)
        k = 2*numpy.sqrt(2*numpy.log(2))
        sigX = 12.4e-10*k/(self.ekev*4*numpy.pi*theta_fwhm)

        print('sigX, waist_fwhm [um], far field theta_fwhms [urad]: {}, {},{}'.format(
                                    sigX*1e6, sigX*k*1e6, theta_fwhm*1e6)
              )

        #define limits
        range_xy = theta_fwhm/k*self.distance*7. # sigma*7 beam size
        npoints=180


        wfr0 = build_gauss_wavefront_xy(npoints,
                                        npoints,
                                        self.ekev,
                                        -range_xy/2,
                                        range_xy/2,
                                        -range_xy/2,
                                        range_xy/2,
                                        sigX,
                                        sigX,
                                        self.distance,
                                        pulseEn=self.pulseEnergy,
                                        pulseTau=self.coh_time/numpy.sqrt(2),
                                        repRate=1/(numpy.sqrt(2)*self.pulse_duration))


        return Wavefront(wfr0)


    def extract_plot_data_from_calculation_output(self, calculation_output):
        plot_wfront(calculation_output, 'at '+ str(self.distance) +' m',False, False, 1e-5,1e-5,'x', False)

        return self.getFigureCanvas(pylab.figure(1)), \
               self.getFigureCanvas(pylab.figure(2)), \
               self.getFigureCanvas(pylab.figure(3))

    def getTabTitles(self):
        return ["Intensity", "Vertical Cut", "Horizontal Cut"]

    def extract_wpg_output_from_calculation_output(self, calculation_output):
        return WPGOutput(wavefront=calculation_output, beamline=None)


    def calculate_theta_fwhm_cdr(self, ekev, qnC):
        """
        Calculate angular divergence using formula from XFEL CDR2011

        :param ekev: Energy in keV
        :param qnC: e-bunch charge, [nC]
        :return: theta_fwhm [units?]
        """
        return (17.2 - 6.4 * numpy.sqrt(qnC))*1e-6/ekev**0.85