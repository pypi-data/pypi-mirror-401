import os
import json

from vhwebscan.atw.format import Format

class AtwBlockBlank(Format):
    def __init__(self):
        super(AtwBlockBlank, self).__init__("block-blank")
    

    def desktop_postion(self, x: int, y: int, width: int, height: int, z_index: int = 1):
        position            = self.getAttribute(["desktop_position"])
        position['left']    = x
        position['top']     = y
        position['height']  = height
        position['width']   = width
        position['z_index'] = z_index
        # cập nhật lại thông tin
        self.setAttribute(["desktop_position"], position)

    def desktop_class(self, key: str, value):
        pass

    def desktop_config(self, key: str, value):
        pass
