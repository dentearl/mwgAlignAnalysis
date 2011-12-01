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

def stem_print(close, dist, ndigits):
    """/*
    *  R : A Computer Language for Statistical Data Analysis
    *  Copyright (C) 1995, 1996  Robert Gentleman and Ross Ihaka
    *  Copyright (C) 1997-2000   Robert Gentleman, Ross Ihaka and the
    *                            R Development Core Team
    #  This function ported to Python by Dent Earl, UCSC BME Dept. 2010
    *
    *  This program is free software; you can redistribute it and/or modify
    *  it under the terms of the GNU General Public License as published by
    *  the Free Software Foundation; either version 2 of the License, or
    *  (at your option) any later version.
    *
    *  This program is distributed in the hope that it will be useful,
    *  but WITHOUT ANY WARRANTY; without even the implied warranty of
    *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    *  GNU General Public License for more details.
    *
    *  You should have received a copy of the GNU General Public License
    *  along with this program; if not, a copy is available at
    *  http://www.r-project.org/Licenses/
    */
    """
    import sys
    if (close/10 == 0) and (dist < 0):
        sys.stdout.write('  %*s | ' %(ndigits, '-0'))
    else:
        sys.stdout.write('  %*d | ' %(ndigits, int(close/10)))

def stem(data, scale=1, width=80, atom=1e-8):
    """/*
    *  R : A Computer Language for Statistical Data Analysis
    *  Copyright (C) 1995, 1996  Robert Gentleman and Ross Ihaka
    *  Copyright (C) 1997-2000   Robert Gentleman, Ross Ihaka and the
    *                            R Development Core Team
    #  This function ported to Python by Dent Earl, UCSC BME Dept. 2010
    *
    *  This program is free software; you can redistribute it and/or modify
    *  it under the terms of the GNU General Public License as published by
    *  the Free Software Foundation; either version 2 of the License, or
    *  (at your option) any later version.
    *
    *  This program is distributed in the hope that it will be useful,
    *  but WITHOUT ANY WARRANTY; without even the implied warranty of
    *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    *  GNU General Public License for more details.
    *
    *  You should have received a copy of the GNU General Public License
    *  along with this program; if not, a copy is available at
    *  http://www.r-project.org/Licenses/
    */
    """
    import math, sys
    if len(data) <= 1:
        return False
    data = sorted(data)
    if data[-1] > data[0]:
        r = atom + (data[-1] - data[0]) / scale
        c = 10.0**(11.0 - int(math.log10(r) + 10))
        mm = min(2, max(0, int(r * c / 25)))
        k = 3 * mm + 2 - 150 / (len(data) + 50)
        if (k - 1) * (k - 2) * (k - 5) == 0:
            c = c * 10.0
        x1 = abs(data[0])
        x2 = abs(data[-1]);
        if x2 > x1:
            x1 = x2;
        while(x1 * c > sys.maxint):
            c /= 10
        if k * (k - 4) * (k - 8) == 0:
            mu = 5
        if (k - 1) * (k - 5) * (k - 6) == 0:
            mu = 20
    else:
        r = atom + abs(data[0]) / scale;
        c = 10.0**(11.0 - int(math.log10(r) + 10))
        k = 2 #/* not important what   */
   
    mu = 10
    if (k * (k - 4) * (k - 8)) == 0:
        mu = 5
    if (k - 1) * (k - 5) * (k - 6) == 0:
        mu = 20
    
    # Find and print width of the stem.
    lo = math.floor(data[0]*c/mu)*mu
    hi = math.floor(data[-1] *c/mu)*mu
    ldigits = int(math.floor(math.log10(-lo))+1) if (lo < 0) else 0
    hdigits = int(math.floor(math.log10(hi))) if (hi > 0) else 0
    ndigits = int(hdigits) if (ldigits < hdigits) else ldigits
   
    # Starting cell
    if (lo < 0) and (math.floor(data[0]*c) == lo):
        lo = lo - mu
    hi = lo + mu
    if math.floor(data[0]*c+0.5) > hi:
        lo = hi
        hi = lo+mu
    # Print decimal info
    pdigits = 1 - math.floor(math.log10(c)+0.5)
    decStr = '\n  The decimal point is '
    if pdigits == 0:
        decStr = decStr + 'at the |\n'
    else:
        direction = 'right' if pdigits > 0 else 'left'
        decStr = decStr + '%d digit(s) to the %s of the |\n'%(pdigits, direction)
    print decStr
    i=0
    while True:
        if lo < 0:
            stem_print(int(hi), int(lo), ndigits)
        else:
            stem_print(int(lo), int(hi), ndigits)
        j=0
        while i < len(data):
            if data[i] < 0:
                xi = data[i]*c - .5
            else:
                xi = data[i]*c + .5
            if (hi == 0 and data[i] >=0) or (lo<0 and xi > hi) or (lo >= 0 and xi >=hi):
                break
            j += 1
            if (j<=width-12):
                sys.stdout.write('%d' %(abs(xi)%10))
            i += 1
        if j > width:
            sys.stdout.write('+%d' %(j-width))
        sys.stdout.write('\n')
        if i >=len(data):
            break
        hi += mu
        lo += mu
    sys.stdout.write('\n')
