#!/usr/bin/env python

"""Parser for Quartus template (source code) file
"""

import io
import os
import sys
try:
    from argparse import ArgumentParser
except ImportError:  # for version < 3.0
    from ArgParse import ArgumentParser


__prog__ = "quartus_template_parser.py"
__description__ = "Parser for Quartus templates"
__version__ = "0.1"
__version_string__ = '%s version %s' % (__prog__, __version__)
__epilog__ = "Example usage: %s systemverilog.tpl systemverilog-mode qps-" % (__prog__)


def get_args():
    """Run Argument Parser and get argument from command line"""
    parser = ArgumentParser(prog=__prog__,
                            description=__description__,
                            epilog=__epilog__)
    parser.add_argument('fname',
                        help="Quartus template file (<dir>/intelFPGA/<version>\
/quartus/common/templates/languages/<name>.tpl)")
    parser.add_argument('dir_name',
                        nargs='?',
                        help="Output directory name (default: quartus)")
    parser.add_argument('prefix',
                        nargs='?',
                        help="Prefix for output files (default: '')")
    parser.add_argument('-V', '--version',
                        action='version',
                        version=__version_string__)
    return parser.parse_args()


def file_exist(fname, verbosity=False, abort_and_exit=False):
    """Check if file exist
    Keyword Arguments:
    fname     -- file names
    verbosity -- verbosity operation
    Return: True if file exist
    """
    result = False
    try:
        if os.path.exists(fname):
            if os.path.isfile(fname):
                result = True
    except Exception as err:
        print(err)
    if verbosity:
        if not result:
            print("Can't open file: '%s'" % fname)
            if abort_and_exit:
                sys.exit("ERROR! Open file: '%s'\nExit from program!" % fname)
    return result


def makedir(dir_name):
    """Make directory
    """
    try:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
    except Exception as err:
        print("Error! can't create directory: %s" % err)


class QuartusTemplateParser():
    """
    Keyword Arguments:
    fname   -- parser file name
    dirname -- directory to output files
    prefix  -- output files prefix
    """
    def __init__(self, fname, dirname, prefix):
        self.build(fname, dirname, prefix)

    def build(self, fname, dirname, fprefix):
        """Run"""
        makedir(dirname)
        if file_exist(fname, True, True):
            with open(fname, 'r') as f:
                body = False
                s_data = ''
                template_title = ''
                group = ''
                key = ''
                for line in f:
                    s = line.rstrip()
                    if s.find('begin_group') == 0:
                        group = s[12:]
                        group = self.replace(group)
                    if s.find('begin_template') == 0:
                        s_data = ''
                        body = True
                        name = s[15:]
                        template_title = '// ' + name
                        name = self.replace(name)
                        name = fprefix + name
                    if body:
                        if s.find('standard_edition_only') == 0:
                            name = name + '-StdOnly'
                        if s.find('pro_edition_only') == 0:
                            name = name + '-ProOnly'
                        if s_data == '':
                            s_data = template_title
                        else:
                            if not s.find('end_template') == 0:
                                s_data = '%s\n%s' % (s_data, s)
                    if s.find('end_template') == 0:
                        body = False
                        key = fprefix + group + '-' + name[len(fprefix):]
                        prefix = self.yas_header(name, key)
                        s_data = '%s\n%s' % (prefix, s_data)
                        fname = '%s/%s' % (dirname, name)
                        print('File: %s' % fname)
                        print('  name = %s' % name)
                        print('  key  = %s' % key)
                        self.write_file(fname, s_data)

    def replace(self, st):
        """Replace chars in name."""
        st = st.replace(' ', '-')
        st = st.replace('/', '-')
        st = st.replace('|', '-')
        st = st.replace(':', '-')
        st = st.replace(',', '-')
        st = st.replace('.', '-')
        st = st.replace('+', '-')
        st = st.replace('--', '-')
        return st

    def write_file(self, fname, s):
        """Write output file."""
        f = io.open(fname, 'w', newline='\n')
        strg = u'%s\n' % s
        f.write(strg)
        f.close()

    def yas_header(self, name, key):
        """Prepare Yasnippet header."""
        s = '# -*- mode: snippet -*-'
        s = '%s\n# name: %s' % (s, name)
        s = '%s\n# key: %s' % (s, key)
        s = '%s\n# --' % s
        return s


def main():
    """Main"""
    args = get_args()
    fname = args.fname
    dir_name = args.dir_name
    prefix = args.prefix
    if dir_name is None:
        dir_name = 'quartus'
    if prefix is None:
        prefix = ''
    QuartusTemplateParser(fname, dir_name, prefix)


if __name__ == '__main__':
    main()
