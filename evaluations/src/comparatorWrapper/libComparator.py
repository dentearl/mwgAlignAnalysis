import os 

def initOptions(parser):
   pass

def getAnnots(targetAnnot, options):
   ga = []
   for annot in options.reg['annotations']:
      a = annot.split('.')
      if a[2] == targetAnnot:
         ga.append(os.path.join(options.location, annot))
   if ga == []:
      raise RuntimeError('unable to find target annotation "%s" in registry.' % targetAnnot)
   return ga

def basicCommand(filename, truth, options):
   cmd = ['mafComparator']
   cmd.append('--mafFile1=%s' % os.path.join(options.location, options.reg[truth][0]))
   cmd.append('--mafFile2=%s' % options.predMaf)
   cmd.append('--outputFile=%s' % os.path.join(options.outDir, filename))
   cmd.append('--sampleNumber=%d' % (2 * 10**8)) # 200,000,000
   return cmd
