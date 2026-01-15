from vhwebscan.atw.format         import Format

class AtwInput(Format):
    def __init__(self):
        super(AtwInput, self).__init__("input-content")

    def desktop_position(self, x: int, y: int, w: int, h: int, z_index: int):
        position            = self.getAttribute(["desktop_position"])
        position['left']    = x
        position['top']     = y
        position['z_index'] = z_index
        # cập nhật lại thông tin
        self.setAttribute(["desktop_position"], position)
        self.setAttribute(["desktop_class", "input-content__boundary", "width"],    f"{w}px")
        self.setAttribute(["desktop_class", "input-content__boundary", "hegiht"],   f"{h}px")
        self.setAttribute(["desktop_config", "dimension"],  {"width": w, "height": h})

    def setText(self, text: str):
        self.setAttribute(["staticdata", "content"], text)

    def setStyle(self, style):
        super().setStyle(style)
        if style.font != None:
            try:
                content         = self.getAttribute(["desktop_class", "input-content__boundary"])
                color           = self.getAttribute(["desktop_class", "input-content__boundary", "color"])
                font_weight     = self.getAttribute(["desktop_class", "input-content__boundary", "font-weight"])

                
                font_size       = content['font-size'] if style.font.size == -1 else style.font.size
                font_family     = content['font-family'] if style.font.family == '' else style.font.family
                color           = color if style.font.color == "" else style.font.color
                font_weight     = font_weight if style.font.weight == "" else style.font.weight

                self.setAttribute(["desktop_class", "input-content__boundary", "font-size"], font_size)
                self.setAttribute(["desktop_class", "input-content__boundary", "font-family"], font_family)
                self.setAttribute(["desktop_class", "input-content__boundary", "color"], color)
                self.setAttribute(["desktop_class", "input-content__boundary", "font-weight"], font_weight)
            except KeyError:
                print(content, self.path)