class WPGOutput(object):
    def __init__(self,
                 thetaOM = 0.0,
                 range_xy = 0.0,
                 wavefront=None,
                 distance_to_previous=0.0,
                 total_distance = 0.0,
                 beamline=None):
        self._thetaOM = thetaOM
        self._range_xy = range_xy
        self._wavefront = wavefront
        self._distance_to_previous = distance_to_previous
        self._total_distance = total_distance
        self._beamline = beamline

    def get_thetaOM(self):
        return self._thetaOM

    def get_range_xy(self):
        return self._range_xy

    def has_wavefront(self):
        return not self._wavefront is None

    def get_wavefront(self):
        return self._wavefront

    def get_distance_to_previous(self):
        return self._distance_to_previous

    def get_total_distance(self):
        return self._total_distance

    def has_beamline(self):
        return not self._beamline is None

    def get_beamline(self):
        return self._beamline
