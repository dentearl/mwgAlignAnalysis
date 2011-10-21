#!/usr/bin/env python
""" 
comparatorWrapper.py
dent earl, dearl (a) soe ucsc edu
29 July 2011

Simple wrapper to perform an evaluation
using mafComparator
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
import lib.libCall as libCall
from optparse import OptionParser
import os
import sys

def initOptions(parser):
   pass

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

def callEvaluation(options):
   cmd = ['mafComparator']
   cmd.append('--mafFile1=%s' % os.path.join(options.location, options.reg['truthMRCA']))
   cmd.append('--mafFile2=%s' % options.predMaf)
   cmd.append('--outputFile=%s' % os.path.join(options.outDir, 'comparator.xml'))
   cmd.append('--sampleNumber=100')
   libCall.runCommands([cmd], os.curdir)

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
         # for some k,v pairs the v should not be a list.
         options.reg[key] = val.strip()

def main():
   usage = ('usage: %prog location/ pred.maf set.reg.tab tempDir/ outDir/\n\n'
            '%prog takes five arguments, the path to the package set, the path\n'
            'to the predicted maf, the path to the registry file, the\n'
            'path to the temporary directory and the path to the output directory.')
   parser = OptionParser(usage)
   initOptions(parser)
   options, args = parser.parse_args()
   checkOptions(options, args, parser)
   
   parseRegistry(options)
   if 'mafComparator' not in options.reg['evaluations']:
      sys.exit(0)
   
   callEvaluation(options)

if __name__ == '__main__':
   main()

