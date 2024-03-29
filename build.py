import argparse
import os
import shutil
import subprocess
import sys


def run(args):
    try:
        ec = subprocess.call(' '.join(args), shell=True)
    except OSError as e:
        print("Execution failed:", e, file=sys.stderr)
        ec = 1

    if ec:
        sys.exit(ec)

parser = argparse.ArgumentParser()
parser.add_argument('--installed-qt-dir', help="the name of a directory containing pre-built Qt installations", metavar="DIR")
parser.add_argument('--no-sysroot', help="do not build the sysroot", action='store_true')
parser.add_argument('--source-dir', help="a directory containing the source packages", metavar="DIR", dest='source_dirs', action='append')
parser.add_argument('--target', help="the target platform", default='')
parser.add_argument('--quiet', help="disable progress messages", action='store_true')
parser.add_argument('--verbose', help="enable verbose progress messages", action='store_true')
cmd_line_args = parser.parse_args()
build_sysroot = not cmd_line_args.no_sysroot
installed_qt_dir = cmd_line_args.installed_qt_dir
source_dirs = cmd_line_args.source_dirs
target = cmd_line_args.target
quiet = cmd_line_args.quiet
verbose = cmd_line_args.verbose

if not target:
    print("--target must be specified")
    sys.exit(2)

if target in ('android-32', 'android-64') and not installed_qt_dir:
    print("--installed-qt-dir must be specified for", target, file=sys.stderr)
    sys.exit(2)

if not source_dirs:
    source_dirs = ['.']

if installed_qt_dir:
    source_dirs.insert(0, installed_qt_dir)

source_dirs = [os.path.abspath(s) for s in source_dirs]
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

sysroot_dir = 'sysroot-' + target
build_dir = 'build-' + target
host_bin_dir = os.path.abspath(os.path.join(sysroot_dir, 'host', 'bin'))

if build_sysroot:
    args = ['pyqtdeploy-sysroot', '--target', target, '--sysroot', sysroot_dir, "--no-clean"]

    for s in source_dirs:
        args.append('--source-dir')
        args.append(s)

    if quiet:
        args.append('--quiet')

    if verbose:
        args.append('--verbose')

    args.append('sysroot.json')

    run(args)

run(['pyqtdeploy-build', '--target', target, '--sysroot', sysroot_dir, '--build-dir', build_dir, 'dynpy.pdy'])
cp = "cp " + os.path.join(dir_path, "main.qml") + " " + os.path.join(dir_path, build_dir)
run([cp])

with open(os.path.join(dir_path, build_dir, "main.pro"), "a") as fp:
    fp.write("\ncontains(ANDROID_TARGET_ARCH, armeabi-v7a) {\nANDROID_PACKAGE_SOURCE_DIR = " + os.path.join(dir_path, "android") + "\n}")

os.chdir(build_dir)
run([os.path.join(host_bin_dir, 'qmake')])
make = 'nmake' if sys.platform == 'win32' else 'make'
run([make])
run([make, 'INSTALL_ROOT=dynpy', 'install'])
run([os.path.join(host_bin_dir, 'androiddeployqt'), '--gradle', '--input', 'android-libmain.so-deployment-settings.json', '--output', 'dynpy'])
apk_dir = os.path.join(build_dir, 'dynpy', 'build', 'outputs', 'apk', 'debug')
print("The pyqt-demo-debug.apk file can be found in the '{0}' directory.  Run adb to install it to a simulator.".format(apk_dir))
