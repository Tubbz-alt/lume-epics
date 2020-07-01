import numpy as np
from lume_model.variables import (
    ScalarInputVariable,
    ScalarOutputVariable,
    ImageInputVariable,
    ImageOutputVariable,
)

from lume_epics.client.widgets.tables import ValueTable
from lume_epics.client.widgets.sliders import build_sliders
from lume_epics.client.widgets.plots import ImagePlot, Striptool
from lume_epics.client.controller import Controller
from lume_epics import epics_server
from lume_model.models import SurrogateModel


class ExampleModel(SurrogateModel):
    input_variables = {
        "input1": ScalarInputVariable(name="input1", value=1, range=[0.0, 5.0]),
        "input2": ScalarInputVariable(name="input2", value=2, range=[0.0, 5.0]),
    }

    output_variables = {
        "output1": ScalarOutputVariable(name="output1"),
        "output2": ScalarOutputVariable(name="output2"),
        "output3": ImageOutputVariable(
            name="output3",
            value=np.array([[1, 2,], [3, 4]]),
            axis_labels=["count_1", "count_2"],
            x_min=0,
            y_min=0,
            x_max=5,
            y_max=5,
        ),
    }

    def evaluate(self, input_variables):

        self.input_variables = {variable.name: variable for variable in input_variables}

        self.output_variables["output1"].value = (
            self.input_variables["input1"].value * 2
        )
        self.output_variables["output2"].value = (
            self.input_variables["input2"].value * 2
        )

        # return inputs * 2
        return list(self.output_variables.values())


def test_sliders():
    PREFIX = "test"

    server = epics_server.Server(ExampleModel, PREFIX)
    server.start(monitor=False)

    inputs = list(ExampleModel.input_variables.values())

    # create controller
    controller = Controller("pva")

    # build sliders for the command process variable database
    sliders = build_sliders(inputs, controller, PREFIX)

    controller.close()
    server.stop()


def test_value_table():
    PROTOCOL = "pva"
    PREFIX = "test"

    server = epics_server.Server(ExampleModel, PREFIX)
    server.start(monitor=False)

    output1 = ScalarOutputVariable(name="output1")
    output2 = ScalarOutputVariable(name="output2")

    # create controller
    controller = Controller(PROTOCOL)

    outputs = [output1, output2]

    value_table = ValueTable(outputs, controller, PREFIX)

    controller.close()
    server.stop()


def test_image_plot():
    PROTOCOL = "pva"
    PREFIX = "test"

    server = epics_server.Server(ExampleModel, PREFIX)
    server.start(monitor=False)
    # create controller
    controller = Controller(PROTOCOL)

    outputs = [ExampleModel.output_variables["output3"]]
    value_table = ImagePlot(outputs, controller, PREFIX)

    controller.close()
    server.stop()


def test_striptool():
    PROTOCOL = "pva"
    PREFIX = "test"

    server = epics_server.Server(ExampleModel, PREFIX)
    server.start(monitor=False)

    output1 = ScalarOutputVariable(name="output1")
    output2 = ScalarOutputVariable(name="output2")

    # create controller
    controller = Controller(PROTOCOL)

    outputs = [output1, output2]

    value_table = Striptool(outputs, controller, PREFIX)

    controller.close()
    server.stop()
