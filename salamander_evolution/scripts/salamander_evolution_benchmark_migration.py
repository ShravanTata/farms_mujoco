#!/usr/bin/env python3
"""Benchmark evolution migration"""

import argparse

import pygmo as pg

import matplotlib.pyplot as plt

from salamander_evolution.viewer import AlgorithmViewer2D
from salamander_evolution.migration import RingMigration


def parse_args():
    """ Parse arguments """
    parser = argparse.ArgumentParser(description='Test evolution')
    # parser.add_argument(
    #     'model_names',
    #     type=str,
    #     nargs='+',
    #     help='Name of Gazebo model to simulate'
    # )
    parser.add_argument(
        "-s", '--save',
        action='store_true',
        dest='save',
        help='Save results'
    )
    args = parser.parse_args()
    return args


def main(n_threads=8):
    """Main"""

    args = parse_args()

    kwargs = {"memory": True, "seed": 0}
    algorithms = [
        pg.sade(gen=1, **kwargs)  # , variant=variant+1
        for _ in range(8)
    ]

    # Instantiate viewers
    viewer = AlgorithmViewer2D(
        algorithms,
        n_pop=10,
        n_gen=100
    )
    # Run evolutions
    print("Running archipelago evolutions")
    viewer.run_evolutions(migration=RingMigration(len(algorithms), 1, 1))
    # Animate
    viewer.animate(write=args.save)
    # Save
    if not args.save:
        plt.show()


if __name__ == '__main__':
    main()
