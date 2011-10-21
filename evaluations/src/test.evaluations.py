import unittest
import glob
import os
import shutil
import subprocess
import sys

script = sys.argv[0]
binDir = os.path.normpath(os.path.join(os.path.dirname(script), '..', 'bin'))

registry = '''#toy registry
# Key	Value
####################
evaluations	grep, ls, man
truthMRCA	truths/truth.maf
truthROOT	truths/truth.maf
species	test1, test2, test3
tree	((test1:0.21,test2:0.18):0.1, test3);
# comment line
sequences	sequences/test1.fa, sequences/test2.fa, sequences/test3.fa
annotations	annotations/test1.bed
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

class VerifyEvaluationsDontRun(unittest.TestCase):
   def test_evaluationsDontRun(self):
      """ Evaluations should not run when they're not on the evaluations list
      """
      items = glob.glob(os.path.join(binDir, '*'))
      binaries = filterItems(items)
      for bin in binaries:
         path = os.path.abspath(os.path.join(os.curdir, 'tempTestFiles'))
         writeTempFiles(registry, truth, pred, path)
         cmd = [bin, path, os.path.join(path, 'predictions', 'pred.maf'),
                os.path.join(path, 'testSet.reg.tab'),
                os.path.join(path, 'tmp'), os.path.join(path, 'out')]

         p = subprocess.Popen(cmd, cwd = os.path.join(path, 'tmp'), 
                              stdout = subprocess.PIPE, stderr = subprocess.PIPE)
         pout, perr = p.communicate()
         
         self.assertEqual(pout, '')
         self.assertEqual(perr, '')
         
         self.assertTrue(not p.returncode)
         self.assertTrue(glob.glob(os.path.join(path, 'out', '*')) == [])
         self.assertTrue(glob.glob(os.path.join(path, 'tmp', '*')) == [])
         shutil.rmtree(os.path.join(os.curdir, 'tempTestFiles'))

class VerifyEvaluationsAcceptExactlyFiveArgs(unittest.TestCase):
   def test_evaluationsFailTooMany(self):
      """ When provided with more than five arguments, evaluations should fail
      """
      items = glob.glob(os.path.join(binDir, '*'))
      binaries = filterItems(items)
      for bin in binaries:
         path = os.path.abspath(os.path.join(os.curdir, 'tempTestFiles'))
         writeTempFiles(registry, truth, pred, path)
         cmd = [bin, path, os.path.join(path, 'predictions', 'pred.maf'),
                os.path.join(path, 'testSet.reg.tab'),
                os.path.join(path, 'tmp'), os.path.join(path, 'out'),
                'extraVariable']

         p = subprocess.Popen(cmd, cwd = os.path.join(path, 'tmp'), 
                              stdout = subprocess.PIPE, stderr = subprocess.PIPE)
         pout, perr = p.communicate()
         
         self.assertTrue(p.returncode)

         shutil.rmtree(os.path.join(os.curdir, 'tempTestFiles'))
   def test_evaluationsFailTooFew(self):
      """ When provided with fewer than five arguments, evaluations should fail
      """
      items = glob.glob(os.path.join(binDir, '*'))
      binaries = filterItems(items)
      for bin in binaries:
         path = os.path.abspath(os.path.join(os.curdir, 'tempTestFiles'))
         writeTempFiles(registry, truth, pred, path)
         cmd = [bin, path, os.path.join(path, 'predictions', 'pred.maf'),
                os.path.join(path, 'testSet.reg.tab'),
                os.path.join(path, 'tmp') ]

         p = subprocess.Popen(cmd, cwd = os.path.join(path, 'tmp'), 
                              stdout = subprocess.PIPE, stderr = subprocess.PIPE)
         pout, perr = p.communicate()
         
         self.assertTrue(p.returncode)

         shutil.rmtree(os.path.join(os.curdir, 'tempTestFiles'))
         
def writeTempFiles(reg, truth, pred, path):
   # the basename directory of path should not exist
   regPath = os.path.join(path, 'testSet.reg.tab')
   truthPath = os.path.join(path, 'truths', 'truth.maf')
   predPath = os.path.join(path, 'predictions', 'pred.maf')
   tempDir = os.path.join(path, 'tmp')
   outDir = os.path.join(path, 'out')
   if not os.path.exists(path):
      os.mkdir(path)
   if not os.path.exists(os.path.join(path, 'truths')):
      os.mkdir(os.path.join(path, 'truths'))
   if not os.path.exists(os.path.join(path, 'predictions')):
      os.mkdir(os.path.join(path, 'predictions'))
   if not os.path.exists(outDir):
      os.mkdir(outDir)
   if not os.path.exists(tempDir):
      os.mkdir(tempDir)
   for p, v in ((regPath, reg), (truthPath, truth), (predPath, pred)):
      f = open(p, 'w')
      f.write(v)
      f.close()

def filterItems(items):
   bins = []
   for f in items:
      if os.path.basename(f) == 'makefileEvalWrapper.sh':
         continue
      if os.access(f, os.X_OK) and not os.path.isdir(f):
         bins.append(os.path.abspath(f))
   return bins

if __name__ == '__main__':
   unittest.main()

