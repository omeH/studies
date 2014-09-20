"""The module read the file contents.

Usage:
    fileread.py [filename ...]

Description:
    In the absence of input file, reading comes from the standard input.
    Display the contents of the files produced on standard output.
"""
import const


def copy_file_to_stdout(file_):
    """This function reads data from a file blocks and writes them to
    standard output.
    """
    while True:
        block = file_.read(const.BUFFER_SIZE)
        if not block:
            break
        const.STDOUT.write(block)


def main():
    """The main function
    """
    const.init_options()
    file_names = const.get_file_names()

    if file_names is None or len(file_names) == 0:
        copy_file_to_stdout(const.STDIN)
        const.EXIT(0)

    const.print_help(__doc__)

    for file_name in file_names:
        try:
            file_ = open(file_name, 'rb')
            copy_file_to_stdout(file_)
            file_.close()
        except IOError as error:
            const.STDERR.write('fileread.py: {}\n'.format(error))


if __name__ == '__main__':
    main()
