==================
Writing installers
==================

Fetching required files
=======================

The ``files`` section of the installer references every file needed for
installing the game. This section's keys are unique identifier used later in
the ``installer`` section. The value can either be a string containing a URI
pointing at the required file or a dictionary containing the ``filename`` and
``uri`` keys. The ``uri`` key is equivalent to passing only a string to the
installer and the ``filename`` key will be used to give the local copy another
name. [TODO: example]

If the game contains copyrighted files that cannot be redistributed, the value
should begin with ``N/A``. When the installer encounter this value, it will
prompt the user for the location of the file. To indicate to the user what file
to select, append a message to ``N/A`` like this:
``N/A:Please select the installer for this game``

Examples:

::

    files:
    - file1: http://site.com/gamesetup.exe
    - file2: "N/A:Select the game's setup file"


If the game makes use of (Windows) Steam data, the value should be
``$WINESTEAM:appid:path/to/data``. This will check that the data is available
or install it otherwise.


Installer meta data
===================

Referencing the main file
---------------------------

For Linux and Wine games, specify the executable file with the ``exe``
directive. The given path is relative to the game directory.
Example: ``exe: game.sh``

For emulator games, in case you don't ask the user to select the rom
directly but make the installer extract it from an archive or something, you
can reference the rom with the ``main_file`` parameter.
Example: ``main_file: game.rom``

For browser games, specify the game's URL with ``main_file``.
Example: ``main_file: http://www...``

Presetting game parameters
--------------------------

The ``game`` directive lets you preset game parameters and options. Available
parameters depend on the runner:

* linux: ``args`` (optional command arguments), ``working_dir``
 (optional working directory, defaults to the exe's dir).

* wine:  ``args``, ``prefix`` (optional Wine prefix), ``working_dir`` (optional
 working directory, defaults to the exe's dir).

* winesteam: ``args``, ``prefix`` (optional Wine prefix).

[TODO: reference all options] Meanwhile, you can check the configuration window
of any game using the runner you're writing for to get a list of the available
options.

Example:

::

    game:
        exe: drive_c/Game/game.exe
        prefix: $GAMEDIR
        args: -arg

Mods and add-ons
----------------

Mods and add-ons require that a base game is already installed on the system.
You can let the installer know that you want to install an add-on by specifying
the ``requires`` directive. The value of ``requires`` must be the canonical
slug name of the base game, not one of its aliases. For example, to install the
add-on "The reckoning" for Quake 2, you should add:

``requires: quake-2``


Writing the installation script
===============================

After every file needed by the game has been aquired, the actual installation
can take place. A series of directives will tell the installer how to set up
the game correctly. Start the installer section with ``installer:`` then stack
the directives by order of execution (top to bottom).

Displaying an 'Insert disc' dialog
----------------------------------

The ``insert-disc`` command will display a message box to the user requesting
him to insert the game's disc into the optical drive.

Ensure a correct disc detection by specifying a file or folder present on the
disc with the ``requires`` parameter.

A link to CDEmu's homepage and PPA will also be displayed if the program isn't
detected on the machine, otherwise it will be replaced with a button to open
gCDEmu. You can override this default text with the ``message`` parameter.

Example:

::

    - insert-disc:
        message: Insert the Diablo CD to continue
        requires: diablosetup.exe

Moving files and directories
----------------------------

Move files by using the ``move`` command. ``move``  requires two parameters:
``src`` and ``dst``.

The ``src`` parameter can either be a ``file id`` or a path relative to game
dir. If the parameter value is not found in the list of file ids,
then it must be prefixed by either ``$CACHE`` or ``$GAMEDIR`` to move a file or
directory from the download cache or the game's install dir, respectively.

The ``dst`` parameter should be prefixed by either ``$GAMEDIR`` or ``$HOME``
to move files to path relative to the game dir or the current user's home
directory.

The ``move`` command cannot overwrite files.

Example:

::

    - move:
        src: game-file-id
        dst: $GAMEDIR/location

Copying and merging directories
-------------------------------

Both merging and copying actions are done with the ``merge`` directive.
Whether the action does a merge or copy depends on the existence of the
destination directory. When merging into an existing directory, original files
with the same name as the ones present in the merged directory will be
overwritten. Take this into account when writing your script and order your
actions accordingly.

Example:

::

    - merge:
        src: game-file-id
        dst: $GAMEDIR/location

Extracting archives
-------------------

Extracting archives is done with the ``extract`` directive, the ``file``
argument is a ``file id``. If the archive should be extracted in some other
location than the ``$GAMEDIR``, you can specify a ``dst`` argument.

You can optionally specify the archive's type with the ``format`` option.
This is useful if the archive's file extension does not match what it should
be. Accepted values for ``format`` are: zip, tgz, gzip and bz2.

Example:

::

    - extract:
        file: game-archive
        dst: $GAMEDIR/datadir/

Making a file executable
------------------------

Marking the file as executable is done with the ``chmodx`` command. It is often
needed for games that ship in a zip file, which does not retain file
permissions.

Example: ``- chmodx: $GAMEDIR/game_binary``

Executing a file
----------------

Execute files with the ``execute`` directive. Use the ``args`` parameter to add
command arguments, and ``file`` to reference a ``file id``.

Example:

::

    - execute:
         args: --argh
         file: great-id

Running a task provided by a runner
-----------------------------------

Some actions are specific to some runners, you can call them with the ``task``
command. You must at least provide the ``name`` parameter which is the function
that will be called. Other parameters depend on the task being called.

Currently, the following tasks are implemented:

* wine / winesteam: ``wineexec`` Runs a windows executable. Parameters are
  ``executable``, ``args`` (optional arguments passed to the executable),
  ``prefix`` (optional WINEPREFIX), ``working_dir`` (optional working directory).

Example:

::

    - task:
         name: wineexec
         prefix: $GAMEDIR
         executable: drive_c/Program Files/Game/Game.exe
         args: --windowed


* wine / winesteam: ``winetricks`` Runs winetricks with the ``app`` argument.
  ``prefix`` is an optional WINEPREFIX path.

Example:

::

    - task:
         name: winetricks
         prefix: $GAMEDIR
         app: nt40

* wine / winesteam: ``set_regedit`` Modifies the Windows registry. Parameters
  are ``path`` (the registry path), ``key``, ``value``, ``prefix`` (optional
  WINEPREFIX), ``working_dir`` (optional working directory).

Example:

::

    - task:
        name: set_regedit
        prefix: $GAMEDIR
        path: HKEY_CURRENT_USER\Software\Wine\AppDefaults\Sacrifice.exe
        key: Version
        value: nt40


Trying the installer locally
============================

If needed (i.e. you didn't download the installer first from the website), add
the ``runner`` and ``name`` directives. The value for ``runner`` must be the
slug name for the runner. (E.g. winesteam for Steam Windows.)
Save your script in a file and use the following command in a terminal:
``lutris -i /path/to/file``


Calling the online installer
============================

The installer can be called with the ``lutris:<game-slug>`` url scheme.
