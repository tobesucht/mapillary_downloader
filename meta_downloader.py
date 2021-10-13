from mapillary_processor import mapillary_processor
from os import path
import os


class meta_downloader(mapillary_processor):

    # vector tile endpoints -- change this in the API request to reference the correct endpoint
    feature_types = {'mly1_public'}

    # tile layer depends which vector tile endpoints: 
    # 1. if map features or traffic signs, it will be "point" always
    # 2. if looking for coverage, it will be "image" for points, "sequence" for lines, or "overview" for far zoom
    tile_layers = {"image"}

    resolution = 'id,captured_at,compass_angle,sequence,geometry'

    def __process_feature__(self, feature):
        # create a folder for each unique tile and sequence ID to group images by tiles and sequence
        sequence_id = feature['properties']['sequence_id']
        tile_x = feature['properties']['tile_x']
        tile_y = feature['properties']['tile_y']
        tile_z = feature['properties']['tile_z']
        my_path = path.join(self.root_dir, '{}_{}_{}'.format(tile_x, tile_y, tile_z), sequence_id)
        if not os.path.exists(my_path):
            os.makedirs(my_path)

        # request the URL of each image
        image_id = feature['properties']['id']
        # in order to continue previously started runs
        if not os.path.exists('{}/{}.jpg'.format(my_path, image_id)):
            header = {'Authorization' : 'OAuth {}'.format(self.access_token)}
            url = 'https://graph.mapillary.com/{}?fields={}'.format(image_id, self.resolution)
            resp = self.session.get(url, headers=header, timeout=self.timeout)
            data = resp.json()
            # only for test purposes
            print(data)

    def __export__(self, type, layer):
        return