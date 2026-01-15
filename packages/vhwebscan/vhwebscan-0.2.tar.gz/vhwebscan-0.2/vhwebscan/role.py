

class Role:
    def __init__(self, tag):
        self.tag        = tag
        self.process()


    def process(self):
        from .tag               import Tag
        self.tag    : Tag       = self.tag

        if self.tag.tag_name == "button":
            self.tag.role_name      = "button"
            self.tag.role_detail    = RoleButton()
        elif(self.tag.tag_name == "img"):
            self.tag.role_name      = "img"

        elif self.tag.tag_name == "input":
            self.tag.role_name      = "input"
            self.tag.role_detail    = RoleInput()

        elif ((self.tag.tag_name in ["a", "p", "h1", "h2", "h3", "span", "label"]) or ("text" in self.tag.attr.keys())) and (not self.tag.children):
            self.tag.role_name      = "text"
            self.tag.role_detail    = RoleText()

        elif self.tag.tag_name == "ul":
            self.tag.children.extend(self.tag.inherits)
            
            removes             = list()
            for child in self.tag.children:
                if not child.rect.isValid():    removes.append(child)

            for child in removes:               self.tag.children.remove(child)

            is_horizontal   = True if self.tag.attr["display"] == "flex" else False
            for child in self.tag.children:
                if child.attr["display"] == "inline-block":
                    is_horizontal   = True
                    break
            self.tag.role_name      = "menu_horizontal" if is_horizontal else "menu_vertical"

            detail                  = RoleMenu(self.tag.children)
            self.tag.role_detail    = detail

            # xoa danh sách con.
            self.tag.children.clear()
        else:
            self.tag.role_name      = "frame"

        

class RoleMenuItem:
    def __init__(self, tag):
        from .tag            import Tag
        if isinstance(tag, Tag):
            self.data : Tag     = tag
            self.name           = ""
            self.styles         = self.data.styles

        self.handle()

    def handle(self):
        from .tag            import Tag
        if "text" in self.data.attr.keys():
            if self.data.attr["text"]:
                self.name   = self.data.attr["text"][0]
            else:
                print(self.data.depth())
        else:
            count           = self.data.depth()
            lst             = self.data.children
            for i in range(0, count):
                for c in lst:
                    c : Tag = c
                    if "text" in c.attr.keys():
                        if c.attr["text"]:
                            self.name   = c.attr["text"][0]
                            self.styles.update(c.styles)
                            break

class RoleMenu:
    def __init__(self, inherits : list):
        from .tag            import Tag
        self.items : list[RoleMenuItem] = list()

        for child in inherits:
            child : Tag  = child
            if child.tag_name == "li":
                menu_item   = RoleMenuItem(child)
                self.items.append(menu_item)


class RoleButton:
    def __init__(self):
        pass

class RoleInput:
    def __init__(self):
        pass

class RoleText:
    def __init__(self):
        pass