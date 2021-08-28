# Changelog

All notable changes to udemyscraper will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [0.7.4] - 2021-08-25

### Added

- Checks if cache files are present in the working directory or not
- If cache files are present and caching is set to enabled, it will use the cached files for scraping
- Added a clear cache argument that will delete the cache files and generate new ones
- Automatically clear cache if query/ course being scraped is different

- | With Cache               | Without Cache               |
  | ------------------------ | --------------------------- |
  | ![Cache](docs/cache.gif) | ![Cache](docs/no_cache.gif) |
  | 3 Seconds                | 17 Seconds                  |


## [0.7.3] - 2021-08-25


### Added

- Udemyscraper now shows a progressbar when active displaying the task being done.
- Disable progressbar when evoked as a module
- Add an argument to enable/disable progressbar
- Progress check sections and modules
- Disable Progressbar when quiet mode is on.


## [0.7.2] - 2021-08-23

### Added

- Logging levels - debug and info


## [0.7.1] - 2021-08-16

### Added

-  Added another key to the options dictionary for debug level.

### Changed

- Now Displays all the debug messages of both selenium's web driver and the script
- Increased timeout limit for page load
- Removed some redundant code and fixed typos


[0.7.4]: https://github.com/sortedcord/udemy-web-scraper/pull/32
[0.7.3]: https://github.com/sortedcord/udemy-web-scraper/pull/29
[0.7.2]: https://github.com/sortedcord/udemy-web-scraper
[0.7.1]: https://github.com/sortedcord/udemy-web-scraper
