from utils import airports
from third_party.openweather import client as weather_client


def main(iata_code: str):
    coords = airports.get_coord_by_iata_code(iata_code)
    # tz = airports.get_tz_by_iata_code(iata_code)

    weather_data = weather_client.get_weather_by_coord(lat=coords.lat, lon=coords.lon)

    for w in weather_data:
        import pdb

        pdb.set_trace()
        pass
    pass


if __name__ == "__main__":
    main("ICN")
