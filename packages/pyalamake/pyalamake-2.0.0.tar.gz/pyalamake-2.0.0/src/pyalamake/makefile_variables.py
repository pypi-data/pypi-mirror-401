import os

from .path_handle import PathHandle
from .svc import svc


# --------------------
## handle Makefile variables
class MakefileVariables:
    # --------------------
    ## constructor
    def __init__(self):
        ## the current set of variables
        self._variables = {}

        home = os.path.expanduser('~')
        home = home.replace('\\', '/')
        self._variables['HOME'] = home

    # --------------------
    ## return the defined variables
    # @return the defined variables
    @property
    def variables(self):
        return self._variables

    # --------------------
    ## generator for looping through the variables
    # @return the keys/values
    def generator(self):
        return (
            (key, value)
            for key, value in self._variables.items()
        )

    # --------------------
    ## set the name and value, then return the name
    # @param name    the name of the variable
    # @param val     the value of the variable
    # @return the makefile variable $(xx)
    def set_get(self, name, val):
        self.set(name, val)
        return self.get_use(name)

    # --------------------
    ## set the name and value, then return the name
    # @param name    the name of the variable
    # @param val     the value of the variable
    # @return None
    def set(self, name, val):
        if not isinstance(val, PathHandle):
            val = PathHandle(val).fixed
        if name in self._variables and self._variables[name] != val:
            svc.log.warn(f'set: Makefile variable: {name} changed:')
            svc.log.warn(f'   was: "{self._variables[name]}"')
            svc.log.warn(f'    to: "{val}"')
        self._variables[name] = val

    # --------------------
    ## get the name to use in a makefile
    # @param name    the name of the variable
    # @return the makefile variable $(xx)
    def get_use(self, name):
        if name not in self._variables:
            svc.log.warn(f'get_use: Makefile variable: {name} not in current list')
        return f'$({name})'

    # --------------------
    ## get the value of the given variable
    # @param name  the name of the variable
    # @return the variables current value
    def get_value(self, name):
        if name not in self._variables:
            svc.log.warn(f'get_value: Makefile variable: {name} not in current list')
            return ''
        return self._variables[name]

    # --------------------
    ## (deprecated) undo changes to a path
    # @param path   the path to unfix
    # @return the unfixed path
    def unfix_path(self, path):
        for variable, val in self._variables.items():
            path = path.replace(f'$({variable})', val)
        home = os.path.expanduser('~')
        path = path.replace('$(HOME)', home)
        path = path.replace('//', '/')
        return path
