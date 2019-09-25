import cv2

from streamer import Streamer
from visualizer import Visualizer
from detector import Detector
from publisher import Publisher


SOURCE = 1
PORT = "5555"
TOPIC = "obstacle_detector"
FRAME_SIZE = (960, 640)

streamer = Streamer(SOURCE)
streamer.start()

visualizer = Visualizer(streamer.frame)
visualizer.start()

detector = Detector(streamer.frame)
detector.start()

publisher = Publisher(port=PORT, topic=TOPIC)
publisher.start()

while True:
    if streamer.is_stopped or visualizer.is_stopped:
        streamer.stop()
        visualizer.stop()
        detector.stop()
        publisher.stop()
        break

    # get frame from streamer
    frame, frame_timestamp = streamer.get_frame_and_timestamp
    # resize frame to yolov3.cfg input size
    resized = cv2.resize(frame, FRAME_SIZE)

    # update frame and frame timestamp in detector
    detector.frame = resized
    detector.frame_timestamp = frame_timestamp

    # get detected objects dict from detector
    objects_dict = detector.get_objects_dict
    # update objects dict into publisher for publishing messages with detected objects into network
    publisher.objects_dict = objects_dict

    visualizer.frame = resized
    visualizer.objects_dict = objects_dict
