#!/usr/bin/env python

"""
Low-level/standalone host-environment handling/checking utilities/classes/data

:Note: This module must _NOT_ depend on anything in dockertest package or
       in autotest!
"""

import subprocess


def set_selinux_context(pwd, context=None, recursive=True):
    """
    When selinux is enabled it sets the context by chcon -t ...
    :param pwd: target directory
    :param context: desired context (svirt_sandbox_file_t by default)
    :param recursive: set context recursively (-R)
    :raise OSError: In case of failure
    """
    if context is None:
        context = "svirt_sandbox_file_t"
    if recursive:
        flags = 'R'
    else:
        flags = ''
    # changes context in case selinux is supported and is enabled
    _cmd = ("type -P selinuxenabled || exit 0 ; "
            "selinuxenabled || exit 0 ; "
            "chcon -%st %s %s" % (flags, context, pwd))
    cmd = subprocess.Popen(_cmd, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, shell=True)
    if cmd.wait() != 0:
        raise OSError("Fail to set selinux context by '%s' (%s):\nSTDOUT:\n%s"
                      "\nSTDERR:\n%s" % (_cmd, cmd.poll(), cmd.stdout.read(),
                                         cmd.stderr.read()))
