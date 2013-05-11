import os
import re
# import pkg_resources
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
    count_result = check_output(['convert', path_to_gif_file+'[-1]', '-format', 
                                 '"%[scene]"','info:'])

    # count_result example: '"30"\n'
    # extracts and converts the frame count value from a string to an int
    # The count calculated is an index, so we increment by one to get a count
    frame_count = int(re.findall('\d+', count_result)[0]) + 1
    

    # returns the frame_count, frame_path and asset_name
    data = {'frame_count' : frame_count,
            'asset_name': filename_without_extension }

    return data



def select_subset_of_frames(start_frame, end_frame, path_to_frame_directory, target=None):

    basename = os.path.basename(path_to_frame_directory)

    frames = os.listdir(path_to_frame_directory)

    # Deletes temporary files from the directory array
    for item in frames:
        if item.startswith("."):
            frames.remove(item)

    # Sample filename 07c15-39f70_0.png
    frames.sort(key=lambda frame: int(re.findall('_\d+', frame)[0][1:]))

    frames_iter = []
    frames_iter.extend(frames)

    subset = []

    # Remove all frames that *are not* between the start frame and the end frame
    if (start_frame < end_frame):
        subset = frames[start_frame:end_frame+1]
        for frame in frames_iter:
            if frame not in subset:
                os.remove(os.path.join(path_to_frame_directory, frame))
                frames.remove(frame)

    # Remove all frames that *are* between the end frame and the start frame
    #  (since we're wrapping)
    elif(start_frame > end_frame):
        subset = frames[end_frame+1:start_frame]
        for frame in frames_iter:
            if frame in subset:
                os.remove(os.path.join(path_to_frame_directory, frame))
                frames.remove(frame)

                
    # If a target parameter is specified, we set a new target 
    # the new target is the index of old target
    if (target != None ):
        
        new_target = subset.index('%s_%d.png' % (basename, target))

        return new_target



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

    
    # Splits the frame directory in two, based on target index
    first_half = frame_directory[:target]
    last_half = frame_directory[target:]

    # adds all frames behind the target to the end of the directory list
    reordered_frames = last_half+first_half

    temp_dir = os.path.join(file_directory, basename+'_temp')
    
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

    result = check_output(['identify', os.path.join(path+'/'+basename, basename+'_0.png')])

    # finds (length)x(width) pattern, takes the first result
    # and replaces all whitespace with empty strings
    ''' Replaced this code with the scale=640...
    image_size = re.findall(' \d+x\d+ ', result)[0].replace(' ', '')
    image_size = image_size.split('x')
    # converts items in image_size list to integers
    image_size = [int(dimension) for dimension in image_size]
    # turns all odd numbers to even in list
    image_size = [ value - 1 if value % 2 != 0 else value for value in image_size]
    image_size = "%dx%d" % (image_size[0], image_size[1])
    '''

    call([ 'ffmpeg','-y', '-r', '12' , 
           '-i', os.path.join(path+'/'+basename, basename+'_%d.png'), 
           '-vf' , "scale='640:trunc(ow/a/2)*2'", 
           '-vcodec' ,'libx264', 
           os.path.join(path, basename+'.m4v')
           ])
    
    return basename+'.m4v'


######################################################################
