import os
import re
from shutil import rmtree
from subprocess import check_output, call



################# GIF PROCESSING FUNCTIONS ##############################

# split_gif() Takes a path to a gif file and splits it into frames 
# saves the frames into png files in a subdirectory 
# generated from the filename. It returns the number of frames 
# in the gif file and a path to the individual png files

def split_gif_into_frames(path_to_gif_file):

    basename = os.path.basename(path_to_gif_file)
    directory = os.path.dirname(path_to_gif_file)
    filename_without_extension = basename.split('.')[0]

    output_directory = os.path.join(directory,filename_without_extension)

    os.mkdir(os.path.join(directory, filename_without_extension))

    # making call to imagemagick to convert gifs to individual frames
    call(['convert', path_to_gif_file, '-coalesce',
          os.path.join(output_directory, filename_without_extension+'_%d.png')])

    
    # calculates the number of frames in a gif using imagemagick
    get_count = check_output(['convert', path_to_gif_file+'[-1]', '-format', 
                              '"%[scene]"','info:'])

    # extracts and converts the frame count value from a string to an int
    frame_count = int(re.findall('\d+', get_count)[0])
    
    # returns the frame_count, frame_path and asset_name
    data = {'frame_count' : frame_count, 'frame_path' : output_directory,
            'asset_name': filename_without_extension }

    return data




# Takes the frame number(target) of the frame which will be the target 
# and a path to frame directory. renames the image files in the frame 
# directory to make the given frame the new first frame

def change_frame_order(target, path_to_frame_directory):

    basename = os.path.basename(path_to_frame_directory)
    file_directory = os.path.dirname(path_to_frame_directory)
    
    # creates a list of all the files in the directory
    dir_list = os.listdir(path_to_frame_directory)

    # clears the file list of hidden files
    for item in dir_list:
        if item.startswith("."):
            dir_list.remove(item)

    frame_directory = dir_list


    # sorts the directory by the digit after the underscore
    # the sort lambda does a regex to match the pattern '_number'
    # findall returns the list, so we take the result at index[0].
    # We truncate the underscore(_) from the result and convert 
    # the number string into an integer.
    frame_directory.sort(key=lambda frame: int(re.findall('_\d+', frame)[0][1:]))
    
    
    # Splits the frame directory in two
    first_half = frame_directory[:target]
    last_half = frame_directory[target:]

    # adds all frames behind the target to the end of the directory list
    reordered_frames = last_half+first_half
    
    
    temp_dir = os.path.join(file_directory,basename+'_temp')
    
    if os.path.exists(temp_dir):
        rmtree(temp_dir)

    os.mkdir(temp_dir)

    # renames the filenames to reflect the new order
    for index, value in enumerate(reordered_frames):
        os.rename(os.path.join(path_to_frame_directory, value), 
                  '%s/%s_%d.png' % (temp_dir, basename, index))
        
    rmtree(path_to_frame_directory)
    os.rename(temp_dir, path_to_frame_directory)



def convert_frames_to_mp4(path, basename):

    call(['ffmpeg','-y', '-r', '12', '-i', path+'/'+basename+'_%d.png',
          '-s', '640x360', '-vcodec' ,'libx264', 'data/'+basename+'.mp4'])
    
    return basename+'.mp4'


######################################################################
