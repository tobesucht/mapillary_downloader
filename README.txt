The tool downloads all trips, images and observations from mapillay which reside in the configured bounding box. The content is stored in directories per tile at the specified loaction (volume). 
The tool checks if the imagery has already been downloaded to the specified location and skips it accordingly. This processing allows to update the data set without downloading all raster images over and over again. 
The vector information (geojson files) are always recreated.

How to start:
Build locally:
docker build --no-cache -t mapillary_downloader-2.0.5 .

docker-compose -f docker-compose.yml up

Release to GitLab Container Registry:
docker build -t mapillary_downloader:2.0.5 .
docker push mapillary_downloader:2.0.5

Usage examples: 

Using standard values:
docker run -d=false --tty --network host -v /home/tobesucht/temp/mapillary:/app/data/ mapillary_downloader-2.0.5

Setting proxies and disabling the download of meta information:
docker run -d=false --tty --network host -v /home/tobesucht/temp/mapillary:/app/data/ --env HTTP_PROXY=http://127.0.0.1:3128 --env HTTPS_PROXY=http://127.0.0.1:3128 --env DOWNLOAD_IMAGE_META_INFORMATION=FALSE  mapillary_downloader-2.0.5

Download some area of Munich:
docker run -d=false --tty --network host -v /home/tobesucht/temp/mapillary:/app/data/ --env MIN_LON=11.51422 --env MAX_LON=11.55642 --env MIN_LAT=48.16665 --env MAX_LAT=48.19522  mapillary_downloader-2.0.5

Download Munich:
docker run -d=false --tty --network host -v /home/tobesucht/temp/mapillary:/app/data/ --env MIN_LON=11.384 --env MAX_LON=11.755 --env MIN_LAT=48.0314 --env MAX_LAT=48.25 mapillary_downloader:2.0.5

Setting all parameters:
docker run -d=false --tty --network host -v /home/tobesucht/temp/mapillary:/app/data/ --env HTTP_PROXY=http://127.0.0.1:3128 --env HTTPS_PROXY=http://127.0.0.1:3128 --env DOWNLOAD_DIRECTORY=/app/data/ --env ACCESS_TOKEN=MLY| --env TIMEOUT_TIME=5 --env TIMEOUT_RETRIES=5 --env RETRIES_BACKOFF_FACTOR=2 --env NUMBER_OF_THREADS=20 --env MIN_LON=11.51422 --env MAX_LON=11.53425 --env MIN_LAT=48.16665 --env MAX_LAT=48.19522 --env DOWNLOAD_FEATURES=TRUE --env DOWNLOAD_IMAGES=TRUE --env DOWNLOAD_IMAGE_META_INFORMATION=TRUE  mapillary_downloader-2.0.5

API documentation: https://www.mapillary.com/developer/api-documentation/

Here are two queries which alow to query meta data for a BB or a sequence ID using the browser:
https://graph.mapillary.com/images?access_token=MLY|&fields=id,altitude,atomic_scale,camera_parameters,camera_type,captured_at,compass_angle,computed_altitude,computed_compass_angle,computed_geometry,computed_rotation,exif_orientation,height,width,merge_cc,sfm_cluster,sequence,geometry,mesh,detections,thumb_256_url,thumb_1024_url,thumb_2048_url,thumb_original_url&sequence_ids=dbu7kk2xxvx5t42pxgnizb
https://graph.mapillary.com/images?access_token=MLY|&fields=id,altitude,atomic_scale,camera_parameters,camera_type,captured_at,compass_angle,computed_altitude,computed_compass_angle,computed_geometry,computed_rotation,exif_orientation,height,width,merge_cc,sfm_cluster,sequence,geometry,mesh,detections,thumb_256_url,thumb_1024_url,thumb_2048_url,thumb_original_url&bbox=11.51422,48.16665,11.53425,48.19522

