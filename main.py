import cv2
from djitellopy import Tello
import time

# Initialize Tello
drone = Tello()
if not drone.connect():
    print("Failed to connect to drone.")
    exit(1)
drone.streamon()


# Helper function to detect obstacle direction
def detect_obstacle_direction(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    height, width = edges.shape
    left_region = edges[:, :width // 3]
    center_region = edges[:, width // 3: 2 * width // 3]
    right_region = edges[:, 2 * width // 3:]
    left_edge_count = cv2.countNonZero(left_region)
    center_edge_count = cv2.countNonZero(center_region)
    right_edge_count = cv2.countNonZero(right_region)
    total_edges = left_edge_count + center_edge_count + right_edge_count

    if total_edges > 3000:  # Adjust threshold as needed
        if center_edge_count > left_edge_count and center_edge_count > right_edge_count:
            return "front"
        elif left_edge_count > right_edge_count:
            return "left"
        else:
            return "right"
    return None


def main():
    drone.takeoff()
    time.sleep(2)

    try:
        while True:
            frame = drone.get_frame_read().frame
            if frame is None:
                print("No frame received.")
                continue

            direction = detect_obstacle_direction(frame)

            if direction == "left":
                print("Obstacle detected on the left! Moving right.")
                drone.move_right(20)
            elif direction == "right":
                print("Obstacle detected on the right! Moving left.")
                drone.move_left(20)
            elif direction == "front":
                print("Obstacle detected in front! Moving backward.")
                drone.move_back(20)
            else:
                print("No obstacle detected, moving forward.")
                drone.move_forward(20)

            time.sleep(2)  # Give time to complete movements

            cv2.imshow("Tello Camera", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"Error: {e}")

    finally:
        drone.land()
        cv2.destroyAllWindows()
        drone.streamoff()


main()
