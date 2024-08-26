import numpy as np
import pytest
from ovito.data import DataObject, Particles
from ovito.io import import_file
from ovito.modifiers import ExpressionSelectionModifier

from ReduceProperty import ReduceProperty


@pytest.fixture
def get_pipeline():
    return import_file(
        "https://gitlab.com/ovito-org/ovito-sample-data/-/raw/183ba555b78381e8b9589973f7ac4df2aa6122ae/LAMMPS/water.unwrapped.lammpstrj.gz?inline=false",
        multiple_frames=True,
    )


def test_modifier(get_pipeline):
    pipeline = get_pipeline
    pipeline.modifiers.append(
        ReduceProperty(
            input_container=DataObject.Ref(Particles, "particles"),
            input_property="Velocity",
        )
    )
    data = pipeline.compute()

    assert np.allclose(
        data.attributes["particles_Velocity_Mean"],
        [-2.92323378e-04, 1.42415646e-04, -8.32030491e-05],
    )


def test_modifier_component(get_pipeline):
    pipeline = get_pipeline
    pipeline.modifiers.append(
        ReduceProperty(
            input_container=DataObject.Ref(Particles, "particles"),
            input_property="Velocity.X",
            operation="Sum",
        )
    )
    data = pipeline.compute()

    assert np.isclose(data.attributes["particles_Velocity.X_Sum"], -0.87697)


def test_modifier_selection(get_pipeline):
    pipeline = get_pipeline
    pipeline.modifiers.append(
        ExpressionSelectionModifier(expression="VelocityMagnitude > 0.01")
    )
    pipeline.modifiers.append(
        ReduceProperty(
            input_container=DataObject.Ref(Particles, "particles"),
            input_property="Velocity.X",
            operation="Standard Deviation",
            only_selected=True,
        )
    )
    data = pipeline.compute()

    assert np.isclose(
        data.attributes["particles_Velocity.X_Standard Deviation"], 0.0155778
    )
