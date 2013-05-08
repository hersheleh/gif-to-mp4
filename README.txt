gif_to_video README

There are a couple of program that this app requires for installation

It relies on a command line version of FFmpeg and Imagemagick to work. 
You also need to install the libx264 codec

On Mac: 
   You can simply install the packaged version of FFmpeg.
   I installed it with Homebrew
   The brew version of imagemagick should also suffice

On Ubuntu:
   On ubuntu you need to install the libavcodec-extra-53 package to 
   to get libx264 to run. I also installed the other libx264 packages
   for safety:

   Run:
      sudo apt-get install ffmpeg x264 libx264-dev libavcodec-extra-53
      sudo apt-get install imagemagick

