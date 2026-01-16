from .data import REGIONS


def get_regions():
    """Return all Tanzania regions"""
    return sorted(REGIONS.keys())


def get_districts(region_name: str):
    """Return districts for a given region"""
    return REGIONS.get(region_name, [])
