from .path_handle import PathHandle
from .svc import svc
from .target_base import TargetBase


# --------------------
## target for an Arduino app
class TargetArduino(TargetBase):
    # --------------------
    ## create an Arduino target
    #
    # @param targets      current list of targets
    # @param target_name  name of the new target
    # @param shared       info for shared core
    @classmethod
    def create(cls, targets, target_name, shared=None):
        impl = TargetArduino(target_name, shared)
        targets.append(impl)
        return impl

    # --------------------
    ## constructor
    #
    # @param target_name  name of the new target
    # @param shared       info for shared core
    def __init__(self, target_name, shared):
        super().__init__(target_name)

        if shared is None:
            svc.abort('Arduino Targets must have a shared Arduino Core component passed in')

        ## shared Arduino Core info
        self._shared = shared

        ## compile options
        self.add_compile_options(self._shared.debug_compile_opts)  # pylint: disable=E1101

        ## build directories
        self._build_dirs = {}

        # these need to be set below
        ## target build directory
        self.tgt_build_dir = None
        ## ELF file generated for this app
        self._elffile = None
        ## EEP file generated for this app
        self._eepfile = None
        ## HEX file generated for this app
        self._hexfile = None
        ## list of target dependencies for this app
        self._app_deps = None

    # --------------------
    ## type of this target
    # @return arduino target
    @property
    def target_type(self):
        return 'arduino'

    # --------------------
    ## update include directories params string
    #
    # @return None
    def _update_inc_dirs(self):
        super()._update_inc_dirs()
        for inc_dir in self._shared.core_includes:
            if isinstance(inc_dir, PathHandle):
                inc_dir = inc_dir.fixed
            self._inc_dirs += f' "-I{inc_dir}" '

    # --------------------
    ## add an arduino library to list of libraries.
    # these libraries are recognized:
    #  * Servo
    #
    # @param lib  the library to add
    # @return None
    def add_library(self, lib):
        if lib == 'Servo':
            svc.log.line(f'adding arduino library: {lib}')
            path = PathHandle(f'{self._shared.library_root}/Servo/src')
            self.add_sources(f'{path.fixed}/avr/Servo.cpp')  # pylint: disable=E1101
            self.add_include_directories(path.fixed)  # pylint: disable=E1101
            self.add_compile_options('-DARDUINO_ARCH_AVR')  # pylint: disable=E1101
        else:
            svc.abort(f'{self.target} target_arduino: unknown arduino library: {lib}')

    # --------------------
    ## check various aspects of parameters
    #
    # @return None
    def check(self):
        svc.log.highlight(f'{self.target}: check target...')
        self._common_check()

        errs = 0
        self._shared.check()
        if errs > 0:
            svc.abort(f'{self.target} target_arduino: resolve errors')

    # --------------------
    ## generate Arduino target
    #
    # @return None
    def gen_target(self):
        self.tgt_build_dir = f'{svc.gbl.build_dir}/{self.target}-dir'

        svc.log.highlight(f'{self.target}: gen target, type:{self.target_type}')
        svc.log.line(f'   boardid  : {self._shared.boardid}')
        svc.log.line(f'   port     : {self._shared.avrdude_port}')
        svc.log.line(f'   baud_rate: {self._shared.avrdude_baudrate}')
        svc.log.line(f'   mcu      : {self._shared.mcu}')
        svc.log.line(f'   tgt dir  : {self.tgt_build_dir}')
        svc.log.line(f'   corelib  : {self._shared.corelib}')
        svc.log.line(f'   coredir  : {self._shared.coredir}')

        self._elffile = f'{svc.gbl.build_dir}/{self.target}.elf'
        self.add_clean(f'{self.target}.elf')

        self._eepfile = f'{svc.gbl.build_dir}/{self.target}.eep'
        self.add_clean(f'{self.target}.eep')

        self._hexfile = f'{svc.gbl.build_dir}/{self.target}.hex'
        self.add_clean(f'{self.target}.hex')

        self._gen_args()
        self._gen_init()
        self._gen_app()
        self._gen_link()
        self._gen_upload()

    # --------------------
    ## generate arguments for build
    def _gen_args(self):
        # create output build directory
        self._build_dirs[svc.gbl.build_dir] = 1

        for file in self.sources:  # pylint: disable=E1101
            _, _, dst_dir = self._get_obj_path(file)
            self._build_dirs[dst_dir] = 1

        self._writeln('')

    # --------------------
    ## generate initialization rule
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
    ## generate build rule
    #
    # @return None
    def _gen_app(self):
        rule = f'{self.target}-build'
        self.add_rule(rule)

        # assumes _app_deps is only used in writeln()
        self._app_deps = ''
        build_deps = ''
        for file in self.sources:  # pylint: disable=E1101
            obj, mmd_inc, dst_dir = self._get_obj_path(file)
            file_ph = PathHandle(file)
            obj_ph = PathHandle(obj)

            # gen clean paths
            clean_path = PathHandle(dst_dir.replace(f'{svc.gbl.build_dir}/', ''))
            self.add_clean(f'{clean_path.fixed}/*.o')
            self.add_clean(f'{clean_path.fixed}/*.d')

            self._writeln(f'-include {PathHandle(mmd_inc).fixed}')
            self._writeln(f'{obj_ph.fixed}: {file_ph.fixed}')
            self._writeln(f'\t{self._shared.cpp} {self._shared.cpp_opts} '
                          f'{self._compile_opts} {self._inc_dirs} '
                          f'{file_ph.fixed} -o {obj_ph.fixed}')
            self._app_deps += f'{obj_ph.fixed} '
            build_deps += f'{file_ph.fixed} '

        self._writeln('')

        self._gen_rule(rule, build_deps, f'{self.target}: build sketch')
        self._writeln('')

    # --------------------
    ## generate link rule
    #
    # @return None
    def _gen_link(self):
        rule = f'{self.target}-link'
        self.add_rule(rule)
        tgt_deps = f'{self.target}-init {self._shared.core_tgt} {self._hexfile}'

        self._gen_rule(rule, tgt_deps, f'{self.target}: link sketch and core')
        self._writeln('')

        elffile_ph = PathHandle(self._elffile)
        eepfile_ph = PathHandle(self._eepfile)
        hexfile_ph = PathHandle(self._hexfile)
        corelib_ph = PathHandle(self._shared.corelib)

        # creates the ELF
        self._writeln(f'{elffile_ph.fixed}: {self._app_deps} {corelib_ph.fixed}')
        self._writeln(f'\t{self._shared.cc} -Os -Wl,--gc-sections -mmcu={self._shared.mcu} '
                      f'-o {elffile_ph.fixed} '
                      f'{self._app_deps} '
                      f'{corelib_ph.fixed} -lm')
        self._writeln('')

        # creates the EEP
        self._writeln(f'{eepfile_ph.fixed}: {elffile_ph.fixed}')
        self._writeln(f'\t{self._shared.obj_copy} -O ihex -j .eeprom --set-section-flags=.eeprom=alloc,load '
                      f'--no-change-warnings --change-section-lma .eeprom=0 '
                      f'{elffile_ph.fixed} {eepfile_ph.fixed}')
        self._writeln('')

        # creates the HEX
        self._writeln(f'{hexfile_ph.fixed}: '
                      f'{elffile_ph.fixed} {eepfile_ph.fixed}')
        self._writeln(f'\t{self._shared.obj_copy} -O ihex -R .eeprom '
                      f'{elffile_ph.fixed} {hexfile_ph.fixed}')
        self._writeln('')

    # --------------------
    ## generate upload rule
    #
    # @return None
    def _gen_upload(self):
        rule = f'{self.target}-upload'
        # don't add rule
        tgt_deps = f'{self.target}-init {self.target}-link'

        avrdude_conf_dir = svc.gbl.mf_variables.set_get('PAM_AVRDUDE_CONF_DIR',
                                                        PathHandle(svc.osal.avrdude_conf_dir()).fixed)
        avrdude_conf = PathHandle(f'{avrdude_conf_dir}/avrdude.conf')

        avrdude_protocol = self._shared.avrdude_protocol
        avrdude_args = f'-C{avrdude_conf.fixed} -p{self._shared.mcu} -c{avrdude_protocol} ' \
                       f'-P{self._shared.avrdude_port} -b{self._shared.avrdude_baudrate}'

        self._gen_rule(rule, tgt_deps, f'{self.target}: upload to arduino')
        avrdude_path = f'{PathHandle(self._shared.avrdude_dir).fixed}/{PathHandle(self._shared.avrdude).embedded}'
        self._writeln(f'\t{avrdude_path} -v {avrdude_args} -D '
                      f'-Uflash:w:{PathHandle(self._hexfile).fixed}:i '
                      f'-Ueeprom:w:{PathHandle(self._eepfile).fixed}:i')
        self._writeln('')
