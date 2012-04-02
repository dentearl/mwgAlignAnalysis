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
import xml.parsers.expat
from optparse import OptionParser
import os

class ComparisonPair:
    def __init__(self, speciesA, speciesB):
        assert(speciesA is not None)
        assert(speciesB is not None)
        self.species = set([speciesA, speciesB])
        self.truePosA = 0 # with respect to the A->B comparison
        self.truePosB = 0 # with respect to the B->A comparison
        self.falsePos = 0
        self.falseNeg = 0
        # region numbers are for comparisons using .bed files
        self.truePosRegionA = 0 # wrt A->B
        self.truePosRegionB = 0 # wrt B->A
        self.falsePosRegion = 0
        self.falseNegRegion = 0
        self.truePosRegionOutsideA = 0 # wrt A->B
        self.truePosRegionOutsideB = 0 # wrt B->A
        self.falsePosRegionOutside = 0
        self.falseNegRegionOutside = 0
        self.precision = None
        self.recall = None
        self.precisionRegion = None
        self.recallRegion = None
        self.precisionRegionOutside = None
        self.recallRegionOutside = None
        names = list(self.species)
        names = sorted(names, key = lambda x: x[3:]) # ignore the "sim" part of the name
        self.niceNames =  '-'.join(names)
        if len(names) == 1:
            self.niceNames = 'self-%s' % names[0]

    def calcPrecision(self):
        # Precision is calculated as 
        # TP_B / (TP_B + FP)
        # We use the TP_B since FP comes from the B->A comparison
        if (self.truePosB + self.falsePos) == 0:
            self.precision = float('nan')
        else:
            self.precision = float(self.truePosB) / (self.truePosB + self.falsePos)
        if (self.truePosRegionB + self.falsePosRegion) == 0:
            self.precisionRegion = float('nan')
        else:
            self.precisionRegion = float(self.truePosRegionB) / (self.truePosRegionB + self.falsePosRegion)
        if (self.truePosRegionOutsideB + self.falsePosRegionOutside) == 0:
            self.precisionRegionOutside = float('nan')
        else:
            self.precisionRegionOutside = (float(self.truePosRegionOutsideB) / 
                                           (self.truePosRegionOutsideB + self.falsePosRegionOutside))

    def calcRecall(self):
        # Recall is calculated as 
        # TP_A / (TP_A + FN)
        # We use the TP_A since FN comes from the A->B comparison
        if (self.truePosA + self.falseNeg) == 0:
            self.recall = -1.0
        else:
            self.recall = float(self.truePosA) / (self.truePosA + self.falseNeg)
        if (self.truePosRegionA + self.falseNegRegion) == 0:
            self.recallRegion = -1.0
        else:
            self.recallRegion = float(self.truePosRegionA) / (self.truePosRegionA + self.falseNegRegion)
        if (self.truePosRegionOutsideA + self.falseNegRegionOutside) == 0:
            self.recallRegionOutside = -1.0
        else:
            self.recallRegionOutside = (float(self.truePosRegionOutsideA) / 
                                        (self.truePosRegionOutsideA + self.falseNegRegionOutside))

def initOptions(parser):
    parser.add_option('--xml', dest = 'xml', 
                      help = 'location of mafComparator output xml to summarize.')

def checkOptions(options, args, parser):
    if options.xml is None:
        parser.error('specify --xml')
    if not os.path.exists(options.xml):
        parser.error('--xml %s does not exist' % options.xml)

