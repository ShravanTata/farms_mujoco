"""Arena"""

from .create import create_scene
from ..simulations.element import SimulationElement


class Floor(SimulationElement):
    """Floor"""

    def __init__(self, position):
        super(Floor, self).__init__()
        self._position = position

    def spawn(self):
        """Spawn floor"""
        self._identity = self.from_urdf(
            "plane.urdf",
            basePosition=self._position
        )


class Arena:
    """Documentation for Arena"""

    def __init__(self, elements):
        super(Arena, self).__init__()
        self.elements = elements

    def spawn(self):
        """Spawn"""
        for element in self.elements:
            element.spawn()


class FlooredArena(Arena):
    """Arena with floor"""

    def __init__(self, position=None):
        super(FlooredArena, self).__init__(
            [Floor(position if position is not None else [0, 0, -0.1])]
        )

    @property
    def floor(self):
        """Floor"""
        return self.elements[0]


class ArenaScaffold(FlooredArena):
    """Arena for scaffolding"""

    def spawn(self):
        """Spawn"""
        FlooredArena.spawn(self)
        create_scene(self.floor.identity)
