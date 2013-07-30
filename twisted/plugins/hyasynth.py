from twisted.application.service import ServiceMaker


CarapaceSSHService = ServiceMaker(
    "Hyasynth SSH Server",
    "hyasynth.app.service",
    ("An SSH shell for Hy-SuperCollider interaction."),
    "hyasynth")
