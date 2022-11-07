import mercantile, requests, json
from vt2geojson.tools import vt_bytes_to_geojson
import os
from tqdm import tqdm
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from config import Config
import concurrent.futures

class mapillary_processor:

    # https://www.mapillary.com/developer/api-documentation/
    output = {}
    feature_types = {}
    tile_layers = {}
    pbar = None
    session = None
    extra_name = ''

    def __init__(self):
        self.__reset__()
        self.access_token = Config.ACCESS_TOKEN
        self.root_dir = Config.DOWNLOAD_DIRECTORY
        self.bounding_box = Config.BOUNDING_BOX
        self.number_of_threads = Config.NUMBER_OF_THREADS
        self.timeout_time = Config.TIMEOUT_TIME
        self.timeout_retries = Config.TIMEOUT_RETRIES
        self.retries_backoff_factor = Config.RETRIES_BACKOFF_FACTOR
        
        # get the list of tiles with x and y coordinates which intersect our bounding box
        # MUST be at zoom level 14 where the data is available, other zooms currently not supported
        self.tiles = list(mercantile.tiles(self.bounding_box.west, self.bounding_box.south, self.bounding_box.east, self.bounding_box.north, 14))
        # https://stackoverflow.com/questions/15431044/can-i-set-max-retries-for-requests-request
        self.session = requests.Session()
        retries = Retry(total=self.timeout_retries,
            backoff_factor=self.retries_backoff_factor,
            #status_forcelist= tuple( x for x in requests.status_codes._codes if x != 400))
            status_forcelist=[ 500, 502, 503, 504 ])
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

    def process(self):
        print('processing {} tiles in {}'.format(str(len(self.tiles)), self.__class__.__name__))
        # loop through list of tiles to get tile z/x/y to plug in to Mapillary endpoints and make request
        for tile in self.tiles:
            for type in self.feature_types:
                # limited to 50.000 per day
                tile_url = 'https://tiles.mapillary.com/maps/vtp/{}/2/{}/{}/{}?access_token={}'.format(type,tile.z,tile.x,tile.y,self.access_token)
                response = self.session.get(tile_url, timeout=self.timeout_time)
                for layer in self.tile_layers:
                    data = vt_bytes_to_geojson(response.content, tile.x, tile.y, tile.z,layer=layer)
                    if len(data['features']) > 0:
                        print('Tile {}/{}/{}: processing {} {}s in {}'.format(tile.z,tile.x,tile.y,str(len(data['features'])),type,self.__class__.__name__))
                        features = []
                        for feature in data['features']:
                            if self.__in_bb__(feature):
                                feature['properties']['tile_x'] = tile.x
                                feature['properties']['tile_y'] = tile.y
                                feature['properties']['tile_z'] = tile.z
                                features.append(feature)
                        with tqdm(total=len(features)) as pbar:
                            with concurrent.futures.ThreadPoolExecutor(max_workers=self.number_of_threads) as executor:
                                futures = {executor.submit(self.__process_feature__, feature): feature for feature in features}
                                for future in concurrent.futures.as_completed(futures):
                                    pbar.update(1)
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
        my_dir = os.path.join(self.root_dir, '{}_{}_{}'.format(tile_x, tile_y, tile_z))
        if not os.path.exists(my_dir):
            os.makedirs(my_dir)
        my_file = os.path.join(my_dir, '{}_{}_{}_{}_{}_{}.geojson'.format(tile_x, tile_y, tile_z, type, layer, self.extra_name))
        if (len(self.output["features"])) > 0:
            with open(my_file, 'w') as f:
                json.dump(self.output, f)
            self.__reset__()

    def __reset__(self):
        self.output = { "type": "FeatureCollection", "features": [] }

    

