# copyright ############################### #
# This file is part of the Xboinc Package.  #
# Copyright (c) CERN, 2025.                 #
# ######################################### #

from pathlib import Path

_pkg_root = Path(__file__).parent.absolute()


# ==============================================================================
# Do not change
# ==============================================================================

__version__ = '0.6.0'

# These are the xsuite modules that are used by boinc and the versions they are
# tied to. This will be automatically updated from the active environment when
# making a minor release. If a new package needs to be pinned, add it here with
# a random version number, and similarily in the pyproject.toml
__xsuite__versions__ = {
    'xobjects' : '0.5.12',
    'xdeps'    : '0.10.10',
    'xpart'    : '0.23.7',
    'xtrack'   : '0.98.12',
    'xfields'  : '0.25.8',
    'xcoll'    : '0.9.1',
}
# ==============================================================================
