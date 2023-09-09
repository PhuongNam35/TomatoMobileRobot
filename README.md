# TomatoMobileRobot
Project Overview Description:
The objective of this project is to design a mobile robot that navigates to each location of tomato plants in a field, stops, captures images, and employs the YOLOv8 deep learning model to recognize how many ripe fruits are on the captured plant, whether it is healthy, and if any leaves are diseased (two types of diseases trained in the model are Early Blight and Late Blight). The robot then proceeds to traverse all the planted rows and returns to its initial starting position.

Due to limited hardware resources (utilizing a Raspberry Pi 4 with 1GB of RAM), the image prediction and web display processes are performed on a personal laptop. The Raspberry Pi's sole task is to receive image capture commands from the controller and send them to the web, where the images are subsequently processed.

The website is created using the Flask framework, with the source code attached. The web serves three primary functions:
- Receives images sent from the Raspberry Pi through an upload function and stores the received images in the framework's static folder.
- Displays the results after analysis using YOLOv8, performed in the get_images function, and counts the number of detected objects.
- Provides information about the project and ongoing developments such as viewing videos recorded by the robot and access statistics.
