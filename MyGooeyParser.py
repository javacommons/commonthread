from gooey import GooeyParser

class MyGooeyParser(GooeyParser):
    def __init__(self):
        GooeyParser.__init__(self)

    def add_file_chooser(self, name, help=None, default=None, message=None):
        import os
        initial_folder = None
        if default:
            if default.strip() == '':
                initial_folder = os.path.expanduser('~')
            else:
                old_value = os.path.abspath(default).replace('/', '\\')
                initial_folder = os.path.dirname(old_value)
        else:
            initial_folder = os.path.expanduser('~')
        self.add_argument(
            name, help=help, widget="FileChooser",
            default=default,
            gooey_options={'default_dir': initial_folder, 'message': message, 'full_width': True})

    def add_multi_file_chooser(self, name, help=None, default=None, message=None):
        import os
        initial_folder = None
        if default:
            if default.strip() == '':
                initial_folder = os.path.expanduser('~')
            else:
                file_list = default.split(';')
                old_value = os.path.abspath(file_list[0]).replace('/', '\\')
                initial_folder = os.path.dirname(old_value)
        else:
            initial_folder = os.path.expanduser('~')
        self.add_argument(
            name, nargs='*', help=help, widget="MultiFileChooser",
            default=default,
            gooey_options={'default_dir': initial_folder, 'message': message, 'full_width': True})

    def add_file_saver(self, name, help=None, default=None, message=None):
        import os
        initial_folder = None
        if default:
            if default.strip() == '':
                initial_folder = os.path.expanduser('~')
            else:
                old_value = os.path.abspath(default).replace('/', '\\')
                initial_folder = os.path.dirname(old_value)
        else:
            initial_folder = os.path.expanduser('~')
        self.add_argument(
            name, help=help, widget="FileSaver",
            default=default,
            gooey_options={'default_dir': initial_folder, 'message': message, 'full_width': True})

    def add_dir_chooser(self, name, help=None, default=None, message=None):
        import os
        initial_folder = None
        if default:
            if default.strip() == '':
                initial_folder = os.path.expanduser('~')
            else:
                old_value = os.path.abspath(default).replace('/', '\\')
                initial_folder = old_value
        else:
            initial_folder = os.path.expanduser('~')
        self.add_argument(
            name, help=help, widget="DirChooser",
            default=default,
            gooey_options={'default_path': initial_folder, 'message': message, 'full_width': True})
