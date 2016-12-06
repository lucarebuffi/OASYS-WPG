class WPGOutput(object):
    _wavefront = None
    _beamline=None

    def __init__(self,
                 wavefront=None,
                 beamline=None):
        self._wavefront = wavefront
        self._beamline = beamline

    def has_wavefront(self):
        return not self._wavefront is None

    def get_wavefront(self):
        return self._wavefront

    def has_beamline(self):
        return not self._beamline is None

    def get_beamline(self):
        return self._beamline
