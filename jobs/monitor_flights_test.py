import pytest_mock

from jobs import monitor_flights

_FLIGHT_SEARCH_RESULT = {
    "flight_date": "2025-02-23",
    "flight_status": "active",
    "departure": {
        "airport": "Seoul (Incheon)",
        "timezone": "Asia/Seoul",
        "iata": "ICN",
        "icao": "RKSI",
        "terminal": "1",
        "gate": "19",
        "delay": 42,
        "scheduled": "2025-02-23T12:40:00+00:00",
        "estimated": "2025-02-23T12:40:00+00:00",
        "actual": "2025-02-23T13:21:00+00:00",
        "estimated_runway": "2025-02-23T13:21:00+00:00",
        "actual_runway": "2025-02-23T13:21:00+00:00",
    },
    "arrival": {
        "airport": "Narita International Airport",
        "timezone": "Asia/Tokyo",
        "iata": "NRT",
        "icao": "RJAA",
        "terminal": "1",
        "gate": "44",
        "baggage": None,
        "delay": 18,
        "scheduled": "2025-02-23T14:55:00+00:00",
        "estimated": "2025-02-23T14:55:00+00:00",
        "actual": None,
        "estimated_runway": None,
        "actual_runway": None,
    },
    "airline": {"name": "Asiana Airlines", "iata": "OZ", "icao": "AAR"},
    "flight": {
        "number": "104",
        "iata": "OZ104",
        "icao": "AAR104",
        "codeshared": None,
    },
    "aircraft": {"registration": "HL7793", "iata": "A333", "icao": "A333", "icao24": "71BF93"},
    "live": {
        "updated": "2025-02-23T05:44:57+00:00",
        "latitude": 36.5384,
        "longitude": 140.613,
        "altitude": 4579.62,
        "direction": 182.3,
        "speed_horizontal": 646.884,
        "speed_vertical": -2.34,
        "is_ground": False,
    },
}


def test_monitor_flights(mocker: pytest_mock.MockFixture):
    mock_kakaotalk = mocker.patch("third_party.kakao.client.send_to_me")
    mock_filter_flights_of_interest = mocker.patch(
        "jobs.monitor_flights._filter_flights_of_interest", return_value=[_FLIGHT_SEARCH_RESULT]
    )
    mock_aviation_request = mocker.patch(
        "third_party.aviationstack.request.get_live_flights", return_value=[_FLIGHT_SEARCH_RESULT]
    )

    monitor_flights.main("ICN", "NRT")

    mock_filter_flights_of_interest.assert_called_once_with([_FLIGHT_SEARCH_RESULT])
    mock_aviation_request.assert_called_once_with(dep_iata="ICN", arr_iata="NRT", airline="asiana")
    mock_kakaotalk.assert_called_once_with(
        """
            비행편 OZ104 조회 결과
            출발지: Seoul (Incheon)
            도착지: Narita International Airport
            출발 지연: 총 42분
            도착 지연: 총 18분
            실제 출발: 오후 01시 21분
            도착 예정: 오후 03시 13분
        """
    )
