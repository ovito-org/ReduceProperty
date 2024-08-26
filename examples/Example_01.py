from ovito.data import DataObject, Particles
from ovito.io import import_file

from ReduceProperty import ReduceProperty


def main():
    # Data import:
    pipeline = import_file(
        "https://gitlab.com/ovito-org/ovito-sample-data/-/raw/183ba555b78381e8b9589973f7ac4df2aa6122ae/LAMMPS/water.unwrapped.lammpstrj.gz?inline=false",
        multiple_frames=True,
    )

    # Reduce Property:
    pipeline.modifiers.append(
        ReduceProperty(
            input_container=DataObject.Ref(Particles, "particles"),
            input_property="Velocity",
        )
    )

    # Reduce Property:
    pipeline.modifiers.append(
        ReduceProperty(
            input_container=DataObject.Ref(Particles, "particles"),
            input_property="Velocity.X",
        )
    )

    # Compute and print
    data = pipeline.compute()
    print(f"{data.attributes['particles_Velocity_Mean'] = }")
    print(f"{data.attributes['particles_Velocity.X_Mean'] = }")


if __name__ == "__main__":
    main()
