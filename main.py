import argparse
import os
import shutil
from pathlib import Path

def copy_to_single_dir(path: str, destination: str, extension: list, show: bool):
    path += '/'
    entries = os.scandir(path)
    for entry in entries:
        if entry.is_dir():
            if show:
                print("DIR: {}".format(entry.path))
            copy_to_single_dir(entry.path, destination, extension, show)
        elif entry.is_file():
            split_tup = os.path.splitext(entry.name)

            if split_tup[1] in extension:
                if show:
                    print(split_tup)
                shutil.copy(entry.path, destination)


def count_files(path: str) -> int:
    path += '/'
    num_files = len(os.listdir(path))
    return num_files


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""This script copies all contents inside directories
        and puts them in a single location.""")
    parser.add_argument('in_dir', type=lambda p: Path(p).absolute(),
                        default=Path(__file__).absolute().parent / "data",
                        help='<Required> Target directory location')
    parser.add_argument('out_dir', type=str,
                        help='<Required> Destination directory name.')
    parser.add_argument('ext', type=str,
                        help='<Required> Extension file to be copy, include the dot, example: .pdf .epub',
                        nargs='+')
    parser.add_argument('-q','--quiet',
                        help='Do not print directory and file names',
                        action='store_const', dest='quiet', const=True,
                        default=False)

    args = parser.parse_args()
    dest = os.getcwd() + '/' + args.out_dir

    try:
        if not args.in_dir.exists() or not args.in_dir.is_dir():
            raise Exception('Target directory must be valid.')

        print("Copy files of extension: {}.".format(args.ext))

        os.mkdir(dest)
        print("Directory '{}' created.".format(args.out_dir))

        print('Processing, please wait...')
        copy_to_single_dir(str(args.in_dir), dest, args.ext, not args.quiet)

        num_files = count_files(dest);

        if num_files == 0:
            os.rmdir(dest)
            print("Remove empty directory '{}'.".format(args.out_dir))
        else:
            print('Output directory location: {}'.format(dest))
        print('{} File(s) copied successfully.'.format(num_files))

    except Exception as e:
        print(e)
    except OSError as error:
        print(error)
