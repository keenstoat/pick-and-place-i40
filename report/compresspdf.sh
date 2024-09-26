#!/usr/bin/env bash

gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/default \
-dNOPAUSE  -dBATCH \
-sOutputFile=report-compressed.pdf report.pdf

rm report.pdf