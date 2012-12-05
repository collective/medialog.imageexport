# coding: utf-8

# Python imports
import os
import tempfile
import zipfile
#import types

#from zope import interface
#from zope import component
#from Products.CMFPlone import utils
#from zope.interface import implements
#from Acquisition import aq_inner
#from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#from Products.CMFPlone.utils import getToolByName
from Products.Five import BrowserView
from tempfile import TemporaryFile


class Exporter(BrowserView):
    
    def __init__(self, context, request):
        super(Exporter, self).__init__(context, request)

    
    def __call__(self,REQUEST):
        '''Returns the file (with the preview images
        '''
        imagesize = self.request.get('imagesize', 'preview')  #Using preview if nothing is specified
        
    
        # Write ZIP archive
        zip_filename = tempfile.mktemp()
        ZIP = zipfile.ZipFile(zip_filename, 'w')

        for obj in self.context.getFolderContents():
            obj = obj.getObject()
            #imageformat is image/jpg so we are skipping the first part
            #this leaves us with png / jpg / gif or something else.
            imageformat = obj.getContentType()
            imageformat = imageformat.split("/")
            image_suffix = imageformat[1]
            if image_suffix == 'jpeg':
                image_suffix = 'jpg'
            
            if obj.portal_type == 'Image':
                # export one scale
                #unfortunately, I dont know the format.
                #Guessing on jpg
                full_image_name = obj.getId() + '.' + image_suffix
                img = obj.Schema().getField('image').getScale(obj,scale=imagesize)
                ZIP.writestr(self.context.getId() + '/' + full_image_name, str(img.data))
        
        ZIP.close()
        data = file(zip_filename).read()
        os.unlink(zip_filename) 
        R = self.request.RESPONSE
        R.setHeader('content-type', 'application/zip')
        R.setHeader('content-length', len(data))
        R.setHeader('content-disposition', 'attachment; filename="%s.zip"' % self.context.getId())
        return R.write(data) 




    
    
    