def addPairData(pairs, homTests, falsePosMode = False):
    """ given the dict `pairs' and a part of the xml tree `homTests',
    addPairData() walks the tree to add data to the pairs dict.
    falsePosMode vs truePosMode:
    the first homology test in the mafComparator output is A->B and the 
    results of this comparison will be truePositives.
    the second homology test in the mC output is B->A and the results
    of this comparison can be false positives (falsePosMode).
    """
    hpTests = homTests.find('homologyPairTests')
    tests = hpTests.findall('homologyTest')
    for t in tests:
        seqA = t.attrib['sequenceA'].split('.')[0]
        seqB = t.attrib['sequenceB'].split('.')[0]
        if seqA == 'self' or seqB == 'self':
            continue
        if seqA == seqB:
            pass
            # do not compare a genome to itself
            # continue
        if t.attrib['sequenceA'] == 'aggregate' or t.attrib['sequenceB'] == 'aggregate':
            # ignore the aggregate sequences
            continue
        p = findPair(seqA, seqB, pairs)
        if p is None:
            p = ComparisonPair(seqA, seqB)
            pairs['%s-%s' % (seqA, seqB)] = p
        if falsePosMode:
            # the second homology test in the xml, B->A
            p.truePosB += int(t.find('aggregateResults').find('all').attrib['totalTrue'])
            p.falsePos += int(t.find('aggregateResults').find('all').attrib['totalFalse'])
            if t.find('aggregateResults').find('both') is not None:
                # bed file established regions
                p.truePosRegionB += int(t.find('aggregateResults').find('both').attrib['totalTrue'])
                p.falsePosRegion += int(t.find('aggregateResults').find('both').attrib['totalFalse'])
                p.truePosRegionOutsideB += int(t.find('aggregateResults').find('neither').attrib['totalTrue'])
                p.falsePosRegionOutside += int(t.find('aggregateResults').find('neither').attrib['totalFalse'])
        else:
            # the first homology test in the xml, A->B
            p.truePosA += int(t.find('aggregateResults').find('all').attrib['totalTrue'])
            p.falseNeg += int(t.find('aggregateResults').find('all').attrib['totalFalse'])
            if t.find('aggregateResults').find('both') is not None:
                # bed file established regions
                p.truePosRegionA += int(t.find('aggregateResults').find('both').attrib['totalTrue'])
                p.falseNegRegion += int(t.find('aggregateResults').find('both').attrib['totalFalse'])
                p.truePosRegionOutsideA += int(t.find('aggregateResults').find('neither').attrib['totalTrue'])
                p.falseNegRegionOutside += int(t.find('aggregateResults').find('neither').attrib['totalFalse'])

def findPair(seqA, seqB, pairs):
    # Check to see if the pair (seqA, seqB) is stored in pairs. Return None if not, return the pair if so.
    if '%s-%s' % (seqA, seqB) in pairs:
        # if '%s-%s' % (seqB, seqA) in pairs:
        #    raise RuntimeError('Duplicate pair found in `pairs\' dict: %s-%s' % (seqA, seqB))
        return pairs['%s-%s' % (seqA, seqB)]
    if '%s-%s' % (seqB, seqA) in pairs:
        # if '%s-%s' % (seqA, seqB) in pairs:
        #    raise RuntimeError('Duplicate pair found in `pairs\' dict: %s-%s' % (seqA, seqB))
        return pairs['%s-%s' % (seqB, seqA)]
    return None

def reportPairs(pairs, options):
    print ''
    sortedPairs = sorted(pairs, key = lambda x: pairs[x].niceNames)
    for pair in sortedPairs:
        p = pairs[pair]
        p.calcRecall()
        p.calcPrecision()
        if p.precision == -1.0 or (p.precision + p.recall) == 0:
            precStr = 'nan'
            fStr = 'nan'
        else:
            precStr = '%.5f' % p.precision
            fStr = '%.5f' % (2 * ((p.precision * p.recall)/
                                  (p.precision + p.recall)))
        if p.precisionRegion == -1.0 or (p.precisionRegion + p.recallRegion) == 0:
            precRegStr = 'nan'
            fRegStr = 'nan'
        else:
            precRegStr = '%.5f' % p.precisionRegion
            fRegStr = '%.5f' % (2 * ((p.precisionRegion * p.recallRegion)/
                                     (p.precisionRegion + p.recallRegion)))
        if p.precisionRegionOutside == -1.0 or (p.precisionRegionOutside + p.recallRegionOutside) == 0:
            precRegOutStr = 'nan'
            fRegOutStr = 'nan'
        else:
            precRegOutStr = '%.5f' % p.precisionRegionOutside
            fRegOutStr = '%.5f' % (2 * ((p.precisionRegionOutside * p.recallRegionOutside)/
                                        (p.precisionRegionOutside + p.recallRegionOutside)))
        if not isRegionMode(pairs):
            print('%35s %10s %10.5f %10s %9d %9d %9d %9d' % 
                  (p.niceNames, precStr, p.recall, fStr,
                   p.truePosA, p.truePosB, p.falsePos, p.falseNeg))
        else:
            print('%35s %10s %10.5f %10s %9d %9d %9d %9d' % 
                  ('%s  inside' % p.niceNames, precRegStr, p.recallRegion,
                   fRegStr,
                   p.truePosRegionA, p.truePosRegionB, p.falsePosRegion, p.falseNegRegion))
            print('%35s %10s %10.5f %10s %9d %9d %9d %9d' % 
                  ('%s outside' % p.niceNames, precRegOutStr, p.recallRegionOutside,
                   fRegOutStr,
                   p.truePosRegionOutsideA, p.truePosRegionOutsideB, 
                   p.falsePosRegionOutside, p.falseNegRegionOutside))

