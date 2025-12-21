"""
  File    : pth2safe.py
  Purpose : Convert checkpoints stored in .pth format to .safetensors
  Author  : Martin Rizzo | <martinrizzo@gmail.com>
  Date    : Dec 21, 2025
  Repo    : https://github.com/martin-rizzo/AmazingZImageWorkflow
  License : Unlicense
 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                            Amazing Z-Image Workflow
   Z-Image workflow with customizable image styles and GPU-friendly versions
 _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
"""
import os
import sys
import argparse
import torch
from safetensors.torch import save_file as save_safetensors_file

# ANSI escape codes for colored terminal output
RED      = '\033[91m'
DKRED    = '\033[31m'
YELLOW   = '\033[93m'
DKYELLOW = '\033[33m'
GREEN    = '\033[92m'
CYAN     = '\033[96m'
DKGRAY   = '\033[90m'
RESET    = '\033[0m'

#----------------------------- ERROR MESSAGES ------------------------------#

def disable_colors():
    global RED, DKRED, YELLOW, DKYELLOW, GREEN, CYAN, DKGRAY, RESET
    RED, DKRED, YELLOW, DKYELLOW, GREEN, CYAN, DKGRAY, RESET = "", "", "", "", "", "", "", ""


def info(message: str, padding: int = 0, file=sys.stderr) -> None:
    """Displays an informational message to the error stream.
    """
    print(f"{" "*padding}{CYAN}\u24d8 {message}{RESET}", file=file)


def warning(message: str, *info_messages: str, padding: int = 0, file=sys.stderr) -> None:
    """Displays a warning message to the standard error stream.
    """
    print(f"{" "*padding}{CYAN}[{YELLOW}WARNING{CYAN}]{DKYELLOW} {message}{RESET}", file=file)
    for info_message in info_messages:
        info(info_message, padding=padding, file=file)


def error(message: str, *info_messages: str, padding: int = 0, file=sys.stderr) -> None:
    """Displays an error message to the standard error stream.
    """
    print(f"{" "*padding}{DKRED}[{RED}ERROR!{DKRED}]{DKYELLOW} {message}{RESET}", file=file)
    for info_message in info_messages:
        info(info_message, padding=padding, file=file)


#--------------------------------- HELPERS ---------------------------------#

def looks_like_state_dict(obj):
    """Returns `True` if `obj` looks like a PyTorch state dictionary."""
    MIN_STATE_DICT_KEYS = 10
    return callable(getattr(obj, 'keys', None)) and len(list(obj.keys())) >= MIN_STATE_DICT_KEYS


#===========================================================================#
#////////////////////////////////// MAIN ///////////////////////////////////#
#===========================================================================#

def convert_to_safetensors(checkpoint: str, /,*,
                           overwrite : bool = False,
                           ) -> bool:
    """
    Convert a checkpoint file into the safetensors format.
    Args:
        checkpoint (str): The path to the checkpoint file.
        overwrite (bool): Whether to overwrite an existing safetensors file. Defaults to False.
    Returns:
        `True` if conversion was successful, otherwise `False`.
    """
    # get the filename and add .safetensors extension to it
    new_filename = os.path.splitext(os.path.basename(checkpoint))[0] + ".safetensors"
    print(f' -Generating "{new_filename}"')

    if not os.path.exists(checkpoint):
        error(f"Checkpoint '{checkpoint}' does not exist", padding=2)
        return False

    try:
        state_dict = torch.load(checkpoint, map_location='cpu', weights_only=True)
    except Exception as e:
        error(f"Failed to load checkpoint. ({e})", padding=2)
        return False

    if not looks_like_state_dict(state_dict):
        error(f"Checkpoint {checkpoint} doesn't look like a state dict", padding=2)
        return False

    if os.path.exists(new_filename) and not overwrite:
        error(f"File '{new_filename}' already exists.",
               "You can use the --overwrite flag to overwrite any file.",
               padding=2)
        return False

    try:
        save_safetensors_file(state_dict, new_filename)
    except Exception as e:
        error(f"Failed to save checkpoint. ({e})", padding=2)
        return False

    print(f"    {GREEN}Convertion successful!{RESET}")
    return True


def main(args=None, parent_script=None):
    """
    Main entry point for the script.
    Args:
        args          (optional): List of arguments to parse. Default is None, which will use the command line arguments.
        parent_script (optional): The name of the calling script if any. Used for customizing help output.
    """    
    prog = None
    if parent_script:
        prog = parent_script + " " + os.path.basename(__file__).split('.')[0]

    parser = argparse.ArgumentParser(
        prog=prog,
        description="Convert checkpoints stored in .pth format to .safetensors",
        formatter_class=argparse.RawTextHelpFormatter
        )
    parser.add_argument('checkpoints'      , nargs="+"          , help="The checkpoint(s) you want converted")
    parser.add_argument('-w', '--overwrite', action='store_true', help="Overwrite existing .safetensors file if it exists.")
    parser.add_argument('--no-color'       , action='store_true', help="Disable colored output.")
    args = parser.parse_args(args=args)

    # If the user requested to disable colors, call disable_colors()
    if args.no_color:
        disable_colors()

    # iterate over all the checkpints
    print()
    error_count = 0
    for checkpoint in args.checkpoints:
        success = convert_to_safetensors(checkpoint, overwrite=args.overwrite)
        if not success: error_count += 1
        print()

    # print the final report
    if error_count == 0:
        print(f"All checkpoints converted successfully!")
    elif error_count == len(args.checkpoints):
        print(f"{RED}Failed to convert any checkpoint.{RESET}")
    else:
        print(f"{RED}Failed to convert {error_count} checkpoint(s).{RESET}")



if __name__ == "__main__":
    main()
