import os
import time
import base64

from vhwebscan.config                       import Configure
from selenium                               import webdriver
from selenium.webdriver.chrome.options      import Options
from selenium.webdriver.chrome.service      import Service

class RenderWebsite:
    def __init__(self, url: str, ws: str):
        self.url            = url
        self.ws             = ws
        # gọi selenium webdriver
        options             = Options()
        # options.add_argument("--headless")

        # khợi tạo browser để thực hiện chạy crawler website
        service             = Service(executable_path=Configure.DRIVER_PATH)
        self.browser        = webdriver.Chrome(options=options, service=service)
        self.browser.set_window_size(Configure.SCREEN_WIDTH, 800)

    def scroll_to_end(self, scroll_step : int = 500, pause : int = 2):
        """
        Hàm `scroll_and_capture` chức năng cuộn trang và chụp màn hình của trang.

        Parameter
        ---------
        - `scroll_step` :           Bước cuộn, mỗi lần cuộn mặc định là 500px.
        - `pause` :                 Thời gian mỗi lần chờ khi cuộn là 1s.
        - `screenshot_path` :       Đường dẫn lưu chụp màn hình.
        """
        last_height         = 0
        max_height          = self.browser.execute_script("return document.body.scrollHeight")

        while True:
            # thực hiện scoll với scorll step
            self.browser.execute_script(f"window.scrollBy(0, {scroll_step});")
            # scroll xong đứng chờ
            time.sleep(pause)
            # cập nhật lại kích thước mới
            new_height      = self.browser.execute_script("return document.body.scrollHeight")
            # kiểm tra kích thước mới
            if new_height == last_height:   break
            # cập nhật lash height
            last_height     = new_height

        time.sleep(pause)
        # cuộn ngược lên từ từ để load lại hết nội dung
        for y in range(last_height, 0, -scroll_step):
            self.browser.execute_script(f"window.scrollTo(0, {max(y - scroll_step, 0)});")
            time.sleep(pause)
        
        # Đảm bảo body không cuộn thêm khi chụp
        self.browser.execute_script("document.body.style.overflow = 'hidden';")

        # Cập nhật lại kích thước cửa sổ để đủ chụp hết nội dung
        time.sleep(1)
        self.browser.execute_script("window.scrollTo(0,0);")
        time.sleep(2)

        return last_height

    def crawler(self):
        # yêu cầu trình duyệt lấy nội dung trang web.
        self.browser.get(self.url)
        # đừng chờ 30s để trang web có thể tải
        time.sleep(30)
        # cuộn trang để lấy nội dung và chụp lại nội dung màn hình.
        self.scroll_to_end()
        time.sleep(10)

        self.browser.execute_script("""
            let style = document.createElement('style');
            style.innerHTML = 'div[class*="popup"], div[class*="modal"], div[class*="overlay"] { display: none !important; }';
            document.head.appendChild(style);
        """)
        # dùng script để lấy độ dài của trang
        page_height         = self.browser.execute_script("return document.documentElement.scrollHeight")
        # thiết lại kích thước trang
        self.browser.set_window_size(Configure.SCREEN_WIDTH, page_height)
        time.sleep(5)
        # chụp màn hình và lưu lại
        result              = self.browser.execute_cdp_cmd("Page.captureScreenshot", {
            "fromSurface": True,
            "captureBeyondViewport": True
        })

        with open(os.path.join(self.ws, "screenshot.png"), "wb") as fp:
            fp.write(base64.b64decode(result['data']))

        # lấy mã nguồn của trang web để xử lý.
        with open(os.path.join(self.ws, "index.html"), "w", encoding="utf-8") as fp:
            fp.write(self.browser.page_source)

    def close(self):        self.browser.close()