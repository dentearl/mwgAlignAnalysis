#!/usr/bin/env python2.6
"""
"""
import glob
from optparse import OptionParser
import os
import shutil
import sys
import subprocess

registry = '''#toy registry
# Key	Value
####################
evaluations	grep
truthMRCA	truths/truth.maf
truthROOT	truths/truth.maf
truthMRCAnp	truths/truth.maf
truthROOTnp	truths/truth.maf
species	test1, test2, test3
tree	((test1:0.21,test2:0.18):0.1, test3);
# comment line
sequences	
annotations	
'''

truth = '''##maf version=1

s test1.chrA 0 10 + 100 ACTG-CCCGTA-
s test2.chrB 0 10 + 100 ACTGA--CGTAC
s test3.chrC 0 12 + 100 ACTGAAACGTAC

'''
pred = '''##maf version=1

s test1.chrA 0 10 + 100 ACTGCCCGTA--
s test2.chrB 0 10 + 100 ACTGA-CGTAC-
s test3.chrC 0 12 + 100 ACTGAAACGTAC

'''

def initOptions(parser):
   parser.add_option('--evalsDir', dest = 'evalsDir', 
                     help = 'Location of the evaluation bin directory')

def checkOptions(options, args, parser):
   if options.evalsDir is None:
      parser.error('Specify --evalsDir')
   if not os.path.exists(options.evalsDir):
      parser.error('--evalsDir %s does not exist' % options.evalsDir)
   if not os.path.isdir(options.evalsDir):
      parser.error('--evalsDir %s is not a directory' % options.evalsDir)

def validateFilename(filename):
   if filename != filename.replace('-', ''):
      raise RuntimeError('Filenames may not contain hypens, '
                         'bad name: %s' % filename)
def testEvaluation(filename):
   """ Run the evaluation on an ultra simple example. The evaluation will NOT
   be in the demo registry and therefore the evaluation should just accept the 
   arguments and exit normally. So we make sure it doesn't write to stdout or 
   stderr, and doesn't have an error return code.
   """
   global registry, truth, pred
   regPath = os.path.abspath(os.path.join(os.curdir, 'tempTestFiles', 'testSet.reg.tab'))
   truthPath = os.path.abspath(os.path.join(os.curdir, 'tempTestFiles', 'truths', 'truth.maf'))
   predPath = os.path.abspath(os.path.join(os.curdir, 'tempTestFiles', 'pred.maf'))
   tempDir = os.path.abspath(os.path.join(os.curdir, 'tempTestFiles', 'tmp'))
   outDir = os.path.abspath(os.path.join(os.curdir, 'tempTestFiles', 'out'))
   location = os.path.abspath(os.path.join(os.curdir, 'tempTestFiles'))
   sys.stdout.write('Testing evaluation %s...' % filename)
   if not os.path.exists('tempTestFiles'):
      os.mkdir('tempTestFiles')
   if not os.path.exists(os.path.join('tempTestFiles', 'truths')):
      os.mkdir(os.path.join('tempTestFiles', 'truths'))
   if not os.path.exists(outDir):
      os.mkdir(outDir)
   if not os.path.exists(tempDir):
      os.mkdir(tempDir)
   
   for p, v in ((regPath, registry), (truthPath, truth), (predPath, pred)):
      f = open(p, 'w')
      f.write(v)
      f.close()
   cmd = [os.path.abspath(filename), location, predPath, regPath, tempDir, outDir]
   p = subprocess.Popen(cmd, cwd = tempDir)
   pout, perr = p.communicate()
   if pout is not None:
      raise RuntimeError('Evaluation %s produced standard out: %s' 
                         % (os.path.basename(filename), pout))
   if pout is not None:
      raise RuntimeError('Evaluation %s produced standard error: %s' 
                         % (os.path.basename(filename), perr))
   if p.returncode:
        if p.returncode < 0:
            raise RuntimeError('Experienced an error while trying to execute: '
                               '%s SIGNAL:%d' %(' '.join(cmd), -p.returncode))
        else:
            raise RuntimeError('Experienced an error while trying to execute: '
                               '%s retcode:%d' %(' '.join(cmd), p.returncode))
   shutil.rmtree('tempTestFiles')
   sys.stdout.write(' OK\n')

def validateBins(options):
   items = glob.glob(os.path.join(options.evalsDir, '*'))
   bins = []
   for f in items:
      if os.access(f, os.X_OK) and not os.path.isdir(f):
         bins.append(f)
   for f in bins:
      if os.path.basename(f) == 'makefileEvalWrapper.sh':
         continue
      validateFilename(f)
      testEvaluation(f)

def main():
   parser = OptionParser()
   initOptions(parser)
   options, args = parser.parse_args()
   checkOptions(options, args, parser)
   validateBins(options)

if __name__ == '__main__':
   main()
