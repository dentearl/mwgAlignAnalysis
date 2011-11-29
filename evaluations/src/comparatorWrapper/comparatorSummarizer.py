#!/usr/bin/env python
""" 
comparatorSummarizer.py
dent earl, dearl (a) soe ucsc edu
22 November 2011

Simple utility to summarize output of mafComparator
for use with alignathon competetition.
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
import xml.etree.ElementTree as ET
from optparse import OptionParser
import os

class ComparisonPair:
   def __init__(self, speciesA, speciesB):
      assert(speciesA is not None)
      assert(speciesB is not None)
      self.species = set([speciesA, speciesB])
      self.truePos = 0
      self.falsePos = 0
      self.falseNeg = 0
      # region numbers are for comparisons using .bed files
      self.truePosRegion = 0
      self.falsePosRegion = 0
      self.falseNegRegion = 0
      self.truePosRegionOutside = 0
      self.falsePosRegionOutside = 0
      self.falseNegRegionOutside = 0
      self.precision = None
      self.recall = None
      self.precisionRegion = None
      self.recallRegion = None
      self.precisionRegionOutside = None
      self.recallRegionOutside = None
      names = list(self.species)
      names = sorted(names, key = lambda x: x[3:])
      self.niceNames =  '-'.join(names)
      if len(names) == 1:
         self.niceNames = 'self-%s' % names[0]

   def calcPrecision(self):
      # assert((self.truePos + self.falsePos) != 0)
      if (self.truePos + self.falsePos) == 0:
         self.precision = -1.0
      else:
         self.precision = float(self.truePos) / (self.truePos + self.falsePos)
      if (self.truePosRegion + self.falsePosRegion) == 0:
         self.precisionRegion = -1.0
      else:
         self.precisionRegion = float(self.truePosRegion) / (self.truePosRegion + self.falsePosRegion)
      if (self.truePosRegionOutside + self.falsePosRegionOutside) == 0:
         self.precisionRegionOutside = -1.0
      else:
         self.precisionRegionOutside = (float(self.truePosRegionOutside) / 
                                        (self.truePosRegionOutside + self.falsePosRegionOutside))

   def calcRecall(self):
      # assert((self.truePos + self.falseNeg) != 0)
      if (self.truePos + self.falseNeg) == 0:
         self.recall = -1.0
      else:
         self.recall = float(self.truePos) / (self.truePos + self.falseNeg)
      if (self.truePosRegion + self.falseNegRegion) == 0:
         self.recallRegion = -1.0
      else:
         self.recallRegion = float(self.truePosRegion) / (self.truePosRegion + self.falseNegRegion)
      if (self.truePosRegionOutside + self.falseNegRegionOutside) == 0:
         self.recallRegionOutside = -1.0
      else:
         self.recallRegionOutside = (float(self.truePosRegionOutside) / 
                                     (self.truePosRegionOutside + self.falseNegRegionOutside))

def initOptions(parser):
   parser.add_option('--xml', dest = 'xml', 
                     help = 'location of comparator output xml to summarize.')

def checkOptions(options, args, parser):
   if options.xml is None:
      parser.error('specify --xml')
   if not os.path.exists(options.xml):
      parser.error('--xml %s does not exist' % options.xml)

def addPairData(pairs, homTests, falsePosMode = False):
   """ given the dict `pairs' and a part of the xml tree `homTests',
   addPairData() walks the tree to add data to the pairs dict.
   falsePosMode vs truePosMode.
   """
   hpTests = homTests.find('homologyPairTests')
   tests = hpTests.findall('homologyTest')
   for t in tests:
      seqA = t.attrib['sequenceA'].split('.')[0]
      seqB = t.attrib['sequenceB'].split('.')[0]
      if seqA == 'self':
         continue
      if seqA == seqB:
         pass
         # do not compare a genome to itself
         # continue
      if t.attrib['sequenceA'] == 'aggregate':
         # ignore the aggregate sequences
         continue
      p = findPair(seqA, seqB, pairs)
      if p is None:
         p = ComparisonPair(seqA, seqB)
         pairs['%s-%s' % (seqA, seqB)] = p
      if falsePosMode:
         p.falsePos += int(t.find('aggregateResults').find('all').attrib['totalFalse'])
         if t.find('aggregateResults').find('both') is not None:
            p.falsePosRegion += int(t.find('aggregateResults').find('both').attrib['totalFalse'])
            p.falsePosRegionOutside += int(t.find('aggregateResults').find('neither').attrib['totalFalse'])
      else:
         p.truePos += int(t.find('aggregateResults').find('all').attrib['totalTrue'])
         p.falseNeg += int(t.find('aggregateResults').find('all').attrib['totalFalse'])
         if t.find('aggregateResults').find('both') is not None:
            p.truePosRegion += int(t.find('aggregateResults').find('both').attrib['totalTrue'])
            p.falseNegRegion += int(t.find('aggregateResults').find('both').attrib['totalFalse'])
            p.truePosRegionOutside += int(t.find('aggregateResults').find('neither').attrib['totalTrue'])
            p.falseNegRegionOutside += int(t.find('aggregateResults').find('neither').attrib['totalFalse'])

def findPair(seqA, seqB, pairs):
   if '%s-%s' % (seqA, seqB) in pairs:
      # if '%s-%s' % (seqB, seqA) in pairs:
      #    raise RuntimeError('Duplicate pair found in `pairs\' dict: %s-%s' % (seqA, seqB))
      return pairs['%s-%s' % (seqA, seqB)]
   if '%s-%s' % (seqB, seqA) in pairs:
      # if '%s-%s' % (seqA, seqB) in pairs:
      #    raise RuntimeError('Duplicate pair found in `pairs\' dict: %s-%s' % (seqA, seqB))
      return pairs['%s-%s' % (seqB, seqA)]

def reportPairs(pairs, options):
   print ''
   sortedPairs = sorted(pairs, key = lambda x: pairs[x].niceNames)
   for pair in sortedPairs:
      p = pairs[pair]
      p.calcRecall()
      p.calcPrecision()
      if p.precision == -1.0:
         precStr = 'nan'
      else:
         precStr = '%.5f' % p.precision
      if p.precisionRegion == -1.0:
         precRegStr = 'nan'
      else:
         precRegStr = '%.5f' % p.precisionRegion
      if p.precisionRegionOutside == -1.0:
         precRegOutStr = 'nan'
      else:
         precRegOutStr = '%.5f' % p.precisionRegionOutside
      if not isRegionMode(pairs):
         print('%35s %10s %10.5f %9d %9d %9d' % 
               (p.niceNames, precStr, p.recall, 
                p.truePos, p.falsePos, p.falseNeg))
      else:
         print('%35s %10s %10.5f %9d %9d %9d' % 
               ('%s inside' % p.niceNames, precRegStr, p.recallRegion, 
                p.truePosRegion, p.falsePosRegion, p.falseNegRegion))
         print('%35s %10s %10.5f %9d %9d %9d' % 
               ('%s outside' % p.niceNames, precRegOutStr, p.recallRegionOutside, 
                p.truePosRegionOutside, p.falsePosRegionOutside, p.falseNegRegionOutside))

def summarize(options):
   """ summarize() summizes the information contained in options.xml
   """
   tree = ET.parse(options.xml)
   root = tree.getroot()
   homTests = root.findall('homologyTests')
   pairs = {}
   addPairData(pairs, homTests[0])
   addPairData(pairs, homTests[1], falsePosMode = True)
   
   if isRegionMode(pairs):
      suffix = 'Region'
      truePosOut = getItem(pairs, 'truePosRegionOutside', False)
      falseNegOut = getItem(pairs, 'falseNegRegionOutside', False)
      falsePosOut = getItem(pairs, 'falsePosRegionOutside', False)
      truePosSelfOut = getItem(pairs, 'truePosRegionOutside', True)
      falsePosSelfOut = getItem(pairs, 'falsePosRegionOutside', True)
      falseNegSelfOut = getItem(pairs, 'falseNegRegionOutside', True)
      precisionOut = float(truePosOut) / (truePosOut + falsePosOut)
      recallOut = float(truePosOut) / (truePosOut + falseNegOut)
      precisionSelfOut = float(truePosSelfOut) / (truePosSelfOut + falsePosSelfOut)
      recallSelfOut = float(truePosSelfOut) / (truePosSelfOut + falseNegSelfOut)
   else:
      suffix = ''
   truePos = getItem(pairs, 'truePos' + suffix, False)
   falseNeg = getItem(pairs, 'falseNeg' + suffix, False)
   falsePos = getItem(pairs, 'falsePos' + suffix, False)
   truePosSelf = getItem(pairs, 'truePos' + suffix, True)
   falsePosSelf = getItem(pairs, 'falsePos' + suffix, True)
   falseNegSelf = getItem(pairs, 'falseNeg' + suffix, True)
   
   precision = float(truePos) / (truePos + falsePos)
   recall = float(truePos) / (truePos + falseNeg)
   precisionSelf = float(truePosSelf) / (truePosSelf + falsePosSelf)
   recallSelf = float(truePosSelf) / (truePosSelf + falseNegSelf)

   print '%35s %10s %10s %9s %9s %9s' % ('', 'Precision', 'Recall', 'TP', 'FP', 'FN')
   if isRegionMode(pairs):
      print '%35s %10.5f %10.5f %9d %9d %9d' % ('Overall (w/o self) inside', precision, recall, 
                                                truePos, falsePos, falseNeg)
      print '%35s %10.5f %10.5f %9d %9d %9d' % ('Overall (w/o self) outside', precisionOut, recallOut, 
                                                truePosOut, falsePosOut, falseNegOut)
      print '%35s %10.5f %10.5f %9d %9d %9d' % ('Overall (w/  self) inside', precisionSelf, recallSelf, 
                                                truePosSelf, falsePosSelf, falseNegSelf)
      print '%35s %10.5f %10.5f %9d %9d %9d' % ('Overall (w/  self) outside', precisionSelfOut, recallSelfOut, 
                                                truePosSelfOut, falsePosSelfOut, falseNegSelfOut)
   else:
      print '%35s %10.5f %10.5f %9d %9d %9d' % ('Overall (w/o self)', precision, recall, 
                                                truePos, falsePos, falseNeg)
      print '%35s %10.5f %10.5f %9d %9d %9d' % ('Overall (w/  self)', precisionSelf, recallSelf, 
                                                truePosSelf, falsePosSelf, falseNegSelf)
   reportPairs(pairs, options)

def isRegionMode(pairs):
   for pair in pairs:
      p = pairs[pair]
      if p.truePosRegion > 0 or p.falsePosRegion > 0 or p.falseNegRegion > 0:
         return True

def getItem(pairs, item, alignSelf):
   ans = 0
   for pair in pairs:
      p = pairs[pair]
      if not alignSelf:
         if len(p.species) == 1:
            continue
      ans += p.__dict__[item]
   return ans

def main():
   usage = ('usage: %prog \n\n'
            '%prog \n')
   parser = OptionParser(usage)
   initOptions(parser)
   options, args = parser.parse_args()
   checkOptions(options, args, parser)
   
   summarize(options)
   
if __name__ == '__main__':
   main()

