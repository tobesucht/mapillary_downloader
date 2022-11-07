from mapillary_processor import mapillary_processor
from os import path
import os
import threading

class meta_downloader(mapillary_processor):

    # vector tile endpoints -- change this in the API request to reference the correct endpoint
    feature_types = {'mly1_public'}

    # tile layer depends which vector tile endpoints: 
    # 1. if map features or traffic signs, it will be "point" always
    # 2. if looking for coverage, it will be "image" for points, "sequence" for lines, or "overview" for far zoom
    tile_layers = {"image"}

    extra_name = 'meta'

    fields = 'id,altitude,atomic_scale,camera_parameters,camera_type,captured_at,compass_angle,computed_altitude,computed_compass_angle,computed_geometry,computed_rotation,exif_orientation,height,width,merge_cc,sfm_cluster,sequence,geometry,mesh,detections,thumb_256_url,thumb_1024_url,thumb_2048_url,thumb_original_url'

    def __process_feature__(self, feature):
        # request the URL of each image
        image_id = feature['properties']['id']
        header = {'Authorization' : 'OAuth {}'.format(self.access_token)}
        # limited to 50.000 per hour
        url = 'https://graph.mapillary.com/{}?fields={}'.format(image_id, self.fields)
        resp = self.session.get(url, headers=header, timeout=self.timeout_time)
        data = resp.json()
        feature = {"type":"Feature"}
        feature['geometry'] = None
        feature['computed_geometry'] = None
        feature['properties'] = {}
        feature['properties']['id'] = None
        feature['properties']['sequence'] = None
        feature['properties']['altitude'] = None
        feature['properties']['atomic_scale'] = None
        feature['properties']['camera_parameters'] = None
        feature['properties']['camera_type'] = None
        feature['properties']['captured_at'] = None
        feature['properties']['compass_angle'] = None
        feature['properties']['computed_altitude'] = None
        feature['properties']['computed_compass_angle'] = None
        feature['properties']['computed_rotation'] = None
        feature['properties']['exif_orientation'] = None
        feature['properties']['height'] = None
        feature['properties']['width'] = None
        feature['properties']['merge_cc'] = None
        feature['properties']['sfm_cluster'] = None

        # The position of the meta information and the position of the image differ between the two 
        # different sources https://graph.mapillary.com/ (image data) and https://tiles.mapillary.com/ (tile content data).
        # TODO: We have to find out which is the more correct location using some experiments
        if 'geometry' in data:
            feature['geometry'] = data['geometry']
        if 'computed_geometry' in data:
            feature['computed_geometry'] = data['computed_geometry']
        if 'id' in data:
            feature['properties']['id'] = data['id']
        if 'sequence' in data:
            feature['properties']['sequence'] = data['sequence']
        if 'altitude' in data:
            feature['properties']['altitude'] = data['altitude']
        if 'atomic_scale' in data:
            feature['properties']['atomic_scale'] = data['atomic_scale']
        if 'camera_parameters' in data:
            feature['properties']['camera_parameters'] = data['camera_parameters']
        if 'camera_type' in data:
            feature['properties']['camera_type'] = data['camera_type']
        if 'captured_at' in data:
            feature['properties']['captured_at'] = data['captured_at']
        if 'compass_angle' in data:
            feature['properties']['compass_angle'] = data['compass_angle']
        if 'computed_altitude' in data:
            feature['properties']['computed_altitude'] = data['computed_altitude']
        if 'computed_compass_angle' in data:
            feature['properties']['computed_compass_angle'] = data['computed_compass_angle']
        if 'computed_rotation' in data:
            feature['properties']['computed_rotation'] = data['computed_rotation']
        if 'exif_orientation' in data:
            feature['properties']['exif_orientation'] = data['exif_orientation']
        if 'height' in data:
            feature['properties']['height'] = data['height']
        if 'width' in data:
            feature['properties']['width'] = data['width']
        if 'merge_cc' in data:
            feature['properties']['merge_cc'] = data['merge_cc']
        if 'sfm_cluster' in data:
            feature['properties']['sfm_cluster'] = data['sfm_cluster']

        self.output['features'].append(feature)
