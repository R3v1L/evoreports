# -*- coding: utf-8 -*-
###############################################################################
# Author: (C) 2011 Oliver Gutiérrez <ogutsua@evosistemas.com>
# Module: evoreports.labels
# Description: EVO Report generation labels module 
###############################################################################

# Python imports
import sys, os
import xml.dom.minidom

# Reportlab imports
from reportlab.pdfgen import canvas
from reportlab.lib import pagesizes
from reportlab.lib.units import mm,cm,inch

class LabelMedia(object):
    """
    Label media class
    """
    __supported_units=['mm','cm','inch']
    __supported_pagesizes=['A0','A1','A2','A3','A4','A5','A6','B0','B1','B2','B3','B4','B5','B6','LEGAL','LETTER']
    # Default product
    product=None
    
    def __init__(self,pagesize='A4',orientation='portrait',topmargin=0,leftmargin=0,rightmargin=0,bottommargin=0,
                 hlabels=2,vlabels=8,horizmargin=0,vertmargin=0,
                 units='mm',name='EVOLabel Custom label',provider='EVOLabel',model='Custom',
                 product=None):
        """
        Class initialization
        """
        if product:
            self.product=product
        if self.product:
            self.__load_product_definition()
        else:
            self.name=name
            self.provider=provider
            self.model=model
            self.units=self.__get_units(units)
            self.pagesize=self.__get_page_size(pagesize,orientation)
            self.hlabels=hlabels
            self.vlabels=vlabels
            self.top=topmargin*self.units
            self.left=leftmargin*self.units
            self.right=rightmargin*self.units
            self.bottom=bottommargin*self.units
            self.horiz=horizmargin*self.units
            self.vert=vertmargin*self.units
        # Calculate label size
        self.labelwidth=(self.pagesize[0]-(self.left+self.right +(self.hlabels-1)*self.horiz))/self.hlabels
        self.labelheight=(self.pagesize[1]-(self.top+self.bottom +(self.vlabels-1)*self.vert))/self.vlabels

    def __get_units(self,units):
        """
        Get units constant for specified unit name
        """
        if units in self.__supported_units:
            if units=='mm':
                return mm
            elif units=='cm':
                return cm
            elif units=='inch':
                return inch
        return mm
    
    def __get_page_size(self,size,orientation):
        """
        Get page size for a given page size and orientation orientation
        """
        ps=pagesizes.A4
        if size in self.__supported_pagesizes:
            ps=getattr(pagesizes,size)
        if orientation=='landscape':
            return (ps[1],ps[0])
        return (ps[0],ps[1])

    def __load_product_definition(self):
        """
        Loads a product definition file
        """
        # Search product definition file in python path
        filename=None
        for path in sys.path:
            if os.path.isfile(path + '/evoreports/label_definitions/' + self.product + '.xml' ):
                filename=path + '/evoreports/label_definitions/' + self.product + '.xml'
        if not filename:
            raise IOError('Product file %s.xml not found' % self.product)
        # Parse XML file
        prod=xml.dom.minidom.parse(filename).documentElement
        # Get product information
        self.name=prod.getAttribute('name')
        self.provider=prod.getAttribute('provider')
        self.model=prod.getAttribute('model')
        # Get media information
        media=prod.getElementsByTagName('media')[0]
        self.pagesize=self.__get_page_size(media.getAttribute('size'),media.getAttribute('orientation'))
        self.orientation=media.getAttribute('orientation')
        self.units=self.__get_units(media.getAttribute('units'))
        # Get labels information
        labels=prod.getElementsByTagName('labels')[0]
        self.hlabels=int(labels.getAttribute('horiz'))
        self.vlabels=int(labels.getAttribute('vert'))
        # Get margin information
        margins=prod.getElementsByTagName('margins')[0]
        self.top=float(margins.getAttribute('top'))*self.units
        self.left=float(margins.getAttribute('left'))*self.units
        self.right=float(margins.getAttribute('right'))*self.units
        self.bottom=float(margins.getAttribute('bottom'))*self.units
        self.horiz=float(margins.getAttribute('horiz'))*self.units
        self.vert=float(margins.getAttribute('vert'))*self.units

    def __draw(self,c,lines,linewidth):
        """
        Draws the labels
        """
        # Draw label contents
        self.__draw_contents(c)
        # Draw label lines
        if lines:
            self.__draw_lines(c,linewidth)
        
    def __draw_contents(self,c):
        """
        Draw label contents
        """
        for x in range(self.hlabels):
            for y in range(self.vlabels):
                xpos=self.left+x*self.labelwidth
                ypos=self.top+y*self.labelheight
                self.draw_contents(c,xpos,ypos,self.labelwidth,self.labelheight)

    def gen_contents(self):
        """
        Content generation for drawing on each label
        """
        raise NotImplementedError('You must override the gen_contents method')

    def __draw_lines(self,c,linewidth):
        """
        Draw label lines
        """
        # Set line width
        c.setLineWidth(linewidth*mm)
        # Draw horizontal label boundaries
        left=self.left
        c.line(left,self.top,left,self.pagesize[1]-self.top)
        for i in range(self.hlabels):
            left+=self.labelwidth
            c.line(left,self.top,left,self.pagesize[1]-self.top)
            if self.horiz > 0 and i<self.hlabels-1:
                left+=self.horiz
                c.line(left,self.top,left,self.pagesize[1]-self.top)
        # Draw vertical label boundaries
        top=self.top
        c.line(self.left,top,self.pagesize[0]-self.left,top)
        for i in range(self.vlabels):
            top+=self.labelheight
            c.line(self.left,top,self.pagesize[0]-self.left,top)  
            if self.vert > 0 and i<self.vlabels-1:
                top+=self.vert
                c.line(self.left,top,self.pagesize[0]-self.left,top)          
        
    def write_pdf(self,filename,lines=False,linewidth=0.1):
        """
        Writes a pdf file with labels
        """
        c=canvas.Canvas(filename,pagesize=self.pagesize)
        self.__draw(c,lines=lines,linewidth=linewidth)
        c.showPage()
        c.save()

        