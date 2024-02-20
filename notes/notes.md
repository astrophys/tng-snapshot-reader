<!--
Compile :
    pandoc -f markdown notes/somefile.md - -filter pandoc-crossref -t latex -o somefile.pdf

Notes:
    1. http://lierdakil.github.io/pandoc-crossref/
    #. On over/under braces : https://tex.stackexchange.com/a/132527/84495
-->


<!--
    YAML section
-->
---
title: Notes on developing tng-snapshot-reader
author: Ali Snedden
date: 2024-02-01
abstract:
...
---
header-includes:
  - \hypersetup{colorlinks=true,
            urlcolor=blue,
            pdfborderstyle={/S/U/W 1}}
    \usepackage{mathtools}
    \usepackage{cancel}
---
\definecolor{codegray}{gray}{0.9}
\newcommand{\code}[1]{\colorbox{codegray}{\texttt{#1}}}
<!-- \let\overbracket\overbracket[0.2mm][0.6mm]{#1}      not sure that this works -->

\maketitle
\tableofcontents
\pagebreak


13-feb-2024 :
======================================
1. Cleaned up duplicate files in top level dir on CRC
    a) There are copies in output/
        #. star_snap_135_nvox_100.pkl
        #. dm_snap_135_nvox_100.pkl
        #. gas_snap_135_nvox_100.pkl
#. In previous commits, I'd started adding the ability to output the halos in a format
   that Disperse would like. 
    a) This is a non-starter b/c I had real difficulty getting CGAL built so I can
       actually run his code. This is a nightmare b/c the software is so old that it
       is going to be darn near impossible to rebuild
        #. Likely will turn into dependency hell
#. Also, I'd like to build the ability to see what kind of halos are in what kind
   of structure. 
    a) First pass using plot.py, doesn't seem promising
        #. Ran w/
            * python -m pdb src/collate_segmentation_results.py --data snap_099/data/halo_pos_mass.npz  --vessels /afs/crc.nd.edu/group/phillips/software/SEGMENT_das/2.0/data/2almost3_donut_matlab_int.txt --clusters snap_099/output/clusters/vesselness.txt --voids snap_099/output/voids/vesselness.tx
            * Takes 5-10 min to run, so iteration time is terrible, I need a smaller 
              set to work on.
            * The halos don't take much time to read, but the 600^3 volumes do
        #. See : segmentation_with_halos.png
            * The axis need flipped, but still looks like bad
            * I wonder if this is a bug on the segmentation part or if its the
              visualization part
#. Let's read in both the halos and gas and hold side-by-side to see that they
   make sense
    a) Did this with src/plot_halo_pos_mass_npz.py
    #) Turns out that plotting subDF['x'], subDF['y'] (halos) maps exactly to 
       np.sum(density[0:gasthresh,:,:], axis=0)
        #. CONCLUSION : Yes my axis are flipped. 
            * See halo_vs_gas_npsum_axis0.jpg
            * From the meeting today, in fact that was done intentionally, the axis
              are ordered by z,x,y


20-feb-2024 :
======================================
1. Trying to adjust my code st G and M can see what I'm referring to


