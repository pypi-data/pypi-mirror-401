import os
import json
import random
import string

from vhwebscan.role           import RoleMenuItem, RoleMenu
from vhwebscan.atw.format     import Format

# menu Item
# {
#     "type": "link-page",
#     "group": "link",
#     "groups": [
#         "link",
#         "category",
#         "pop-up"
#     ],
#     "click_action": "scroll_to_top",
#     "scroll_block_id": "",
#     "name_vn": "Trang chủ",
#     "children": [],
#     "level": 0,
#     "_id": "f538"
# }

# SubItem
# {
#     "type": "none",
#     "groupParent": "link",
#     "name": "Menu cấp 1",
#     "id_page_category": null,
#     "level": 1,
#     "_id": "6XJbjmDEe79lXs6W4gzIE8L5",
#     "children": [
#         {
#             "type": "none",
#             "name": "Menu cấp 2",
#             "id_page_category": null,
#             "level": 2,
#             "_id": "nDLdKeQCnzm3Oo8zJj1SXGvv",
#             "children": []
#         }
#     ]
# }

class AtwMenuItem:
    def __init__(self, role: RoleMenuItem):
        self.id             = self.genId()
        self.role           = role

    def __iter__(self):
        yield "_id",        self.id
        yield "type",       "none"
        yield "group",      "link"
        yield "groups",     [
            "link",
            "category",
            "pop-up"
        ]
        yield "name_vn",            self.role.name
        yield "children",   []
        yield "level",      0

    def genId(self) -> str:
        chars       = string.ascii_lowercase + string.digits
        result      = ''.join(random.choices(chars, k=4))

        return result


class AtwMenuHorizontal(Format):
    def __init__(self):
        super(AtwMenuHorizontal, self).__init__("menu_horizontal")
        

    def desktop_postion(self, x: int, y: int, width: int, height: int, z_index: int = 1):
        position            = self.getAttribute(["desktop_position"])
        position['left']    = x
        position['top']     = y
        position['z_index'] = z_index
        # cập nhật lại thông tin
        self.setAttribute(["desktop_position"], position)
        # câp nhật 2 thuộc tính width và min-height ở trường desktop-class
        self.setAttribute(["desktop_class", "menu", "width"], f"{width}px")
        self.setAttribute(["desktop_class", "menu", "height"], f"{height}px")
        self.setAttribute(["desktop_config", "dimension"],  {"width": width, "height": height})

    def desktop_class(self, key: str, value):
        pass

    def desktop_config(self, key: str, value):
        pass

    def setMenu(self, detail: RoleMenu):
        menu_items          = list()
        for item in detail.items:
            item            = AtwMenuItem(item)
            menu_items.append(dict(item))
        
        self.setAttribute(["staticdata", "menu_data"], menu_items)


class AtwMenuVertical(Format):
    def __init__(self):
        super(AtwMenuVertical, self).__init__("menu_vertical")
        

    def desktop_postion(self, x: int, y: int, width: int, height: int, z_index: int = 1):
        position            = self.getAttribute(["desktop_position"])
        position['left']    = x
        position['top']     = y
        position['z_index'] = z_index
        # cập nhật lại thông tin
        self.setAttribute(["desktop_position"], position)
        # câp nhật 2 thuộc tính width và min-height ở trường desktop-class
        self.setAttribute(["desktop_class", "menu", "width"], f"{width}px")
        self.setAttribute(["desktop_class", "menu", "height"], f"{height}px")
        self.setAttribute(["desktop_config", "dimension"],  {"width": width, "height": height})

    def desktop_class(self, key: str, value):
        pass

    def desktop_config(self, key: str, value):
        pass

    def setMenu(self, detail: RoleMenu):
        menu_items          = list()
        for item in detail.items:
            item            = AtwMenuItem(item)
            menu_items.append(dict(item))
        
        self.setAttribute(["staticdata", "menu_data"], menu_items)