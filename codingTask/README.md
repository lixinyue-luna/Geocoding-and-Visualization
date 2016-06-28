# US Power Plant Cooling Systems
*Written in Python v2.7.11. Please install [openpyxl](https://openpyxl.readthedocs.io/en/default/) library to read Excel. Please install [SQLite Browser](http://sqlitebrowser.org/) if you wish to view and modify the databases (optional).*

## 1. `solution.py`
The scrip `solution.py` does the following:

1. Reads Excel files and create databases of cooling types and geographic information for US power plants.
2. Create a folder for each cooling type.
3. Uses [Google Static Maps API](https://developers.google.com/maps/documentation/static-maps/intro) to find satellite images of the plants.
4. Save images in the folder of the corresponding cooling type.

To avoid wasting rate limit, the program fires a new query through API only when the image has never been downloaded before, i.e., does not exist in any folder.

For each run, the program will check if the image already exists in folder or not. If yes, then the program will not consume the Google API. In the case where a power plant has multiple cooling types, the program will download image for one cooling folder, and copy the image to the other cooling folders. For example, plant Barry has two types of cooling systems: Once through cooling and Recirculating. The program will retrieve the plant satellite image to the Once through cooling folder, and copy the image file to the Recirculating folder instead of downloading a new one.

Please run `solution.py` to start downloading images. All the images will be saved in the folder `images`. You can change 'countLimit' to limit the number of queries per run. Please note that the with current API key, the number of free queries is rate limited 2500 per day.

## 2. `solution2.py`
`solution2.py` has the same functionality as `solution.py` but adds more flexibility. It enables user to customize the following variables:
* General:
  * `countLimit`: Defines how many new images to be retrieved for each run. Default `100`.
* Image specifications:
  * `mapType`: The type of map to construct. Possible types include `satellite` (default), `roadmap`, `hybrid`, and `terrain`.
  * `zoom`: Defines the zoom level of the map, which determines the magnification level of the map. Default value is `16`.
  * `size`: Defines the rectangular dimensions of the map image. Default value is `640 pixels x 640 pixels`.
  * `image_format`: Defines the format of the resulting image. Possible formats include `png` (default), `jpeg`, and `gif`.
  * `key`: Google API key. Enables access to daily quota. Available in the [Google Developers Console](https://console.developers.google.com)

For more on image specifications, please see [Google Static Maps Developer Guide](https://developers.google.com/maps/documentation/static-maps/intro#URL_Parameters).

`soultion2.py` also takes a different approach to determining when to fire a request to download a new image. A database is used to track saved images and their corresponding folders.

Please run `solution2.py` to customize image specifications and start downloading images. If you wish to start all over, please delete both the power plant database (`powerPlant.sqlite`) and the downloaded images in the folder named `images2`. 
