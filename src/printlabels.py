#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# Author: (C) 2011 Oliver Gutiérrez <ogutsua@evosistemas.com>
# Module: evolabel
# Description: EVO Label generator program
###############################################################################

# Python imports
import os, sys, tempfile

from labels import LabelMedia

from reportlab.graphics import barcode
from reportlab.lib.units import mm

class BarcodeLabelsAPLI_01286(LabelMedia):
    """
    Barcode labels class
    """    
    product='APLI_01286'

    def __init__(self,ref,desc,bctype,code):
        LabelMedia.__init__(self)
        self.ref=ref
        self.bctype=bctype
        self.code=code
        self.desc=desc

    def draw_contents(self,c,xpos,ypos,width,height):
        # Generate barcode
        bc=barcode.createBarcodeDrawing('Extended93',width=width, height=40, value=self.code,checksum=0,humanReadable=True,fontSize=2*mm,fontName='Helvetica')    
        bc.drawOn(c,xpos,ypos+5*self.units)
        c.setFont("Helvetica", 6)
        c.drawCentredString(xpos+width/2, ypos+23*self.units,self.ref)
        c.setFont("Helvetica", 4)
        c.drawCentredString(xpos+width/2, ypos+20*self.units,self.desc)



args=''
for arg in sys.argv[1:]:
    args+=arg

parms=args.split('#$-@-$#')
a=BarcodeLabelsAPLI_01286(*parms)

f,fname=tempfile.mkstemp(suffix='.pdf')
a.write_pdf(fname,lines=True)
#os.system('/usr/bin/xdg-open "%s"' % fname)
os.system('/usr/bin/lpr "%s"' % fname)
