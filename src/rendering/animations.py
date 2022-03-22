import time


def ms_time():
    return int(time.time() * 1000)


class Animation_manager:
    def __init__(self) -> None:
        self.z_dict = {}

    def tile(self, animation, tag, tmxdata, image):
        try:
            if (
                ms_time() - self.z_dict[tag]["last"]
                >= self.z_dict[tag]["animation"][self.z_dict[tag]["frame"] - 1].duration
            ):
                self.z_dict[tag]["frame"] += 1
                if (
                    self.z_dict[tag]["frame"] >= self.z_dict[tag]["total"] + 1
                    and self.z_dict[tag]["loop"]
                ):
                    self.z_dict[tag]["frame"] = 0
                self.z_dict[tag]["last"] = ms_time()

            if self.z_dict[tag]["frame"] == 0:
                return image
            else:
                return tmxdata.get_tile_image_by_gid(
                    self.z_dict[tag]["animation"][self.z_dict[tag]["frame"] - 1].gid
                )

        except KeyError:
            self.z_dict[tag] = {
                "animation": animation,
                "frame": 0,
                "total": len(animation),
                "last": ms_time(),
                "loop": True,
            }
            return tmxdata.get_tile_image_by_gid(animation[0].gid)
