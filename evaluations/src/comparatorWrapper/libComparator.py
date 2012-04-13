import os 

def initOptions(parser):
   pass

def getAnnots(targetAnnot, options):
   """ Given a target annotation, returns a list of file paths.
   """
   ga = []
   for annot in options.reg['annotations']:
      a = annot.split('.')
      if a[2] == targetAnnot:
         ga.append(os.path.join(options.location, annot))
   if ga == []:
      raise RuntimeError('unable to find target annotation "%s" in registry.' % targetAnnot)
   return ga

def basicCommand(filename, truth, options):
   """ Create the basic mafComparator command.
   """
   cmd = ['mafComparator']
   cmd.append('--mafFile1=%s' % os.path.join(options.location, options.reg[truth][0]))
   cmd.append('--mafFile2=%s' % options.predMaf)
   cmd.append('--outputFile=%s' % os.path.join(options.outDir, filename))
   cmd.append('--sampleNumber=%d' % (2 * 10**8)) # 200,000,000
   return cmd

def moveCommand(a, b):
   """ Create a move command to move a file from `a' to `b'
   """
   cmd = ['mv']
   cmd.append(a)
   cmd.append(b)
   return cmd
