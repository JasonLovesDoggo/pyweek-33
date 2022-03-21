import time


def ms_time():
    return int(time.time() * 1000)


class Animation_manager:
    def __init__(self) -> None:
        self.z_dict = {}

    def tile(self, animation, x, y, z, tmxdata):
        i = f"{z} {y} {x}"
        try:
            if (
                ms_time() - self.z_dict[i]["last"]
                >= self.z_dict[i]["animation"][self.z_dict[i]["frame"] - 1].duration
            ):
                self.z_dict[i]["frame"] += 1
                if (
                    self.z_dict[i]["frame"] >= self.z_dict[i]["total"] + 1
                    and self.z_dict[i]["loop"]
                ):
                    self.z_dict[i]["frame"] = 0
                self.z_dict[i]["last"] = ms_time()

            if self.z_dict[i]["frame"] == 0:
                return tmxdata.get_tile_image(x, y, z)
            else:
                return tmxdata.get_tile_image_by_gid(
                    self.z_dict[i]["animation"][self.z_dict[i]["frame"] - 1].gid
                )

        except KeyError:
            self.z_dict[i] = {
                "animation": animation,
                "frame": 0,
                "total": len(animation),
                "last": ms_time(),
                "loop": True,
            }
            return tmxdata.get_tile_image_by_gid(animation[0].gid)
