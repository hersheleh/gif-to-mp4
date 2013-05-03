from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    config.include('pyramid_jinja2')
    config.add_jinja2_search_path("gif_to_video:templates")

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('data', 'data')
    
    config.add_route('display_frames','/display_frames')
    config.add_route('download', '/download')

    config.scan()

    return config.make_wsgi_app()
