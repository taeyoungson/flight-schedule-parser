import pytest_mock

from jobs import parse_flight_ocr_result

_FLIGHT_OCR_RESULT = """
Total Block Time 90:35, Total Add Block Time 12:35, DAFF (Total : 119.0, Used : 26), ANLV (Total : 17, Used : 1)
DATE
FLIGHT
SHOWUP
SECTOR
STD
STA
03/01(토)
STBY확인요망




03/02(일)
521
02 10:15
ICN/LHR
02 12:25
02 18:05
03/03(월)
522

LHR/ICN
03 20:10
04 17:45
03/04(화)
ICN




(03/05(7
DAY OFF




03/06(목)
DAY OFF




03/07(3)
DAY OFF




03/08(토)
8967
G 08 13:50
GMP/CJU
08 14:50
08 16:00
8966

CJU/GMP
08 16:45
08 18:00
8985

GMP/CJU
08 18:45
08 19:55

8984

CJU/GMP
08 20:40
08 21:55
03/09(일)
707
09 19:20
ICN/CRK
09 21:30
10 00:30
03/10(월)
CRK




03/11(화)
708

CRK/ICN
11 01:35
11 06:30
03/12(7)
202
12 12:20
ICN/LAX
12 14:40
12 09:40
"""


def test_parse_flight_schedule(mocker: pytest_mock.MockFixture):
    mock_kakaotalk = mocker.patch("third_party.kakao.client.send_to_me")
    mock_google_calendar_config = mocker.patch("third_party.calendars.config.load_config")
    mock_google_calendar = mocker.patch("third_party.calendars.gcal.GoogleCalendar.create_event")

    parse_flight_ocr_result.build_flight_schedule(_FLIGHT_OCR_RESULT, year=2025, month=3)

    assert mock_kakaotalk.call_count == 1
    assert mock_google_calendar_config.call_count == 1
    assert mock_google_calendar.call_count == 9
