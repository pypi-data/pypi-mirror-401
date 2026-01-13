# patch-path
Run a command with patched executables on the path

This is vibe coded but I am using it.

## Alternatives and prior work
This is encouraged by patching frameworks like `mock` in python and the LD_PRELOAD environment variable.

You could patch your PATH directory and have it point at a directory containing patching programs


#  Usage
Patch fzf with a program that returns an empty string and log calls to fzf along with their input

```
patch-path --fzf  program
```

Patch fzf and have it return hello

```
patch-path --fzf=hello  program
```


