import os
import bs4
import uuid
import copy
import json
import tinycss2

from vhwebscan.atw                  import *
from vhwebscan.style                import *

from urllib.parse                   import urljoin
from tinycss2.ast                   import QualifiedRule, Declaration
from tinycss2.ast                   import QualifiedRule, Declaration

from selenium                       import webdriver
from selenium.webdriver.common.by   import By
from selenium.common.exceptions     import NoSuchElementException

class Size:
    def __init__(self, w: int = -1, h: int = -1):
        self.width                  = w
        self.height                 = h
    
    def __iter__(self):
        yield 'w',      self.width
        yield 'h',     self.height

    @property
    def area(self):                 return self.width * self.height

    def isValid(self):              return (self.width < 0 or self.height < 0)

class Point:
    def __init__(self, x: int = -1, y: int = -1):
        self.x                      = x
        self.y                      = y

    def isValid(self):              return True

class Rect:
    def __init__(self, h: int = -1, w: int = -1, x: int = -1, y: int = -1):
        self.height                 = h
        self.width                  = w
        self.x                      = x
        self.y                      = y

    def __str__(self) -> str:
        return f"width: {self.width} height: {self.height} x: {self.x} y: {self.y}"
    
    def __iter__(self):
        yield 'x',  self.x
        yield 'y',  self.y
        yield 'w',  self.width
        yield 'h',  self.height

    def __eq__(self, other : 'Rect'):
        if isinstance(other, Rect):
            return (self.x == other.x and 
                    self.y == other.y and 
                    self.width == other.width and 
                    self.height == other.height)
        return NotImplemented

    @property
    def topLeft(self):          return Point(self.x, self.y)

    @property
    def topRight(self):         return Point(self.x + self.width, self.y)

    @property
    def bottomLeft(self):       return Point(self.x, self.y + self.height)

    @property
    def bottomRight(self):      return Point(self.x + self.width, self.y + self.height)

    def isValid(self):
        return True if self.x >= 0 and self.y >= 0 and self.width > 0 and self.height > 0 else False
    
    def contains(self, p : Point):
        return (self.topLeft.x < p.x < self.bottomRight.x) and (self.topLeft.y < p.y < self.bottomRight.y)

    def pos(self):              return Point(self.x, self.y)

    def size(self):             return Size(self.width, self.height)

