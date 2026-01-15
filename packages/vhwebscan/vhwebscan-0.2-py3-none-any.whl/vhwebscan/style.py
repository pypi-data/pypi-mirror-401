
DEG_TO_DIRECTION = {
    "180deg": "to top,",
    "0deg":   "to bottom,",
    "90deg":  "to right,",
    "270deg": "to left,",
    "135deg": "to bottom right,",
    "225deg": "to bottom left,",
    "45deg":  "to top right,",
    "315deg": "to top left,",
}

class Border:
    def __init__(self, d: dict = None):
        self.data                   = d

        self.color                  = ""
        self.style                  = ""
        self.top_width              = -1
        self.bottom_width           = -1
        self.left_width             = -1
        self.right_width            = -1

        self.bottom_left_radius     = -1
        self.bottom_right_radius    = -1

        self.top_left_radius        = -1
        self.top_right_radius       = -1

        self.is_radius              = False
        self.is_border              = False

        self.handle()

    def isValid(self):      return True if self.data else False

    def handle(self):
        for key in self.data.keys():
            value           = self.data[key]
            if key == "border-radius":
                self.is_radius              = True
                self.bottom_right_radius    = value
                self.bottom_left_radius     = value
                self.top_left_radius        = value
                self.top_right_radius       = value
            elif key == "border-top-right-radius":
                self.top_right_radius       = value
            elif key == "border-top-left-radius":
                self.top_left_radius        = value
            elif key == "border-bottom-right-radius":
                self.bottom_right_radius    = value
            elif key == "border-bottom-left-radius":
                self.bottom_left_radius     = value
            elif key == "border":
                try:
                    value                       = str(value)
                    if value == "none":         continue
                    width, style, color         = value.split(" ")
                except:
                    continue
                self.is_border              = True
                self.color                  = color
                self.style                  = style
                self.top_width              = width
                self.bottom_width           = width
                self.left_width             = width
                self.right_width            = width



class Background:
    def __init__(self, d: dict):
        self.data               = d

        self.color              = ""
        # này là gradient color
        self.gradient           = ""
        self.gradient_check     = False
        self.gradient_type      = ""
        self.gradient_background    = ""
        self.gradient_range     = 1
        self.gradient_parameter = 100
        self.gradient_arr       = list()
        self.gradient_direction = ""
        # này là hình ảnh.
        self.url                = ""

        self.is_color           = False
        self.is_image           = False
        self.is_gradient        = False

        self.handle()

    def handle(self):
        for k in self.data.keys():
            value : str         = self.data[k]

            if "gradient" in value:
                self.gradient   = value
                self.is_gradient = True
                self.gradient_check = True

                # linear-gradient / radial-gradient / conic-gradient
                self.gradient_type = value[:value.find("(")].strip()

                # nội dung trong ()
                content = value[value.find("(") + 1:value.rfind(")")]
                parts = [p.strip() for p in content.split(",")]

                # direction (nếu có)
                if parts[0].startswith("to "):
                    self.gradient_direction = parts[0] + ","
                    color_parts     = parts[1:]
                elif "deg" in parts[0]:
                    self.gradient_direction = DEG_TO_DIRECTION.get(parts[0])
                    color_parts     = parts[1:]
                else:
                    self.gradient_direction = ""
                    color_parts     = parts

                # chỉ lấy màu
                self.gradient_arr   = []
                for c in color_parts:
                    color           = c.split()[0]   # bỏ % nếu có
                    self.gradient_arr.append(color)

                self.gradient_background = value
            elif value.startswith("#") or value.startswith("rgb"):
                self.is_color       = True
                self.color          = value
            else:
                if k == "background-color":
                    self.is_color   = True
                    self.color      = value
                elif k == "background-image":
                    self.is_image   = True
                    self.url        = value
                else:
                    self.is_color   = True
                    self.color      = value


class Font:
    def __init__(self, d: dict):
        self.data           = d

        self.size           = -1
        self.family         = "inherit"
        self.weight         = ""
        self.color          = ""
        self.style          = ""

        self.handle()

    def handle(self):
        for k in self.data.keys():
            value           = self.data[k]
            if k == "font-size":
                self.size   = value
            elif k == "font-family":
                self.family = value
            elif k == "font-weight":
                self.weight = value
            elif k == "color":
                self.color  = value

class Padding:
    def __init__(self, d: dict):
        self.data           = d

        self.top            = -1
        self.bottom         = -1
        self.left           = -1
        self.right          = -1

        self.is_padding     = False

        self.handle()

    def handle(self):
        for k in self.data.keys():
            value           = self.data[k]
            if k == "padding":
                self.is_padding = True
                pad         = str(value).split(" ")
                length      = len(pad)

                if length   == 1:
                    self.top        = pad[0]
                    self.bottom     = self.top
                    self.left       = self.top
                    self.right      = self.top

                elif length == 2:
                    self.left       = pad[1]
                    self.top        = pad[0]
                    self.right      = self.left
                    self.bottom     = self.top
                elif length == 3:
                    self.top        = pad[0]
                    self.bottom     = pad[2]
                    self.left       = pad[1]
                    self.right      = self.left
                elif length == 4:
                    self.top        = pad[0]
                    self.right      = pad[1]
                    self.bottom     = pad[2]
                    self.left       = pad[3]

class Style:
    def __init__(self):
        self.background : Background    = None
        self.border : Border            = None
        self.font : Font                = None
        self.padding : Padding          = None
        self.other                      = dict()