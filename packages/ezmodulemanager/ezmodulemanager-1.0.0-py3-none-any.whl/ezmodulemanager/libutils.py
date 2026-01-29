# libutils.py
import os
import traceback
import pathlib

from typing import Sequence

def parse_traceback(e_type: str) -> Sequence[str]:
    """Parses the traceback stack for console debugging
    
    This function extracts the traceback stack. 
    It filters though each frame in the stack to find
    specific values to return for console debugging.

    :param e_type: The type of error actually raised as a
        str literal. Acts as an internal switch for debug logic
    """
    tags = ['register_func', 'call_func', 'import_modlist']
    current_tag = None


    # Extract the traceback stack and then format(list) to 
    # retrieve explicit calls.
    f_list = traceback.format_list(traceback.extract_stack())

    for line in reversed(f_list):
        
        if any(tag in line for tag in tags):
            if tags[0] in str(line): 
                current_tag = tags[0]
                break

            elif tags[1] in line:
                current_tag = tags[1]
                break

            elif tags[2] in line:
                current_tag = tags[2]
                break

            else:
                print('pass')
   

    frame = None
    # Checks for most recent error only.
    for line in reversed(f_list):
        if all(tag in line for tag in ('<module>', current_tag)): # pyright: ignore
            frame = line
            break
        
    
    raw_frame = str(frame).split(",")
    raw_fp = raw_frame[0].strip().replace('"', '')


    if '\n' in frame: # pyright: ignore
        raw_func = raw_frame[2].splitlines()
    else:
        raw_func = raw_frame[2]
    

    line_num = raw_frame[1].strip()
    func = raw_func[1].strip()
    
    # if UNIX
    if os.name == 'posix':
        module = pathlib.PurePosixPath(raw_fp).stem
        if e_type == 'RegistryKeyError':
            return module, line_num, func
        return module, line_num
    # if Windows
    elif os.name == 'nt':
        module = pathlib.PureWindowsPath(raw_fp).stem
        if e_type == 'RegistryKeyError':
            return module, line_num, func
        return module, line_num
    else:
        print('Unknown OS')
