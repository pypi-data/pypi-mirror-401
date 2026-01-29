from pathlib import Path
from typing import NewType


KubeArtifactFilePath = NewType("KubeArtifactFilePath", Path)
"""FilePath to a Kube Artifact File"""
