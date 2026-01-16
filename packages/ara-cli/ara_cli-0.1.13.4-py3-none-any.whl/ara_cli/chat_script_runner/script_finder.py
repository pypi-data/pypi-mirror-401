import os
from ara_cli.ara_config import ConfigManager


class ScriptFinder:
    def __init__(self):
        config = ConfigManager.get_config()
        # Convert to absolute path NOW, before any chdir operations
        # This ensures scripts are found after Chat.start() changes cwd
        self.local_prompt_templates_dir = os.path.abspath(
            config.local_prompt_templates_dir
        )

    def get_custom_scripts_dir(self):
        return os.path.join(self.local_prompt_templates_dir, "custom-scripts")

    def get_global_scripts_dir(self):
        return os.path.join(self.local_prompt_templates_dir, "global-scripts")

    def find_script(self, script_name: str) -> str | None:
        # Handle explicit global path for backward compatibility or specific cases
        if script_name.startswith("global/"):
            script_path = os.path.join(
                self.get_global_scripts_dir(), script_name.replace("global/", ""))
            if os.path.exists(script_path):
                return script_path
            return None

        # 1. Search in custom-scripts first (allows overriding global scripts)
        custom_script_path = os.path.join(
            self.get_custom_scripts_dir(), script_name)
        if os.path.exists(custom_script_path):
            return custom_script_path

        # 2. If not found in custom, fall back to global-scripts
        global_script_path = os.path.join(
            self.get_global_scripts_dir(), script_name)
        if os.path.exists(global_script_path):
            return global_script_path

        return None
