# Difference in position calculator

Here is example of calculation pose difference based on two images (frames).

Program based on:
  - optical flow Lucas-Kanade algo; 
  - finding essential matrix using RANSAC;
  - recovering essential matrix and getting two matrices: translation and rotation;
  - getting angles from rotation matrix using Rodrigues algo.

On the picture you can see current frame from my webcam with drawing line which show trajectory of tracking features. In the console on each iteration (separated by empty lines) represented two matrices: rotation (andgles) and translation.

![Example](https://github.com/exotikh3/pose_difference_calculator/blob/master/screen.png)

> PLEASE, PAY ATTENTION!
> Due to specialities of RANSAC algo you need to have no less than 5 tracking points in frame. In other way you will have exception "ShapeError". 
