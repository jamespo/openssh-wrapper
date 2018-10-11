from __future__ import print_function
from backports import tempfile
from openssh_wrapper import SSHConnection
import getpass
import os.path


class TestSSHCommandNames(object):

    def setup_method(self, meth):
        self.user = getpass.getuser()
        self.srcdir = tempfile.TemporaryDirectory()
        self.destdir = tempfile.TemporaryDirectory()

    def test_scpget(self):
        conn = SSHConnection('localhost', login=self.user)
        srcfile = os.path.join(self.srcdir.name, 'a')
        destfile = os.path.join(self.destdir.name, 'a')
        text = 'some text'
        self._writefile(text, srcfile)
        conn.scpget(srcfile, self.destdir.name)
        assert self._readfile(destfile) == text

    @staticmethod
    def _readfile(path):
        with open(path) as f:
            contents = f.read()
        return contents

    @staticmethod
    def _writefile(text, path):
        with open(path, 'w') as f:
            print(text, file=f, end='')

    def teardown_method(self, method):
        for tempd in self.srcdir, self.destdir:
            tempd.cleanup()
