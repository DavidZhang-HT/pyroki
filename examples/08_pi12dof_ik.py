"""IK Demo for PI 12-DoF Robot

This example demonstrates solving a simple inverse kinematics problem using a
custom URDF bundled with the repository.
"""

import time
from pathlib import Path

import numpy as np
import pyroki as pk
import viser
from viser.extras import ViserUrdf

import pyroki_snippets as pks


URDF_PATH = Path(__file__).resolve().parents[1] / "urdf" / "pi_12dof_release_v1_rl.urdf"


def main() -> None:
    """Run the IK demo for the PI 12-DoF robot."""
    urdf = pk.loaders.load_custom_urdf(URDF_PATH.name)
    target_link_name = "r_ankle_roll_link"

    # Create robot.
    robot = pk.Robot.from_urdf(urdf)

    # Set up visualizer.
    server = viser.ViserServer()
    server.scene.add_grid("/ground", width=2, height=2)
    urdf_vis = ViserUrdf(server, urdf, root_node_name="/robot")

    # Create interactive controller with initial position.
    ik_target = server.scene.add_transform_controls(
        "/ik_target", scale=0.2, position=(0.3, -0.2, 0.0), wxyz=(1, 0, 0, 0)
    )
    timing_handle = server.gui.add_number("Elapsed (ms)", 0.001, disabled=True)

    while True:
        # Solve IK.
        start_time = time.time()
        solution = pks.solve_ik(
            robot=robot,
            target_link_name=target_link_name,
            target_position=np.array(ik_target.position),
            target_wxyz=np.array(ik_target.wxyz),
        )

        # Update timing handle.
        elapsed_time = time.time() - start_time
        timing_handle.value = 0.99 * timing_handle.value + 0.01 * (elapsed_time * 1000)

        # Update visualizer.
        urdf_vis.update_cfg(solution)


if __name__ == "__main__":
    main()
