# -*- coding:Utf-8 -*-
import os
from lutris import settings
from lutris.runners.runner import Runner


class jzintv(Runner):
    """Intellivision Emulator"""
    package = "jzintv"
    executable = "jzintv"
    platform = "Intellivision"

    tarballs = {
        'i386': None,
        'x64': 'jzintv-1.0-beta4-x86_64.tar.gz',
    }

    game_options = [{
        'option': 'main_file',
        'type': 'file',
        'label': "Rom File",
        'default_path': 'game_path',
    }]
    runner_options = [
        {
            "option": "bios_path",
            "type": "directory_chooser",
            "label": "Bios Path"
        },
        {
            "option": "fullscreen",
            "type": "bool",
            "label": "Fullscreen"
        }
    ]

    def get_executable(self):
        return os.path.join(settings.RUNNER_DIR, 'jzintv/bin/jzintv')

    def play(self):
        """Run Intellivision game"""
        arguments = [self.get_executable()]
        if self.runner_config.get("fullscreen"):
            arguments = arguments + ["-f"]
        bios_path = self.runner_config.get("bios_path", '')
        if os.path.exists(bios_path):
            arguments.append("--execimg=\"%s/exec.bin\"" % bios_path)
            arguments.append("--gromimg=\"%s/grom.bin\"" % bios_path)
        else:
            return {'error': 'NO_BIOS'}
        rom_path = self.settings["game"].get("main_file", '')
        if not os.path.exists(rom_path):
            return {'error': 'FILE_NOT_FOUND', 'file': rom_path}
        romdir = os.path.dirname(rom_path)
        romfile = os.path.basename(rom_path)
        arguments += ["--rom-path=\"%s/\"" % romdir]
        arguments += ["\"%s\"" % romfile]
        return {'command': arguments}
