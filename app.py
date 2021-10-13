from meta_downloader import meta_downloader
from multi_downloader import multi_downloader 
from image_downloader import image_downloader 
from bounding_box import *

# https://help.mapillary.com/hc/en-us/articles/360010234680-Accessing-imagery-and-data-through-the-Mapillary-API
access_token = 'MLY|'
root_dir = '/home/mapillary/20210924_test/'
bb = bounding_box().novi_small()


mid = image_downloader(access_token, root_dir, bb)
mid.process()

mid = multi_downloader(access_token, root_dir, bb)
mid.process()

mid = meta_downloader(access_token, root_dir, bb)
#mid.process()