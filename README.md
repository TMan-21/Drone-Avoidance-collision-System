This project is structured using the Model-View-Controller (MVC) design pattern. It controls a Tello drone using the DJITelloPy library, processes video frames to detect obstacles, and makes movement decisions accordingly.
1. Model: drone_model.py
This file defines the DroneModel class, which handles drone operations, including movement and obstacle detection.

Key Functionalities
Initialization (__init__)

Connects to the Tello drone.
Starts video streaming.
takeoff()

Commands the drone to take off and waits for stability.
land()

Lands the drone, stops video streaming, and closes any open windows.
move(direction)

Moves the drone based on the detected obstacle direction.
Possible movements:
"left" → Move right
"right" → Move left
"front" → Move backward
"forward" → Continue moving forward
get_frame()

Retrieves the current video frame from the drone's camera.
detect_obstacle(frame)

Uses OpenCV to process the video frame:
Converts the frame to grayscale.
Applies Canny edge detection to find object boundaries.
Divides the frame into three regions (left, center, right).
Counts the number of edges in each region.
Determines where the obstacle is located:
Center has the most edges → Obstacle is in front.
Left has more edges → Obstacle is on the left.
Right has more edges → Obstacle is on the right.
2. View: drone_view.py
This file defines the DroneView class, which is responsible for displaying the drone’s camera feed.

Key Functionalities
display_frame(frame)
Opens a window to show the live video feed.
Listens for keyboard input (q) to close the video feed and stop the program.
3. Controller: drone_controller.py
This file defines the DroneController class, which manages the logic of the drone.

Key Functionalities
Initialization (__init__)

Creates an instance of DroneModel (for drone control).
Creates an instance of DroneView (for video display).
run()

Starts the drone's takeoff sequence.
Enters a loop where it:
Captures a video frame from the drone.
Detects if there is an obstacle.
Moves the drone based on obstacle detection:
Moves left if the obstacle is on the right.
Moves right if the obstacle is on the left.
Moves back if an obstacle is in front.
Moves forward if no obstacles are detected.
Displays the video feed.
Stops if the user presses 'q'.
if __name__ == "__main__":

Runs the DroneController when the script is executed.
