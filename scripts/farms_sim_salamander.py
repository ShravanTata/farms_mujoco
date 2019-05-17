#!/usr/bin/env python3
"""Run salamander simulation with bullet"""

import cProfile
import pstats
import matplotlib.pyplot as plt
from farms_bullet.simulations.salamander import main as run_simulation
from farms_bullet.animats.model_options import ModelOptions
from farms_bullet.simulations.simulation_options import SimulationOptions


def main():
    """Main"""
    animat_options = ModelOptions()
    # animat_options = ModelOptions(
    #     frequency=1.7,
    #     body_stand_amplitude=0.42
    # )
    simulation_options = SimulationOptions.with_clargs(
        timestep=1e-3,
        duration=50
    )
    run_simulation(
        simulation_options=simulation_options,
        animat_options=animat_options
    )
    plt.show()


def profile():
    """Profile"""
    cProfile.run("main()", "simulation.profile")
    pstat = pstats.Stats("simulation.profile")
    pstat.sort_stats('time').print_stats(30)
    pstat.sort_stats('cumtime').print_stats(30)


if __name__ == '__main__':
    # main()
    profile()
