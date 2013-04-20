import os
import re
from subprocess import check_output, call



################# GIF PROCESSING FUNCTIONS ##############################

# split_gif() Takes a path to a gif file and splits it into frames 
# saves the frames into png files in a subdirectory 
# generated from the filename. It returns the number of frames 
# in the gif file and a path to the individual png files

def split_gif(gif_filename):
    
    basename = gif_filename.split('.')[0]

    split_gif_dir = os.path.join('data', basename+"_frames")


    if not os.path.exists(split_gif_dir):
        os.mkdir(split_gif_dir)

    call(['convert', gif_filename, '-coalesce',
          os.path.join(split_gif_dir, basename+'%d.png')])

    get_count = check_output(['convert', gif_filename+'[-1]', '-format', 
                              '"%[scene]"','info:'])


    frame_count = int(re.findall('\d+', get_count)[0])
    
    data = {'frame_count' : frame_count, 'gif_frame_path' : split_gif_dir }

    return data


def convert_gif_to_mp4():
    pass


######################################################################
