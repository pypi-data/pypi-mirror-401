#!/usr/bin/env python3

import os
import sys
import tempfile
import shutil
from pathlib import Path


def main():
    patches = []
    command_args = []
    parsing_patches = True

    for arg in sys.argv[1:]:
        if parsing_patches and arg == "--":
            # Double dash separator - stop parsing patches
            parsing_patches = False
        elif parsing_patches and arg.startswith("--"):
            # Parse patch specification
            patch_spec = arg[2:]
            if "=" in patch_spec:
                executable, return_value = patch_spec.split("=", 1)
            else:
                executable = patch_spec
                return_value = ""
            patches.append((executable, return_value))
        else:
            parsing_patches = False
            command_args.append(arg)

    if not command_args:
        print("Usage: patch-path [--executable[=value]] ... command [args...]", file=sys.stderr)
        print("Example: patch-path --fzf=hello --grep vim", file=sys.stderr)
        sys.exit(1)

    # Create temporary directory for patches
    patch_dir = tempfile.mkdtemp(prefix="patch-path-")
    
    try:
        # Create patch scripts
        for executable, return_value in patches:
            patch_script = Path(patch_dir) / executable
            
            script_content = "#!/usr/bin/env bash\n"
            script_content += f'echo "[patch-path] {executable} $@" >&2\n'
            script_content += 'if [ -p /dev/stdin ]; then\n'
            script_content += '  input=$(cat)\n'
            script_content += '  echo "[patch-path] stdin: $input" >&2\n'
            script_content += 'fi\n'
            if return_value:
                script_content += f"echo '{return_value}'\n"
            script_content += "exit 0\n"
            
            patch_script.write_text(script_content)
            patch_script.chmod(0o755)

        # Prepend patch directory to PATH
        original_path = os.environ.get("PATH", "")
        new_path = f"{patch_dir}:{original_path}"
        os.environ["PATH"] = new_path

        # Execute the command
        os.execvp(command_args[0], command_args)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        shutil.rmtree(patch_dir, ignore_errors=True)
        sys.exit(1)


if __name__ == "__main__":
    main()