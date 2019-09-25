import cv2
from base import BaseThread


class Visualizer(BaseThread):
    def __init__(self, frame):
        super().__init__()
        self.frame = frame
        self.objects_dict = None

    def run(self):
        while not self.is_stopped:
            if self.objects_dict:
                detected_objects = self.objects_dict["objects"]
                for detected_object in detected_objects:
                    x, y, w, h = detected_object["x"],\
                                 detected_object["y"],\
                                 detected_object["w"],\
                                 detected_object["h"], \

                    xmin = int(x - w/2)
                    xmax = int(x + w/2)
                    ymin = int(y - h/2)
                    ymax = int(y + h/2)

                    pt1 = (xmin, ymin)
                    pt2 = (xmax, ymax)
                    cv2.rectangle(self.frame, pt1, pt2, (0, 255, 0), 2)
                    cv2.putText(
                        self.frame,
                        detected_object["class"].decode() +
                        " [" +
                        str(round(detected_object["probability"] * 100, 1)) +
                        "]",
                        (pt1[0], pt1[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0, 255, 0], 1)
            cv2.imshow("frame", self.frame)
            if cv2.waitKey(1) == ord("q"):
                self.is_stopped = True

    @property
    def return_objects_dict(self):
        return self.objects_dict

    @return_objects_dict.setter
    def return_objects_dict(self, value):
        self.objects_dict = value