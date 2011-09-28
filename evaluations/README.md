# Evaluations HOWTO
29 July 2011
Dent Earl

## Introduction
An _evaluation_ in this document refers to a program (or wrapper) that that takes three inputs in the following order: 
1. the path to the true maf
2. the path to the predicted maf
3. the newick tree for the simulation
4. the path to a temporary directory
5. the path to the directory where output may be written
I.e. <code>myEval path/to/truth.maf path/to/prediction.maf path/to/diretory/ </code>

The _evaluation_ will be passed these arguments by the analysis Makefile. The output directory will be specific to one prediction and evaluation pair. I.e. if there are four prediction mafs and two evaluations then eight different directories will be created. If you have multiple parameters to pass to a custom _evaluation_ then you would do that through a wrapper that would accept the three arguments and then perform the multi parameter assessments.

An _evalution_ may be included in the <code>src/</code> directory in its own self-contained directory with a Makefile to perform the build. Each _evaluation_ should be installed in the <code>evaluations/bin/</code> directory located in this directory. Each file in <code>evaluations/bin/</code> is considered an _evaluation_ by the analysis rule of the Makefile and will be called on each prediction maf.

An _evaluation_ may NOT include a hyphen, '-', in its filename. Doing so will gum up the makefile. Use underscores instead.

## Requirements
This pipeline requires the following software. 

* Will run in a Linux pipeline
* Python 2.6 &le; version &lt; 3.0

## Dependencies
Your _evaluation_ is allowed to have dependencies that are not included in this repository, simply update the list of dependencies in the README.md located at the project root directory. 
