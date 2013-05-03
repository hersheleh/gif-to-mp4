import os
import uuid
import json
import re
import pkg_resources
from zipfile import ZipFile
from utilities_ar_gif import split_gif_into_frames, convert_frames_to_mp4, change_frame_order, select_subset_of_frames

from pyramid.response import Response
from pyramid.renderers import render_to_response
from pyramid.view import view_config

from pyramid.httpexceptions import HTTPFound

''' 
These views handle stuff
'''


'''
@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'gif_to_video'}
'''

@view_config()
def home(request):
    return render_to_response('gif_upload_form.jinja2', {})

# This view handles an uploaded file
# it expects the file posted to be called gif. 
@view_config(name="uploaded_gif", request_method="POST")
def handle_uploaded_gif_file(request):
    
    uploaded_filename = request.POST['gif'].filename

    input_file = request.POST['gif'].file

    new_filename = '%s.gif' % uuid.uuid4()

    # creates the data directory to serve static data
    data_path = pkg_resources.resource_filename('gif_to_video', 'data')
    if not os.path.exists(data_path):
        os.mkdir(data_path)

    # creates a temporary file
    file_path = os.path.join(data_path, new_filename)
    temp_file_path = file_path + '~'
    output_file = open(temp_file_path, 'wb')
    

    while True:
        data = input_file.read(2<<16)
        if not data:
            break
        output_file.write(data)

    output_file.close()

    os.rename(temp_file_path, file_path)

    data = split_gif_into_frames(file_path)
    
    params = "?"
    for key in data.keys():
        params += key+"="+str(data[key])+"&"
        
    return HTTPFound('/display_frames/'+params)



@view_config(name="display_frames", request_method='GET')
def display_frames(request):

    frame_count = range(int(request.GET['frame_count']))
    asset_name = request.GET['asset_name']

    return render_to_response('frames.jinja2',
                              { 'frame_count':frame_count,
                                'asset_name':asset_name })



@view_config(name="subset", request_method="POST")
def convert_subset(request):
    
    target = int(request.POST['frame'])
    basename = request.POST['basename']
    start_frame = int(request.POST['start_frame'])
    end_frame = int(request.POST['end_frame'])
    
    
    data_path = pkg_resources.resource_filename('gif_to_video', 'data')
    asset_path = os.path.join(data_path, basename)

    new_target = select_subset_of_frames(start_frame, end_frame, asset_path, target)

    return HTTPFound("/convert?frame=%s&basename=%s" % (new_target, basename) )



@view_config(name="convert", request_method="GET")
def convert(request):
    
    target = int(request.GET['frame'])
    basename = request.GET['basename']


    data_path = pkg_resources.resource_filename('gif_to_video', 'data')
    asset_path = os.path.join(data_path, basename)

    change_frame_order(target, asset_path)

    mp4_file = convert_frames_to_mp4(asset_path, basename)
    target = os.path.join(asset_path, basename+"_0.png")

    zip_file = ZipFile(asset_path+'.zip', 'w')
    zip_file.write(os.path.join(data_path, mp4_file), arcname=mp4_file)
    zip_file.write(target, arcname=basename+'0.png')
    
    return Response("/download/?zip=/data/"+basename+'.zip')



@view_config(name='download', request_method='GET')
def download(request):
    
    zip_file = request.GET['zip']
    
    return render_to_response('download_zip.jinja2', { 'zip_file' : zip_file })

