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
from optparse import OptionParser
import os
import lib.libCall as libCall

def initOptions(parser):
   pass

def checkOptions(options, args, parser):
   if len(args) != 3:
      parser.error('Args should contain three items: 1) true maf 2) predicted maf 3) output directory')
   for a in args[:3]:
      if not os.path.exists(a):
         parser.error('%s does not exist.' % a)
   if not os.path.isdir(args[2]):
      parser.error('%s is not a directory.' % args[2])
   
   options.trueMaf = args[0]
   options.predMaf = args[1]
   options.outDir = args[2]

def callEvaluation(options):
   cmd = ['mafComparator']
   cmd.append('--mafFile1=%s' % options.trueMaf)
   cmd.append('--mafFile2=%s' % options.predMaf)
   cmd.append('--outputFile=%s' % os.path.join(options.outDir, 'comparator.xml'))
   libCall.runCommands([cmd], os.curdir)

def main():
   usage = ('usage: %prog true.maf pred.maf outDir/\n\n'
            '%prog takes three arguments, the path to the true maf, the path\n'
            'to the predicted maf and the path to the output directory.')
   parser = OptionParser(usage)
   initOptions(parser)
   options, args = parser.parse_args()
   checkOptions(options, args, parser)
   
   callEvaluation(options)

if __name__ == '__main__':
   main()

