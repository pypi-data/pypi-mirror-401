import os
import re

from .svc import svc


# --------------------
## a wrapper for paths used in a makefile
class PathHandle:
    # --------------------
    ## constructor. Load the given path and store variants of it
    # @param path  the path to handle, may be a directory or file
    def __init__(self, path):
        ## the raw path initially provided
        self._raw = path

        home = os.path.expanduser('~')
        home_pfx = home
        if svc.gbl.os_name == 'win':
            home_pfx = home_pfx.replace('\\', '/')
            home_pfx = home_pfx.replace('//', '/')

        ## the cleaned up path: all forward slashes, no home tilde, no duplicate backslashes
        self._fixed = path
        self._fixed = self._fixed.replace('~', home)
        self._fixed = self._fixed.replace('\\', '/')
        self._fixed = self._fixed.replace('//', '/')

        ## the variant to use if it is going to be embedded in another path
        self._embedded = self._fixed
        # print(f'home: {home_pfx} {self._embedded}')
        if self._embedded.startswith(home_pfx):
            # make the embedded paths more similar
            self._embedded = self._embedded.replace(home_pfx, 'os_home')
        if svc.gbl.os_name == 'win':
            # convert "stuff/c:/xx" to stuff/c/xx
            # note: if the path starts with "c:/" then it is left as is
            # make can handle c:/abc/def format as long as it is at the start of the path
            m = re.search(r'(.*)/(.):/(.*)', self._fixed)
            if m:
                drive = m.group(2).lower()
                self._embedded = f'{m.group(1)}/{drive}/{m.group(3)}'
            m = re.search(r'(.):/(.*)', self._embedded)
            if m:
                drive = m.group(1).lower()
                self._embedded = f'{drive}/{m.group(2)}'

    # --------------------
    ## return the embedded path
    # @return the embedded path
    @property
    def embedded(self):
        return self._embedded

    # --------------------
    ## return the fixed path
    # @return the fixed path
    @property
    def fixed(self):
        return self._fixed

    # --------------------
    ## return the raw path
    # @return the raw path
    @property
    def raw(self):
        return self._raw
