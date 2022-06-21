# Video-Cropper

This tool is for cropping and cutting videos

## Features
- Crop: you can extract roi of videos
<img src="/doc/roi.png" alt="olcft" width="500">
- Cut: you can cut videos to process only some portion of the videos
<img src="/doc/cut.png" alt="olcft" width="500">
- Reference frame: Select reference frame for roi selection
<img src="/doc/fs.png" alt="olcft" width="500">

## How to use

First you need to run the cropper.py code with arguments

| Argument      | Description   | 
| ------------- |:-------------:| 
| (first argument) videoName.format        | Name of input video             |
| (optional last argument) videoName.format| Name of output video            |
| (optional)  -crop                        | Enable crop feature             |
| (optional)  -cut                         | Enable cut feature              |  
| (optional)  -fs                          | Select reference frame manually for roi selection | 

For example command bellow is going to take example.mp4 video and outputs output.mp4 video with both features enable with manual frame selection
```
python cropper.py example.mp4 -crop -cut -fs output.mp4
```
After that you can follow command line instructions of the program

#### Notes
- While selecting roi rectange, you must select the <b>upper-left corner first then select the bottom right corner</b>
- If you dont give -fs argument the first frame of the video is going to be used as reference frame for roi selection
- Currently it is working with mp4 and xvid codecs and tested with .mp4 and .avi files 
- Double click to select roi corners
- If output name is not given, the program picks default name for output video to avoid overriding the original data
