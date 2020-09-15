from gooey import Gooey, GooeyParser
from commonthread import *
import sys
import time

CommonThreadLogger.setup_basic_logging()
lg = CommonThreadLogger()

program_message = \
    '''
Thanks for checking out out Gooey!

This is a sample message to demonstrate Gooey's functionality.

Here are the arguments you supplied:

{0}

-------------------------------------

Gooey is an ongoing project, so feel free to submit any bugs you find to the
issue tracker on Github[1], or drop me a line at audionautic@gmail.com if ya want.

[1](https://github.com/chriskiehl/Gooey)

See ya!

^_^

'''


def display_message():
    message = program_message.format('\n'.join(sys.argv[1:])).split('\n')
    delay = 1.8 / len(message)

    for line in message:
        print(line)
        time.sleep(delay)


@Gooey(dump_build_config=False, program_name="Widget Demo")
def main():
    desc = "Example application to show Gooey's various widgets"
    file_help_msg = "Name of the file you want to process"

    my_cool_parser = GooeyParser(description=desc)

    my_cool_parser.add_argument(
        "FileChooser", help=file_help_msg, widget="FileChooser",
        default='C:\\temp\\test.txt',
        gooey_options={'default_dir': "c:\\temp", 'message': "選択してね!", 'full_width': True})
    my_cool_parser.add_argument(
        "DirectoryChooser", help=file_help_msg, widget="DirChooser")
    my_cool_parser.add_argument(
        "FileSaver", help=file_help_msg, widget="FileSaver")
    my_cool_parser.add_argument(
        "MultiFileChooser", nargs='*', help=file_help_msg, widget="MultiFileChooser")
    my_cool_parser.add_argument("directory", help="Directory to store output")

    my_cool_parser.add_argument('-d', '--duration', default=2,
                                type=int, help='Duration (in seconds) of the program output')
    my_cool_parser.add_argument('-s', '--cron-schedule', type=int,
                                help='datetime when the cron should begin', widget='DateChooser')
    my_cool_parser.add_argument('--cron-time',
                                help='datetime when the cron should begin', widget="TimeChooser")
    my_cool_parser.add_argument(
        "-c", "--showtime", action="store_true", help="display the countdown timer")
    my_cool_parser.add_argument(
        "-p", "--pause", action="store_true", help="Pause execution")
    my_cool_parser.add_argument('-v', '--verbose', action='count')
    my_cool_parser.add_argument(
        "-o", "--overwrite", action="store_true", help="Overwrite output file (if present)")
    my_cool_parser.add_argument(
        '-r', '--recursive', choices=['yes', 'no'], help='Recurse into subfolders')
    my_cool_parser.add_argument(
        "-w", "--writelog", default="writelogs", help="Dump output to local file")
    my_cool_parser.add_argument(
        "-e", "--error", action="store_true", help="Stop process on error (default: No)")
    verbosity = my_cool_parser.add_mutually_exclusive_group()
    verbosity.add_argument('-t', '--verbozze', dest='verbose',
                           action="store_true", help="Show more details")
    verbosity.add_argument('-q', '--quiet', dest='quiet',
                           action="store_true", help="Only output on error")

    params = my_cool_parser.parse_args()
    lg.debug('params={}'.format(params))
    lg.debug('sys.argv={}'.format(sys.argv))
    print('sys.argv={}'.format(sys.argv))
    display_message()


if __name__ == '__main__':
    main()
