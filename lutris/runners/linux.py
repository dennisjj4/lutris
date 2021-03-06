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
            "option": "working_dir",
            "type": "directory_chooser",
            "label": "Working directory"
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
    def game_exe(self):
        """Return the game's executable's path."""
        exe = self.settings['game'].get('exe')
        if exe:
            if os.path.isabs(exe):
                return exe
            else:
                return os.path.join(self.get_game_path(), exe)
        else:
            logger.error("Game executable not configured.")

    @property
    def browse_dir(self):
        """Return the path to open with the Browse Files action."""
        return self.working_dir  # exe path

    @property
    def working_dir(self):
        """Return the working directory to use when running the game."""
        option = self.settings['game'].get('working_dir')
        if option:
            return option
        if self.game_exe:
            return os.path.dirname(self.game_exe)
        else:
            return super(wine, self).working_dir

    def is_installed(self):
        """Well of course Linux is installed, you're using Linux right ?"""
        return True

    def play(self):
        """Run native game."""
        launch_info = {}
        game_config = self.settings.get('game')

        if not os.path.exists(self.game_exe):
            return {'error': 'FILE_NOT_FOUND', 'file': self.game_exe}

        ld_preload = game_config.get('ld_preload')
        if ld_preload:
            launch_info['ld_preload'] = ld_preload

        ld_library_path = game_config.get('ld_library_path')
        if ld_library_path:
            launch_info['ld_library_path'] = ld_library_path

        command = []
        command.append('"%s"' % self.game_exe)

        args = game_config.get('args', "")
        for arg in args.split():
            command.append(arg)
        launch_info['command'] = command
        return launch_info
