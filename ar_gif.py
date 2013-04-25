import os
import uuid
import json
import re

from zipfile import ZipFile
from utilities_ar_gif import split_gif_into_frames, convert_frames_to_mp4, change_frame_order
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.renderers import render_to_response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound



@view_config()
def home(request):
    return render_to_response('gif_upload_form.jinja2', {})



@view_config(name="uploaded_gif", request_method="POST")
def handle_uploaded_gif_file(request):
    
    uploaded_filename = request.POST['gif'].filename

    input_file = request.POST['gif'].file

    new_filename = '%s.gif' % uuid.uuid4()

    # creates the data directory to serve static data
    if not os.path.exists('data'):
        os.mkdir('data')

    # creates a temporary file
    # 
    file_path = os.path.join('data/', new_filename)
    temp_file_path = file_path + '~'
    output_file = open(temp_file_path, 'wb')
    

    while True:
        data = input_file.read(2<<16)
        if not data:
            break
        output_file.write(data)

    output_file.close()

    os.rename(temp_file_path, file_path)

    data = split_gif_into_frames('data/'+new_filename)
    
    params = "?"
    for key in data.keys():
        params += key+"="+str(data[key])+"&"

        
    return HTTPFound('/display_frames/'+params)




@view_config(name="display_frames", request_method='GET')
def display_frames(request):

    frame_count = range(int(request.GET['frame_count']))
    frame_path = request.GET['frame_path']
    asset_name = request.GET['asset_name']

    return render_to_response('choose_target.jinja2',
                              { 'frame_count':frame_count,
                                'frame_path':frame_path,
                                'asset_name':asset_name })




@view_config(name="convert", request_method="GET")
def convert(request):
    
    target = int(request.GET['frame'])
    basename = request.GET['basename']

    change_frame_order(target, 'data/'+basename)

    mp4_file = convert_frames_to_mp4('data/'+basename, basename)
    target = os.path.join('data',basename,basename+"_0.png")

    zip_file = ZipFile('data/'+basename+'.zip', 'w')
    zip_file.write('data/'+mp4_file, arcname=mp4_file)
    zip_file.write(target, arcname=basename+'0.png')
    
    return Response("/download/?zip=/data/"+basename+'.zip')
    


@view_config(name='download', request_method='GET')
def download(request):
    
    zip_file = request.GET['zip']
    
    return render_to_response('download_zip.jinja2', { 'zip_file' : zip_file })



if __name__ == '__main__':

    config = Configurator()

    config.include('pyramid_jinja2')
    config.add_jinja2_search_path("ar_gif:templates")
    config.add_static_view(name='static', path='./static')
    config.add_static_view(name='data', path='./data')

    config.add_route('display_frames','/display_frames')
    config.add_route('download', '/download')

    config.scan()
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
    
