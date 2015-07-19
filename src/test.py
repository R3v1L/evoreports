# -*- coding: utf-8 -*-
###############################################################################
# Author: (C) 2011 Oliver Gutiérrez <ogutsua@evosistemas.com>
# Module: evolabel
# Description: EVO Label generator test program
###############################################################################

# Python imports
import os, sys, tempfile

from labels import LabelMedia

from reportlab.lib.units import mm
from reportlab.graphics import barcode
from reportlab.graphics.barcode import code39 

class BarcodeLabelsAPLI_01287(LabelMedia):
    """
    Barcode labels class
    """
    
    product='APLI_01286'
    
    def gen_contents(self):
        # Generate barcode
        bc=barcode.createBarcodeDrawing('Standard93', value=sys.argv[1], barWidth=0.25*mm, barHeight=10*mm,checksum=0,humanReadable=True,fontSize=3*mm,fontName='Helvetica')
        #bc=code39.Extended39(sys.argv[1],barWidth=0.25*mm,barHeight=6*mm,checksum=0,humanReadable=True,fontSize=3*mm,fontName='Helvetica')
        #bc.
        return bc

a=BarcodeLabelsAPLI_01287()
f,fname=tempfile.mkstemp(suffix='.pdf')
a.write_pdf(fname,lines=True)
os.system('/usr/bin/xdg-open "%s"' % fname)
#os.system('/usr/bin/lpr "%s"' % fname)
