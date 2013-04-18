"""
Provide the Reporter class.
"""

import sys

if sys.version_info < (3,):
    _fsencoding = sys.getfilesystemencoding() or 'utf-8'

    def _write(stream, text, encoding=_fsencoding):
        stream.write(text.decode(encoding, 'replace'))
else:
    def _write(stream, text):
        stream.write(text)


class Reporter(object):
    """
    Formats the results of pyflakes checks to users.
    """

    def __init__(self, warningStream, errorStream):
        """
        Construct a L{Reporter}.

        @param warningStream: A file-like object where warnings will be
            written to.  The stream's C{write} method must accept unicode.
            C{sys.stdout} is a good value.
        @param errorStream: A file-like object where error output will be
            written to.  The stream's C{write} method must accept unicode.
            C{sys.stderr} is a good value.
        """
        self._stdout = warningStream
        self._stderr = errorStream

    def unexpectedError(self, filename, msg):
        """
        An unexpected error occurred trying to process C{filename}.

        @param filename: The path to a file that we could not process.
        @ptype filename: C{unicode}
        @param msg: A message explaining the problem.
        @ptype msg: C{unicode}
        """
        _write(self._stderr, "%s: %s\n" % (filename, msg))

    def syntaxError(self, filename, msg, lineno, offset, text):
        """
        There was a syntax errror in C{filename}.

        @param filename: The path to the file with the syntax error.
        @ptype filename: C{unicode}
        @param msg: An explanation of the syntax error.
        @ptype msg: C{unicode}
        @param lineno: The line number where the syntax error occurred.
        @ptype lineno: C{int}
        @param offset: The column on which the syntax error occurred.
        @ptype offset: C{int}
        @param text: The source code containing the syntax error.
        @ptype text: C{unicode}
        """
        line = text.splitlines()[-1]
        if offset is not None:
            offset = offset - (len(text) - len(line))
        _write(self._stderr, '%s:%d: %s\n' % (filename, lineno, msg))
        _write(self._stderr, line)
        _write(self._stderr, '\n')
        if offset is not None:
            _write(self._stderr, " " * (offset + 1) + "^\n")

    def flake(self, message):
        """
        pyflakes found something wrong with the code.

        @param: A L{pyflakes.messages.Message}.
        """
        _write(self._stdout, str(message))
        _write(self._stdout, '\n')


def _makeDefaultReporter():
    """
    Make a reporter that can be used when no reporter is specified.
    """
    return Reporter(sys.stdout, sys.stderr)
