from .path_handle import PathHandle
from .svc import svc
from .target_base import TargetBase


# --------------------
## generate a C/C++ base functions
class TargetCCppBase(TargetBase):
    # create() is c/c++ specific

    # --------------------
    ## constructor
    #
    # @param target_name  the name of this target
    def __init__(self, target_name):
        super().__init__(target_name)

        ## the C/C++ target type
        self._target_type = 'unset'
        ## list of object files
        self._objs = ''
        ## compiler to use
        self._cxx = svc.osal.cpp_compiler()
        ## list of compile options
        self.add_compile_options('-D_GNU_SOURCE')  # pylint: disable=E1101

        ## list of build directories
        self._build_dirs = {}

    # compiler() setter/getter are c/c++ specific

    # --------------------
    ## return target type
    #
    # @return cpp target
    @property
    def target_type(self):
        return self._target_type

    # --------------------
    ## check target for any issues
    #
    # @return None
    def check(self):
        svc.log.highlight(f'{self.target}: check target...')
        self._common_check()

    # --------------------
    ## gen C++ target
    #
    # @return None
    def gen_target(self):
        svc.log.highlight(f'{self.target}: gen target, type:{self._target_type}')

        self._gen_args()
        self._gen_init()
        self._gen_app()
        self._gen_link()
        self._gen_run()

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
    ## gen initial content for C++ target
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
    ## gen app build target
    #
    # @return None
    def _gen_app(self):
        rule = f'{self.target}-build'
        self.add_rule(rule)
        tgt_deps = f'{self.target}-init '

        build_deps = ''
        for file in self.sources:  # pylint: disable=E1101
            obj, mmd_inc, dst_dir = self._get_obj_path(file)
            obj_ph = PathHandle(obj)
            mmd_inc_ph = PathHandle(mmd_inc)
            file_ph = PathHandle(file)

            # gen clean paths
            clean_path = PathHandle(dst_dir.replace(f'{svc.gbl.build_dir}/', ''))
            self.add_clean(f'{clean_path.fixed}/*.o')
            self.add_clean(f'{clean_path.fixed}/*.d')

            self._writeln(f'-include {mmd_inc_ph.fixed}')
            self._writeln(f'{obj_ph.fixed}: {file_ph.fixed}')
            self._writeln(f'\t{self._cxx} -MMD -c {self._inc_dirs} {self._compile_opts} '
                          f'{file_ph.fixed} -o {obj_ph.fixed}')
            self._objs += f'{obj_ph.fixed} '
            build_deps += f'{file_ph.fixed} '

        self._writeln('')

        self._gen_rule(rule, tgt_deps + self._objs, f'{self.target}: build source files')
        self._writeln('')

    # --------------------
    ## gen link target
    #
    # @return None
    def _gen_link(self):
        rule = f'{self.target}-link'
        self.add_rule(rule)
        tgt_deps = f'{self.target}-init '

        exe = PathHandle(f'{svc.gbl.build_dir}/{self.target}')
        self._writeln(f'{exe.fixed}: {self._objs}')
        # FYI "-Xlinker -Map=debug/x.map" to see the contents
        self._writeln(f'\t{self._cxx} {self._objs} {self._link_opts} {self._link_paths} {self._libs} '
                      f'-o {exe.fixed}')
        self._writeln('')
        ## see baseclass for definition of self.target
        self.add_clean(self.target)

        self._gen_rule(rule, tgt_deps + exe.fixed, f'{self.target}: link')
        self._writeln('')

    # --------------------
    ## gen target to run c++ target
    #
    # @return None
    def _gen_run(self):
        rule = f'{self.target}-run'
        # don't add rule

        exe = PathHandle(f'{svc.gbl.build_dir}/{self.target}')

        self._gen_empty_rule()
        self._gen_rule(rule, f'{self.target}-link', f'{self.target}: run executable')
        self._writeln(f'\t@{exe.fixed} $(filter-out $@,$(MAKECMDGOALS))')
        self._writeln('')