def summarize(options):
    """ summarize() summizes the information contained in file stored in options.xml
    """
    try:
        tree = ET.parse(options.xml)
    except xml.parsers.expat.ExpatError:
        raise RuntimeError('Input xml, %s is not a well formed xml document.' % options.xml)
    root = tree.getroot()
    homTests = root.findall('homologyTests')
    pairs = {}
    addPairData(pairs, homTests[0])
    addPairData(pairs, homTests[1], falsePosMode = True)
    
    if isRegionMode(pairs):
        # if a BED was used by mafComparator then the xml will be in Region mode
        suffix = 'Region'
        truePosOutA = getItem(pairs, 'truePosRegionOutsideA', False)
        truePosOutB = getItem(pairs, 'truePosRegionOutsideB', False)
        falseNegOut = getItem(pairs, 'falseNegRegionOutside', False)
        falsePosOut = getItem(pairs, 'falsePosRegionOutside', False)
        truePosSelfOutA = getItem(pairs, 'truePosRegionOutsideA', True)
        truePosSelfOutB = getItem(pairs, 'truePosRegionOutsideB', True)
        falsePosSelfOut = getItem(pairs, 'falsePosRegionOutside', True)
        falseNegSelfOut = getItem(pairs, 'falseNegRegionOutside', True)
        precisionOut = float(truePosOutB) / (truePosOutB + falsePosOut)
        recallOut = float(truePosOutA) / (truePosOutA + falseNegOut)
        precisionSelfOut = float(truePosSelfOutB) / (truePosSelfOutB + falsePosSelfOut)
        recallSelfOut = float(truePosSelfOutA) / (truePosSelfOutA + falseNegSelfOut)
    else:
        suffix = ''
    truePosA = getItem(pairs, 'truePos' + suffix + 'A', False)
    truePosB = getItem(pairs, 'truePos' + suffix + 'B', False)
    falseNeg = getItem(pairs, 'falseNeg' + suffix, False)
    falsePos = getItem(pairs, 'falsePos' + suffix, False)
    truePosSelfA = getItem(pairs, 'truePos' + suffix + 'A', True)
    truePosSelfB = getItem(pairs, 'truePos' + suffix + 'B', True)
    falsePosSelf = getItem(pairs, 'falsePos' + suffix, True)
    falseNegSelf = getItem(pairs, 'falseNeg' + suffix, True)
    
    if (truePosB + falsePos) == 0:
        precision = float('nan')
    else:
        precision = float(truePosB) / (truePosB + falsePos)
    if (truePosA + falseNeg) == 0:
        recall = float('nan')
    else:
        recall = float(truePosA) / (truePosA + falseNeg)
    if (truePosSelfB + falsePosSelf) == 0:
        precisionSelf = float('nan')
    else:
        precisionSelf = float(truePosSelfB) / (truePosSelfB + falsePosSelf)
    if (truePosSelfA + falseNegSelf) == 0:
        recallSelf = float('nan')
    else:
        recallSelf = float(truePosSelfA) / (truePosSelfA + falseNegSelf)

    print '%35s %10s %10s %10s %9s %9s %9s %9s' % ('', 'Precision', 'Recall', 'F-score', 'TP (A)', 'TP (B)', 'FP (B)', 'FN (A)')
    if isRegionMode(pairs):
        sanityCheckRegionMode(truePosA, truePosB, falsePos, falseNeg, 
                              truePosOutA, truePosOutB, falsePosOut, falseNegOut, 
                              truePosSelfA, truePosSelfB, falsePosSelf, falseNegSelf, 
                              truePosSelfOutA, truePosSelfOutB, falsePosSelfOut, falseNegSelfOut, 
                              pairs, options)
        print '%35s %10.5f %10.5f %10.5f %9d %9d %9d %9d' % ('Overall (w/o self)  inside', precision, recall, 
                                                             2 * (precision * recall) / (precision + recall),
                                                             truePosA, truePosB, falsePos, falseNeg)
        print '%35s %10.5f %10.5f %10.5f %9d %9d %9d %9d' % ('Overall (w/o self) outside', precisionOut, recallOut, 
                                                             2 * ((precisionOut * recallOut) / 
                                                                  (precisionOut + recallOut)),
                                                             truePosOutA, truePosOutA, falsePosOut, falseNegOut)
        print '%35s %10.5f %10.5f %10.5f %9d %9d %9d %9d' % ('Overall (w/  self)  inside', precisionSelf, recallSelf, 
                                                             2 * ((precisionSelf * recallSelf) / 
                                                                  (precisionSelf + recallSelf)),
                                                             truePosSelfA, truePosSelfB, falsePosSelf, falseNegSelf)
        print '%35s %10.5f %10.5f %10.5f %9d %9d %9d %9d' % ('Overall (w/  self) outside', precisionSelfOut, 
                                                             recallSelfOut,
                                                             2 * ((precisionSelfOut * recallSelfOut) / 
                                                                  (precisionSelfOut + recallSelfOut)),
                                                             truePosSelfOutA, truePosSelfOutB, falsePosSelfOut, falseNegSelfOut)
    else:
        sanityCheck(truePosA, truePosB, falsePos, falseNeg, truePosSelfA, 
                    truePosSelfB, falsePosSelf, falseNegSelf, pairs, options)
        print '%35s %10.5f %10.5f %10.5f %9d %9d %9d %9d' % ('Overall (w/o self)', precision, recall, 
                                                             2 * (precision * recall) / (precision + recall),
                                                             truePosA, truePosB, falsePos, falseNeg)
        print '%35s %10.5f %10.5f %10.5f %9d %9d %9d %9d' % ('Overall (w/  self)', precisionSelf, recallSelf, 
                                                             2 * ((precisionSelf * recallSelf) / 
                                                                  (precisionSelf + recallSelf)),
                                                             truePosSelfA, truePosSelfB, falsePosSelf, falseNegSelf)
    
    reportPairs(pairs, options)
