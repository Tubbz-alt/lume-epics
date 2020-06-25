import time

import numpy as np
from typing import List, Dict, Tuple

from lume_epics.client.controller import Controller
from lume_model.variables import ImageVariable, ScalarVariable


class PVImage:
    """
    Object for updating and formatting image data.

    Attributes
    ----------
    prefix: str
        Server prefix

    variable: ImageVariable

    controller: Controller
        Controller object for getting pv values

    units: str
        Units associated with the variable

    pvname: str
        Name of the process variable to access.

    """

    def __init__(
        self, prefix: str, variable: ImageVariable, controller: Controller,
    ) -> None:
        """
        Initialize monitor for an image variable.

        Parameters
        ----------
        prefix: str
            Server prefix

        variable: ImageVariable
            Image variable to display

        controller: Controller
            Controller object for getting pv values
        """
        self.units = None
        # check if units has been set
        if "units" in variable.__fields_set__:
            self.units = variable.units.split(":")

        self.pvname = f"{prefix}:{variable.name}"
        self.controller = controller
        self.axis_labels = variable.axis_labels
        self.axis_units = variable.axis_units

    def poll(self) -> Dict[str, list]:
        """
        Collects image data via appropriate protocol and builds image data dictionary.

        Returns
        -------
        dict
            Dictionary mapping image components to values.
        """

        return self.controller.get_image(self.pvname)


class PVTimeSeries:
    """
    Monitor for scalar process variables.

    Attributes
    ----------
    time: np.ndarray
        Array of sample times

    data: np.ndarray
        Array of data samples

    prefix: str
        Server prefix

    variable: ScalarVariable
        Variable to monitor for time series

    controller: Controller
        Controller object for getting pv values

    units: str
        Units associated with the variable

    pvname: str
        Name of the process variable to access

    """

    def __init__(
        self, prefix: str, variable: ScalarVariable, controller: Controller,
    ) -> None:
        """
        Initializes monitor attributes.

        Parameters
        ----------
        prefix: str
            Server prefix

        variable: ScalarVariable
            Variable to monitor for time series

        controller: Controller
            Controller object for getting pv values

        """
        self.pvname = f"{prefix}:{variable.name}"
        self.tstart = time.time()
        self.time = np.array([])
        self.data = np.array([])

        self.units = None
        # check if units has been set
        if "units" in variable.__fields_set__:
            self.units = variable.units

        self.controller = controller

    def poll(self) -> Tuple[np.ndarray]:
        """
        Collects image data via appropriate protocol and returns time and data.

        Returns
        -------
        tuple
            (time, data)
        """
        t = time.time()
        v = self.controller.get(self.pvname)

        self.time = np.append(self.time, t)
        self.data = np.append(self.data, v)
        return self.time - self.tstart, self.data


class PVScalar:
    """
    Monitor for scalar process variables.

    Attributes
    ----------
    prefix: str
        Server prefix

    variable: ScalarVariable
        Variable to monitor for time series

    controller: Controller
        Controller object for getting pv values

    units: str
        Units associated with the variable

    pvname: str
        Name of the process variable to access

    """

    def __init__(
        self, prefix: str, variable: ScalarVariable, controller: Controller,
    ) -> None:
        """
        Initializes monitor attributes.

        Parameters
        ----------
        prefix: str
            Server prefix

        variable: ScalarVariable
            Variable to monitor for time series

        controller: Controller
            Controller object for getting pv values
        """
        self.units = None
        # check if units has been set
        if "units" in variable.__fields_set__:
            self.units = variable.units
        self.pvname = f"{prefix}:{variable.name}"
        self.controller = controller

    def poll(self) -> Tuple[np.ndarray]:
        """
        Poll variable for value

        Returns
        -------
        Return value
        """
        return self.controller.get(self.pvname)
