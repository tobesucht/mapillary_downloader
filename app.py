import os

def is_docker():
    path = '/proc/self/cgroup'
    return (
        os.path.exists('/.dockerenv') or
        os.path.isfile(path) and any('docker' in line for line in open(path))
    )

is_docker = is_docker()
if is_docker:
    print("Running in Docker environment.")

if not is_docker:
    print("Running in normal environment.")

from config import Config
from meta_downloader import meta_downloader
from multi_downloader import multi_downloader 
from image_downloader import image_downloader 

if Config.DOWNLOAD_IMAGES:
    mid = image_downloader()
    mid.process()

if Config.DOWNLOAD_FEATURES:
    mid = multi_downloader()
    mid.process()

if Config.DOWNLOAD_IMAGE_META_INFORMATION:
    mid = meta_downloader()
    mid.process()