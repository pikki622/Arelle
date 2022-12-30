"""
See COPYRIGHT.md for copyright information.

This module emits the version.py file contents which are used in the
build process to indicate the time that this version was built.

"""

import datetime
import sys

if __name__ == "__main__":
    timestamp = datetime.datetime.utcnow()
    date_dash_ymd = timestamp.strftime("%Y-%m-%d")

    # add name suffix, like ER3 or TKTABLE
    if len(sys.argv) > 1 and sys.argv[1] and sys.platform not in ("linux",):
        date_dash_ymd += f"-{sys.argv[1]}"

    if sys.platform == "darwin":
        with open("buildRenameDmg.sh", "w") as fh:
            fh.write(f"cp dist_dmg/arelle.dmg dist/arelle-macOS-{date_dash_ymd}.dmg\n")
    elif sys.platform.startswith("linux"):
        sysName = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else "linux"
        with open("buildRenameLinux-x86_64.sh", "w") as fh:
            fh.write(
                f"mv dist/exe.linux-x86_64-{sys.version_info[0]}.{sys.version_info[1]}.tgz dist/arelle-{sysName}-x86_64-{date_dash_ymd}.tgz\n"
            )
    elif sys.platform.startswith("win"):
        renameCmdFile = "buildRenamer.bat"
        with open("buildRenameX86.bat", "w") as fh:
            fh.write(
                f"rename dist\\arelle-win-x86.exe arelle-win-x86-{date_dash_ymd}.exe\n"
            )
        with open("buildRenameX64.bat", "w") as fh:
            fh.write("rename dist\\arelle-win-x64.exe arelle-win-x64-{0}.exe\n"
                     "rename dist\\arelle-win-x64.zip arelle-win-x64-{0}.zip\n"
                     .format(date_dash_ymd))
        with open("buildRenameSvr27.bat", "w") as fh:
            fh.write(
                f"rename dist\\arelle-svr-2.7.zip arelle-svr-2.7-{date_dash_ymd}.zip\n"
            )
        with open("buildRenameZip32.bat", "w") as fh:
            fh.write(f"rename dist\\arelle-cmd32.zip arelle-cmd32-{date_dash_ymd}.zip\n")
        with open("buildRenameZip64.bat", "w") as fh:
            fh.write(f"rename dist\\arelle-cmd64.zip arelle-cmd64-{date_dash_ymd}.zip\n")
