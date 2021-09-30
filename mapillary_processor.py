import mercantile, requests, json
from vt2geojson.tools import vt_bytes_to_geojson
from os import path
import tqdm
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

class mapillary_processor:

    output = {}
    feature_types = {}
    tile_layers = {}
    pbar = None
    session = None
    timeout = 2

    def __init__(self, access_token, root_dir, bounding_box):
        self.access_token = access_token
        self.root_dir = root_dir
        self.bounding_box = bounding_box
        # get the list of tiles with x and y coordinates which intersect our bounding box
        # MUST be at zoom level 14 where the data is available, other zooms currently not supported
        self.tiles = list(mercantile.tiles(self.bounding_box.west, self.bounding_box.south, self.bounding_box.east, self.bounding_box.north, 14))
        # https://stackoverflow.com/questions/15431044/can-i-set-max-retries-for-requests-request
        self.session = requests.Session()
        retries = Retry(total=5,
            backoff_factor=2,
            status_forcelist=[ 500, 502, 503, 504 ])
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

    def process(self):
        print('processing {} tiles in {}'.format(str(len(self.tiles)), self.__class__.__name__))
        # loop through list of tiles to get tile z/x/y to plug in to Mapillary endpoints and make request
        for tile in self.tiles:
            for type in self.feature_types:
                tile_url = 'https://tiles.mapillary.com/maps/vtp/{}/2/{}/{}/{}?access_token={}'.format(type,tile.z,tile.x,tile.y,self.access_token)
                response = self.session.get(tile_url, timeout=self.timeout)
                for layer in self.tile_layers:
                    data = vt_bytes_to_geojson(response.content, tile.x, tile.y, tile.z,layer=layer)
                    if len(data['features']) > 0:
                        print('Tile {}/{}/{}: processing {} {}s in {}'.format(tile.z,tile.x,tile.y,str(len(data['features'])),type,self.__class__.__name__))
                        pbar = tqdm.tqdm(total=len(data['features']), desc='features', position=0, leave=True)
                        for feature in data['features']:
                            if self.__in_bb__(feature):
                                feature['properties']['tile_x'] = tile.x
                                feature['properties']['tile_y'] = tile.y
                                feature['properties']['tile_z'] = tile.z
                                self.__process_feature__(feature)
                            pbar.update(1)

                        pbar.close()
                        self.__export__(tile.x, tile.y, tile.z, type, layer)
        print('end {}'.format(self.__class__.__name__))
        print('====================================')

    def __process_feature__(self, feature):
        self.output['features'].append(feature)

    def __in_bb__(self, feature):
        if feature['geometry']['type'] == 'Point':
            long = feature['geometry']['coordinates'][0]
            lat = feature['geometry']['coordinates'][1]
            return long > self.bounding_box.west\
                and long < self.bounding_box.east\
                and lat > self.bounding_box.south\
                and lat < self.bounding_box.north
        else:
            # we only filter for point features
            return True
        

    def __export__(self, tile_x, tile_y, tile_z, type, layer):
        # save a local geojson with the filtered data

        my_path = path.join(self.root_dir, '{}_{}_{}_{}_{}.geojson'.format(tile_x, tile_y, tile_z, type, layer))
        #my_path = path.join(self.root_dir, '{}_{}.geojson'.format(type, layer))
        # TODO: Don´t do, if 0 features!
        with open(my_path, 'w') as f:
            json.dump(self.output, f)
        # TODO: Make more beautyful
        self.output= { "type": "FeatureCollection", "features": [] }

    

