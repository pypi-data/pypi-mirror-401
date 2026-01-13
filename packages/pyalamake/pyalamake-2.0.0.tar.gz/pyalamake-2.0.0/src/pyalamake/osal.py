import os
import re
import subprocess

from .svc import svc


# --------------------
## Operating System Abstraction Layer; provides functions to make cross-platform behavior similar
class Osal:
    # --------------------
    ## check if a path to a file exists
    # note: use this function instead of os.path.isfile otherwise it may fail on windows/msys2
    #
    # @param path   the path to fix
    # @return the fixed path
    @classmethod
    def isfile(cls, path):
        path = cls._unfix_path(path)
        return os.path.isfile(path)

    # --------------------
    ## check if a path exists
    # note: use this function instead of os.path.isdir otherwise it may fail on windows/msys2
    #
    # @param path   the path to fix
    # @return the fixed path
    @classmethod
    def isdir(cls, path):
        path = cls._unfix_path(path)
        return os.path.isdir(path)

    # --------------------
    ## (deprecated) unfix a path
    # @param path the path to unfix
    # @return the unfixed path
    @classmethod
    def _unfix_path(cls, path):
        path = os.path.expanduser(path)
        path = svc.gbl.mf_variables.unfix_path(path)
        if svc.gbl.os_name == 'win':
            # assumes there is only one character and it is for a drive letter
            # can only be done at the start of the path
            m = re.search(r'^/(.)/(.*)', path)
            if m:
                drive = m.group(1).lower()
                path = f'{drive}:/{m.group(2)}'
        path = path.replace('\\', '/')
        path = path.replace('//', '/')
        return path

    # --------------------
    ## get the homebrew link libraries root directory
    #
    # @return the homebrew link lib root dir
    @classmethod
    def homebrew_link_dirs(cls):
        return []  # TODO del; '/opt/homebrew/lib'

    # --------------------
    ## get the homebrew includes root directory
    #
    # @return the homebrew includes dir
    @classmethod
    def homebrew_inc_dirs(cls):
        return [
            # TODO del;
            # '/opt/homebrew/opt/llvm/include',
            # '/opt/homebrew/opt/gcc/include/c++/15',
            # '/opt/homebrew/Cellar/gcc/15.1.0',
            # '/opt/homebrew/include',
        ]

    # --------------------
    ## get C++ compiler per OS
    # @return C++ compiler
    @classmethod
    def cpp_compiler(cls):
        if svc.gbl.os_name == 'macos':
            comp = 'g++-15'
        else:
            comp = 'g++'
        return svc.gbl.mf_variables.set_get('PAM_GPP', comp)

    # --------------------
    ## get C compiler per OS
    # @return C compiler
    @classmethod
    def c_compiler(cls):
        if svc.gbl.os_name == 'macos':
            comp = 'gcc-15'
        else:
            comp = 'gcc'
        return svc.gbl.mf_variables.set_get('PAM_GCC', comp)

    # --------------------
    ## get the root of the arduino cores, tools, etc.
    #
    # @return the root arduino directory
    @classmethod
    def arduino_root_dir(cls):
        if svc.gbl.os_name == 'macos':
            path = os.path.expanduser('~/Library/Arduino15')
        elif svc.gbl.os_name == 'win':
            path = os.path.expanduser('~/AppData/Local/Arduino15')
            path = path.replace('\\', '/')
        else:  # ubuntu
            path = os.path.expanduser('~/.arduino15')
        # do not fix_path()
        return path

    # --------------------
    ## get the root of the arduino libraries
    #
    # @return the root arduino library directory
    @classmethod
    def arduino_library_dir(cls):
        if svc.gbl.os_name == 'macos':
            path = os.path.expanduser('~/Library/Arduino15/libraries')
        elif svc.gbl.os_name == 'win':
            path = os.path.expanduser('~/AppData/Local/Arduino15/libraries')
            path = path.replace('\\', '/')
        else:  # ubuntu
            path = os.path.expanduser('~/Arduino/libraries')
        # do not fix_path()
        return path

    # --------------------
    ## get the library directory for arduino core source files
    #
    # @return the arduino core's root source directory
    @classmethod
    def arduino_core_src_dir(cls):
        path = f'{cls.arduino_root_dir()}/packages/arduino/hardware/avr/1.8.6/cores/arduino'
        # do not fix_path()
        return path

    # --------------------
    ## get the list of included directories for arduino core
    #
    # @return the list of include directories
    @classmethod
    def arduino_core_includes(cls):
        incs = [
            f'{cls.arduino_root_dir()}/packages/arduino/hardware/avr/1.8.6/cores/arduino',
            f'{cls.arduino_root_dir()}/packages/arduino/hardware/avr/1.8.6/variants/standard',
        ]
        # do not fix_path()
        return incs

    # --------------------
    ## get the directory for all tools (except avrdude)
    #
    # @return the tools directory
    @classmethod
    def arduino_tools_dir(cls):
        path = f'{cls.arduino_root_dir()}/packages/arduino/tools/avr-gcc/7.3.0-atmel3.6.1-arduino7/bin'
        return path

    # --------------------
    ## get the directory for avrdude.conf
    #
    # @return the avrdude directory
    @classmethod
    def avrdude_dir(cls):
        path = f'{cls.arduino_root_dir()}/packages/arduino/tools/avrdude/6.3.0-arduino17/bin'
        # do not fix_path()
        return path

    # --------------------
    ## get the directory for avrdude.conf
    #
    # @return the avrdude directory
    @classmethod
    def avrdude_conf_dir(cls):
        path = f'{cls.arduino_root_dir()}/packages/arduino/tools/avrdude/6.3.0-arduino17/etc'
        # do not fix_path()
        return path

    # --------------------
    ## return default gtest include directories
    #
    # @return the list of include directories
    @classmethod
    def gtest_includes(cls):
        incs = []
        if svc.gbl.os_name == 'win':
            incs.append('c:/msys64/mingw64/include')
        elif svc.gbl.os_name == 'macos':
            incs.append('/opt/homebrew/Cellar/googletest/1.17.0/include')

        # do not fix_path()
        return incs

    # --------------------
    ## return default gtest link directories
    #
    # @return the list of link directories
    @classmethod
    def gtest_link_dirs(cls):
        dirs = []
        if svc.gbl.os_name == 'win':
            dirs.append('c:/msys64/mingw64/lib')
        elif svc.gbl.os_name == 'macos':
            dirs.append('/opt/homebrew/Cellar/googletest/1.17.0/lib')
        # do not fix_path()
        return dirs

    # --------------------
    ## return default ruby include directories
    #
    # @return the list of include directories
    @classmethod
    def ruby_includes(cls):
        incs = [
            cls._get_ruby_inc1(),
            cls._get_ruby_inc2()
        ]

        # do not fix_path()
        return incs

    # --------------------
    ## get include directory1 using ruby utility
    #
    # @return path
    @classmethod
    def _get_ruby_inc1(cls):
        cmd = ['ruby', '-rrbconfig', '-e', 'puts RbConfig::CONFIG["rubyhdrdir"]']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, shell=False)
        lines = result.stdout.strip().splitlines()
        if lines:
            inc1 = lines[0].strip()
        else:
            if svc.gbl.os_name == 'macos':
                inc1 = '/opt/homebrew/Cellar/ruby/3.3.5/include/ruby-3.3.0'
            elif svc.gbl.os_name == 'ubuntu':
                inc1 = '/usr/include/ruby-3.2.0'
            else:
                # TODO del; check if these work in msys2
                #  C:/Ruby33-x64/include/ruby-3.3.0
                inc1 = 'unknown_inc1'
        return inc1

    # --------------------
    ## get include directory2 using ruby utility for ubuntu
    #
    # @return path
    @classmethod
    def _get_ruby_inc2(cls):
        cmd = ['ruby', '-rrbconfig', '-e', 'puts RbConfig::CONFIG["rubyarchhdrdir"]']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, shell=False)
        lines = result.stdout.strip().splitlines()
        if lines:
            inc2 = lines[0].strip()
        else:
            if svc.gbl.os_name == 'macos':
                inc2 = '/opt/homebrew/Cellar/ruby/3.3.5/include/ruby-3.3.0'
            elif svc.gbl.os_name == 'ubuntu':
                inc2 = '/usr/include/x86_64-linux-gnu/ruby-3.2.0'
            else:
                inc2 = 'C:/ruby/include/ruby-3.3.0/x64-mingw-ucrt'
        return inc2

    # --------------------
    ## return default ruby link directories
    #
    # @return the list of link directories
    @classmethod
    def ruby_link_dirs(cls):
        dirs = [cls._get_ruby_lib()]

        # do not fix_path()
        return dirs

    # --------------------
    ## get link library using ruby utility
    #
    # @return link library
    @classmethod
    def _get_ruby_lib(cls):
        cmd = ['ruby', '-rrbconfig', '-e', 'puts RbConfig::CONFIG["libdir"]']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, shell=False)
        lines = result.stdout.strip().splitlines()
        if lines:
            lib = lines[0].strip()
        elif svc.gbl.os_name == 'macos':
            lib = '/opt/homebrew/Cellar/ruby/3.3.5/lib'
        elif svc.gbl.os_name == 'win':
            lib = 'C:/ruby/lib'
        else:  # ubuntu
            lib = '/usr/lib'

        return lib

    # --------------------
    ## return default link libraries needed for ruby
    #
    # @return the list of link libraries
    @classmethod
    def ruby_link_libs(cls):
        libs = []
        if svc.gbl.os_name == 'win':
            libs.append('x64-ucrt-ruby330.dll')
        # do not fix_path()
        return libs

    # --------------------
    ## return default python include directories
    #
    # @return the list of include directories
    @classmethod
    def python_includes(cls):
        import sysconfig
        incs = [sysconfig.get_path('include')]
        # do not fix_path()
        return incs

    # --------------------
    ## return default link libraries needed for ruby
    #
    # @return the list of link libraries
    @classmethod
    def python_link_libs(cls):
        import sysconfig
        if svc.gbl.os_name == 'win':
            libs = [sysconfig.get_config_var('installed_base'), 'c:/msys64/mingw64/lib']
        else:
            libs = [sysconfig.get_config_var('LIBDIR')]
        # print(f"platlibdir    : {sysconfig.get_config_var('platlibdir')}")
        # print(f"installed_base: {sysconfig.get_config_var('installed_base')}")
        # print(f"platbase      : {sysconfig.get_config_var('platbase')}")
        # libs = [sysconfig.get_config_var('prefix')]

        # do not fix_path()
        return libs
