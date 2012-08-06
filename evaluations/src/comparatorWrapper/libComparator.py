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

numberOfPairs = {'primates.ancestor.maf' : 1104990158,
                 'primates.ancestor.noparalogies.maf' : 1075339194,
                 'primates.burnin.maf' : 1643763392,
                 'primates.burnin.noparalogies.maf' : 1075213159,
                 'primates.brudno.orig.maf' : 1133763359,
                 'primates.brudno.tc.maf' : 1488085114,
                 'primates.cactus.orig.maf' : 1106291204,
                 'primates.cactus.tc.maf' : 1106291204,
                 'primates.compara.orig.maf' : 1042047548,
                 'primates.compara.tc.maf' : 1042047548,
                 'primates.kimMa.orig.maf' : 1088327867,
                 'primates.kimMa.tc.maf' : 1148313565,
                 'primates.minmei.automz.orig.maf' : 1092771166,
                 'primates.minmei.automz.tc.maf' : 1225366921,
                 'primates.minmei.tba.orig.maf' : 1094404937,
                 'primates.minmei.tba.tc.maf' : 1227036564,
                 'primates.mugsy.orig.maf' : 1084995390,
                 'primates.mugsy.tc.maf' : 1085030967,
                 'primates.pmauve.orig.maf' : 1078990290,
                 'primates.pmauve.tc.maf' : 1075344377,
                 'primates.robusta.orig.maf' : 1055381731,
                 'primates.robusta.tc.maf' : 1055381731,
                 'primates.softberry.v1.orig.maf' : 995680230,
                 'primates.softberry.v1.tc.maf' : 1146456887,
                 'primates.softberry.v2.orig.maf' : 1020909238,
                 'primates.softberry.v2.tc.maf' : 10700516693144,
                 'primates.softberry.v2.tc.trim.maf' : 10644813568,
                 'primates.softberry.v3.orig.maf' : 4227127066,
                 'primates.softberry.v3.tc.maf' : 177334504277992,
                 'primates.softberry.v3.tc.trim.maf' : 42380969964,
                 'primates.ucsc.orig.maf' : 1091860358,
                 'primates.ucsc.tc.maf' : 1198028631,
                 'mammals.ancestor.maf' : 1689721432,
                 'mammals.ancestor.noparalogies.maf' : 1035661958,
                 'mammals.burnin.maf' : 2430331968,
                 'mammals.burnin.noparalogies.maf' : 1035314662,
                 'mammals.brudno.orig.maf' : 1396737191,
                 'mammals.brudno.tc.maf' : 5021387646,
                 'mammals.cactus.orig.maf' : 1345885372,
                 'mammals.cactus.tc.maf' : 1345885372,
                 'mammals.ebi.epo.orig.maf' : 424629309,
                 'mammals.ebi.epo.tc.maf' : 424629309,
                 'mammals.ebi.mp.orig.maf' : 708313333,
                 'mammals.ebi.mp.tc.maf' : 708313333,
                 'mammals.kimMa.orig.maf' : 1257197174,
                 'mammals.kimMa.tc.maf' : 20980345820898,
                 'mammals.kimMa.tc.trim.maf' : 59376532053,
                 'mammals.minmei.automz.orig.maf' : 1480410781,
                 'mammals.minmei.automz.tc.maf' : 878094707863024,
                 'mammals.minmei.automz.tc.trim.maf' : 2899889434,
                 'mammals.minmei.tba.orig.maf' : 1406302931,
                 'mammals.minmei.tba.tc.maf' : 1406302931,
                 'mammals.mugsy.orig.maf' : 118359959,
                 'mammals.mugsy.tc.maf' : 118359959,
                 'mammals.robusta.orig.maf' : 810277937,
                 'mammals.robusta.tc.maf' : 810277937,
                 'mammals.softberry.v1.orig.maf' : 179195346,
                 'mammals.softberry.v1.tc.maf' : 195381716,
                 'mammals.softberry.v2.orig.maf' : 180338753,
                 'mammals.softberry.v2.tc.maf' : 212738132,
                 'mammals.softberry.v3.orig.maf' : 187591638,
                 'mammals.softberry.v3.tc.maf' : 4348526102,
                 'mammals.softberry.v3.tc.trim.maf' : 395454116,
                 'mammals.ucsc.orig.maf' : 1276425130,
                 'mammals.ucsc.tc.maf' : 61425685490270,
                 'mammals.ucsc.tc.trim.maf' : 12770875049,
                 }
primateSequences = 'simChimp.chrA:53121445,simChimp.chrB:85778862,simChimp.chrC:35661804,simChimp.chrD:10574168,simGorilla.chrA:53120926,simGorilla.chrB:85848133,simGorilla.chrC:35654756,simGorilla.chrD:10570608,simHuman.chrA:53106993,simHuman.chrB:85835872,simHuman.chrC:35630306,simHuman.chrD:10572275,simOrang.chrB:85903762,simOrang.chrC:35683973,simOrang.chrD:10564720,simOrang.chrE:37692687,simOrang.chrF:15493520'
mammalSequences = 'simCow.chrA:42017321,simCow.chrB:86443571,simCow.chrC:33408597,simCow.chrD:6172747,simCow.chrE:24983699,simDog.chrA:39124508,simDog.chrD:35271305,simDog.chrF:64906724,simDog.chrG:26567043,simDog.chrH:20782131,simDog.chrI:5551284,simHuman.chrD:15973151,simHuman.chrF:41914564,simHuman.chrH:2880482,simHuman.chrI:13410180,simHuman.chrJ:88398963,simHuman.chrK:28218656,simMouse.chrA:34021255,simMouse.chrF:60272644,simMouse.chrF:60272644,simMouse.chrL:71158916,simMouse.chrM:5488388,simMouse.chrN:16897397,simMouse.chrO:3949899,simMouse.chrP:7132917,simRat.chrA:45269609,simRat.chrO:4060565,simRat.chrP:7089915,simRat.chrQ:54146922,simRat.chrR:88137694'
def basicCommand(filename, truth, options):
   """ Create the basic mafComparator command.
   """
   cmd = ['mafComparator']
   maf1 = os.path.basename(os.path.join(options.location, options.reg[truth][0]))
   maf2 = os.path.basename(options.predMaf)
   cmd.append('--maf1=%s' % os.path.join(options.location, options.reg[truth][0]))
   cmd.append('--maf2=%s' % options.predMaf)
   cmd.append('--out=%s' % os.path.join(options.outDir, filename))
   cmd.append('--samples=%d' % (1 * 10**7)) # 10,000,000
   if 'mammals' in options.outDir.split('-')[1].split('.'):
      test = 'mammals'
      cmd.append('--wigglePairs=simHuman*,simCow*,simHuman*,simDog*,simHuman*,simMouse*,simHuman*,simRat*')
      cmd.append('--legitSequences=%s' % mammalSequences)
   else:
      test = 'primates'
      cmd.append('--wigglePairs=simHuman*,simChimp*,simHuman*,simGorilla*,simHuman*,simOrang*')
      cmd.append('--legitSequences=%s' % primateSequences)
   key = '%s.%s' % (test, maf1)
   if key in numberOfPairs and maf2 in numberOfPairs:
      cmd.append('--numberOfPairs=%d,%d' % (numberOfPairs[key], numberOfPairs[maf2]))
   return cmd

def moveCommand(a, b):
   """ Create a move command to move a file from `a' to `b'
   """
   cmd = ['mv']
   cmd.append(a)
   cmd.append(b)
   return cmd
