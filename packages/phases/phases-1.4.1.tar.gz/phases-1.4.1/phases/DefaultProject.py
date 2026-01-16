from pyPhases import pdict
from .commands.run import Run


class DefaultProject:
  
  @staticmethod
  def create(configFiles=None, plugins=""):
    config = pdict()
    config["name"] = "myProject"
    config["plugins"] = plugins
    config["config"] = pdict()
    config["phases"] = []
    config["exporter"] = []
    config["data"] = []

    phasesRun = Run({})
    phasesRun.projectFileName = None
    if configFiles != "":
      phasesRun.projectConfigFileName = configFiles
    
    phasesRun.prepareConfig(config)

    return phasesRun.createProjectFromConfig(phasesRun.config)
    