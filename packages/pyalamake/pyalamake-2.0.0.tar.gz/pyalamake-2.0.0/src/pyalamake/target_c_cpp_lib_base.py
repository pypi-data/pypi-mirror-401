from .path_handle import PathHandle
from .svc import svc
from .target_base import TargetBase


# --------------------
## generate a C++ Library target, static (default) or shared
# see https://renenyffenegger.ch/notes/development/languages/C-C-plus-plus/GCC/create-libraries/index
class TargetCCppLibBase(TargetBase):
    # create() is c/c++ specific

    # --------------------
    ## constructor
    #
    # @param target_name  the name of this target
    def __init__(self, target_name):
        super().__init__(target_name)

        ## the C/C++ lib target type
        self._target_type = 'unset'
        ## list of object files
        self._objs = ''
        ## compiler to use
        self._cxx = 'unset'
        ## list of compile options
        self.add_compile_options('-D_GNU_SOURCE')  # pylint: disable=E1101

        ## list of build directories
        self._build_dirs = {}

        ## library type: static, shared
        self._lib_type = 'static'

    # compiler() getter/setter are c/c++ specific

    # --------------------
    ## return target type
    #
    # @return cpp target
    @property
    def target_type(self):
        return self._target_type

    # --------------------
    ## set the library type to generate
    #
    # @param val  the type to set: static or shared
    def set_type(self, val):
        valid_types = ['static', 'shared', 'bundle']
        if val not in valid_types:
            svc.abort(f'invalid library type, expected {valid_types}, actual: {val}')
        self._lib_type = val

    # --------------------
    ## return library type
    @property
    def lib_type(self):
        return self._lib_type

    # --------------------
    ## check target for any issues
    #
    # @return None
    def check(self):
        svc.log.highlight(f'{self.target}: check target...')
        self._common_check()

    # --------------------
    ## gen C++ library target
    #
    # @return None
    def gen_target(self):
        svc.log.highlight(f'{self.target}: gen target, type:{self._target_type}')

        self._gen_args()
        self._gen_init()
        self._gen_lib()
        if self._lib_type in ['shared', 'bundle']:
            self._gen_shared_library()
        else:
            self._gen_static_library()

    # --------------------
    ## create output directory
    #
    # @return None
    def _gen_args(self):
        # create output build directory
        self._build_dirs[svc.gbl.build_dir] = 1

        for file in self.sources:  # pylint: disable=E1101
            _, _, dst_dir = self._get_obj_path(file)
            self._build_dirs[dst_dir] = 1

        self._writeln('')

    # --------------------
    ## gen initial content for C++ library
    #
    # @return None
    def _gen_init(self):
        rule = f'{self.target}-init'
        self.add_rule(rule)

        self._gen_rule(rule, '', f'{self.target}: initialize for {svc.gbl.build_dir} build')
        for bld_dir in self._build_dirs:
            self._writeln(f'\t@mkdir -p {PathHandle(bld_dir).fixed}')
        self._writeln('')

    # --------------------
    ## gen lib build target
    #
    # @return None
    def _gen_lib(self):
        rule = f'{self.target}-build'
        self.add_rule(rule)
        tgt_deps = f'{self.target}-init '

        build_deps = ''
        for src_file in self.sources:  # pylint: disable=E1101
            obj, mmd_inc, dst_dir = self._get_obj_path(src_file)
            obj_ph = PathHandle(obj)
            mmd_inc_ph = PathHandle(mmd_inc)
            src_file_ph = PathHandle(src_file)

            # gen clean paths
            clean_path = PathHandle(dst_dir.replace(f'{svc.gbl.build_dir}/', ''))
            self.add_clean(f'{clean_path.fixed}/*.o')
            self.add_clean(f'{clean_path.fixed}/*.d')

            self._writeln(f'-include {mmd_inc_ph.fixed}')
            self._writeln(f'{obj_ph.fixed}: {src_file_ph.fixed}')
            if self._lib_type == 'shared' and svc.gbl.os_name != 'win':
                fpic = '-fPIC '
            else:
                fpic = ''
            self._writeln(f'\t{self._cxx} -MMD {fpic} -c {self._inc_dirs} {self._compile_opts} '
                          f'{src_file_ph.fixed} -o {obj_ph.fixed}')
            self._objs += f'{obj_ph.fixed} '
            build_deps += f'{src_file_ph.fixed} '

        self._writeln('')

        self._gen_rule(rule, tgt_deps + self._objs, f'{self.target}: build source files')
        self._writeln('')

    # --------------------
    ## gen shared library
    #
    # @return None
    def _gen_shared_library(self):
        rule = f'{self.target}-shared'
        self.add_rule(rule)
        tgt_deps = f'{self.target}-init '

        if svc.gbl.os_name == 'win':  # pragma: no cover ; used only on windows
            extension = 'dll'
            fpic = ''
        elif svc.gbl.os_name == 'macos':
            fpic = ''
            if self._lib_type == 'bundle':
                extension = 'bundle'
            else:
                extension = 'so'
        else:
            fpic = '-fPIC '
            extension = 'so'
        lib_name = f'lib{self.target}.{extension}'
        lib = PathHandle(f'{svc.gbl.build_dir}/{lib_name}')
        self._writeln(f'{lib.fixed}: {self._objs}')
        self._writeln(f'\t{self._cxx} -MMD -{self._lib_type} {self._link_opts} {fpic} {self._objs} {self._link_paths} '
                      f'{self._libs} '
                      f'-o {lib.fixed}')
        self._writeln('')
        ## see baseclass for definition of self.target
        self.add_clean(lib_name)

        self._gen_rule(rule, tgt_deps + lib.fixed, f'{self.target}: link')
        self._writeln('')

    # --------------------
    ## gen static library
    #
    # @return None
    def _gen_static_library(self):
        rule = f'{self.target}-static'
        self.add_rule(rule)
        tgt_deps = f'{self.target}-init '

        lib_name = f'lib{self.target}.a'
        lib = PathHandle(f'{svc.gbl.build_dir}/{lib_name}')
        self._writeln(f'{lib.fixed}: {self._objs}')
        self._writeln(f'\tar rcs {lib.fixed} {self._objs} {self._link_opts} {self._link_paths} {self._libs}')
        self._writeln('')
        ## see baseclass for definition of self.target
        self.add_clean(lib_name)

        self._gen_rule(rule, tgt_deps + lib.fixed, f'{self.target}: link')
        self._writeln('')