class Tag:
    def __init__(self, parent: 'Tag' = None, tag: bs4.element.Tag = None, viewport: Size = None, url: str = ""):
        self.id                     = str(uuid.uuid4())
        self.parent                 = parent
        self.path                   = ""
        self.url                    = url
        self.tag                    = None
        self.children   : list[Tag] = list()
        self.hidden     : list[Tag] = list()
        self.inherits   : list[Tag] = list()
        self.rect                   = Rect()
        self.new_rect               = Rect()
        self.name                   = ""
        self.tag_name               = ""
        self.index                  = -1
        self.styles                 = { }
        self.attr                   = { }
        self.viewport               = viewport
        self.ratio                  = 0
        self.role_name              = ""
        self.role_detail            = None
        # khởi tạo các đối tượng style giao diện
        self.style                  = Style()


        if tag != None:
            if isinstance(tag, bs4.element.Tag):
                self.tag            = tag
                self.name           = self.tag.name
                self.tag_name       = self.name
                # thực hiện quét các tag ở trong
                if self.tag.name == "img" or self.tag.get("type") == "img":
                    src                     = self.tag.get("src")
                    if src != None:
                        if src.startswith("http"):
                            self.attr['img']    = src
                        else:
                            self.attr['img']    = urljoin(self.url, src)
                
                if self.tag.name in ["a", "i", "span", "p", "h1", "h2", "h3", "button", "label"]:
                    self.attr['text']       = list()
                    for text in self.tag.stripped_strings:
                        self.attr['text'].append(text)

                if "role" in self.tag.attrs.keys():
                    self.attr['role']       = self.tag.attrs["role"]

                if "href" in self.tag.attrs.keys():
                    self.attr['href']       = self.tag.attrs['href']

                if "style" in self.tag.attrs.keys():
                    self.styles['on_attribute']     = dict()
                    l_style                 = self.tag.attrs['style']
                    if isinstance(l_style, dict):
                        self.styles['on_attribute'] = l_style
                    elif isinstance(l_style, str):
                        lst_style           = l_style.split(';')
                        for seg in lst_style:
                            if not seg:     continue
                            seg             = seg.strip()
                            if seg.find(":") > -1:
                                key             = seg[:seg.find(':')].strip()
                                value           = seg[seg.find(':') + 1:].strip()
                                self.styles['on_attribute'][key]    = value
                self.scan()
        else:
            pass

    def __iter__(self):
        try:
            yield   'id',           self.id
            yield   'tag',          self.tag_name
            yield   'role',         self.role_name
            yield   'css_selector', self.path
            yield   'rect',         dict(self.rect)
            yield   'new_rect',     dict(self.new_rect)
            yield   'attr',         self.attr
            yield   'styles',       self.styles

            if self.viewport:
                yield   'viewport',     dict(self.viewport)

            if self.children:
                lst                         = list()
                for child in self.children: lst.append(dict(child))
                yield 'objects',            lst
            else:
                yield 'objects',            []
        except Exception as e:
            print(self.id, str(e))

    def set_id(self, idx: int):
        """
        Hàm `set_id` thiệt lập định danh cho đối tượng có thứ tự.

        Parameter
        ----------
        - `idx` :           thứ tự/định danh dành đối tượng.
        """
        self.index                  = idx
        self.name                   = f"{self.name}:nth-of-type({self.index})"

    def copy(self):
        new_tag                     = Tag()
        new_tag                     = copy.copy(self)
        new_tag.id                  = str(uuid.uuid4())

        return new_tag

    def set_url(self, url: str):
        self.url                    = url

    def scan(self):
        l_sub                       = { }

        for i, child in enumerate(self.tag.children):
            if isinstance(child, bs4.element.Tag):
                # bỏ qua các thẻ không phải thẻ giao diện.
                if child.name in ["script", "style", "meta", "link", "noscript"]: continue
                # kiểm tra tên thẻ có trong danh sách chưa.
                if not child.name in l_sub.keys():
                    l_sub[child.name]       = 1
                else:
                    idx         = l_sub[child.name]
                    l_sub[child.name]       = idx + 1

                ch              = Tag(self, child, None, self.url)
                self.children.append(ch)
        # bỏ các trường đơn chỉ có 1 phần tử vào danh sách cần xóa
        removes                 = list()
        for sub in l_sub:
            if l_sub[sub] == 1:     removes.append(sub)
        # thực hiện xóa dánh sách
        for n in removes:       l_sub.pop(n)

        for child in reversed(self.children):
            if child.tag_name in l_sub.keys():
                idx             = l_sub[child.tag_name]
                if l_sub[child.tag_name] > 0:
                    child.set_id(idx)
                    l_sub[child.tag_name]    = idx - 1

        # duyệt qua danh sách và cập nhật đường dẫn của đối tượng.
        self.browse()
    
    def browse(self):
        # cập nhật đường dẫn của đối tượng
        self.path   = self.parent.path + " > " if self.parent != None else "html > "
        self.path   = self.path + self.name
        # duyệt qua các danh sách con để cập nhật cho đối tượng.
        for child in self.children: child.browse()

    def print_tag(self, s: str = ""):
        if not self.children:
            if self.parent != None:
                print(f"tag: {self.tag_name} parent: {self.parent.tag_name}")
            else:
                print(f"tag: {self.tag_name} parent: None")
        else:
            for child in self.children: child.print_tag()

    def execute(self, browser : webdriver.Chrome):
        if browser == None:         raise Exception("Browser is null.")
        try:
            element             = browser.find_element(By.CSS_SELECTOR, self.path)

            self.rect.x         = int(round(element.rect['x'], 2))
            self.rect.y         = int(round(element.rect['y'], 2))
            self.rect.width     = int(round(element.rect['width'], 2))
            self.rect.height    = int(round(element.rect['height'], 2))

            display             = element.value_of_css_property("display")
            visibility          = element.value_of_css_property("visibility")

            self.attr['display']    = display
            self.attr['visibility'] = visibility

            if element.get_attribute("type") == "img":
                src                 = element.get_attribute("src")
                if src != None:
                    if src.startswith("http"):
                        self.attr['img']    = src
                    else:
                        self.attr['img']    = urljoin(self.url, src)
            # kiểm tra nếu thuộc tính text ko có và đối tượng khong có con nghĩa là đối tượng lá của cây
            if not "text" in self.attr.keys() and not self.children:
                #/ thực hiện lấy text.
                self.attr['text']       = list()
                for text in self.tag.stripped_strings:
                    self.attr['text'].append(text)

            self.viewport       = Size(self.rect.width, self.rect.height) if(self.parent == None) else self.parent.viewport
            self.ratio          = round(self.rect.height / self.viewport.height, 2)
            for child in self.children: child.execute(browser)
        except NoSuchElementException:
            print(f"{self.path} not found.")

    def analyse(self, css : 'StyleCSS'):
        # phân tích style của element.
        styles                  = css.analyse(self.tag)
        for rule in styles:
            selector_name       = rule['selector']
            d                   = { }
            for name, value in rule["declarations"]:
                d[name]         = value
            
            self.styles[selector_name]  = d

        # tiếp tục xử lý với các đối tượng con
        for child in self.children:     child.analyse(css)

    def contains(self, x: int, y: int):
        """
        Hàm `contains` kiểm tra tọa độ có nằm trong phạm vị của khối.

        Parameter
        ----------
        - `x` :         tọa độ x.
        - `y` :         tọa độ y.
        """
        return (self.rect.x <= x < (self.rect.x + self.rect.width)) or (self.rect.y <= y < (self.rect.y + self.rect.height))

    def filter(self):
        removes                 = list()
        # phân loại lọc theo kích thước xác thực
        for child in self.children:
            # kiểm tra tọa độ có hợp lệ đối với tag_name là div và tọa đó có nằm trong phạm vị của cha ko.
            if ((child.rect.width < 2 or child.rect.height < 2)) and child.tag_name == "div":
                # nếu thỏa điều kiện trên thì sẽ bỏ vào danh sách ẩn và xóa khỏi danh sách con.
                self.children.extend(child.children)
                self.hidden.append(child)
                removes.append(child)
            elif ((child.rect.width < 2 or child.rect.height < 2)) and child.tag_name != "div":
                self.children.extend(child.children)
                removes.append(child)
            else:
                child.filter()
        # xóa các phần tử nằm trong danh sách
        if removes:                 self.attr['hidden']     = True
        for child in removes:       self.children.remove(child)

    def duplicate(self):
        pass

    def collect(self):
        elements                    = ['button', 'input', 'svg', 'label', 'ul']
        role                        = self.attr['role'] if 'role' in self.attr.keys() else ""
        if (self.tag_name in elements) or (role in elements):
            if self.tag_name == "ul":
                if 1 < self.depth() <= 3:
                    if len(self.children) < 2:
                        self.tag_name       = "div"
                        for child in self.children:     child.collect()
                        return
                else:
                    self.tag_name           = "div"
                    for child in self.children:         child.collect()
                    return
                
            self.attr['inherits']   = True
            # cha sẽ kế thừa các thuộc tính của con nếu cha thuộc các thành phần UI.
            for child in self.children:
                if 'text' in child.attr.keys():
                    if not 'text' in self.attr.keys():  self.attr['text']   = list()
                    self.attr['text'].extend(child.attr['text'])
                for style in child.styles:
                    self.styles[style]      = child.styles[style]
            # sẻ mở rộng danh sách kế thừa từ child nếu tag_name hoặc role thuộc danh sách
            self.inherits.extend(self.children)
            # xóa danh sách con
            self.children           = []
        else:
            # xử lý tương tự với các nhánh con.
            for child in self.children:     child.collect()

    def inheritance(self):
        removes                 = list()

        for child in self.children:
            if child.rect == self.rect and self.tag_name == child.tag_name:
                removes.append(child)
                # mở rộng danh sách con bằng danh sách con
                self.children.extend(child.children)
            elif len(child.children) == 1:
                removes.append(child)
                self.children.extend(child.children)
                
                for c in child.children:    c.styles.update(child.styles)
            elif not self.contains(child.rect.x, child.rect.y):
                self.attr['hidden']     = True
                removes.append(child)
                self.hidden.append(child)
            else:
                child.inheritance()
            
        for child in removes:   self.children.remove(child)

    def check_styles(self):
        removes             = list()

        for child in self.children:
            if child.attr['display'] == "none" or child.attr['visibility'] == "hidden": 
                removes.append(child)
            else:
                child.check_styles()

        for c in removes:
            self.hidden.append(child)
            self.children.remove(c)

    def check_frame(self):
        # chức năng kiểm tra các thẻ có diện tích lớn > 30% thì phải bỏ.
        removes         = list()

        for child in self.children:
            ratio       = (child.rect.width * child.rect.height) / (child.viewport.area)
            if ratio >= 0.3:
                removes.append(child)
                self.children.extend(child.children)
            else:
                child.check_frame()

        # thực hiện xóa các đối tượng trong danh sách xóa
        for c in removes:       self.children.remove(c)

    def repair(self):
        for child in self.children:
            child.parent    = self
            child.repair()

    def find(self, _id: str):
        pass

    def format(self):
        atw             = None
        if self.parent  == None:
            atw         = AtwBlockBlank()
            atw.desktop_postion(self.new_rect.x, self.new_rect.y, self.new_rect.width, self.new_rect.height)
        else:
            # phân loại role name 
            if self.role_name == "button":
                atw     = AtwButton()
                atw.desktop_position(self.new_rect.x, self.new_rect.y, self.new_rect.width, self.new_rect.height, 1)
                if "text" in self.attr.keys():
                    if self.attr["text"]:   atw.setText(self.attr["text"][0])
                    else:   atw.setText("")
            elif self.role_name == "img":
                atw     = AtwImage()
                atw.desktop_position(self.new_rect.x, self.new_rect.y, self.new_rect.width, self.new_rect.height, 1)
                if "img" in self.attr.keys():       atw.setImage(self.attr["img"])
            elif self.role_name == "text":
                atw     = AtwText()
                atw.desktop_position(self.new_rect.x, self.new_rect.y, self.new_rect.width, self.new_rect.height, 1)
                if "text" in self.attr.keys():
                    if self.attr["text"]:   atw.setText(self.attr["text"][0])
                    else:   atw.setText("")
            elif self.role_name == "menu_horizontal":
                atw     = AtwMenuHorizontal()
                atw.desktop_postion(self.new_rect.x, self.new_rect.y, self.new_rect.width, self.new_rect.height, 1)
                if self.role_detail:    atw.setMenu(self.role_detail)
            elif self.role_name == "menu_vertical":
                atw     = AtwMenuVertical() 
                atw.desktop_postion(self.new_rect.x, self.new_rect.y, self.new_rect.width, self.new_rect.height)
                if self.role_detail:    atw.setMenu(self.role_detail)
            elif self.role_name == "input":
                atw     = AtwInput()
                atw.desktop_position(self.new_rect.x, self.new_rect.y, self.new_rect.width, self.new_rect.height, 1)
            else:
                atw     = AtwFrameBlank() 
                atw.desktop_postion(self.new_rect.x, self.new_rect.y, self.new_rect.width, self.new_rect.height)

        # duyệt qua danh sách các đối tượng con và xử lý định dạng của các đối tượng con
        if atw != None:
            atw.setStyle(self.style)
            # duyệt qua danh sách con.
            for child in self.children: atw.objects(child.format())

        return atw


    def leaf(self):
        lst             = list()
        if not self.children:
            # nếu ko có danh sách con thì trả về danh sách chỉ mình nó
            return [self]
        else:
            # duyệt danh sách và mở rộng đối tượng.
            for child in self.children:     lst.extend(child.leaf())
        return lst
    
    def inheritlist(self):
        """
        Hàm `inheritlist` trả vè danh sách các đối tượng kế thừa.
        """
        d               = dict()
        if self.inherits:
            t           = dict()
            t[self.id]  = self.inherits
            d.update(t)

        for child in self.children:     d.update(child.inheritlist())

        return d

    def level(self, lv: int):
        pass

    def depth(self):
        lst                     = list()
        for child in self.children:     lst.append(child.depth())

        return max(lst) + 1 if lst else 1
    
    def breadth(self) -> int:
        level = [self]
        max_width = 0

        while level:
            max_width = max(max_width, len(level))
            next_level = []

            for node in level:
                next_level.extend(node.children)

            level = next_level

        return max_width

    def count(self):
        length                  = len(self.children)

        for child in self.children: length += child.count()

        return length
    
    def load(self, ws: str = "", path: str = "", data : dict = None):
        """
        Hàm `load` chức năng tải nội dung đã lưu trong file json vào đối tượng Tag.

        Parameter
        ---------
        - `ws` :            Đường dẫn tới workspace.
        - `data` :          Dữ liệu dưới dạng dict, dùng cho đệ quy
        """
        try:
            if not data:
                if not path:
                    if ws == "":                    raise Exception("Workspace is not found")
                    if not os.path.isdir(ws):       raise Exception("Workspace is not found")
                    # đọc file và load vào json
                    raw_path            = os.path.join(ws, "raw.json")
                    inherits_path       = os.path.join(ws, "inherits.json")
                    if not os.path.isfile(raw_path):    raise Exception("File raw.json not found.")
                    data                = dict()
                    with open(raw_path, "r", encoding="utf-8") as fp:
                        data            = json.load(fp)
                else:
                    if not os.path.isfile(path):    raise Exception("File json not found.")
                    data                = dict()
                    with open(path, "r", encoding="utf-8") as fp:
                        data            = json.load(fp)

            # ghi dữ liệu vào class
            self.id             = data['id']
            self.name           = data['tag']
            self.path           = data['css_selector']
            self.tag_name       = self.name

            geo                 = data['rect']
            self.rect           = Rect(geo['h'], geo['w'], geo['x'], geo['y'])

            geo                 = data['new_rect']
            self.new_rect       = Rect(geo['h'], geo['w'], geo['x'], geo['y'])

            self.attr : dict    = data['attr']
            self.styles         = data['styles']

            if 'viewport' in data.keys():
                self.viewport       = Size(data['viewport']['w'], data['viewport']['h'])
            else:
                self.viewport   = Size()

            for ele in data['objects']:
                # khởi tạo Tag con và load dữ liệu vào tag con.
                child           = Tag(parent=self)
                child.load(data = ele)
                # thêm con và danh sách 
                self.children.append(child)

        except Exception as e:
            print("error in load: ", str(e))

    def normalize(self):
        if self.parent != None:
            top_x               = self.rect.x - self.parent.rect.x
            top_y               = self.rect.y - self.parent.rect.y
            self.new_rect       = Rect(self.rect.height, self.rect.width, top_x, top_y)
        else:
            top_x               = self.rect.x
            top_y               = self.rect.y

            self.new_rect       = Rect(self.rect.height, self.rect.width, top_x, top_y)
            
        for child in self.children: child.normalize()

    def normalize_reverse(self):
        if self.parent != None:
            top_x               = self.new_rect.x + self.parent.rect.x
            top_y               = self.new_rect.y + self.parent.rect.y
            self.rect           = Rect(self.new_rect.height, self.new_rect.width, top_x, top_y)
        else:
            top_x               = self.new_rect.x
            top_y               = self.new_rect.y

            self.rect           = Rect(self.new_rect.height, self.new_rect.width, top_x, top_y)
            
        for child in self.children: child.normalize_reverse()

    def normalize_style(self):
        font_key                = ['font-size', 'font-family', 'font-weight', 'color']
        border_key              = ['border', 'border-radius', 'border-width', 
                                   'border-style', 'border-color', 'border-top', 
                                   'border-right', 'border-bottom', 'border-left']
        padding_key             = ['padding', 'padding-top', 'padding-right', 'padding-left', 'padding-bottom']
        margin_key              = ['margin', 'margin-top', 'margin-bottom', 'margin-left', 'margin-right']
        background_key          = ['background-color', 'background', 'background-image']

        font_styles             = dict()
        border_styles           = dict()
        padding_styles          = dict()
        margin_styles           = dict()
        background_style        = dict()
        other_style             = dict()

        for class_name in self.styles:
            for key in self.styles[class_name]:
                if key in font_key:
                    font_styles[key]    = self.styles[class_name][key]
                elif key in border_key:
                    border_styles[key]  = self.styles[class_name][key]
                elif key in padding_key:
                    padding_styles[key] = self.styles[class_name][key]
                elif key in margin_key:
                    margin_styles[key]  = self.styles[class_name][key]
                elif key in background_key:
                    background_style[key]   = self.styles[class_name][key]
                else:
                    other_style[key]    = self.styles[class_name][key]

        self.style.background       = Background(background_style)
        self.style.padding          = Padding(padding_styles)
        self.style.border           = Border(border_styles)
        self.style.font             = Font(font_styles)

        for child in self.children:     child.normalize_style()

    def role(self):
        from .role          import Role

        role                = Role(self)
        for child in self.children: child.role()

    def recheck(self):
        removes             = list()
        if len(self.children) == 1:
            self.children.extend(self.children[0].children)
            
            self.children.remove(self.children[0])

        for child in self.children: child.recheck()

    def check(self):
        removes             = list()
        for child in self.children:
            x               = child.new_rect.x
            y               = child.new_rect.bottomRight.y

            top_x           = child.new_rect.x
            bottom_x        = child.new_rect.bottomRight.x

            wp              = child.parent.new_rect.width
            hp              = child.parent.new_rect.height
            # kiểm tra để thỏa điều kiện là đối tượng con chỉ được nằm trong phạm vi và khu vực của đối tượng
            # cha nếu vượt ra ngoài theo hàng ngang thì sẽ xử lý lại đối tượng con đó
            if (top_x < 0 and (abs(top_x) / wp) > 0.2) or ((bottom_x > wp) and (((bottom_x - wp) / wp) > 0.2)):
                self.outline(child, self)
                child.children.clear()
            elif ((bottom_x > wp) and (((bottom_x - wp) / wp) > 0.2)):
                pass
                # self.outline(child, child.parent)
                # child.children.clear()
            # elif (y > child.parent.new_rect.height) and (child.parent.new_rect.height / y) > 0.2:
            #     # child.children.clear()
            #     # self.outline(child, child.parent)
            #     removes.append(child)
            else:
                child.check()

        for child in removes:   self.children.remove(child)

    def outline(self, tag: 'Tag', parent: 'Tag', dir: str = "horizontal"):
        if dir == "horizontal":
            rect_1              = tag.rect
            rect_2              = parent.rect

            x                   = rect_2.x if rect_2.x > rect_1.x else rect_1.x
            y                   = rect_1.y

            bx                  = rect_2.bottomRight.x if rect_1.bottomRight.x > rect_2.bottomRight.x else rect_1.bottomRight.x
            by                  = rect_1.bottomRight.y

            w                   = bx - x
            h                   = by - y
            print(w, h, "real", x, bx, tag.id, parent.id)

            # new_rect        = Rect(tag.new_rect.height, tag.new_rect.bottomRight.x, 0, tag.new_rect.y)
            # rect            = Rect(tag.rect.height, new_rect.width, tag.rect.x - tag.new_rect.x, tag.rect.y)
            # # cập nhật lại kịch thước mới cho đối tượng.
            # tag.rect        = rect
            # tag.new_rect    = new_rect



            # removes         = list()
            # for child in tag.children:
            #     if not new_rect.contains(child.new_rect.topLeft):
            #         removes.append(child)
            #     # else:
            #     #     print(new_rect, child.new_rect)
            #     #     print(child.id)
            
            # for c in removes:       tag.children.remove(c)

