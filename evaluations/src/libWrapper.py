##################################################
# Copyright (C) 2009-2011 by
# Dent Earl (dearl@soe.ucsc.edu, dentearl@gmail.com)
# ... and other members of the Reconstruction Team of David Haussler's
# lab (BME Dept. UCSC)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
##################################################
def runCommands(cmds, localTempDir, inPipes = [], outPipes = [], mode = 's', debug = False):
    """ runCommands is a wrapper function for the parallel and serial
    versions of runCommands(). mode may either be s or p.
    """
    from libCall import runCommandsP, runCommandsS
    import os

    if not os.path.exists(localTempDir):
        raise ValueError('localTempDir "%s" does not exist.' % localTempDir)
    if not isinstance(cmds, list):
        raise TypeError('runCommands() takes a list of command lists '
                        'not a %s.' % cmds.__class__)
    for c in cmds:
       if not isinstance(c, list):
          raise TypeError('runCommands() takes a list of cmds, each cmd is itself a list '
                          'not a %s.' % c.__class__)
    if mode not in ('s', 'p'):
        raise ValueError('runCommands() "mode" argument must be either '
                         's or p, not %s.' % mode)
    
    if outPipes != []:
        if len(cmds) != len(outPipes):
            raise ValueError('runCommands() length of outPipes list %d '
                             'not equal to cmds list %d.' % (len(outPipes), len(cmds)))
    else:
        outPipes = [None] * len(cmds)
    if inPipes != []:
        if len(cmds) != len(inPipes):
            raise ValueError('runCommands() length of inPipes list %d '
                             'not equal to cmds list %d.' % (len(inPipes), len(cmds)))
    else:
        inPipes = [None] * len(cmds)

    if mode == 's':
        # logger.info('Issuing serial commands %s %s %s.' % (str(cmds), str(inPipes), str(outPipes)))
        runCommandsS(cmds, localTempDir, inPipes = inPipes, outPipes = outPipes, debug = debug)
    else:
        # logger.info('Issuing parallel commands %s %s %s.' % (str(cmds), str(inPipes), str(outPipes)))
        runCommandsP(cmds, localTempDir, inPipes = inPipes, outPipes = outPipes, debug = debug)

def runCommandsP(cmds, localTempDir, inPipes = [], outPipes = [], debug = False):
    """ runCommandsP uses the subprocess module
    to issue parallel processes from the cmds list.
    """
    import os
    import subprocess
    from libCall import handleReturnCode
    procs = []
    i = -1
    for c in cmds:
        i += 1
        if inPipes[i] is None:
            sin = None
        else:
            sin = subprocess.PIPE
        if outPipes[i] is None:
            sout = None
        else:
            sout = subprocess.PIPE
        # logger.info('Executing parallel %s < %s > %s' % (' '.join(c), inPipes[i], outPipes[i]))
        procs.append(subprocess.Popen(c, cwd = localTempDir, stdin = sin, stdout = sout))
    i = -1
    for p in procs:
        i += 1
        if inPipes[i] is None:
            sin = None
        else:
            if not os.path.exists(inPipes[i]):
                raise IOError('Unable to locate inPipe file: %s for command %s' % (inPipes[i], cmds[i]))
            sin = open(inPipes[i], 'r').read()
        if outPipes[i] is None:
            pout, perr = p.communicate(sin)
            handleReturnCode(p.returncode, cmds[i])
        else:
            f = open(outPipes[i], 'w')
            f.write(p.communicate(sin)[0])
            f.close()
            handleReturnCode(p.returncode, cmds[i])

def runCommandsS(cmds, localTempDir, inPipes=[], outPipes=[], debug = False):
    """ runCommandsS uses the subprocess module
    to issue serial processes from the cmds list.
    """
    import os
    import subprocess
    from libCall import handleReturnCode
    i = -1
    for c in cmds:
        i += 1
        if inPipes[i] is None:
            sin = None
        else:
            sin = subprocess.PIPE
        if outPipes[i] is None:
            sout = None
        else:
            sout = subprocess.PIPE
        # logger.info('Executing serial %s < %s > %s' % (' '.join(c), inPipes[i], outPipes[i]))
        p = subprocess.Popen(c, cwd = localTempDir, stdin = sin, stdout = sout)
            
        if inPipes[i] is None:
            sin = None
        else:
            if not os.path.exists(inPipes[i]):
                raise IOError('Unable to locate inPipe file: %s for command %s' % (inPipes[i], c))
            sin = open(inPipes[i], 'r').read()
        if outPipes[i] is None:
            pout, perr = p.communicate(sin)
            handleReturnCode(p.returncode, cmds[i])
        else:
            f = open(outPipes[i], 'w')
            f.write(p.communicate(sin)[0])
            f.close()
            handleReturnCode(p.returncode, cmds[i])

def handleReturnCode(retcode, cmd):
    """ handleReturnCode works with the libCall functions and raises errors when
    subprocesses go bad. Includes returncodes, which can be useful for debugging.
    """
    if not isinstance(retcode, int):
        raise TypeError('handleReturnCode() takes an integer for '
                        'retcode, not a %s.' % retcode.__class__)
    if not isinstance(cmd, list):
        raise TypeError('handleReturnCode() takes a list for '
                        'cmd, not a %s.' % cmd.__class__)
    if retcode:
        if retcode < 0:
            raise RuntimeError('Experienced an error while trying to execute: '
                               '%s SIGNAL:%d' %(' '.join(cmd), -retcode))
        else:
            raise RuntimeError('Experienced an error while trying to execute: '
                               '%s retcode:%d' %(' '.join(cmd), retcode))
