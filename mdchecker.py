#! /usr/bin/env python3

""" mdchecker.py -- Markdown Lint checker
"""

import sys
import os
from pymarkdown.main import PyMarkdownLint
from io import StringIO


def main():
    mkd = MyMarkdown()
    lst = mkd.scan_dir(os.path.join("stars", "sets"))
    #print("List:", mkd.paths())
    for mdf, path in mkd.listed():
        res = mkd.scan(path)
        print(f"{path}:")
        dump_stuff(res, path, mkd.listed())
        print()

def dump_stuff(lst, path, mkd):
    path = os.path.realpath(path)
    for idx, line in enumerate(lst, 1):
        pre = f"{mdf}:" if len(mkd) > 1 else ""
        uline = line[len(path) + 1:] if line.startswith(path + ":") else line
        print(f"{pre}err={idx}/{len(lst)}: {uline}")
    return len(lst) <= 0


class GenericDown:
    """ Generic class for handling dirs/ files. """
    candidates = (".md", ".markdown")

    def __init__(self, name):
        self.name = name
        self._paths = []
        self._list = []

    def listed(self):
        return self._list

    def paths(self):
        lst = [path for _, path in self._list]
        return lst

    def scan_dir(self, a_dir):
        self._paths.append(a_dir)
        lst = self._scan_dir(a_dir)
        self._list = lst
        return len(lst) > 0

    def _scan_dir(self, path: str):
        """ Scan dir and return markdown files. """
        results = []
        with os.scandir(path) as item:
            for entry in item:
                if not entry.is_file():
                    continue
                if entry.name.lower().endswith(GenericDown.candidates):
                    results.append((entry.name, entry.path))
        return results


class MyMarkdown(GenericDown):
    """ Wrapper around PyMarkdownLint that returns lint results as a list of lines.
    """
    def __init__(self, name="md"):
        super().__init__(name)
        self.linter = PyMarkdownLint()

    def scan(self, path: str):
        """ Run 'pymarkdown scan <path>' and return a list of output lines.
        """
        buffer = StringIO()
        old_stdout = sys.stdout
        sys.stdout = buffer
        #self.linter.main(["--log-level", "DEBUG", "scan", path])
        try:
            self.linter.main(["scan", path])
        except SystemExit:
            pass
        output = buffer.getvalue()
        sys.stdout = old_stdout
        lines = [
            line for line in output.splitlines()
        ]
        return lines


if __name__ == "__main__":
    main()
