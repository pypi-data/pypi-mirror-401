import os
import json
import uuid

from vhwebscan.tag            import Tag, Rect, Point, Size

class WebScan:
    def __init__(self):
        self.tag : Tag      = None

    def load(self, parent: Tag = None, data: dict = {}) -> Tag:
        if parent != None:
            x               = int(round(data["left"], 2))
            y               = int(round(data["top"], 2))
            w               = int(round(data["width"], 2))
            h               = int(round(data["height"], 2))

            type            = data["type"]
            role            = data["id"]
            id              = str(uuid.uuid4())

            child           = Tag(parent=parent)
            child.new_rect  = Rect(h, w, x, y)
            child.id        = id
            child.tag       = type
            child.tag_name  = type
            child.role_name = role

            if "text" in data.keys():
                child.attr['text']  = data['text']
            
            if "url" in data.keys():
                child.attr['img']   = data['url']

            for ch in data['objects']:  self.load(child, ch)

            parent.children.append(child)
        else:
            parent                 = Tag(parent=None)
            parent.new_rect.x      = 0
            parent.new_rect.y      = 0
            parent.new_rect.width  = 0
            parent.new_rect.height = 0

            for element in data:
                x               = int(round(element["left"], 2))
                y               = int(round(element["top"], 2))
                w               = int(round(element["width"], 2))
                h               = int(round(element["height"], 2))

                type            = element["type"]
                role            = element["id"]
                id              = str(uuid.uuid4())

                child           = Tag(parent=parent)
                child.new_rect  = Rect(h, w, x, y)
                child.id        = id
                child.tag       = type
                child.tag_name  = type
                child.role_name = role
                
                if "text" in element.keys():
                    child.attr['text']  = element['text']
                
                if "url" in element.keys():
                    child.attr['img']   = element['url']

                parent.new_rect.width  = max(parent.new_rect.width, w)
                parent.new_rect.height += h

                for ch in element['objects']:   self.load(child, ch)

                parent.children.append(child)

        return parent

    def save(self, tag: Tag):
        data                = dict()
        data["type"]        = tag.tag_name
        data["id"]          = tag.role_name
        data["left"]        = tag.new_rect.x
        data["top"]         = tag.new_rect.y
        data["width"]       = tag.new_rect.width
        data["height"]      = tag.new_rect.height
        data["type_parent"] = tag.parent.tag_name

        if "text" in tag.attr.keys():
            data["text"]    = tag.attr["text"]
        if "img" in tag.attr.keys():
            data["url"]     = tag.attr["img"]

        if "name" in tag.attr.keys():
            data["name"]    = tag.attr["name"]

        if "metadata" in tag.attr.keys():
            data["metadata"]    = tag.attr["metadata"]

        if tag.tag_name == "frame-tabs":
            if "class_child" in tag.attr.keys():
                data["cutdown_childs"]      = dict()
                data["cutdown_childs"]      = tag.attr["class_child"]

        data["objects"]     = list()

        for child in tag.children:
            data["objects"].append(self.save(child))
        
        return data

    def frame_repeat(self, parent: Tag):
        # bỏ qua nếu đối tượng ko phải là frame_blank
        if parent.tag_name != "frame-blank":    return
        if not len(parent.children):            return

        is_repeat           = True
        # kiểm tra số lượng con của mỗi con nếu đồng nhất và diện tích ko sai lệch quá nhiều thì
        for c1 in parent.children:
            for c2 in parent.children:
                if len(c1.children) != len(c2.children):
                    is_repeat    = False
                    break
            if not is_repeat:   break

        if is_repeat:
            area                = 0
            max_area            = 0
            min_area            = -1
            for child in parent.children:
                area            += child.new_rect.size().area
                max_area        = max(child.new_rect.size().area, max_area)
                min_area        = min(child.new_rect.size().area, min_area) if min_area > -1 else child.new_rect.size().area
            area                = area / (len(parent.children))

            ratio_max           = (max_area - area) / area
            ratio_min           = (area - min_area) / min_area

            is_repeat           = True if ratio_max < 0.1 and ratio_min < 0.1 else False
        
        # duyệt qua các đối tượng con để biết các đối tượng con của frame_blank đang
        # được phân bố như nào
        if is_repeat:
            vertical            = 0
            horizontal          = 0

            max_vertical        = 0
            max_horizontal      = 0
            # duyệt qua danh sách con để tìm hướng phân bố các thành phần trong parent.
            for child in parent.children:
                new_horizontal  = max(max_horizontal, child.new_rect.bottomRight.x)
                new_vertical    = max(max_vertical, child.new_rect.bottomRight.y)

                if max_horizontal != 0:
                    if (new_horizontal - max_horizontal) / max_horizontal > 0.2:
                        horizontal      += 1
                        max_horizontal  = new_horizontal
                else:
                    horizontal          += 1
                    max_horizontal      = new_horizontal
                
                if max_vertical != 0:
                    if(new_vertical - max_vertical) / max_vertical > 0.2:
                        vertical        += 1
                        max_vertical    = new_vertical
                else:
                    vertical            += 1
                    max_vertical        = new_vertical

        if is_repeat:
            # chuyển loại đối tượng  
            parent.tag_name     = "frame-repeat"

            cols                = horizontal
            rows                = vertical
            total               = len(parent.children)

            first : Tag         = parent.children[0]
            min_x               = first.new_rect.x
            min_y               = first.new_rect.y
            for child in parent.children:
                new_x           = child.new_rect.x
                new_y           = child.new_rect.y

                if(new_x < min_x) and (new_y < min_y):
                    min_x       = new_x
                    min_y       = new_y

                    first       = child

            removes             = list()
            for child in parent.children:
                if child != first:  removes.append(child)
            
            for ch in removes:  parent.children.remove(ch)
            
            meta                = dict()
            meta["cols"]        = cols
            meta["rows"]        = rows
            meta["total_products"]  = total

            meta["dimension"]   = dict()
            meta["dimension"]["width"]          = parent.new_rect.width
            meta["dimension"]["height"]         = first.new_rect.height
            meta["product_id"]  = first.role_name

            parent.attr["metadata"]         = meta
            
            # loại bỏ khung trống ngoài mang hết các phần tử ra ngoài.
            parent.children.extend(first.children)
            # xóa đối tuog bao.
            parent.children.remove(first)
        else:
            # lập lại với đối tượng con.
            for child in parent.children:       self.frame_repeat(child)

    def frame_tab(self, parent: Tag):
        if parent.role_name == "frame-repeat":  return
        # sắp xếp lại theo tọa độ y
        parent.children.sort(key=lambda i1: i1.rect.y)
        # phân loại chỉ kiểm tra các role_name là frame-blank
        if parent.tag_name == "frame-blank":
            is_button_list          = -1
            is_tab                  = False

            tab : Tag               = None
            tab_depend  : Tag       = None
            
            for child in parent.children:
                if child.tag_name == "tab-prepare":
                    is_button_list  = 0
                    idx             = parent.children.index(child)
                    for i in range(idx, len(parent.children)):
                        ch          = parent.children[i]
                        if ch.tag_name == "frame-repeat":
                            # thiết lập đối tượng phụ thuộc của tag
                            tab_depend  = ch
                            tab         = child
                            is_tab      = True
                            # xóa tab depend
                            parent.children.remove(tab_depend)
                            break
                elif child.tag_name == "button":
                    is_button_list  = 1 if is_button_list == -1 or is_button_list == 1 else 0
                else:
                    is_button_list  = 0


            if is_button_list == 1:
                if parent.tag_name == "tab-prepare":    parent.tag_name = "frame-blank"
                elif parent.tag_name == "frame-blank":  parent.tag_name = "tab-prepare"
            elif is_tab:
                tab.tag_name        = "frame-tabs"
                w                   = tab.rect.width
                # h                   = tab.rect.height + tab_depend.rect.height
                h                   = tab_depend.rect.bottomRight.y - tab.rect.topLeft.y
                tab.rect.width      = w
                tab.rect.height     = h

                tab.new_rect.width  = w
                tab.new_rect.height = h
                # TODO: chuyển các đối tượng button trong frame-tab thành các frame-blank
                # và thêm trường name_vn là name của button -> mỗi button là 1 frame-blank
                # trong mỗi frame-blank có 1 frame-repeat với đối tượng đầu tiên sẽ là tab_depend
                # còn các đối tượng còn lại là
                names               = list()
                class_child         = ""
                min_width           = tab.children[0].rect.width
                min_height          = tab.children[0].rect.height
                for child in tab.children:
                    class_child     = child.role_name
                    
                    min_width       = min(min_width, child.rect.width)
                    min_height      = min(min_height, child.rect.height)
                    
                    names.append(child.attr["text"])
                # tạo trường cho đối tượng tab.
                tab.attr["class_child"]   = dict()
                tab.attr["class_child"][class_child]    = {"min-height": min_height, "min-width": min_width}
                # làm sạch danh sách con để tạo danh sách mới.
                tab.children.clear()
                for name in names:
                    frame               = Tag()
                    frame.tag_name      = "frame-blank"
                    frame.attr["name"]  = name
                    frame.rect          = Rect(200, 300, tab.rect.x, tab.rect.y)
                    frame.new_rect      = Rect(200, 300, tab.new_rect.x, tab.new_rect.y)
                    frame.parent        = tab

                    repeat              = tab_depend.copy()
                    w                   = repeat.rect.width
                    h                   = repeat.rect.height
                    repeat.rect         = Rect(h, w, frame.rect.x, frame.rect.y)
                    repeat.new_rect     = Rect(h, w, 0, 0)
                    repeat.parent       = frame
                    frame.children.append(repeat)
                    # thêm fram-blank vào frame-tab
                    tab.children.append(frame)
            else:
                for child in parent.children:   self.frame_tab(child)
        elif parent.tag_name == "tab-prepare":
            parent.tag_name             = "frame-blank"

    def rename(self, parent: Tag):
        for child in parent.children:
            child.tag_name   = "frame-blank" if child.tag_name == "block-blank" else child.tag_name
            self.rename(child)


    def scan(self, data: dict):
        self.tag                 = self.load(None, data)
        # chuyển đổi tọa độ
        self.tag.normalize_reverse()
        # print(f"count: {self.tag.count()} - depth: {self.tag.depth()}")

        for child in self.tag.children:      child.inheritance()

        # print(f"count: {self.tag.count()} - depth: {self.tag.depth()}")

        for child in self.tag.children:      self.rename(child)

        # [Frame-Repeat] thực hiện phân loại frame theo repeat
        for child in self.tag.children:
            for ch in child.children:   self.frame_repeat(ch)
        
        # [Frame-Tabs] thực hiện phân loại frame theo tab.
        for i in range(0, 2):
            for child in self.tag.children:
                for ch in child.children:   self.frame_tab(ch)

        # xử lý lại tọa độ của cây đối tương85
        self.tag.repair()
        self.tag.normalize()

        # print(f"count: {self.tag.count()} - depth: {self.tag.depth()}")

        new_data                    = list()
        for child in self.tag.children:  new_data.append(self.save(child))

        return new_data