from .utils import get_regions, get_districts


def region_choices():
    return [(r, r) for r in get_regions()]


def district_choices(region_name: str):
    return [(d, d) for d in get_districts(region_name)]
