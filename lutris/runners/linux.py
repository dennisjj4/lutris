# -*- coding: utf-8 -*-
import os
from lutris.runners.runner import Runner


class linux(Runner):
    """Runs native games"""

    game_options = [
        {
            "option": "exe",
            "type": "file",
            "default_path": "game_path",
            "label": "Executable"
        },
        {
            "option": "args",
            "type": "string",
            "label": "Arguments"
        },
        {
            "option": "ld_preload",
            "type": "file",
            "label": "Preload library"
        },
        {
            "option": "ld_library_path",
            "type": "directory_chooser",
            "label": "Add directory to LD_LIBRARY_PATH"
        }
    ]

    def __init__(self, settings=None):
        super(linux, self).__init__()
        self.platform = "Linux games"
        self.ld_preload = None
        self.settings = settings

    @property
    def game_exe_dir(self):
        exe_path = self.settings['game'].get('exe') or None
        if exe_path:
            dir_path = os.path.dirname(exe_path)
            if os.path.isabs(dir_path):
                return dir_path
            elif self.prefix_path:
                return os.path.join(self.prefix_path, exe_path)

    @property
    def browse_dir(self):
        """Returns the path to open with the Browse Files action."""
        return self.working_dir  # exe path

    @property
    def working_dir(self):
        """Return the working directory to use when running the game."""
        if self.game_exe_dir:
            return self.game_exe_dir
        else:
            return self.get_game_path()

    def is_installed(self):
        """Well of course Linux is installed, you're using Linux right ?"""
        return True

    def play(self):
        """ Run native game. """
        launch_info = {}
        game_config = self.settings.get('game')
        executable = game_config.get("exe")
        if not os.path.exists(executable):
            return {'error': 'FILE_NOT_FOUND', 'file': executable}

        ld_preload = game_config.get('ld_preload')
        if ld_preload:
            launch_info['ld_preload'] = ld_preload

        ld_library_path = game_config.get('ld_library_path')
        if ld_library_path:
            launch_info['ld_library_path'] = ld_library_path

        command = []
        command.append("./%s" % os.path.basename(executable))

        args = game_config.get('args', "")
        for arg in args.split():
            command.append(arg)
        launch_info['command'] = command
        return launch_info
