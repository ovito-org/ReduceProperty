#### Reduce Property ####
# Apply common reduction operations to properties in the DataCollection.

import numpy as np
from ovito.data import DataCollection, PropertyContainer
from ovito.pipeline import ModifierInterface
from ovito.traits import DataObjectReference, PropertyReference
from traits.api import Bool, Enum


class ReduceProperty(ModifierInterface):
    input_container = DataObjectReference(PropertyContainer, label="Container")
    input_property = PropertyReference(
        container="input_container",
        mode=PropertyReference.Mode.PropertiesAndComponents,
        label="Property",
    )
    operation = Enum(
        [
            "Mean",
            "Median",
            "Standard Deviation",
            "Variance",
            "Minimum",
            "Maximum",
            "Sum",
            "Non-zero",
        ],
        label="Operation",
    )
    only_selected = Bool(False, label="Reduce only selected elements")

    # Apply the reduction operation
    def apply_operation(self, arr: np.ndarray):
        if self.operation.casefold() == "Mean".casefold():
            return np.mean(arr, axis=self.axis)
        elif self.operation.casefold() == "Median".casefold():
            return np.median(arr, axis=self.axis)
        elif self.operation.casefold() == "Variance".casefold():
            return np.var(arr, axis=self.axis)
        elif self.operation.casefold() == "Standard Deviation".casefold():
            return np.std(arr, axis=self.axis)
        elif self.operation.casefold() == "Minimum".casefold():
            return np.min(arr, axis=self.axis)
        elif self.operation.casefold() == "Maximum".casefold():
            return np.max(arr, axis=self.axis)
        elif self.operation.casefold() == "Sum".casefold():
            return np.sum(arr, axis=self.axis)
        elif self.operation.casefold() == "Non-zero".casefold():
            return np.count_nonzero(arr, axis=self.axis)
        else:
            raise NotImplementedError(f"Operation: '{self.operation}' not implemented")

    def modify(self, data: DataCollection, **_):
        container = data.get(self.input_container, require=True)
        prop = container.get(self.input_property, require=True)

        if prop.ndim <= 2:
            self.axis = 0
        else:
            raise NotImplementedError("Reductions not implemented for ndim > 2")

        if len(prop) < 2:
            raise ValueError("2 or more particles required for reduction operations")

        if self.only_selected:
            prop = prop[np.where(container.get("Selection", require=True))[0]]
            assert len(prop) == np.sum(container.get("Selection"))

        container_name = str(self.input_container)
        property_name = str(self.input_property)
        operation_name = self.operation
        output_name = f"{container_name}_{property_name}_{operation_name}"
        result = self.apply_operation(prop)
        data.attributes[output_name] = result
