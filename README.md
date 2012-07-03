# mwgAlignAnalysis
(c) 2011-2012 The Authors, see LICENSE.txt for details.

## Authors
[Dent Earl] (https://github.com/dentearl/)

## Summary
The [Alignathon] (http://compbio.soe.ucsc.edu/alignathon/) is a collaborative project between whole genome aligners intended to help assess methods and promote development of the field. This repository is used to run analyses of predicted alignments within test packages.

## Dependencies
* A Linux system to run the analysis pipeline
* Python 2.7
* [mafTools] (https://github.com/dentearl/maftools/)

## Installation
1. Install dependencies.
2. <code>$ git clone git@github.com:dentearl/mwgAlignAnalysis.git</code>
3. <code>$ cd mwgAlignAnalysis && make</code>

## Use
After downloading a package from the [Alignathon website] (http://compbio.soe.ucsc.edu/alignathon/), performing an alignment and placing the predicted maf in <code>package/predictions/</code>, an analysis can be run using

<code>$ make analysis location=/path/to/package set=testSet</code>

where <code>location</code> is the path to the package and <code>set</code> is one of the prefixes from the registries directory, i.e. <code>flySet</code>, <code>mammalSet</code>, <code>primateSet</code> or <code>testSet</code>. The Makefile can be run in parallel with <code>-j [integer]</code> which allows  the evaluations in an analysis to be run in parallel.
