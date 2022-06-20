# Fast-Crop

This tool is for cropping and cutting videos

## Features
- Crop: you can extract roi of video  
<img src="/images/fractal_trees.png" alt="olcft" width="500">
- Cut: you can cut videos to process only some portion of the video
<img src="/images/fractal_trees.png" alt="olcft" width="500">
- Reference frame: Select reference frame of roi selection

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
- If you dont give -fs argument the first frame of the video is going to be used as reference frame for roi selection
- Currently it is working with mp4 and xvid codecs
- Double click to select roi corners
