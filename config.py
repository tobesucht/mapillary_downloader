import os
from bounding_box import *

class Config(object):

    HTTP_PROXY = "http://127.0.0.1:3128"
    HTTPS_PROXY = "http://127.0.0.1:3128"
    DOWNLOAD_DIRECTORY = "/app/data"
    # https://help.mapillary.com/hc/en-us/articles/360010234680-Accessing-imagery-and-data-through-the-Mapillary-API
    ACCESS_TOKEN = "MLY|" # put your token here
    TIMEOUT_TIME = 5
    TIMEOUT_RETRIES = 5
    RETRIES_BACKOFF_FACTOR = 2
    # testing was successfull with a number of 20 threads
    NUMBER_OF_THREADS = 20
    MIN_LON=float(bounding_box().office_small().west)
    MAX_LON=float(bounding_box().office_small().east)
    MIN_LAT=float(bounding_box().office_small().south)
    MAX_LAT=float(bounding_box().office_small().north)
    DOWNLOAD_FEATURES = "TRUE"
    DOWNLOAD_IMAGE_META_INFORMATION = "TRUE"
    DOWNLOAD_IMAGES = "TRUE"

    # texts for logging
    str_env = ' has been set to: '
    str_std = ' has been set to standard value: '
    attr_http_proxy = 'HTTP_PROXY'
    attr_https_proxy = 'HTTPS_PROXY'
    attr_download_directory = 'DOWNLOAD_DIRECTORY'
    attr_access_tocken = 'ACCESS_TOKEN'
    attr_timeout_time = 'TIMEOUT_TIME'
    attr_timeout_retries = 'TIMEOUT_RETRIES'
    attr_retries_backoff_factor = 'RETRIES_BACKOFF_FACTOR'
    attr_number_of_threads = 'NUMBER_OF_THREADS'
    attr_min_lon = 'MIN_LON'
    attr_max_lon = 'MAX_LON'
    attr_min_lat = 'MIN_LAT'
    attr_max_lat = 'MAX_LAT'
    attr_download_features = 'DOWNLOAD_FEATURES'
    attr_download_image_meta_information = 'DOWNLOAD_IMAGE_META_INFORMATION'
    attr_download_images = 'DOWNLOAD_IMAGES'

    # if some environmental variables are provided, they will override the standard values
    try:
        os.environ[attr_http_proxy] = os.environ[attr_http_proxy]
        print(attr_http_proxy + str_env + os.environ[attr_http_proxy])
    except KeyError:
        os.environ[attr_http_proxy] = HTTP_PROXY
        print(attr_http_proxy + str_std + os.environ[attr_http_proxy])

    try:
        os.environ[attr_https_proxy] = os.environ[attr_https_proxy]
        print(attr_https_proxy + str_env + os.environ[attr_https_proxy])
    except KeyError:
        os.environ[attr_https_proxy] = HTTPS_PROXY
        print(attr_https_proxy + str_std + os.environ[attr_https_proxy])

    try:
        DOWNLOAD_DIRECTORY = os.environ[attr_download_directory]
        print(attr_download_directory + str_env + DOWNLOAD_DIRECTORY)
    except KeyError:
        print(attr_download_directory + str_std + DOWNLOAD_DIRECTORY)

    try:
        ACCESS_TOKEN = os.environ[attr_access_tocken]
        print(attr_access_tocken + str_env + ACCESS_TOKEN)
    except KeyError:
        print(attr_access_tocken + str_std + ACCESS_TOKEN)

    try:
        TIMEOUT_TIME = int(os.environ[attr_timeout_time])
        print(attr_timeout_time + str_env + str(TIMEOUT_TIME))
    except KeyError:
        print(attr_timeout_time + str_std + str(TIMEOUT_TIME))

    try:
        TIMEOUT_RETRIES = int(os.environ[attr_timeout_retries])
        print(attr_timeout_retries + str_env + str(TIMEOUT_RETRIES))
    except KeyError:
        print(attr_timeout_retries + str_std + str(TIMEOUT_RETRIES))

    try:
        RETRIES_BACKOFF_FACTOR = int(os.environ[attr_retries_backoff_factor])
        print(attr_retries_backoff_factor + str_env + str(RETRIES_BACKOFF_FACTOR))
    except KeyError:
        print(attr_retries_backoff_factor + str_std + str(RETRIES_BACKOFF_FACTOR))

    try:
        NUMBER_OF_THREADS = int(os.environ[attr_number_of_threads])
        print(attr_number_of_threads + str_env + str(NUMBER_OF_THREADS))
    except KeyError:
        print(attr_number_of_threads + str_std + str(NUMBER_OF_THREADS))

    try:
        MIN_LON=float(os.environ[attr_min_lon])
        print(attr_min_lon + str_env + str(MIN_LON))
    except KeyError:
        print(attr_min_lon + str_std + str(MIN_LON))

    try:
        MAX_LON=float(os.environ[attr_max_lon])
        print(attr_max_lon + str_env + str(MAX_LON))
    except KeyError:
        print(attr_max_lon + str_std + str(MAX_LON))

    try:
        MIN_LAT = float(os.environ[attr_min_lat])
        print(attr_min_lat + str_env + str(MIN_LAT))
    except KeyError:
        print(attr_min_lat + str_std + str(MIN_LAT))

    try:
        MAX_LAT = float(os.environ[attr_max_lat])
        print(attr_max_lat + str_env + str(MAX_LAT))
    except KeyError:
        print(attr_max_lat + str_std + str(MAX_LAT))
    BOUNDING_BOX = bounding_box(MIN_LON,MIN_LAT, MAX_LON, MAX_LAT)

    try:
        DOWNLOAD_FEATURES = os.environ[attr_download_features].upper() == 'TRUE'
        print(attr_download_features + str_env + str(DOWNLOAD_FEATURES))
    except KeyError:
        print(attr_download_features + str_std + str(DOWNLOAD_FEATURES))

    try:
        DOWNLOAD_IMAGES = os.environ[attr_download_images].upper() == 'TRUE'
        print(attr_download_images + str_env + str(DOWNLOAD_IMAGES))
    except KeyError:
        print(attr_download_images + str_std + str(DOWNLOAD_IMAGES))

    try:
        DOWNLOAD_IMAGE_META_INFORMATION = os.environ[attr_download_image_meta_information].upper() == 'TRUE'
        print(attr_download_image_meta_information + str_env + str(DOWNLOAD_IMAGE_META_INFORMATION))
    except KeyError:
        print(attr_download_image_meta_information + str_std + str(DOWNLOAD_IMAGE_META_INFORMATION))