class StyleCSS:
    def __init__(self, folder: str):
        self.css_rules   : list[tuple]      = list()
        if not os.path.exists(folder):      raise Exception("Folder CSS not found.")
        # duyệt các file css có trong folder và parse nội dung thành các rule để kiểm tra sau này
        for filename in os.listdir(folder):
            # bỏ qua các file ko phải là đuôi .css
            if not filename.endswith(".css"):   continue
            # đọc nội dung file css và parse nội dung thành các rule
            css_file        = os.path.join(folder, filename)
            # đọc nội dung
            css_text        = ""
            with open(css_file, "r", encoding="utf-8") as fp:
                css_text    = fp.read()
            # parse nội dung thành danh sách rule và thêm vào danh sách rule chung.
            self.css_rules.extend(self.parse_css_rules(css_text))

    def parse_css_rules(self, css_text: str) -> list:
        """
        Hàm `parse_css_rules` chức năng chuyển các nội dung trong file css thành các rule
        có quản lý theo selector để khi kiểm tra match từ element.

        Parameter
        ---------
        - `css_text`:        Nội dung của file css
        """
        rules           = list()
        # parse stylesheet từ nội dung css
        stylesheet      = tinycss2.parse_stylesheet(css_text, skip_comments=True, skip_whitespace=True)

        for rule in stylesheet:
            if not isinstance(rule, QualifiedRule):     continue
            # tách selector bằng dấu ,
            selectors               = tinycss2.serialize(rule.prelude).strip().split(',')
            # lấy các declaration
            body                    = tinycss2.parse_declaration_list(rule.content)
            declarations            = list()
            # duyệt qua danh sách nội dung
            for decl in body:
                if not isinstance(decl, Declaration):   continue
                declarations.append((decl.name, tinycss2.serialize(decl.value).strip()))
            # push từng selectro thành rule riêng
            for sel in selectors:   rules.append((sel.strip(), declarations))
        
        return rules
    
    def match_simple(self, selector: str, element: bs4.element.Tag):
        parts               = selector.split('.')
        # với hashtag là # id
        if "#" in selector:
            tag_id          = selector.split("#")
            tag             = tag_id[0] if tag_id[0] else None
            eid             = tag_id[1]

            if element.get("id") != eid:        return False
            if tag and element.name != tag:     return False

            return True
        
        # với đối tượng là .class
        if selector.startswith("."):
            cls             = selector[1:]
            return cls in (element.get("class") or [])
        
        # với đối tượng là tag.class
        if len(parts) == 2:
            if element.name != parts[0]:        return False
            return parts[1] in (element.get("class") or [])
        
        # tag
        return element.name == selector
    
    def match_selector(self, selector : str, element : bs4.element.Tag):
        selector                = selector.strip()

        if ">" in selector:
            parts               = [p.strip() for p in selector.split(">")]
            if not self.match_simple(parts[-1], element):   return False

            parent              = element.parent
            for sel in reversed(parts[:-1]):
                if not parent or not self.match_simple(sel, parent):
                    return False
                parent          = parent.parent
            
            return True
        
        parts                   = selector.split()
        if len(parts) > 1:
            if not self.match_selector(parts[-1], element):
                return False
            ancestor_target     = parts[-2]
            parent              = element.parent
            while parent and parent.name != "[document]":
                if self.match_simple(ancestor_target, parent):
                    return True
                parent          = parent.parent
            return False
        
        return self.match_simple(selector, element)

    def calc_specificity(self, selector: str):
        ids                     = selector.count("#")
        classes                 = selector.count(".")
        tags                    = sum(1 for x in selector.split() if x[0].isalpha())

        return (ids, classes, tags)
    
    def analyse(self, element: bs4.element.Tag):
        applied                 = list()
        for selector, decls in self.css_rules:
            if self.match_selector(selector, element):
                applied.append({
                    "selector": selector,
                    "specificity": self.calc_specificity(selector),
                    "declarations": decls
                })
        applied.sort(key=lambda r: r["specificity"])
        return applied