def sanityCheckRegionMode(truePosA, truePosB, falsePos, falseNeg, 
                          truePosOutA, truePosOutB, falsePosOut, falseNegOut, 
                          truePosSelfA, truePosSelfB, falsePosSelf, falseNegSelf, 
                          truePosSelfOutA, truePosSelfOutB, falsePosSelfOut, falseNegSelfOut, 
                          pairs, options):
    # Each column of  numbers reported in the rows labeled "Overall" should be the sum of 
    # the numbers contained in the column corresponding to "inside" or "outside" status.
    obsTruePosA = 0
    obsTruePosB = 0
    obsFalsePos = 0
    obsFalseNeg = 0
    obsTruePosOutA = 0
    obsTruePosOutB = 0
    obsFalsePosOut = 0
    obsFalseNegOut = 0
    obsTruePosASelf = 0
    obsTruePosBSelf = 0
    obsFalsePosSelf = 0
    obsFalseNegSelf = 0
    obsTruePosASelfOut = 0
    obsTruePosBSelfOut = 0
    obsFalsePosSelfOut = 0
    obsFalseNegSelfOut = 0
    for pair in pairs:
        p = pairs[pair]
        if p.niceNames.startswith('self-'):
            obsTruePosASelf += p.truePosRegionA
            obsTruePosBSelf += p.truePosRegionB
            obsFalsePosSelf += p.falsePosRegion
            obsFalseNegSelf += p.falseNegRegion
            obsTruePosASelfOut += p.truePosRegionOutsideA
            obsTruePosBSelfOut += p.truePosRegionOutsideB
            obsFalsePosSelfOut += p.falsePosRegionOutside
            obsFalseNegSelfOut += p.falseNegRegionOutside
        else:
            obsTruePosA += p.truePosRegionA
            obsTruePosB += p.truePosRegionB
            obsFalsePos += p.falsePosRegion
            obsFalseNeg += p.falseNegRegion
            obsTruePosOutA += p.truePosRegionOutsideA
            obsTruePosOutB += p.truePosRegionOutsideB
            obsFalsePosOut += p.falsePosRegionOutside
            obsFalseNegOut += p.falseNegRegionOutside
    obsTruePosASelf += obsTruePosA
    obsTruePosBSelf += obsTruePosB
    obsFalsePosSelf += obsFalsePos
    obsFalseNegSelf += obsFalseNeg
    obsTruePosASelfOut += obsTruePosOutA
    obsTruePosBSelfOut += obsTruePosOutB
    obsFalsePosSelfOut += obsFalsePosOut
    obsFalseNegSelfOut += obsFalseNegOut
    for obs, exp in [(obsTruePosA, truePosA), (obsTruePosB, truePosB), 
                     (obsFalsePos, falsePos), (obsFalseNeg, falseNeg),
                     (obsTruePosOutA, truePosOutA), (obsTruePosOutB, truePosOutB), 
                     (obsFalsePosOut, falsePosOut), (obsFalseNegOut, falseNegOut),
                     (obsTruePosASelf, truePosSelfA), (obsTruePosBSelf, truePosSelfB), 
                     (obsFalsePosSelf, falsePosSelf), (obsFalseNegSelf, falseNegSelf),
                     (obsTruePosASelfOut, truePosSelfOutA), (obsTruePosBSelfOut, truePosSelfOutB), 
                     (obsFalsePosSelfOut, falsePosSelfOut), (obsFalseNegSelfOut, falseNegSelfOut),
                     ]:
        assert(obs == exp)
