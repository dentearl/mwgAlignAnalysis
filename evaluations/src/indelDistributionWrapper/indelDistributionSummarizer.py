#!/usr/bin/env python
""" 
indelDistributionSummarizer.py
dent earl, dearl (a) soe ucsc edu
30 November 2011

Simple utility to summarize output of mafIndelDistribution
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
from lib.libStem import stem
from numpy import max as npmax
from numpy import mean as npmean
from numpy import median as npmedian
from numpy import min as npmin
from numpy import std as npstd
from optparse import OptionParser
import os
from scipy.stats import scoreatpercentile
import sys
import xml.etree.ElementTree as ET

class CoverageTag:
    def __init__(self, targetGenome, targetChromosome, targetLength, 
                 targetNumberBasesCovered, queryGenome):
        self.targetGenome = targetGenome
        self.targetChromosome = targetChromosome
        self.targetLength = int(targetLength)
        self.targetNumberBasesCovered = int(targetNumberBasesCovered)
        self.queryGenome = queryGenome
        self.targetPercentCovered = float(self.targetNumberBasesCovered) / self.targetLength

def initOptions(parser):
    parser.add_option('--xml', dest = 'xml', 
                      help = 'location of mafIndelDistribution output xml to summarize.')

def checkOptions(options, args, parser):
    if options.xml is None:
        parser.error('specify --xml')
    if not os.path.exists(options.xml):
        parser.error('--xml %s does not exist' % options.xml)

def summarize(options):
    """ summarize() summizes the information contained in options.xml
    """
    print 'Coverage Information:'
    summarizeCoverage(options)
    print '\nGaps Information:'
    summarizeGaps(options)

def summarizeGaps(options):
    tree = ET.parse(options.xml)
    root = tree.getroot()
    gapsText = root.find('gaps').text
    gaps = map(int, gapsText.split(','))

    sevenNumSummary(gaps)
    stem(gaps)

def sevenNumSummary(gaps):
    values = [prettyInt(len(gaps)), prettyInt(npmin(gaps)), scoreatpercentile(gaps, 25), npmedian(gaps), 
              npmean(gaps), scoreatpercentile(gaps, 75), prettyInt(npmax(gaps)), npstd(gaps)]
    labels = ['n', 'Min.', '1st Qu.', 'Median', 'Mean', '3rd Qu.', 'Max.', 'Stdev.']
    s1, s2 = '', ''
    for i in xrange(len(values) - 1, -1, -1):
        s = str(values[i])
        l = labels[i]
        if len(s) > len(l):
            s1 =     ' ' * (len(s) - len(l))+ l + '  ' + s1
            s2 = s + '  ' + s2
        else:
            s1 = l + '  ' + s1
            s2 =  ' ' * (len(l) - len(s))+ s + '  ' + s2
    print ' '*3 + s1
    print ' '*3 + s2

def summarizeCoverage(options):
    targets = {}
    tree = ET.parse(options.xml)
    root = tree.getroot()
    pairs = root.find('pairwiseCoverage').findall('coverage')
    genomes = set([])
    lengths = {}
    for p in pairs:
        c = CoverageTag(p.attrib['targetGenome'], p.attrib['targetChromosome'], 
                        p.attrib['targetLength'], p.attrib['targetNumberBasesCovered'], 
                        p.attrib['queryGenome'])
        if c.targetGenome not in targets:
            targets[c.targetGenome] = {c.targetChromosome : {c.queryGenome : c}}
        else:
            if c.targetChromosome not in targets[c.targetGenome]:
                targets[c.targetGenome][c.targetChromosome] = {c.queryGenome : c}
            else:
                if c.queryGenome not in targets[c.targetGenome][c.targetChromosome]:
                    targets[c.targetGenome][c.targetChromosome][c.queryGenome] = c
                else:
                    raise RuntimeError('Duplicate coverage tag found target: %s targetChrom: %s query: %s' % (c.targetGenome, c.targetChromosome, c.queryGenome))
        if c.targetGenome not in genomes:
            genomes.add(c.targetGenome)
        if c.targetGenome not in lengths:
            lengths[c.targetGenome] = {c.targetChromosome : c.targetLength}
        else:
            if c.targetChromosome not in lengths[c.targetGenome]:
                lengths[c.targetGenome][c.targetChromosome] = c.targetLength
    rowOrder = sorted(targets.keys())
    columns = sorted(genomes)
    sys.stdout.write('%20s %12s' % ('Target', 'Length'))
    for col in columns:
        sys.stdout.write(' %12s' % col)
    sys.stdout.write('\n')
    for i, r in enumerate(rowOrder, 0):
        chromOrder = sorted(targets[r])
        for j, c in enumerate(chromOrder, 0):
            sys.stdout.write('%20s %12s' % ('%s-%s' % (r, c), prettyInt(lengths[r][c])))
            for k, col in enumerate(columns, 0):
                if col in targets[r][c]:
                    sys.stdout.write(' %12.5f' % targets[r][c][col].targetPercentCovered)
                else:
                    sys.stdout.write(' %12s' % ' ')
            sys.stdout.write('\n')

def prettyInt(i):
    if not isinstance(i, int):
        raise RuntimeError('input to prettyInt must be int, not %s' % i.__class__)
    s = ''
    r = '%d' % i
    for j in xrange(0, len(r)):
        if j > 0 and not j % 3:
            s = '%s,%s' % (r[(len(r) - 1) - j], s)
        else:
            s = '%s%s' % (r[(len(r) - 1) - j], s)
    return s

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
