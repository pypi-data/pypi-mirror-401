import glob

from .path_handle import PathHandle
from .svc import svc
from .target_base import TargetBase


# --------------------
## target for an Arduino Core
class TargetArduinoCore(TargetBase):
    # --------------------
    ## create an Arduino Core target
    #
    # @param targets      current list of targets
    # @param target_name  name of the new target
    # @param shared       the shared core info
    @classmethod
    def create(cls, targets, target_name, shared=None):
        impl = TargetArduinoCore(target_name, shared)
        targets.append(impl)
        return impl

    # --------------------
    ## constructor
    #
    # @param target_name  name of the new target
    # @param shared       the shared core info
    def __init__(self, target_name, shared):
        super().__init__(target_name)

        ## shared info
        self._shared = shared
        ## shared core target
        self._shared.core_tgt = target_name
        ## shared core directory
        self._shared.coredir = f'{svc.gbl.build_dir}/{self._shared.core_tgt}-dir'
        ## shared core library name
        self._shared.corelib_name = f'{self._shared.core_tgt}.a'
        ## shared core library path
        self._shared.corelib = f'{svc.gbl.build_dir}/{self._shared.corelib_name}'

        ## compile options to use
        self.add_compile_options(self._shared.debug_compile_opts)  # pylint: disable=E1101

        ## build directories to use
        self._build_dirs = {}

        ## core source directory to use
        self._core_src_dir = None
        ## list of object files to use
        self._objs = []
        ## list of include directories
        self._inc_dirs = []

    # --------------------
    ## the arduino core type
    # @return target type
    @property
    def target_type(self):
        return 'arduino_core'

    # --------------------
    ## check for various conditions in this target
    #
    # @return None
    def check(self):
        svc.log.highlight(f'{self.target}: check target...')
        self._common_check()

        errs = 0
        self._shared.check()
        if errs > 0:
            svc.abort(f'{self.target} target_arduino_core: resolve errors')

    # --------------------
    ## generate this target
    #
    # @return None
    def gen_target(self):
        svc.log.highlight(f'gen target {self.target}, type:{self.target_type}')

        self._gen_args()
        self._gen_init()

        self.add_clean(self._shared.corelib_name)

        self._core_src_dir = PathHandle(svc.osal.arduino_core_src_dir())

        self._inc_dirs = ''
        for inc_dir in self._shared.core_includes:
            if isinstance(inc_dir, PathHandle):
                inc_dir = inc_dir.fixed
            self._inc_dirs += f' "-I{inc_dir}" '

        self._gen_core_compile()
        self._gen_core_link()
        self._writeln('')

    # --------------------
    ## generate argues for the build directory
    #
    # @return None
    def _gen_args(self):
        # create output build directory
        self._build_dirs[svc.gbl.build_dir] = 1
        self._build_dirs[self._shared.coredir] = 1

        self._writeln('')

    # --------------------
    ## generate init rule
    #
    # @return None
    def _gen_init(self):
        rule = f'{self.target}-init'
        self.add_rule(rule)

        self._gen_rule(rule, '', f'{self.target}: initialize for {svc.gbl.build_dir} build')
        for bld_dir in self._build_dirs:
            bld_dir = PathHandle(bld_dir)
            self._writeln(f'\t@mkdir -p {bld_dir.fixed}')
        self._writeln('')

    # --------------------
    ## generate core compilation rule
    #
    # @return None
    def _gen_core_compile(self):
        rule = f'{self.target}-build'
        self.add_rule(rule)
        tgt_deps = f'{self.target}-init '

        cpp_files = self._gen_core_cpp_compile()
        c_files = self._gen_core_c_compile()

        # add clean rules; the clean function automatically adds the build_dir
        self.add_clean(f'{self._shared.core_tgt}-dir/*.o')
        self.add_clean(f'{self._shared.core_tgt}-dir/*.d')

        obj_deps = ''
        for (_, _, obj) in sorted(cpp_files + c_files, key=lambda x: x[2].fixed):
            obj_deps += f' {obj.fixed}'

        self._gen_rule(rule, tgt_deps + obj_deps, f'{self.target}: compile arduino core source files')
        self._writeln('')
        #
        # src_deps = ''
        # for (short_src, _, _) in sorted(cpp_files + c_files, key=lambda x: x[0].fixed):
        #     src_deps += f' {short_src.fixed}'
        #
        # self._gen_rule(rule, src_deps, f'{self.target}: compile arduino core source files')
        # self._writeln('')

    # --------------------
    ## generate list of source files for C++ compilation
    #
    # @return list of source files
    def _gen_core_cpp_compile(self):
        src_files = self._gather_src_files('*.cpp')
        self.gen_core_src_compiles(src_files, self._shared.cpp, self._shared.cpp_opts)
        return src_files

    # --------------------
    ## generate list of source files for C compilation
    #
    # @return list of source files
    def _gen_core_c_compile(self):
        src_files = self._gather_src_files('*.c')
        self.gen_core_src_compiles(src_files, self._shared.cc, self._shared.cc_opts)
        return src_files

    # --------------------
    ## gather the core source files with the given pattern
    # @param core_src_pattern   the pattern to use e.g. "*.c"
    # return the source files as PathHandles
    def _gather_src_files(self, core_src_pattern):
        svc.gbl.mf_variables.set('PAM_ARD_CORE_SRC', self._core_src_dir.fixed)
        src_files = []
        for src in glob.glob(f'{self._core_src_dir.fixed}/{core_src_pattern}', recursive=True):
            src_ph = PathHandle(src)
            obj = PathHandle(src_ph.fixed.replace(self._core_src_dir.fixed, self._shared.coredir) + '.o')
            mmd_inc = PathHandle(src_ph.fixed.replace(self._core_src_dir.fixed, self._shared.coredir) + '.d')
            src_files.append((src_ph, mmd_inc, obj))
        return src_files

    # --------------------
    ## generate the makefile lines to compile core source files
    # @param src_files      a triplet of source files to generate for
    # @param compiler       the compiler to use
    # @param compiler_opts  additional compiler options to use
    def gen_core_src_compiles(self, src_files, compiler, compiler_opts):
        for short_src, mmd_inc, obj in sorted(src_files, key=lambda x: x[0].fixed):
            self._writeln(f'-include {mmd_inc.fixed}')
            self._writeln(f'{obj.fixed}: {short_src.fixed}')
            self._writeln(f'\t{compiler} {compiler_opts} '
                          f'{self._inc_dirs} {self._compile_opts} '
                          f'{short_src.fixed} -o {obj.fixed}')
            self._objs.append(obj)

        self._writeln('')

    # --------------------
    ## generate link rule
    #
    # @return None
    def _gen_core_link(self):
        rule = f'{self.target}-link'
        self.add_rule(rule)
        tgt_deps = f'{self.target}-init '

        self._gen_rule(rule, tgt_deps + self._shared.corelib, f'{self.target}: create arduino core library')
        self._writeln('')

        obj_deps = ''
        for obj in self._objs:
            obj_deps += f' {obj.fixed}'
        self._writeln(f'{self._shared.corelib}: {obj_deps}')
        self._writeln(f'\trm -f {self._shared.corelib}')
        for obj in sorted(self._objs, key=lambda x: x.fixed):
            self._writeln(f'\t{self._shared.ar} rcs {self._shared.corelib} {obj.fixed}')
