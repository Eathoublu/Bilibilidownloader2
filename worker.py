from utils.logger import logger
from utils.auto_utils import AutoUtils
from utils.findauthor import run
from utils.downloader_manager import executor, single_video

import os
import argparse
from tqdm import tqdm

class GreenSystem:
    __doc__ = """
    用于下载指定的up主的视频，从命令行获取要被爬取的up。
    启动后，将不停地爬取数据库中的视频
    鲁棒性暂未提升
    """
    def __init__(self, db_path, user_dy_path, video_down_path):
        self.db_path = db_path
        self.user_dy_path = user_dy_path
        self.video_down_path = video_down_path
        self.check_dirs()
        self.findauthor = run
        self.auto_utils = AutoUtils(db_path=self.db_path)

    @staticmethod
    def make_dirs(path):
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

    def check_dirs(self):
        self.make_dirs(self.user_dy_path)
        self.make_dirs(self.video_down_path)

    def run(self):
        while True:
            bvid = self.auto_utils.get_one_vid()
            # executor([bvid,], location=self.video_down_path)
            single_video(bvid, location=self.video_down_path)
            self.auto_utils.flag_one_video(bvid)


    def find_ups(self, ups=[]):
        for mid in tqdm(ups):
            self.findauthor(mid, down_pics=True, down_loc=self.user_dy_path, db_path=self.db_path)








class BlueSystem:
    __doc__ = """
    不获取视频和图片，专注于研究单个用户数据和用户关系
    """
    def __init__(self, db_path):
        self.db_path = db_path

    def


def main():
    green_system = GreenSystem(db_path='GREEN.DB', user_dy_path='data/green/user_dynamics', video_down_path='data/green/videos')
    # green_system.find_ups(['12473905', ])
    green_system.run()
if __name__ == '__main__':

    main()