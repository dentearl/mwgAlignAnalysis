#!/usr/bin/env python
""" 
comparatorGenesWrapper.py
dent earl, dearl (a) soe ucsc edu
1 November 2011

Simple wrapper to perform an evaluation
using mafComparator and bed files for gene 
annotations
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
import lib.libComparator as libComparator
import lib.libWrapper as libWrapper
from optparse import OptionParser
import os
import sys

def callEvaluation(options):
   cmd = libComparator.basicCommand('comparatorGenes.xml', options)
   geneAnnots = libComparator.getAnnots('genes', options)
   cmd.append('--bedFiles=%s' % ','.join(geneAnnots))
   libWrapper.runCommands([cmd], os.curdir)
   libWrapper.recordCommand(cmd, os.path.join(options.outDir, 'command.txt'))

def main():
   usage = ('usage: %prog location/ pred.maf set.reg.tab tempDir/ outDir/\n\n'
            '%prog takes five arguments, the path to the package set, the path\n'
            'to the predicted maf, the path to the registry file, the\n'
            'path to the temporary directory and the path to the output directory.')
   parser = OptionParser(usage)
   libComparator.initOptions(parser)
   options, args = parser.parse_args()
   libWrapper.checkOptions(options, args, parser)
   
   libWrapper.parseRegistry(options)
   if os.path.basename(sys.argv[0]) not in options.reg['evaluations']:
      sys.exit(0)
   
   callEvaluation(options)

if __name__ == '__main__':
   main()

