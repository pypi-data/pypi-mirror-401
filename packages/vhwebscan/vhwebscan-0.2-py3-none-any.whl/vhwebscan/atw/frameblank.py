import os
import json

from vhwebscan.atw.format import Format


class AtwFrameBlank(Format):
    def __init__(self):
        super(AtwFrameBlank, self).__init__("frame-blank")
        

    def desktop_postion(self, x: int, y: int, width: int, height: int, z_index: int = 1):
        position            = self.getAttribute(["desktop_position"])
        position['left']    = x
        position['top']     = y
        position['height']  = height
        position['width']   = width
        position['z_index'] = z_index
        # cập nhật lại thông tin
        self.setAttribute(["desktop_position"], position)
        # câp nhật 2 thuộc tính width và min-height ở trường desktop-class
        self.setAttribute(["desktop_class", "frame-blank", "width"], width)
        self.setAttribute(["desktop_class", "frame-blank", "min-height"], height)

    def desktop_class(self, key: str, value):
        pass

    def desktop_config(self, key: str, value):
        pass