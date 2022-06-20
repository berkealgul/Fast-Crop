# Fast-Crop

This tool is for cropping and cutting videos

## Features
-Crop: you can select recreate video from roi using referance frame you also select 
-Cut: you can cut videos to process onyl some portion of the video

## How to use

First you need to run the cropper.py code with arguments

| Argument      | Description   | 
| ------------- |:-------------:| 
| (first argument) videoName.format        | Name of input video             |
| (optional last argument) videoName.format| Name of output video            |
| (optional)  -crop                        | Enable crop feature             |
| (optional)  -cut                         | Enable cut feature              |  
| (optional)  -fs                          | Select reference frame manually | 

For example command bellow is going to take example.mp4 video and outputs output.mp4 video with both features enable with manual frame selection

```
python cropper.py example.mp4 -crop -cut -fs output.mp4
```

After that you can follow command line instructions of the program
