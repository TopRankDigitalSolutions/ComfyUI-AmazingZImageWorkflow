"""
  File    : make.py
  Purpose : Build Z-Image Workflows from source templates and configuration files.
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

# list of files that should be taken as global configuration
GLOBAL_CONFIG_FILES = ["global.txt", "globals.txt"]

# default directory where to look for source files
DEFAULT_SOURCE_DIR = "src"

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


def fatal_error(message: str, *info_messages: str, padding: int = 0, file=sys.stderr) -> None:
    """Displays a fatal error message to the standard error stream and exits with status code 1.
    """
    error(message, *info_messages, padding=padding, file=file)
    sys.exit(1)


#===========================================================================#
#////////////////////////////////// MAIN ///////////////////////////////////#
#===========================================================================#

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

    # set up argument parser for the script
    parser = argparse.ArgumentParser(
        prog=prog,
        description="Build Z-Image Workflows from source templates and configuration files.",
        formatter_class=argparse.RawTextHelpFormatter
        )
    parser.add_argument('--no-color'       , action='store_true', help="Disable colored output.")
    parser.add_argument('-s','--source-dir', type=str,            help="The source dir containing templates and config files (default: /src)")

    args = parser.parse_args(args=args)

    # if the user requested to disable colors, call disable_colors()
    if args.no_color:
        disable_colors()

    # get source directory and convert it to absolute path
    source_dir = args.source_dir or DEFAULT_SOURCE_DIR
    source_dir = os.path.join(os.getcwd(), source_dir)
    source_dir = os.path.realpath(source_dir)

    # gather three types of files from the source directory:
    #   1. List of .json files (excluding temporary ~.json files)
    #   2. List of .txt files with "#!ZCONFIG" flag
    #   3. Specific global configuration file matching GLOBAL_CONFIG_FILES
    #
    json_templates = []  #< list to store paths of .json template files
    text_configs   = []  #< list to store paths of valid text config files
    global_config  = ""  #< path to the global configuration file (if found)
    for filename in os.listdir(source_dir):
        if filename.endswith(".json") and not filename.endswith("~.json"):
            json_templates.append( os.path.join(source_dir, filename) )
        elif filename.endswith(".txt") and "#!ZCONFIG" in open(os.path.join(source_dir, filename)).read():
            if filename in GLOBAL_CONFIG_FILES:
                global_config = os.path.join(source_dir, filename)
            else:
                text_configs.append( os.path.join(source_dir, filename) )

    # display errors if no required files were found
    if not json_templates:
        fatal_error("No JSON template files found in the source directory.")
    if not text_configs:
        fatal_error("No valid text configuration files found in the source directory.")

    # show a report of the found files
    print("")
    print(" Configuration Files:")
    if global_config:
        print(f"    - {os.path.basename(global_config)}")
    for fullpath in text_configs:
        print(f"    - {os.path.basename(fullpath)}")
    print(" Template Files:")
    for fullpath in json_templates:
        print(f"    - {os.path.basename(fullpath)}")
    print("")





if __name__ == "__main__":
    main()
