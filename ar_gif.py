
import os
import uuid
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.renderers import render_to_response
from pyramid.view import view_config



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
    
    input_file.seek(0)
    while True:
        data = input_file.read(2<<16)
        if not data:
            break
        output_file.write(data)

    output_file.close()

    os.rename(temp_file_path, file_path)

    return Response('OK')



if __name__ == '__main__':
    config = Configurator()

    config.include('pyramid_jinja2')
    config.add_jinja2_search_path("ar_gif:templates")
    config.add_static_view(name='static', path='./static')

    config.scan()
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
    
