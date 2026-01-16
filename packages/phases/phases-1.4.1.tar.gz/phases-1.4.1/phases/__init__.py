__version__ = "v1.4.1"

from phases.commands.run import Run
from .DefaultProject import DefaultProject


loadProject = Run.loadProject
