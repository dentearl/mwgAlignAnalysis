import os 

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

def getAnnots(whiteList, options):
   ga = []
   for annot in options.reg['annotations']:
      a = annot.split('.')
      if a[2] in whiteList:
         ga.append(os.path.join(options.location, annot))
   return ga

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

def basicCommand(filename, options):
   cmd = ['mafComparator']
   cmd.append('--mafFile1=%s' % os.path.join(options.location, options.reg['truthMRCA'][0]))
   cmd.append('--mafFile2=%s' % options.predMaf)
   cmd.append('--outputFile=%s' % os.path.join(options.outDir, filename))
   cmd.append('--sampleNumber=1000')
   return cmd
