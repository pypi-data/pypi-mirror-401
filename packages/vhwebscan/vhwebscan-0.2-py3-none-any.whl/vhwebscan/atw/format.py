import os
import sys
import json

from vhwebscan.style              import Style

LIB_COMPONENTS              = "components"
LIST_COMPONENTS             = ["button", "text", "frame-blank", "block-blank", "image", "menu_horizontal", "menu_vertical", "input-content"]


class Format:
    def __init__(self, name : str):
        self.name           = name
        if not name:        raise Exception("Name is not found.")
        if not name in LIST_COMPONENTS: raise Exception("Name is not found.")
        # tạo đường dẫn tới template của đối tượng ATW.
        self.path           = os.path.realpath(os.path.join(LIB_COMPONENTS, f"{name}.json"))
        # đọc nội dung template
        with open(self.path, "r", encoding="utf-8") as fp:
            self.template : dict    = json.load(fp)


    def setAttribute(self, keys: list, value):
        if not isinstance(keys, list):  raise Exception("Parameter `keys` must be list.")
        try:
            # sao chép đối tương
            data                        = self.template.copy()
            # duyệt qua danh sách key
            for k in keys[:-1]: data    = data[k]
            # cập nhật lại dữ liệu cho key.
            if not keys[-1] in data.keys():     raise KeyError(f"{keys[-1]}")
            data[keys[-1]]      = value
        except KeyError as e:
            pass
            # sys.stderr.write(f"Error: key {str(e)} not found.{self.name}\n")
            # sys.stderr.flush()

    def getAttribute(self, keys: list):
        if not isinstance(keys, list):  raise Exception("Parameter `keys` must be list.")
        try:
            # sao chep shadow đối tượng
            data                    = self.template.copy()
            # duyệt qua danh sách key
            for k in keys:  data    = data[k]
            # trả về kết qua đọc dữ liệu.
            return data
        except KeyError as e:
            pass
            # sys.stderr.write(f"Error: key {str(e)} not found.\n")
            # sys.stderr.flush()

    def objects(self, obj: 'Format'):
        if isinstance(self.template['objects'], list):
            self.template['objects'].append(obj.template)

    
    def save(self, path: str):
        with open(path, 'w', encoding="utf-8") as fp:
            json.dump(self.template, fp, indent=4, ensure_ascii=False)

    def setStyle(self, style: Style):
        if self.name == "menu_horizontal":      return

        if self.name == "text":             name    = "text__wrapper"
        elif self.name == "image":          name    = "image__boundary--img"
        elif self.name == "input-content":  name    = "input-content__boundary"
        else:                               name    = self.name

        if style.background != None:
            if style.background.is_gradient:
                grd         = {
                    "gradient_type"     : style.background.gradient_type,
                    "background"        : "#8c52ff",
                    "value_range"       : style.background.gradient_range,
                    "gradient_check"    : True,
                    "value_parameter"   : style.background.gradient_parameter,
                    "gradient_arr"      : style.background.gradient_arr,
                    "gradient_direction": style.background.gradient_direction
                }
                self.setAttribute(["desktop_config", "background-color"], grd)
                self.setAttribute(["desktop_class", name, "background-image"], style.background.gradient)
            elif style.background.is_color:
                self.setAttribute(["desktop_class", name, "background-color"], style.background.color)
            elif style.background.is_image:
                self.setAttribute(["desktop_class", name, "background-image"], style.background.url)
        
        if style.border != None:

            if style.border.is_radius:
                self.setAttribute(["desktop_class", name, "border-top-left-radius"],       style.border.top_left_radius)
                self.setAttribute(["desktop_class", name, "border-top-right-radius"],      style.border.top_right_radius)
                self.setAttribute(["desktop_class", name, "border-bottom-left-radius"],    style.border.bottom_left_radius)
                self.setAttribute(["desktop_class", name, "border-bottom-right-radius"],   style.border.bottom_right_radius)

            if style.border.is_border:
                self.setAttribute(["desktop_class", name, "border-color"],                  style.border.color)
                self.setAttribute(["desktop_class", name, "border-style"],                  style.border.style)
                self.setAttribute(["desktop_class", name, "border-top-width"],              style.border.top_width)
                self.setAttribute(["desktop_class", name, "border-bottom-width"],           style.border.bottom_width)
                self.setAttribute(["desktop_class", name, "border-left-width"],             style.border.left_width)
                self.setAttribute(["desktop_class", name, "border-right-width"],            style.border.right_width)

            if style.padding.is_padding:
                if self.name in ["image", "button"]:            return
                elif self.name == "text":           name    = "text__content"

                self.setAttribute(["desktop_class", name, "padding-left"],                  style.padding.left)
                self.setAttribute(["desktop_class", name, "padding-right"],                 style.padding.right)
                self.setAttribute(["desktop_class", name, "padding-top"],                   style.padding.top)
                self.setAttribute(["desktop_class", name, "padding-bottom"],                style.padding.bottom)


    def find(self, key: str, data: dict = None) -> list:
        """
        Hàm `find` chức năng tìm kiếm đương dẫn tới key nếu có nếu ko có thì trả về danh sách rỗng
        
        Parameter
        ----------
        - `key`:        Tên trường cần tìm kiếm trong danh sách.

        Return
        -------
        Danh sách dường dẫn tới key ['A', 'key'] nếu ko có thì []
        """
        if data == None:    data        = self.template['desktop_class']
        # danh sách các trường tới key.
        path            = list()
        for k in data.keys():
            if k == key:
                path.append(k)
                return path
            else:
                value       = data[k]
                if isinstance(value, dict):
                    lst     = self.find(key, value)
                    if lst: 
                        path.append(k)
                        path.extend(lst)
                        return path
        return path