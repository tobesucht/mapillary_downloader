from mapillary_processor import mapillary_processor
import os
#import threading
import urllib3
import requests
import concurrent.futures
from requests.exceptions import HTTPError, RequestException, SSLError

class image_downloader(mapillary_processor):

    # vector tile endpoints -- change this in the API request to reference the correct endpoint
    feature_types = {'mly1_public'}

    # tile layer depends which vector tile endpoints: 
    # 1. if map features or traffic signs, it will be "point" always
    # 2. if looking for coverage, it will be "image" for points, "sequence" for lines, or "overview" for far zoom
    tile_layers = {"image"}

    resolution = 'thumb_original_url'
    # there is also the option to download a lower resolution, but this does not make sense for our use case...:
    # resolution = 'thumb_2048_url'

    def __process_feature__(self, feature):
        # create a folder for each unique tile and sequence ID to group images by tiles and sequence
        sequence_id = feature['properties']['sequence_id']
        tile_x = feature['properties']['tile_x']
        tile_y = feature['properties']['tile_y']
        tile_z = feature['properties']['tile_z']
        my_path = os.path.join(self.root_dir, '{}_{}_{}'.format(tile_x, tile_y, tile_z), sequence_id)
        if not os.path.exists(my_path):
            os.makedirs(my_path)

        image_id = feature['properties']['id']
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.number_of_threads) as executor:
            executor.submit(self.request_image_data, my_path=my_path, image_id=image_id)

    def __export__(self, tile_x, tile_y, tile_z, type, layer):
        return

    def request_image_data(self, my_path, image_id):
        # in order to continue previously started runs
        if not os.path.exists('{}/{}.jpg'.format(my_path, image_id)):
            header = {'Authorization' : 'OAuth {}'.format(self.access_token)}
            # request the URL of each image
            # limited to 50.000 per minute
            url = 'https://graph.mapillary.com/{}?fields={}'.format(image_id, self.resolution)
            resp = self.session.get(url, headers=header, timeout=self.timeout_time)
            data = resp.json()
            if self.resolution in data:
                with concurrent.futures.ThreadPoolExecutor(max_workers=self.number_of_threads) as executor:
                    executor.submit(self.download_image, data=data, my_path=my_path, image_id=image_id)

    def download_image(self, data, my_path, image_id):
        image_url = data[self.resolution]
        image_data = None

        try:
            image_data = self.session.get(image_url, verify='/etc/ssl/certs', stream=True, timeout=self.timeout_time).content
        except (urllib3.exceptions.ReadTimeoutError) as err:
            print('connection timed out: {0}'.format(err))
        except requests.exceptions.ConnectionError as err:
            print('connection error: {0}'.format(err))
        except (HTTPError, RequestException, SSLError) as err:
            print('requests error: {0}'.format(err))
        except BaseException as err:
             print('base exception: {0}'.format(err))

        # save each image with ID as filename to directory by sequence ID
        if image_data: 
            with open('{}/{}.jpg'.format(my_path, image_id), 'wb') as handler:
                handler.write(image_data)
