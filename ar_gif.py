import os
import uuid
import json
import re
from utilities_ar_gif import split_gif, convert_frames_to_mp4

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
    filename = request.POST['gif'].filename

    input_file = request.POST['gif'].file


    if not os.path.exists('data'):
        os.mkdir('data')

    file_path = os.path.join('data/', '%s' % filename)
    temp_file_path = file_path + '~'
    output_file = open(temp_file_path, 'wb')
    
    while True:
        data = input_file.read(2<<16)
        if not data:
            break
        output_file.write(data)

    output_file.close()

    os.rename(temp_file_path, file_path)

    data = split_gif(filename)
    
    params = "?"
    for key in data.keys():
        params += key+"="+str(data[key])+"&"

        
    return HTTPFound('/display_frames/'+params)



@view_config(name="display_frames", request_method='GET')
def display_gif_frames(request):

    frame_count = range(int(request.GET['frame_count']))
    gif_dir = request.GET['gif_frame_path']
    file_basename = request.GET['file_basename']

    return render_to_response('choose_target.jinja2',
                              { 'frame_count':frame_count,
                                'gif_dir':gif_dir,
                                'file_basename':file_basename })


@view_config(name="convert", request_method="GET")
def convert(request):
    target = int(request.GET['frame'])
    basename = request.GET['basename']

    gif_dir = os.listdir(os.path.join("data", basename))
    gif_dir = sorted(gif_dir, key=lambda frame: int(re.findall('\d+', frame)[0]))

    gif_dir_a = gif_dir[:target]
    gif_dir_b = gif_dir[target:]
    gif_dir = gif_dir_b+gif_dir_a

    new_dir = basename+'_new'    
    os.mkdir(os.path.join('data',new_dir))

    for index, value in enumerate(gif_dir):
        os.rename(os.path.join('data', basename, value), 
                  'data/%s/%s%d.png' % (new_dir, basename, index) )
        
    os.rmdir(os.path.join('data', basename))

    convert_frames_to_mp4(new_dir, basename)

    return Response('OK')
    



if __name__ == '__main__':

    config = Configurator()

    config.include('pyramid_jinja2')
    config.add_jinja2_search_path("ar_gif:templates")
    config.add_static_view(name='static', path='./static')
    config.add_static_view(name='data', path='./data')

    config.add_route('display_frames','/display_frames/{data}')    

    config.scan()
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
    
