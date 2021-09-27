from multi_downloader import multi_downloader 
from image_downloader import image_downloader 
from bounding_box import *

access_token = 'MLY|'
root_dir = '/home/mapillary/20210924_test/'
bb = bounding_box().paf()


mid = image_downloader(access_token, root_dir, bb)
mid.process()

mid = multi_downloader(access_token, root_dir, bb)
mid.process()