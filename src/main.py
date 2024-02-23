from config import paths

from argparse import ArgumentParser

from os import listdir
from os.path import basename

def main():

    parser = get_parser()
    select_mode(parser=parser)

def default_message():
    
    print("\r No option specified. \n\r Type '--help' for list of arguments.")

def open_textfile(path: str) -> str:
    
    with open(path, 'r', encoding='utf-8') as file:
        description = file.read().strip()
        return description

def get_descriptions() -> list:

    return [
        open_textfile(path=paths.description_path),
        open_textfile(path=paths.calibration_description_path),
        open_textfile(path=paths.stream_description_path),
        open_textfile(path=paths.stereo_description_path)
        ]

def get_parser():
    
    (
        description_path,
        calibration_description_path,
        stream_description_path,
        stereo_description_path
    ) = get_descriptions() 

    parser = ArgumentParser(description=description_path)
    parser.add_argument('-c','--calibration', action='store_true', help=calibration_description_path)
    parser.add_argument('-s','--stream', action='store_true', help=stream_description_path)
    parser.add_argument('-d','--stereo', action='store_true', help=stereo_description_path)

    return parser

def select_mode(parser):
    # TODO 
    args = parser.parse_args()
    
    if args.calibration: 
        print('calibration mode')
    elif args.stream: 
        print('stream mode')
    elif args.stereo: 
        print('stereo mode')
    else: default_message()

if __name__ == '__main__': main()

