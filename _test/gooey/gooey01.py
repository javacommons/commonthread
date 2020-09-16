from commonthread import *
from gooey import Gooey
from MyGooeyParser import MyGooeyParser
import sys

lg = CommonThreadLogger()
lg.setup_basic()


@Gooey(dump_build_config=False, program_name="Widget Demo")
def main():
    desc = "Example application to show Gooey's various widgets"
    file_help_msg = "Name of the file you want to process"

    parser = MyGooeyParser()

    parser.add_file_chooser("FileChooser",
                            help=file_help_msg,
                            default='C:\\temp\\test.txt',
                            message='選択してね!')
    parser.add_dir_chooser("DirectoryChooser",
                           help=file_help_msg,
                           default='C:\\temp',
                           message='選択してね!')
    parser.add_file_saver("FileSaver",
                          help=file_help_msg,
                          default='C:\\temp\\test2.txt',
                          message='選択してね!')
    parser.add_dir_chooser("directory",
                           help="Directory to store output",
                           default='C:\\temp',
                           message='選択してね!')
    parser.add_argument('-d', '--duration', default=2,
                        type=int, help='Duration (in seconds) of the program output')
    parser.add_argument('-s', '--cron-schedule', type=int,
                        help='datetime when the cron should begin', widget='DateChooser')
    parser.add_argument('--cron-time',
                        help='datetime when the cron should begin', widget="TimeChooser")
    parser.add_argument(
        "-c", "--showtime", action="store_true", help="display the countdown timer")
    parser.add_argument(
        "-p", "--pause", action="store_true", help="Pause execution")
    parser.add_argument('-v', '--verbose', action='count')
    parser.add_argument(
        "-o", "--overwrite", action="store_true", help="Overwrite output file (if present)")
    parser.add_argument(
        '-r', '--recursive', choices=['yes', 'no'], default='yes', help='Recurse into subfolders')
    parser.add_argument(
        "-w", "--writelog", default="writelogs", help="Dump output to local file")
    parser.add_argument(
        "-e", "--error", action="store_true", help="Stop process on error (default: No)")
    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument('-t', '--verbozze', dest='verbose',
                           action="store_true", help="Show more details")
    verbosity.add_argument('-q', '--quiet', dest='quiet',
                           action="store_true", help="Only output on error")

    params = parser.parse_args()
    lg.debug('params={}'.format(params))
    # lg.debug('params.MultiFileChooser={}'.format(params.MultiFileChooser))
    lg.debug('sys.argv={}'.format(sys.argv))
    print('sys.argv={}'.format(sys.argv))


if __name__ == '__main__':
    main()
