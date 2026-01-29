"""State management for Code Discovery application and instance IDs."""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class DiscoveryStateManager:
    """Manages persistent state for application and instance IDs."""

    # YAML header with comments
    YAML_HEADER = """# Code Discovery State File
# ========================
# This file stores the application and instance IDs from your API security platform.
# DO NOT DELETE THIS FILE - it ensures that subsequent runs update the same application
# instead of creating duplicates.
#
# This file is automatically created and managed by Code Discovery.
# You can safely commit this file to your repository (it contains no sensitive data).
#
# If you delete this file, Code Discovery will create a new application on the next run,
# which may result in duplicate applications in your API security platform.

"""

    def __init__(self, repo_path: Path):
        """
        Initialize state manager.

        Args:
            repo_path: Path to the repository root.
        """
        self.repo_path = Path(repo_path)
        self.state_file = self.repo_path / "apisec-bolt-code-discovery" / "state.yaml"
        self.state_dir = self.state_file.parent

    def load_state(self) -> Optional[Dict[str, Any]]:
        """
        Load state from file.

        Returns:
            State dictionary if file exists and is valid, None otherwise.
        """
        if not self.state_file.exists():
            return None

        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                content = f.read()
                # Parse YAML (skip header comments)
                state = yaml.safe_load(content)
                
            # Validate state
            if self.validate_state(state):
                return state
            else:
                print(f"Warning: Invalid state file at {self.state_file}. Treating as missing.")
                return None
        except yaml.YAMLError as e:
            print(f"Warning: Error parsing state file {self.state_file}: {e}. Treating as missing.")
            return None
        except Exception as e:
            print(f"Warning: Error reading state file {self.state_file}: {e}. Treating as missing.")
            return None

    def save_state(self, state: Dict[str, Any]) -> bool:
        """
        Save state to file.

        Args:
            state: State dictionary with applicationId, instanceId, and lastUpdatedAt.

        Returns:
            True if successful, False otherwise.
        """
        try:
            # Ensure directory exists
            self.state_dir.mkdir(parents=True, exist_ok=True)

            # Prepare state data (only the 3 required fields)
            state_data = {
                "applicationId": state.get("applicationId"),
                "instanceId": state.get("instanceId"),
                "lastUpdatedAt": state.get("lastUpdatedAt"),
            }

            # Validate before saving
            if not self.validate_state(state_data):
                print("Error: Invalid state data. Cannot save.")
                return False

            # Write YAML with header comments
            with open(self.state_file, "w", encoding="utf-8") as f:
                f.write(self.YAML_HEADER)
                
                # Add field comments
                f.write("# Application ID from the API security platform\n")
                f.write("# This is used to update the existing application on subsequent runs\n")
                f.write(f"applicationId: \"{state_data['applicationId']}\"\n\n")
                
                f.write("# Instance ID associated with this application\n")
                f.write("# This represents the instance where the API spec will be reloaded\n")
                f.write(f"instanceId: \"{state_data['instanceId']}\"\n\n")
                
                f.write("# Timestamp of the last successful update\n")
                f.write("# Format: ISO 8601 (YYYY-MM-DDTHH:MM:SSZ)\n")
                f.write(f"lastUpdatedAt: \"{state_data['lastUpdatedAt']}\"\n")

            return True
        except Exception as e:
            print(f"Error saving state file {self.state_file}: {e}")
            return False

    def get_application_id(self) -> Optional[str]:
        """
        Get stored application ID.

        Returns:
            Application ID if available, None otherwise.
        """
        state = self.load_state()
        return state.get("applicationId") if state else None

    def get_instance_id(self) -> Optional[str]:
        """
        Get stored instance ID.

        Returns:
            Instance ID if available, None otherwise.
        """
        state = self.load_state()
        return state.get("instanceId") if state else None

    def has_state(self) -> bool:
        """
        Check if state file exists and is valid.

        Returns:
            True if valid state exists, False otherwise.
        """
        state = self.load_state()
        return state is not None

    def clear_state(self) -> bool:
        """
        Clear/delete state file.

        Returns:
            True if successful, False otherwise.
        """
        try:
            if self.state_file.exists():
                self.state_file.unlink()
            return True
        except Exception as e:
            print(f"Error deleting state file {self.state_file}: {e}")
            return False

    @staticmethod
    def validate_state(state: Optional[Dict[str, Any]]) -> bool:
        """
        Validate state dictionary.

        Args:
            state: State dictionary to validate.

        Returns:
            True if valid, False otherwise.
        """
        if not state:
            return False

        # Must have all required fields
        required_fields = ["applicationId", "instanceId", "lastUpdatedAt"]
        for field in required_fields:
            if not state.get(field):
                return False

        # Validate applicationId and instanceId are non-empty strings
        if not isinstance(state.get("applicationId"), str) or not state["applicationId"]:
            return False
        if not isinstance(state.get("instanceId"), str) or not state["instanceId"]:
            return False

        return True

    def update_timestamp(self) -> bool:
        """
        Update only the lastUpdatedAt timestamp in existing state file.

        Returns:
            True if successful, False otherwise.
        """
        state = self.load_state()
        if not state:
            return False

        # Update timestamp
        state["lastUpdatedAt"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        return self.save_state(state)

