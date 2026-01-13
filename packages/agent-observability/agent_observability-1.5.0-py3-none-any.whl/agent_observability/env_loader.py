"""Helper module to load API key and agent ID from .env file."""
from pathlib import Path
from typing import Optional, Tuple


def load_from_env() -> Tuple[Optional[str], Optional[str]]:
    """
    Load API key and agent ID from .env file if it exists.
    
    Returns:
        Tuple of (api_key, agent_id) or (None, None) if not found
    """
    try:
        env_path = Path.cwd() / ".env"
        if not env_path.exists():
            return None, None
        
        api_key = None
        agent_id = None
        
        content = env_path.read_text()
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('AGENT_OBS_API_KEY='):
                api_key = line.split('=', 1)[1].strip()
            elif line.startswith('AGENT_OBS_AGENT_ID='):
                agent_id = line.split('=', 1)[1].strip()
        
        return api_key, agent_id
    except Exception:
        return None, None


def save_to_env(api_key: str, agent_id: str) -> bool:
    """
    Save API key and agent ID to .env file.
    
    Args:
        api_key: API key to save
        agent_id: Agent ID to save
        
    Returns:
        True if saved successfully, False otherwise
    """
    try:
        env_path = Path.cwd() / ".env"
        
        # Check if keys already exist
        if env_path.exists():
            content = env_path.read_text()
            if "AGENT_OBS_API_KEY=" in content:
                # Already saved, don't duplicate
                return True
        
        # Append to .env
        with open(env_path, "a") as f:
            f.write(f"\n# Agent Observability\n")
            f.write(f"AGENT_OBS_API_KEY={api_key}\n")
            f.write(f"AGENT_OBS_AGENT_ID={agent_id}\n")
        
        return True
    except Exception:
        return False
