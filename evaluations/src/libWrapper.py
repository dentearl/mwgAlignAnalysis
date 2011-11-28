""" libWrapper.py
dent earl, dearl (a) soe ucsc edu

November 2011

Common functions used by python wrappers for alignathon

"""
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
import os
import subprocess

def checkOptions(options, args, parser):
   if len(args) != 5:
      parser.error('Args should contain five items: 1) location of package directory '
                   '2) predicted maf 3) registry file 4) temporary directory 5) output directory')
   options.location= args[0]
   options.predMaf = args[1]
   options.registry= args[2]
   options.tempDir = args[3]
   options.outDir  = args[4]
   for a in args:
      if not os.path.exists(a):
         parser.error('%s does not exist.' % a)
   for a in [args[0]] + args[3:]:
      if not os.path.isdir(a):
         parser.error('%s is not a directory.' % a)

def parseRegistry(options):
   f = open(options.registry, 'r')
   options.reg = {}
   for line in f:
      line = line.strip()
      if line.startswith('#'):
         continue
      try:
         key, val = line.split('\t')
      except ValueError:
         sys.stderr.write('Warning: Malformed registry file.\n')
         continue
      if key in options.reg:
         raise RuntimeError('Multiple copies of one key "%s" found in registry' % key)
      if key not in ['tree']:
         options.reg[key] = val.split(',')
         for i, v in enumerate(options.reg[key]):
            options.reg[key][i] = v.strip()
      else:
         # for some k, v pairs the v should not be a list.
         options.reg[key] = val.strip()
   for e in options.reg['evaluations']:
       if e != e.replace(' ', ''):
           raise RuntimeError('Malformed evaluations line: items should be comma separated: %s' % e)
   for elm in ['sequences', 'annotations']:
       if elm in options.reg:
           for s in options.reg[elm]:
               if not os.path.exists(os.path.join(options.location, s)):
                   raise RuntimeError('%s file mentioned in registry not found: %s' % (elm, s))

def runCommands(cmds, localTempDir, inPipes = [], outPipes = [], mode = 's', debug = False):
    """ runCommands is a wrapper function for the parallel and serial
    versions of runCommands(). mode may either be s or p.
    """
    # from libCall import runCommandsP, runCommandsS

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
    # from libCall import handleReturnCode
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
        # logger.info('Executing parallel run %s < %s > %s' % (' '.join(c), inPipes[i], outPipes[i]))
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
    # from libCall import handleReturnCode
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
        # logger.info('Executing serial run %s < %s > %s' % (' '.join(c), inPipes[i], outPipes[i]))
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

def recordCommand(command, filename):
   """ records the given command to the given filename. nothing special
   """
   f = open(filename, 'w')
   f.write('%s\n' % ' '.join(command))
   f.close()
