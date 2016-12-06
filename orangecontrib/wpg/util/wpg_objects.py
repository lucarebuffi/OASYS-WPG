class WPGOutput(object):
    _source = None
    _optical_element = None
    _wavefront = None
    _numerical_integration_parameters = None

    def __init__(self,
                 source=None,
                 optical_element=None,
                 wavefront=None,
                 numerical_integration_parameters=None):
        self._source = source
        self._optical_element = optical_element
        self._wavefront = wavefront
        self._numerical_integration_parameters = numerical_integration_parameters

    def has_source(self):
        return not self._source is None

    def get_source(self):
        return self._source

    def has_optical_element(self):
        return not self._optical_element is None

    def get_optical_element(self):
        return self._optical_element

    def has_wavefront(self):
        return not self._wavefront is None

    def get_wavefront(self):
        return self._wavefront

    def has_numerical_integration_parameters(self):
        return not self._numerical_integration_parameters is None

    def get_numerical_integration_parameters(self):
        return self._numerical_integration_parameters
