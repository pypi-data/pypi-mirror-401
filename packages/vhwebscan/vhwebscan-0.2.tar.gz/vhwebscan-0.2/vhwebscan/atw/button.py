import os
import json

from vhwebscan.atw.format         import Format

class AtwButton(Format):
    def __init__(self):
        super(AtwButton, self).__init__("button")

    def desktop_position(self, x: int, y: int, w: int, h: int, z_index: int):
        position            = self.getAttribute(["desktop_position"])
        position['left']    = x
        position['top']     = y
        # cập nhật lại thông tin
        self.setAttribute(["desktop_position"], position)

    def setText(self, text: str):
        self.setAttribute(["staticdata", "content"], text)

    def setStyle(self, style):
        super().setStyle(style)
        if style.font != None:
            content         = self.getAttribute(["desktop_class", "button__content"])
            color           = self.getAttribute(["desktop_class", "button", "color"])
            font_weight     = self.getAttribute(["desktop_class", "button", "font-weight"])

            font_size       = content['font-size'] if style.font.size == -1 else style.font.size
            font_family     = content['font-family'] if style.font.family == '' else style.font.family
            color           = color if style.font.color == "" else style.font.color
            font_weight     = font_weight if style.font.weight == "" else style.font.weight

            self.setAttribute(["desktop_class", "button__content", "font-size"], font_size)
            self.setAttribute(["desktop_class", "button__content", "font-family"], font_family)
            self.setAttribute(["desktop_class", "button", "color"], color)
            self.setAttribute(["desktop_class", "button", "font-weight"], font_weight)