def sanityCheck(truePosA, truePosB, falsePos, falseNeg, truePosASelf, 
                truePosBSelf, falsePosSelf, falseNegSelf, pairs, options):
    # Each column of numbers reported in the rows labeled "Overall" should be the sum of 
    # the numbers contained in the column.
    obsTruePosA = 0
    obsTruePosB = 0
    obsFalsePos = 0
    obsFalseNeg = 0
    obsTruePosASelf = 0
    obsTruePosBSelf = 0
    obsFalsePosSelf = 0
    obsFalseNegSelf = 0
    for pair in pairs:
        p = pairs[pair]
        if p.niceNames.startswith('self-'):
            obsTruePosASelf += p.truePosA
            obsTruePosBSelf += p.truePosB
            obsFalsePosSelf += p.falsePos
            obsFalseNegSelf += p.falseNeg
        else:
            obsTruePosA += p.truePosA
            obsTruePosB += p.truePosB
            obsFalsePos += p.falsePos
            obsFalseNeg += p.falseNeg
    obsTruePosASelf += obsTruePosA
    obsTruePosBSelf += obsTruePosB
    obsFalsePosSelf += obsFalsePos
    obsFalseNegSelf += obsFalseNeg
    for obs, exp in [(obsTruePosA, truePosA), (obsTruePosB, truePosB), 
                     (obsFalsePos, falsePos), (obsFalseNeg, falseNeg),
                     (obsTruePosASelf, truePosASelf), (obsTruePosBSelf, truePosBSelf), 
                     (obsFalsePosSelf, falsePosSelf), (obsFalseNegSelf, falseNegSelf),]:
        assert(obs == exp)
def isRegionMode(pairs):
    """ Detects if a BED was used to restrict tests to a region
    """
    for pair in pairs:
        p = pairs[pair]
        if p.truePosRegionA > 0 or p.truePosRegionB > 0 or p.falsePosRegion > 0 or p.falseNegRegion > 0:
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

