import os

from .svc import svc


# --------------------
## handle CPIP packages
class PackageCpip:
    # --------------------
    ## find the CPIP package name and return info for it
    #
    # @param pkgname  the CPIP package to search for
    # @return the package info
    def find(self, pkgname):
        pkgname = pkgname.replace('cpip.', '')
        svc.log.line(f'finding cpip package: {pkgname}')

        if not svc.osal.isdir(os.path.join('tools', 'xplat_utils')):  # pragma: no cover ; defence only
            svc.abort('xplat_utils is not installed, aborting')

        from tools.xplat_utils import main
        pkginfo = main.svc.utils.cpip_get(pkgname)
        if pkginfo is None:
            svc.abort(f'could not find info for cpip package: {pkgname}')

        pkginfo.include_dir = pkginfo.include_dir.replace('\\', '/')
        pkginfo.include_dir = pkginfo.include_dir.replace('//', '/')
        for posn, src_path in enumerate(pkginfo.src):
            src_path = src_path.replace('\\', '/')
            src_path = src_path.replace('//', '/')
            pkginfo.src[posn] = src_path
        return pkginfo
