from mapillary_processor import mapillary_processor

class multi_downloader(mapillary_processor):

    # define an empty geojson as output
    output= { "type": "FeatureCollection", "features": [] }

    # vector tile endpoints -- change this in the API request to reference the correct endpoint
    feature_types = {'mly1_public', 'mly_map_feature_point', 'mly_map_feature_traffic_sign', 'mly1_computed_public'}

    # tile layer depends which vector tile endpoints: 
    # 1. if map features or traffic signs, it will be "point" always
    # 2. if looking for coverage, it will be "image" for points, "sequence" for lines, or "overview" for far zoom
    tile_layers = {'image', 'point', 'sequence', 'overview', 'traffic_sign'}

    
