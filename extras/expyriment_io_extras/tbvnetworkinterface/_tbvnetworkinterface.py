"""Turbo Brain Voyager network interface.

This module contains a class implementing a network interface for Turbo Brain
Voyager (see www.brainvoyager.com/products/turbobrainvoyager.html).

"""
from __future__ import absolute_import, print_function, division
from builtins import *

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import struct

from expyriment import _internals
from expyriment.misc._timer import get_time
from expyriment.misc._miscellaneous import byte2unicode, unicode2byte
from expyriment.io._input_output import Input, Output
from ..tcpclient import TcpClient


class TbvNetworkInterface(Input, Output):
    """A class implementing a network interface to Turbo Brain Voyager.

    See http://www.brainvoyager.com/products/turbobrainvoyager.html
    for more information.
    
    """

    class TimeoutError(Exception):
        pass

    class RequestError(Exception):
        pass

    class DataError(Exception):
        pass

    def __init__(self, host, port, timeout=2000, connect=True):
        """Create a TbvNetworkInterface.

        Parameters
        ----------
        host : str
            The hostname or IPv4 address of the TBV server to connect to.
        port : int
            The port on the TBV server to connect to.
        timeout : int, optional
            The maximal time to wait for a response from the server for each
            request (default=2000).
        connect : bool, optional
            If True, connect immediately (default=True).

        """

        Input.__init__(self)
        Output.__init__(self)

        self._host = host
        self._port = port
        self._is_connected = False
        self._tbv_plugin_version = None
        self._tcp = TcpClient(host, port, None, False)
        self._timeout = timeout
        if connect:
            self.connect()

    _getter_exception_message = "Cannot set {0} if connected!"

    @property
    def host(self):
        """Getter for host."""

        return self._host

    @host.setter
    def host(self, value):
        """Setter for host."""

        if self._is_connected:
            raise AttributeError(
                TbvNetworkInterface._getter_exception_message.format("host"))
        else:
            self._host = value

    @property
    def port(self):
        """Getter for port."""

        return self._port

    @port.setter
    def port(self, value):
        """Setter for port."""

        if self._is_connected:
            raise AttributeError(
                TbvNetworkInterface._getter_exception_message.format("port"))
        else:
            self._port = value

    @property
    def is_connected(self):
        """Getter for is_connected."""

        return self._is_connected

    @property
    def tbv_plugin_version(self):
        """Getter for tbv_plugin_version."""

        return self._tbv_plugin_version

    @property
    def timeout(self):
        """Getter for timeout."""

        return self._timeout

    @timeout.setter
    def timeout(self, value):
        """Setter for timeout."""

        self._timeout = value

    def connect(self):
        """Connect to the TBV server."""

        if not self._is_connected:
            self._tcp.connect()
            data, rt = self.request_data("Request Socket")
            try:
                self._tbv_plugin_version = (struct.unpack('!i', data[:4])[0],
                                            struct.unpack('!i', data[4:8])[0],
                                            struct.unpack('!i', data[8:])[0])
            except:
                raise RuntimeError("Connecting to TBV failed!")
            self._is_connected = True
            if self._logging:
                _internals.active_exp._event_file_log(
                    "TbvNetworkInterface,connected,{0}:{1}".format(self._host,
                                                                   self._port))

    def _send(self, message, *args):
        length = len(message)
        arg_length = sum([len(x) for x in args])
        data = struct.pack('!q', length + 5 + arg_length) + \
            b"\x00\x00\x00" + unicode2byte(chr(length + 1)) + message + b"\x00"
        if len(args) > 0:
            for arg in args:
                data += arg
        self._tcp.send(data)

    def _wait(self):
        start = get_time()
        receive, rt = self._tcp.wait(package_size=8, duration=self.timeout,
                                     process_control_events=False)
        if receive is None:
            return None
        length = struct.unpack('!q', receive)[0]
        data = None
        timeout = self.timeout - int((get_time() - start) * 1000)
        if timeout > 0:
            data, rt = self._tcp.wait(package_size=length,
                                      duration=timeout,
                                      process_control_events=False)
        if data is None:
            return None
                
        return data[4:]

    def request_data(self, request, *args):
        """Request data from Turbo Brain Voyager.

        If the request times out, a `TbvNetworkInterface.TimeoutError` is
        raised.
        If a wrong request is sent, a `TbvNetworkInterface.RequestError` is
        raised.
        If the received data does not match the request, a
        `TbvNetworkInterface.DataError` is raised.
        
        Parameters
        ----------
        request : str
            The request to be sent to Turbo Brain Voyager.

        Returns
        -------
        data : str
            The byte string of the received data.
        rt : int
            The time it took to get the data.

        """

        start = get_time()
        self._tcp.clear()
        request = unicode2byte(request)
        self._send(request, *args)
        data = self._wait()
        arg_length = sum([len(x) for x in args])
        arg = b"".join(args)
        if data is None:
            raise TbvNetworkInterface.TimeoutError(
                "Waiting for requested data timed out!")
        elif byte2unicode(data).startswith("Wrong request!"):
            raise TbvNetworkInterface.RequestError(
                "Wrong request '{0}'!".format(data[19:-1]))
        elif data[0:len(request)+1+arg_length] != request+b"\x00"+arg:
            raise TbvNetworkInterface.DataError(
                "Received data does not match request!")
        else:
            return data[len(request) + 1:], int((get_time() - start) * 1000)

    def close(self):
        """Close the connection."""

        self._tcp.close()
        self._is_connected = False

    # Basic Project Queries
    def get_current_time_point(self):
        """Get the current time point.

        Returns
        -------
        data : int
            The current time point (1-based!).
        rt : int
            The time it took to get the data.

        """

        data, rt = self.request_data("tGetCurrentTimePoint")
        return struct.unpack('!i', data)[0], rt

    def get_expected_nr_of_time_points(self):
        """Get the expected number of time points.

        Returns
        -------
        data : int
            The expected number of time points.
        rt : int
            The time it took to get the data.

        """

        data, rt = self.request_data("tGetExpectedNrOfTimePoints")
        return struct.unpack('!i', data)[0], rt

    def get_dims_of_functional_data(self):
        """Get the dimensions of the functional data.

        Returns
        -------
        dims : list
            The dimension of the functional volume.
            [x, y, z]
        rt : int
            The time it took to get the data.

        """

        data, rt = self.request_data("tGetDimsOfFunctionalData")
        return ([struct.unpack('!i', data[:4])[0],
                    struct.unpack('!i', data[4:8])[0],
                    struct.unpack('!i', data[8:])[0]], rt)

    def get_project_name(self):
        """Get the project name.

        Returns
        -------
        name : str
            The project name.
        rt : int
            The time it took to get the data.

        """

        name, rt = self.request_data("tGetProjectName")
        return byte2unicode(name[4:-1]), rt

    def get_watch_folder(self):
        """Get the watch folder.

        Returns
        -------
        folder : str
            The watch folder.
        rt : int
            The time it took to get the data.

        """

        folder, rt = self.request_data("tGetWatchFolder")
        return byte2unicode(folder[4:-1]), rt

    def get_target_folder(self):
        """Get the target folder.

        Returns
        -------
        folder : str
            The target folder.
        rt : int
            The time it took to get the data.

        """

        folder, rt = self.request_data("tGetTargetFolder")
        return byte2unicode(folder[4:-1]), rt

    def get_feedback_folder(self):
        """Get the feedback folder.

        Returns
        -------
        folder : str
            The feedback folder.
        rt : int
            The time it took to get the data.

        """

        folder, rt = self.request_data("tGetFeedbackFolder")
        return byte2unicode(folder[4:-1]), rt

    # Protocol, DM, GLM Queries
    def get_current_protocol_condition(self):
        """Get the current protocol condition.

        Returns
        -------
        condition_nr : int
            The current protocol condition.
        rt : int
            The time it took to get the data.

        """

        condition_nr, rt = self.request_data("tGetCurrentProtocolCondition")
        return struct.unpack('!i', condition_nr)[0], rt

    def get_full_nr_of_predictors(self):
        """Get the full number of predictors.

        Returns
        -------
        nr_predictors : int
            The number of predictors.
        rt : int
            The time it took to get the data.

        """

        nr_predictors, rt = self.request_data("tGetFullNrOfPredictors")
        return struct.unpack('!i', nr_predictors)[0], rt

    def get_current_nr_of_predictors(self):
        """Get the current number of predictors.

        Returns
        -------
        nr_predictors : int
            The number of predictors.
        rt : int
            The time it took to get the data.

        """

        nr_predictors, rt = self.request_data("tGetCurrentNrOfPredictors")
        return struct.unpack('!i', nr_predictors)[0], rt

    def get_nr_of_confound_predictors(self):
        """Get the number of confound predictors.

        Returns
        -------
        nr_predictors : int
            The number of predictors.
        rt : int
            The time it took to get the data.

        """

        nr_predictors, rt = self.request_data("tGetNrOfConfoundPredictors")
        return struct.unpack('!i', nr_predictors)[0], rt

    def get_value_of_design_matrix(self, pred, time_point):
        """Get the value of the design matrix.

        Parameters
        ----------
        pred : int
            The predictor.
        time_point : int
            The time point.

        Returns
        -------
        value : float
            The design matrix value.
        rt : int
            The time it took to get the data.

        """

        pred = struct.pack('!i', pred)
        time_point = struct.pack('!i', time_point)
        data, rt = self.request_data(
            "tGetValueOfDesignMatrix", pred, time_point)
        return struct.unpack('!f', data[8:])[0], rt

    def get_nr_of_contrasts(self):
        """Get the number of contrasts.

        Returns
        -------
        nr_contrasts : int
            The number of contrasts.
        rt : int
            The time it took to get the data.

        """

        nr_contrasts, rt = self.request_data("tGetNrOfContrasts")
        return struct.unpack('!i', nr_contrasts)[0], rt

    # ROI Queries
    def get_nr_of_rois(self):
        """Get the number of ROIs.

        Returns
        -------
        n_rois : int
            The number of ROIs.
        rt : int
            The time it took to get the data.

        """

        n_rois, rt = self.request_data("tGetNrOfROIs")
        return struct.unpack('!i', n_rois)[0], rt

    def get_mean_of_roi(self, roi):
        """Get the mean of a ROI.

        Parameters
        ----------
        roi : int
            The ROI.

        Returns
        -------
        mean : float
            The mean of the ROI.
        rt : int
            The time it took to get the data.

        """

        roi = struct.pack('!i', roi)
        data, rt = self.request_data(
            "tGetMeanOfROI", roi)
        return struct.unpack('!f', data[4:])[0], rt

    def get_existing_means_of_roi(self, roi, to_time_point):
        """Get the existing means of a ROI.

        Parameters
        ----------
        roi : int
            The ROI.
        to_time_point : int
            Get all the means up to this point.

        Returns
        -------
        means : list
            The means of the ROI.
        rt : int
            The time it took to get the data.

        """

        roi = struct.pack('!i', roi)
        to_time_point = struct.pack('!i', to_time_point)
        data, rt = self.request_data(
            "tGetExistingMeansOfROI", roi, to_time_point)
        return ([struct.unpack('!f', data[8 + x * 4:8 + x * 4 + 4])[0]
                 for x in range(0, len(data[8:]) // 4)], rt)

    def get_mean_of_roi_at_time_point(self, roi, time_point):
        """Get the mean of a ROI at a time point.

        Parameters
        ----------
        roi : int
            The ROI.
        time_point : int
            The time point.

        Returns
        -------
        mean : float
            The mean of the ROI (0-based!).
        rt : int
            The time it took to get the data (0-based!).

        """

        roi = struct.pack('!i', roi)
        time_point = struct.pack('!i', time_point)
        data, rt = self.request_data(
            "tGetMeanOfROIAtTimePoint", roi, time_point)
        return struct.unpack('!f', data[8:])[0], rt

    def get_nr_of_voxels_of_roi(self, roi):
        """Get the number of voxels of a ROI.

        Parameters
        ----------
        roi : int
            The ROI.

        Returns
        -------
        nr_voxels : int
            The number of voxels of the ROI.
        rt : int
            The time it took to get the data.

        """

        roi = struct.pack('!i', roi)
        data, rt = self.request_data(
            "tGetNrOfVoxelsOfROI", roi)
        return struct.unpack('!i', data[4:])[0], rt

    def get_beta_of_roi(self, roi, beta):
        """Get the value of a beta of a ROI.

        Parameters
        ----------
        roi : int
            The ROI.
        beta : int
            The beta.

        Returns
        -------
        value : float
            The value of the beta of the ROI.
        rt : int
            The time it took to get the data.

        """

        roi = struct.pack('!i', roi)
        beta = struct.pack('!i', beta)
        data, rt = self.request_data(
            "tGetBetaOfROI", roi, beta)
        return struct.unpack('!f', data[8:])[0], rt

    def get_coord_of_voxel_of_roi(self, roi, voxel):  # TODO: Return as one list?
        """Get the coordinates of a voxel of a ROI.

        Parameters
        ----------
        roi : int
            The ROI.
        voxel : int
            The voxel.

        Returns
        -------
        coords : list
            The coordinates of the voxel.
            [x, y, z]
        rt : int
            The time it took to get the data.

        """

        roi = struct.pack('!i', roi)
        voxel = struct.pack('!i', voxel)
        data, rt = self.request_data(
            "tGetCoordsOfVoxelOfROI", roi, voxel)
        return ([struct.unpack('!i', data[8:12])[0],
                 struct.unpack('!i', data[12:16])[0],
                 struct.unpack('!i', data[16:])[0]], rt)

    def get_all_coords_of_voxels_of_roi(self, roi):  # TODO: Put into lists?
        """Get coordinates for all voxels for a ROI.

        Parameters
        ----------
        roi : int
            The ROI.

        Returns
        -------
        coords : list
            The coordinates of all voxels of the ROI.
            [[v1_x, v1_y, v1_z], [v2_x, v2_z, v2_y], ..., [vn_x, vn_y, _vn_z]]
        rt : int
            The time it took to get the data.

        """

        roi = struct.pack('!i', roi)
        data, rt = self.request_data(
            "tGetAllCoordsOfVoxelsOfROI", roi)
        _all = [struct.unpack('!i', data[4 + x * 4:4 + x * 4 + 4])[0]
                for x in range(0, len(data[4:]) // 4)]
        return [_all[x:x+3] for x in range(0, len(_all), 3)], rt

    # Volume Data Access Queries
    def get_value_of_voxel_at_time(self, coords, time_point):
        """Get the value of a voxel at a certain time point.

        Parameters
        ----------
        coords : list
            The coordinates of the voxel.
            [x, y, z]
        time_point : int
            The time point.

        Returns
        -------
        value : float
            The voxel value.
        rt : int
            The time it took to get the data.

        """

        x = struct.pack('!i', coords[0])
        y = struct.pack('!i', coords[1])
        z = struct.pack('!i', coords[2])
        time_point = struct.pack('!i', time_point)
        data, rt = self.request_data(
            "tGetValueOfVoxelAtTime", x, y, z, time_point)
        return struct.unpack('!f', data[16:])[0], rt

    def get_value_of_all_voxels_at_time(self, time_point):
        """Get the value of all voxels at a certain time point.

        Parameters
        ----------
        time_point : int
            The time point.

        Returns
        -------
        voxels : list
            The data of all voxel values.
            [x1_y1_z1, ..., xn_y1_y1, ..., xn_yn_z1, ..., xn_yn_zn]
            The value of a single voxel can be accessed at:
                z_coord*dim_x*dim_y + y_coord*dim_x + x_coord
        rt : int
            The time it took to get the data.

        """

        time_point = struct.pack('!i', time_point)
        data, rt = self.request_data(
            "tGetValueOfAllVoxelsAtTime", time_point)
        return ([struct.unpack('!h', data[4 + x * 2:4 + x * 2 + 2])[0]
                 for x in range(0, len(data[4:]) // 2)], rt)

    def get_raw_value_of_all_voxels_at_time(self, time_point):
        """Get the raw value of all voxels at a certain time point.

        Parameters
        ----------
        time_point : int
            The time point.

        Returns
        -------
        voxels : list
            The data of all raw voxel values.
            [x1_y1_z1, ..., xn_y1_y1, ..., xn_yn_z1, ..., xn_yn_zn]
            The value of a single voxel can be accessed at:
                z_coord*dim_x*dim_y + y_coord*dim_x + x_coord
        rt : int
            The time it took to get the data.

        """

        time_point = struct.pack('!i', time_point)
        data, rt = self.request_data(
            "tGetRawValueOfAllVoxelsAtTime", time_point)
        return ([struct.unpack('!h', data[4 + x * 2:4 + x * 2 + 2])[0]
                 for x in range(0, len(data[4:]) // 2)], rt)

    def get_beta_of_voxel(self, beta, coords):
        """Get a specific beta value of a voxel.

        Parameters
        ----------
        beta : int
            The beta.
        coords : list
            The coordinates of the voxel.
            [x, y, z]

        Returns
        -------
        value : double
            The beta value.
        rt : int
            The time it took to get the data.

        """

        beta = struct.pack('!i', beta)
        x = struct.pack('!i', coords[0])
        y = struct.pack('!i', coords[1])
        z = struct.pack('!i', coords[2])
        data, rt = self.request_data(
            "tGetBetaOfVoxel", beta, x, y, z)
        return struct.unpack('!d', data[16:])[0], rt

    def get_beta_maps(self):
        """Get the beta maps.

        Returns
        -------
        beta_maps : list
            The data of all raw voxel values.
                [x1_y1_z_p1, ..., xn_y1_y1_p1, ..., xn_yn_z1_p1, ..., xn_yn_zn_p1, ..., xn_yn_zn_pn]
            A beta value of a single predictor can be accessed at:
                beta_i*dim_xyz + z_coord*dim_xy + y_coord*dim_x + x_coord
        rt : int
            The time it took to get the data.

        """

        data, rt = self.request_data(
            "tGetBetaMaps")
        return ([struct.unpack('!d', data[x * 8:x * 8 + 8])[0]
                 for x in range(0, len(data) // 8)], rt)

    def get_map_value_of_voxel(self, map, coords):
        """Get a specific map value of a voxel.

        Parameters
        ----------
        map : int
            The map.
        coords : list
            The coordinates of the voxel.
            [x, y, z]

        Returns
        -------
        value : float
            The map value.
        rt : int
            The time it took to get the data.

        """

        map = struct.pack('!i', map)
        x = struct.pack('!i', coords[0])
        y = struct.pack('!i', coords[1])
        z = struct.pack('!i', coords[2])
        data, rt = self.request_data(
            "tGetMapValueOfVoxel", map, x, y, z)
        return struct.unpack('!f', data[16:])[0], rt

    def get_contrast_maps(self):
        """Get the contrast maps.

        Returns
        -------
        contrast_maps : list
            The data of all contrast maps values.
                [x1_y1_z_c1, ..., xn_y1_y1_c1, ..., xn_yn_z1_c1, ..., xn_yn_zn_cn]
            A t value of a specific contrast map of a voxel with specific
            coordinates can be accessed at:
                map_i*dim_xyz + z_coord*dim_xy + y_coord*dim_x + x_coord
        rt : int
            The time it took to get the data.

        """

        data, rt = self.request_data(
            "tGetContrastMaps")
        return ([struct.unpack('!f', data[x * 4:x * 4 + 4])[0]
                 for x in range(0, len(data) // 4)], rt)

    # SVM Access
    def get_number_of_classes(self):
        """Get the number of classes.

        Returns
        -------
        nr_classes : int
            The number of classes.
        rt : int
            The time it took to get the data.

        """

        nr_classes, rt = self.request_data("tGetNumberOfClasses")
        return struct.unpack('!i', nr_classes)[0], rt

    def get_current_classifier_output(self):  # TODO: Needs testing!
        """Get the current classifier output.

        Returns
        -------
        output : list
            The current classifier output.
            NOTE: Output is 1-based!
        rt : int
            The time it took to get the data.

        """

        data, rt = self.request_data(
            "tGetCurrentClassifierOutput")
        return ([struct.unpack('!f', data[x * 4:x * 4 + 4])[0]
                 for x in range(0, len(data) // 4)], rt)

    # Functional Connectivity
    def get_pearson_correlation(self, window_size):  # TODO: Needs testing!
        """Get Pearson correlation at current time point.

        Parameters
        ----------
        window_size : int
            The size of the window in volumes.

        Returns
        -------
        correlations : list
            The list of correlations between pairs of ROIs
            [(x, y) for x in rois for y in rois if x < y].
        rt : int
            The time it took to get the data.

        """

        window_size = struct.pack('!i', window_size)
        data, rt = self.request_data(
            "tGetPearsonCorrelation", window_size)
        return ([struct.unpack('!f', data[x * 4:x * 4 + 4])[0]
                 for x in range(1, len(data) // 4)], rt)

    def get_pearson_correlation_at_time_point(self, window_size, time_point):  # TODO: Needs testing!
        """Get Pearson correlation at specified time point.

        Parameters
        ----------
        window_size : int
            The size of the window in volumes.
        time_point : int
            The time point.

        Returns
        -------
        correlations : list
            The list of correlations between pairs of ROIs
            [(x, y) for x in rois for y in rois if x < y].
        rt : int
            The time it took to get the data.

        """

        window_size = struct.pack('!i', window_size)
        time_point = struct.pack('!i', time_point)
        data, rt = self.request_data(
            "tGetPearsonCorrelationAtTimePoint", window_size, time_point)
        return ([struct.unpack('!f', data[x * 4:x * 4 + 4])[0]
                 for x in range(2, len(data) // 4)], rt)

    def get_partial_correlation(self, window_size):  # TODO: Needs testing!
        """Get partial correlation at current time point.

        Parameters
        ----------
        window_size : int
            The size of the window in volumes.

        Returns
        -------
        correlations : list
            The list of correlations between pairs of ROIs
            [(x, y) for x in rois for y in rois if x < y]
            while controlling for effects of combination of remaining ROIs.
        rt : int
            The time it took to get the data.

        """

        window_size = struct.pack('!i', window_size)
        data, rt = self.request_data(
            "tGetPartialCorrelation", window_size)
        return ([struct.unpack('!f', data[x * 4:x * 4 + 4])[0]
                 for x in range(1, len(data) // 4)], rt)

    def get_partial_correlation_at_time_point(self, window_size, time_point):  # TODO: Needs testing!
        """Get partial correlation at specified time point.

        Parameters
        ----------
        window_size : int
            The size of the window in volumes.
        time_point : int
            The time point.

        Returns
        -------
        correlations : list
            The list of correlations between pairs of ROIs
            [(x, y) for x in rois for y in rois if x < y]
            while controlling for effects of combination of remaining ROIs.
        rt : int
            The time it took to get the data.

        """

        window_size = struct.pack('!i', window_size)
        time_point = struct.pack('!i', time_point)
        data, rt = self.request_data(
            "tGetPartialCorrelationAtTimePoint", window_size, time_point)
        return ([struct.unpack('!f', data[x * 4:x * 4 + 4])[0]
                 for x in range(2, len(data) // 4)], rt)
