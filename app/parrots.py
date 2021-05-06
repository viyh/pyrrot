from pil_trans import save_transparent_gif
from PIL import Image
import requests
from io import BytesIO
import re
from flask import current_app as app
from urllib.parse import urlparse


PARROTS = {
    "bored": {"moves": [(45, 108)] * 10},
    "conga": {
        "moves": [
            (144, 99),
            [(162, 90), (-108, 90)],
            [(144, 90), (-126, 90)],
            [(135, 99), (-135, 99)],
            [(162, 108), (-108, 108)],
            [(153, 126), (-117, 126)],
            [(198, 144), (-72, 126)],
            [(288, 126), (0, 126)],
            [(324, 135), (54, 135)],
            (108, 108),
        ]
    },
    "left": {
        "moves": [
            (144, 99),
            (108, 90),
            (81, 90),
            (36, 99),
            (36, 108),
            (54, 126),
            (90, 144),
            (135, 126),
            (153, 117),
            (162, 108),
        ]
    },
    "middle": {
        "moves": [
            (81, 90),
            (36, 99),
            (36, 108),
            (54, 126),
            (90, 144),
            (207, 126, True, False),
            (243, 108, True, False),
            (261, 99, True, False),
            (252, 90, True, False),
            (234, 81, True, False),
            (198, 81, True, False),
            (117, 63),
        ]
    },
    "right": {
        "moves": [
            (85, 99),
            (121, 90),
            (148, 90),
            (193, 99),
            (193, 108),
            (175, 126),
            (139, 144),
            (94, 126),
            (76, 117),
            (67, 108),
        ]
    },
}


class Parrot:
    def __init__(
        self,
        name: str,
        moves: list = [],
        overlay: str = None,
        speed: int = 50,
        size: float = 1.0,
        offset_x: int = 0,
        offset_y: int = 0,
        resize: str = None,
    ):
        self.name = name
        self.moves = moves if moves else PARROTS[name]["moves"]
        # 20ms appears to be the minimum duration for the Pillow library
        self.speed = self.set_value(int, speed, "speed", 20, 1000, 50)
        self.offset_x = self.set_value(int, offset_x, "offset_x", -320, 320, 0)
        self.offset_y = self.set_value(int, offset_y, "offset_y", -320, 320, 0)
        self.overlay = overlay
        self.size = self.set_value(float, size, "size", 0.01, 2.0, 1.0)
        self.resize = self.set_resize(resize)
        self.overlay_image = self.get_overlay_image() if self.overlay else None

    def set_resize(self, resize):
        new_resize = None
        if resize:
            match = re.search(r"(\d+)x(\d+)", resize)
            if match and len(match.groups()) == 2:
                new_resize = (int(match.group(1)), int(match.group(2)))
        return new_resize

    def set_value(self, valtype, value, attr, min, max, default):
        try:
            new_val = valtype(value)
            if new_val <= min:
                new_val = min
            if new_val >= max:
                new_val = max
            setattr(self, attr, new_val)
            return new_val
        except ValueError:
            app.logger.info(f"Bad {attr} value: [{value}]")
            return default

    def __str__(self):
        return str(self.__dict__)

    def create_image(self):
        overlay_frames = [self.overlay_frame(frame) for frame in range(len(self.moves))]
        fp_out = f"/tmp/{self.name}.gif"
        save_transparent_gif(overlay_frames, self.speed, fp_out)
        return fp_out

    def overlay_frame(self, frame):
        # create transparent square canvas
        canvas = Image.new("RGBA", (320, 320))
        frame_image = Image.open(f"/app/images/{self.name}/frame-{frame+1:03d}.png")
        frame_image = frame_image.convert("RGBA")

        # put frame image at bottom of canvas square
        canvas.paste(frame_image, (0, 91))

        # center overlay image over frame canvas, then set offset for overlay image
        if self.overlay_image:
            processed_overlay = self.overlay_image
            x1 = int(0.5 * canvas.size[0]) - int(0.5 * processed_overlay.size[0])
            y1 = int(0.5 * canvas.size[1]) - int(0.5 * processed_overlay.size[1])
            if isinstance(self.moves[frame], tuple):
                self.moves[frame] = [self.moves[frame]]
            for moves in self.moves[frame]:
                # if 2 < len(moves) and moves[2]:
                #     processed_overlay = processed_overlay.transpose(
                #         Image.FLIP_LEFT_RIGHT
                #     )
                # if 3 < len(moves) and moves[3]:
                #     processed_overlay = processed_overlay.transpose(
                #         Image.FLIP_TOP_BOTTOM
                #     )
                offset = (
                    x1 + moves[0] + int(self.offset_x),
                    y1 + moves[1] + int(self.offset_y),
                )
                canvas.paste(processed_overlay, offset, processed_overlay)
        if self.resize:
            canvas = canvas.resize(self.resize)
        return canvas

    def get_overlay_image(self):
        if not self.test_image_url():
            app.logger.info(f"Could not download image from URL: [{self.overlay}]")
            return None
        overlay_image = self.get_image_from_url(self.overlay)
        overlay_image = overlay_image.resize(
            (
                int(overlay_image.size[0] * self.size),
                int(overlay_image.size[1] * self.size),
            )
        )
        return overlay_image

    def get_image_from_url(self, url):
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        image = image.convert("RGBA")
        return image

    def is_valid_url(self, x):
        try:
            result = urlparse(x)
            return all([result.scheme, result.netloc, result.path])
        except Exception:
            return False

    def test_image_url(self):
        if not self.is_valid_url(self.overlay):
            app.logger.info("Overlay URL is not a valid URL.")
            return False
        image_formats = ("image/png", "image/jpeg", "image/jpg", "image/gif")
        r = requests.head(self.overlay)
        if r.headers["content-type"] in image_formats:
            return True
        return False
