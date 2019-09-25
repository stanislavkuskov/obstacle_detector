import numpy
import time

from ctypes import *
from darknet_binding import \
    IMAGE, \
    rgbgr_image, \
    predict_image, \
    get_network_boxes, \
    do_nms_obj, \
    free_image, \
    free_detections, \
    load_net, \
    load_meta

from base import BaseThread


class Detector(BaseThread):
    def __init__(self, frame, **kwargs):
        super().__init__()
        model_parameters = {
            "config_path": b"models/yolov3.cfg",
            "weights_path": b"models/yolov3.weights",
            "data_path": b"models/coco.data"
        }

        model_parameters.update(kwargs)

        self._net = load_net(
            model_parameters["config_path"],
            model_parameters["weights_path"],
            0
        )
        self._meta = load_meta(model_parameters["data_path"])

        self._objects_dict = None
        self._thresh = .5
        self._hier_thresh = .5
        self._nms = .45

        self._frame = frame
        self._frame_timestamp = .0

    @staticmethod
    def __array_to_image(arr):
        arr = arr.transpose(2, 0, 1)
        c, h, w = arr.shape[0:3]
        arr = numpy.ascontiguousarray(arr.flat, dtype=numpy.float32) / 255.0
        data = arr.ctypes.data_as(POINTER(c_float))
        im = IMAGE(w, h, c, data)
        # need to return old values to avoid python freeing memory
        return im, arr

    @staticmethod
    def __convert_classes(class_name):
        converted_class_name = b'undefined'

        if class_name == b'person':
            converted_class_name = b'human'
        elif class_name == b'car' or class_name == b'truck' or class_name == b'train':
            converted_class_name = b'vehicle'
        elif class_name == b'sheep' or class_name == b'cow':
            converted_class_name = b'animal'

        return converted_class_name

    @property
    def __detect(self):
        frame_timestamp = self._frame_timestamp
        im, image = self.__array_to_image(self.frame)
        rgbgr_image(im)
        num = c_int(0)
        pnum = pointer(num)
        predict_image(self._net, im)
        dets = get_network_boxes(self._net, im.w, im.h, self._thresh,
                                 self._hier_thresh, None, 0, pnum)
        num = pnum[0]
        if self._nms:
            do_nms_obj(dets, num, self._meta.classes, self._nms)

        objects = []
        for j in range(num):
            a = dets[j].prob[0:self._meta.classes]
            if any(a):
                ai = numpy.array(a).nonzero()[0]
                for i in ai:
                    class_name = self.__convert_classes(self._meta.names[i])
                    b = dets[j].bbox
                    objects_dict = {
                        "class": class_name,
                        "probability": dets[j].prob[i],
                        "x": b.x,
                        "y": b.y,
                        "w": b.w,
                        "h": b.h
                    }
                    objects.append(objects_dict)


        if isinstance(image, bytes):
            free_image(im)
        free_detections(dets, num)

        full_objects_dict = {
            "frame_timestamp": frame_timestamp,
            "objects": objects
        }
        return full_objects_dict

    def run(self):
        while not self.is_stopped:
            x = time.time()
            self._objects_dict = self.__detect
            print(time.time()-x)
    @property
    def get_objects_dict(self):
        return self._objects_dict

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, value):
        self._frame = value

    @property
    def frame_timestamp(self):
        return self._frame

    @frame_timestamp.setter
    def frame_timestamp(self, value):
        self._frame_timestamp = value
