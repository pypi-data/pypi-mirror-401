import subprocess
import sys
from pathlib import Path

import yaml

CONFIG_NAMES = ["aideploy.yml", "aideploy.yaml", ".aideploy.yml", ".aideploy.yaml"]


def find_config() -> Path | None:
    cwd = Path.cwd()
    for name in CONFIG_NAMES:
        path = cwd / name
        if path.is_file():
            return path
    return None


def main():
    config_path = find_config()

    if not config_path:
        print("No aideploy.yml / .aideploy.yml found in current directory.")
        print("Minimal example aideploy.yml:")
        print("""commands:
  - echo "Starting deployment..."
  - npm install
  - npm run build
  - vercel --prod""")
        sys.exit(1)

    try:
        with config_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"YAML parsing error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading config: {e}")
        sys.exit(1)

    commands = data.get("commands")

    if not isinstance(commands, list) or not commands:
        print("No 'commands:' list found in config")
        sys.exit(1)

    print(f"Using config: {config_path.name}")
    print("Running commands:\n")

    for i, cmd in enumerate(commands, 1):
        print(f"[{i}/{len(commands)}] {cmd}")
        try:
            subprocess.run(
                cmd,
                shell=True,
                check=True,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"\nCommand failed (exit {e.returncode})")
            sys.exit(e.returncode)
        except FileNotFoundError:
            print(f"\nCommand not found: {cmd}")
            sys.exit(127)

    print("\nDeployment finished ✓")
    sys.exit(0)


if __name__ == "__main__":
    sys.exit(main())
