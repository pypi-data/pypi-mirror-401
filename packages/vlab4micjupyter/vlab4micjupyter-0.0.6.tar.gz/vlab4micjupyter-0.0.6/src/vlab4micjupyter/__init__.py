import os
from pathlib import Path

# create local configuration directory
local_config_path = Path.home() / "vlab4micjupyter"
if not os.path.exists(local_config_path):
    os.makedirs(local_config_path)

local_fluorophores_path = local_config_path / "fluorophores"
if not os.path.exists(local_fluorophores_path):
    os.makedirs(local_fluorophores_path)
