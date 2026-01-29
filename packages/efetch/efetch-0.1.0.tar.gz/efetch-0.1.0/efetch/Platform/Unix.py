from . import PlatformBase
import re
import os
import subprocess
import efetch.Debug

class Unix(PlatformBase.PlatformBase):
    """
    Unix platform class.
    """

    class Distro:
        class Distro:
            """
            Object to represent a Linux distribution.
            """

            name = "Unknown"
            ascii_art = "unix_placeholder"
            lsb = { "distid": "" }
            fallback = { "file": "", "check": [ "exists", "content" ], "content": "" }

    def default_ascii(self):
        """
        Return the name of the default ASCII art for this platform.

        :rtype: string
        """

        return "unix_placeholder"

    def disk_usage(self, path):
        """
        Get disk usage statistics about the given path.
        Returns a dict with items 'total', 'used' and 'free' as bytes.

        :param path: string
        :rtype: dict
        """

        st = os.statvfs(path)
        free = st.f_bavail * st.f_frsize
        total = st.f_blocks * st.f_frsize
        used = (st.f_blocks - st.f_bfree) * st.f_frsize
        return { 'total': total, 'used': used, 'free': free }

    def uptime(self):
        """
        Return the system uptime in seconds.

        :rtype: int
        """

        with open('/proc/uptime', 'r') as f:
            return float(f.readline().split()[0])

    def os_release(self):
        """
        Return a human-readable string of the OS release information.

        :rtype: dict
        """

        return { 'name': 'Unknown', 'ver': 'Unknown', 'codename': 'Unknown' }

    def cpu(self):
        """
        Get information on the system CPU.
        Returns a dict with 'name', 'load_percentage' values.

        :rtype: dict
        """

        name = "Unknown"
        load_percentage = 0.0

        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if 'model name' in line:
                    name = " ".join([s.strip() for s in line.split(":")[1].split()])
                    break

        with open('/proc/loadavg', 'r') as f:
            load_percentage = float(f.readline().split()[0])

        return { 'name': name, 'load_percentage': load_percentage }
