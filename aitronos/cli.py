# cli.py
import sys
from aitronos.commands import streamline

def main():
    if len(sys.argv) < 2:
        print("Usage: aitronos <command> [options]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "streamLine":
        streamline.handle_streamLine_command(sys.argv[2:])
    # Add future commands here:
    # elif command == "feature_x":
    #     feature_x.handle_feature_x_command(sys.argv[2:])
    else:
        print(f"Unknown command: {command}")
        print("Available commands: streamLine")
        sys.exit(1)

if __name__ == "__main__":
    main()