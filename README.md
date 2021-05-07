# Party Pyrrot
Simple Party Parrot generator API and UI.

* [Party Pyrrot on GitHub](https://github.com/viyh/pyrrot)
* [Party Pyrrot on DockerHub](https://hub.docker.com/repository/docker/viyh/pyrrot)

## Installation
* Build the docker container:

```
    docker build -t viyh/pyrrot .
```

* Run the docker container:
```
    docker run --rm -it -p 5000:5000 viyh/pyrrot
```

* Open a browser and go to http://localhost:5000 then make some parrots.

## API

The API is accessible at `/api/v1`.

* `/parrots` [`GET`] - List the available parrots
* `/parrots/<parrot>` [`GET`, `POST`] - Return default parrot image
    - `overlay` - The URL for the overlay image. Default: None
    - `speed` - The speed of parroting expressed in milliseconds per frame between 20 and 1000. Default: 50 ms per frame
    - `size` - The size of the overlay image expressed as an float between 0.1 and 2.0. Default: 1.0
    - `offset_x` - The x-axis offset in pixels of the overlay image expressed as an integer between -320 and 320. Default: 0
    - `offset_x` - The y-axis offset in pixels of the overlay image expressed as an integer between -320 and 320. Default: 0
    - `resize` - The output image size expressed in pixel dimensions as a string "XxY", e.g. "128x128". Default: "320x320"

### Examples

* http://localhost:5000/api/v1/parrots/left?overlay=https://i.imgur.com/wn6X1o4.png&size=1&offset_x=-104&offset_y=-156&speed=50
* http://localhost:5000/api/v1/parrots/left?speed=20&resize=128x128


## To Do
* Fix middle parrot overlay
* Add resize in UI

## Credit
The inspiration for this came from the original PPaaS code: https://github.com/francoislg/PPaaS
