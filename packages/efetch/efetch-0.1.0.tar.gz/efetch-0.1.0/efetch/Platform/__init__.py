import re
import sys
import efetch.Debug

def guess_platform(platform=False, flag=None):
    """\
    Try to find the Platform of the system that this script is currently
    running on. On failure, print a message to stderr and call sys.exit().
    """

    if not platform:
        platform = __import__('platform').system()

    if platform == "Windows":
        efetch.Debug.debug("Windows found.")
        import efetch.Platform.Windows as Windows
        return Windows.Windows
    elif platform == "Linux":
        efetch.Debug.debug("Linux found.")
        import efetch.Platform.Linux as Linux
        return Linux.Linux
    elif platform == "Darwin":
        import efetch.Platform.Darwin as Darwin
        import efetch.Platform.MacOSX as MacOSX

        if flag == "Darwin":
            efetch.Debug.debug("Force flag has been set to Darwin, so returning the Darwin class")
            return Darwin.Darwin

        efetch.Debug.debug("Darwin found, checking for Mac OS X...")
        osx = False

        try:
            with open('/System/Library/CoreServices/SystemVersion.plist', 'r') as f:
                for line in f:
                    if re.search('Mac OS X', line):
                        osx = True
                        efetch.Debug.debug("Found Mac OS X.")
                        break
        except:
            tt = "assuming Darwin" if osx == False else "but OS X flag already set, so going with that"
            efetch.Debug.debug("Exception occurred checking for Mac OS X, %s" % tt)
            pass

        if osx or flag == "MacOSX":
            return MacOSX.MacOSX
        else:
            return Darwin.Darwin
    else:
        efetch.Debug.debug("Could not find platform, platform.system() is %s" % platform)

        text = """Unfortunately, your system is not currently supported.
        If you would like to help add support for your system, please
        file an issue at https://github.com/bn0x/efetch/issues/."""
        efetch.Debug.debug(text, force=True)
        sys.exit(1)
