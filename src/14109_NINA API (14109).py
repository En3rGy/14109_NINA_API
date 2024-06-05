# coding: UTF-8

import json
import urllib2
import ssl
import urlparse
import threading

##!!!!##################################################################################################
#### Own written code can be placed above this commentblock . Do not change or delete commentblock! ####
########################################################################################################
##** Code created by generator - DO NOT CHANGE! **##

class NINAAPI_14109_14109(hsl20_4.BaseModule):

    def __init__(self, homeserver_context):
        hsl20_4.BaseModule.__init__(self, homeserver_context, "hsl20_4_NINA_API")
        self.FRAMEWORK = self._get_framework()
        self.LOGGER = self._get_logger(hsl20_4.LOGGING_NONE,())
        self.PIN_I_SAGS=1
        self.PIN_I_LATITUDE=2
        self.PIN_I_LONGITUDE=3
        self.PIN_I_NUPDATERATE=4
        self.PIN_I_NON=5
        self.PIN_I_PROCESS_DWD=6
        self.PIN_O_SALLWARNINGS=1
        self.PIN_O_SHEADLINE=2
        self.PIN_O_NSEVERITY=3
        self.PIN_O_SURGENCY=4
        self.PIN_O_SCERTAINTY=5
        self.PIN_O_SDESCR=6
        self.PIN_O_SINSTR=7
        self.PIN_O_NEVENTID=8
        self.PIN_O_SEVENTSYMBOLURL=9
        self.PIN_O_SJSON=10

########################################################################################################
#### Own written code can be placed after this commentblock . Do not change or delete commentblock! ####
###################################################################################################!!!##

        self.debug = False
        self.warnings = []

    # Warnungen vor extremem Unwetter (Stufe 4) → lila
    # Unwetterwarnungen (Stufe 3) → rot
    # Warnungen vor markantem Wetter (Stufe 2) → orange
    # Wetterwarnungen (Stufe 1) → gelb
    # Vorabinformation Unwetter → rot gestreift
    # Hitzewarnung (extrem) → dunkles flieder → Level +20
    # Hitzewarnung → helles flieder → Level +20
    # UV - Warnung → rosa → Level 20
    # Keine Warnungen → ---

    severity = {"Vorwarnung": 1, "Minor": 2, "Moderate": 3, "Severe": 4, "Extreme": 5}

    class Warning:
        def __init__(self):
            self.warning_json = {}  # type: {str, any}
            self.headline = str()  # type: str
            self.severity = str()  # type: str
            self.severity_id = -1  # type: int
            self.id = str()  # type: str
            self.effective = str()  # type: str
            self.expires = str()  # type: str
            self.status = str()  # type: str
            self.description = str()  # type: str
            self.instruction = str()  # type: str
            self.event_code = str()  # type: str
            self.symbol_url = str()  # type: str
            self.event_id = -1  # type: int
            self.severity_lookup = {"Vorwarnung": 1, "Minor": 2, "Moderate": 3, "Severe": 4, "Extreme": 5}
            self.process_dwd = False
            self.geojson = {}

        def __str__(self):
            return str("\n-------------\n" +
                       "headline:    " + self.headline.encode('ascii', 'ignore') + "\n" +
                       "severity:    " + self.severity.encode('ascii', 'ignore') + " / " +
                       str(self.severity_id) + "\n" +
                       "id:          " + self.id.encode('ascii', 'ignore') + "\n" +
                       "effective:   " + self.effective.encode('ascii', 'ignore') + "\n" +
                       "expires:     " + self.expires.encode('ascii', 'ignore') + "\n" +
                       "status:      " + self.status.encode('ascii', 'ignore') + "\n" +
                       "description: " + self.description.encode('ascii', 'ignore') + "\n" +
                       "instruction: " + self.instruction.encode('ascii', 'ignore') + "\n" +
                       "event_code:  " + self.event_code.encode('ascii', 'ignore') + "\n" +
                       "symbol url:  " + self.symbol_url + "\n" +
                       "event_id:    " + str(self.event_id) + "\n" +
                       "geojson:     " + json.dumps(self.geojson))

        def __le__(self, other):
            # <=
            return self.severity_id <= other.severity_id

        def __lt__(self, other):
            # <
            return self.severity_id < other.severity_id

        def __ge__(self, other):
            # >=
            return self.severity_id >= other.severity_id

        def __gt__(self, other):
            # >
            return self.severity_id > other.severity_id

        def __eq__(self, other):
            # ==
            return (self.warning_json == other.warning_json and
                    self.headline == other.headline and
                    self.severity == other.severity and
                    self.severity_id == other.severity_id and
                    self.id == other.id and
                    self.effective == other.effective and
                    self.expires == other.expires and
                    self.status == other.status and
                    self.description == other.description and
                    self.instruction == other.instruction and
                    self.event_code == other.event_code and
                    self.symbol_url == other.symbol_url and
                    self.event_id == other.event_id)

        def __ne__(self, other):
            # !=
            return (self.warning_json != other.warning_json or
                    self.headline != other.headline or
                    self.severity != other.severity or
                    self.severity_id != other.severity_id or
                    self.id != other.id or
                    self.effective != other.effective or
                    self.expires != other.expires or
                    self.status != other.status or
                    self.description != other.description or
                    self.instruction != other.instruction or
                    self.event_code != other.event_code or
                    self.symbol_url != other.symbol_url or
                    self.event_id != other.event_id)

        def check_poi_relevance(self, lat, lon):
            if not self.geojson:
                raise Exception("Warning | get_polygons() | No geojson for warning available!")

            polygons = []
            for feature in self.geojson["features"]:
                polygon = feature["geometry"]["coordinates"][0]
                polygons.append(polygon)

            for polygon in polygons:
                if is_point_in_polygon((lon, lat), polygon):
                    return True

            return False

        def set_detailed_warning(self, detailed_warning_json):
            # type: ({}) -> bool

            self.status = get_val(detailed_warning_json, "status")

            if not "info" in detailed_warning_json:
                raise Exception("No ìnfo-data in detailed_warning!")
            else:
                info = detailed_warning_json["info"]

                if isinstance(info, list) and len(info) == 1:
                    info = info[0]
                elif isinstance(info, list) and len(info) != 1:
                    for i in info:
                        if "de" in get_val(i, "language"):
                            info = i
                            break

                if not isinstance(info, dict):
                    raise Exception("set_detailed_warning | Not a dict. Aborting")

                if ("senderName" in info) and not self.process_dwd:
                    sender_name = get_val(info, "senderName")
                    if sender_name == "Deutscher Wetterdienst":
                        raise Exception("Received DWD warning. Aborting. "
                                        "Use other logic module to capture weather warnings!")

                if "eventCode" in info:
                    if len(info["eventCode"]) == 1:
                        self.event_code = get_val(info["eventCode"][0], "value")
                else:
                    self.event_code = "BBK-EVC-001"

            self.symbol_url = "https://nina.api.proxy.bund.dev/api31/appdata/gsb/eventCodes/{}.png".format(self.event_code)

            if "EVC" in self.event_code:
                self.event_id = int(self.event_code[len(self.event_code) - 3:])
            else:
                self.event_id = 1

            self.geojson = get_val(detailed_warning_json, "geojson")
            self.description = get_val(info, "description")
            self.instruction = get_val(info, "instruction")

            # print("set_detailed_warning | {}".format(detailed_warning_json))

            return True

        def set_warning(self, warning_json):
            # type: (json) -> str
            if isinstance(warning_json, str):
                try:
                    warning_json = json.loads(warning_json)
                except Exception as e:
                    return str()

            self.warning_json = warning_json

            self.id = get_val(warning_json, "id")
            self.expires = get_val(warning_json, "expires")
            self.effective = get_val(warning_json, "effective")

            if "payload" not in warning_json:
                return str()

            payload = warning_json["payload"]
            if "data" in payload:
                data = payload["data"]

                self.headline = get_val(data, "headline")
                self.severity = get_val(data, "severity")
                if self.severity in self.severity_lookup:
                    self.severity_id = self.severity_lookup[self.severity]

            if "id" in payload:
                payload_id = payload["id"]
                return payload_id

            return str()

    def set_output_value_sbc(self, pin, val):
        if pin in self.g_out_sbc:
            if self.g_out_sbc[pin] == val:
                print ("# SBC: pin " + str(pin) + " <- data not send / " + str(val).decode("utf-8"))
                return

        self._set_output_value(pin, val)
        self.g_out_sbc[pin] = val

    def get_nina_data(self, warning_id=str()):
        # type: (str) -> str

        api_url = "https://warnung.bund.de/api31"
        ags = self._get_input_value(self.PIN_I_SAGS)  # type : str

        if warning_id:
            url_json = "{}/warnings/{}.json".format(api_url, warning_id)
        else:
            url_json = "{}/dashboard/{}.json".format(api_url, ags)

        # Build a SSL Context to disable certificate verification.
        response_json = {}

        try:
            response_json = get_web_json(url_json)

            # get geojson & attach to warning infos
            if warning_id:
                url_geojson = "{}/warnings/{}.geojson".format(api_url, warning_id)
                geo_json = get_web_json(url_geojson)
                response_json[u"geojson"] = geo_json

        except Exception as e:
            self.log_msg("get_data | Exception: {}".format(e))

        return response_json

    def reset_outputs(self):
        self.DEBUG.add_message("14109 " + str(self._get_input_value(self.PIN_I_SAGS)) + ": Delete warn data.")
        self.set_output_value_sbc(self.PIN_O_SALLWARNINGS, "")
        self.set_output_value_sbc(self.PIN_O_SHEADLINE, "")
        self.set_output_value_sbc(self.PIN_O_NSEVERITY, 0)
        self.set_output_value_sbc(self.PIN_O_SJSON, "")
        self.set_output_value_sbc(self.PIN_O_SINSTR, "")
        self.set_output_value_sbc(self.PIN_O_SDESCR, "")
        self.set_output_value_sbc(self.PIN_O_SCERTAINTY, "")
        self.set_output_value_sbc(self.PIN_O_SURGENCY, "")
        self.set_output_value_sbc(self.PIN_O_NEVENTID, "")
        self.set_output_value_sbc(self.PIN_O_SEVENTSYMBOLURL, "0")

    def log_msg(self, msg):
        # type: (str) -> None
        self.DEBUG.add_message("14109 " + str(self._get_input_value(self.PIN_I_SAGS)) + ": " + str(msg))

    def update(self):
        # type: () -> None
        interval = self._get_input_value(self.PIN_I_NUPDATERATE)
        if not bool(self._get_input_value(self.PIN_I_NON)) or interval <= 0:
            self.log_msg("update() | Stopping timer due user input.")
            self.t.cancel()
            return

        self.warnings = []  # type: [Warning]

        self.log_msg("Requesting NINA data.")
        data = self.get_nina_data()
        if not data:
            self.reset_outputs()
        else:
            try:
                for warning in data:
                    w = self.Warning()
                    w.process_dwd = bool(self._get_input_value(self.PIN_I_PROCESS_DWD))
                    warning_id = w.set_warning(warning)
                    if warning_id:
                        try:
                            detailed_data = self.get_nina_data(warning_id)
                            w.set_detailed_warning(detailed_data)

                            lat = float(self._get_input_value(self.PIN_I_LATITUDE))
                            lon = float(self._get_input_value(self.PIN_I_LONGITUDE))

                            if not w.check_poi_relevance(lat, lon):
                                # print("DEBUG | update | Area of Interest is NOT part of warning {} {}".format(w.id, w.headline))
                                continue  # don't add warning to warnings
                        except Exception as e:
                            self.log_msg("update() | Exception {}. Continuing with next warning.".format(e))
                            continue

                    if not w in self.warnings:
                        self.warnings.append(w)

                self.warnings = bubble_sort(self.warnings)
                worst_warning = Warning()
                if len(self.warnings) > 0:
                    worst_warning = self.warnings[-1]

                # Remove duplicates from headlines and concatenate them into a single string
                # Use a set to store unique headlines and join the unique headlines with ", " separator
                unique_headlines = set(i.headline for i in self.warnings)
                all_warnings_text = ", ".join(unique_headlines)

                self.set_output_value_sbc(self.PIN_O_SJSON, worst_warning.warning_json)
                self.set_output_value_sbc(self.PIN_O_SDESCR, worst_warning.description)
                self.set_output_value_sbc(self.PIN_O_SINSTR, worst_warning.instruction)
                self.set_output_value_sbc(self.PIN_O_NEVENTID, worst_warning.event_id)
                self.set_output_value_sbc(self.PIN_O_NSEVERITY, worst_warning.severity)
                self.set_output_value_sbc(self.PIN_O_SURGENCY, str(worst_warning.severity_id))
                self.set_output_value_sbc(self.PIN_O_SHEADLINE, worst_warning.headline)
                self.set_output_value_sbc(self.PIN_O_SEVENTSYMBOLURL, worst_warning.symbol_url)
                self.set_output_value_sbc(self.PIN_O_SALLWARNINGS, all_warnings_text)
            except Exception as e:
                self.log_msg("Update() | {}".format(e))

        self.t = threading.Timer(interval, self.update)
        self.t.start()

    def on_init(self):
        self.DEBUG = self.FRAMEWORK.create_debug_section()
        self.g_out_sbc = {}  # type: dict
        interval = self._get_input_value(self.PIN_I_NUPDATERATE)
        self.t = threading.Timer(interval, self.update)  # type: threading.Timer
        self.update()

    def on_input_value(self, index, value):
        self.update()

def is_point_in_polygon(point, polygon):
    """
    Determines if a point is inside a given polygon.

    This function uses the ray-casting algorithm to test if a point is inside a polygon.
    It is particularly useful in geographical and computer graphics applications.

    Args:
    point (tuple): A tuple containing the x and y coordinates of the point to test (x, y).
    polygon (list): A list of tuples where each tuple represents the x and y coordinates of a polygon vertex [(x1, y1), (x2, y2), ...].

    Returns:
    bool: True if the point is inside the polygon, False otherwise.

    Notes:
    - If the polygon has fewer than 3 vertices, the function returns True and logs a debug message.

    Example:
    > is_point_in_polygon((3, 4), [(1, 1), (1, 5), (5, 5), (5, 1)])
    True

    > is_point_in_polygon((6, 4), [(1, 1), (1, 5), (5, 5), (5, 1)])
    False
    """
    x, y = point
    n = len(polygon)
    if n < 3:
        print("DEBUG | is_point_in_polygon({}, {}). Polygon is too short. Returning True!".format(point, polygon))
        return True

    inside = False

    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside

def get_web_json(url):
    """
    Fetches and returns JSON data from a specified URL.

    This function sends a GET request to the given URL, expecting a JSON response.
    It handles SSL verification by creating an unverified context and parses the JSON
    response.

    Args:
    url (str): The URL to fetch the JSON data from.

    Returns:
    dict: A dictionary containing the parsed JSON data.

    Raises:
    Exception: If there is an error during the request or while parsing the response.

    Example:
    > get_web_json('https://api.example.com/data')
    {'key': 'value', ...}

    Note:
    This function ignores SSL certificate verification, which is not recommended
    for production use due to security risks.
    """
    try:
        ctx = ssl._create_unverified_context()
        request = urllib2.Request(url, headers={"accept": "application/json"})
        response = urllib2.urlopen(request, context=ctx)
        response_json = json.loads(response.read())
        return response_json
    except Exception as e:
        raise Exception("get_web_json({}) | {}".format(url, e))

def bubble_sort(w):
    # type: (list) -> list
    """
    Sorts a list of elements in ascending order using the bubble sort algorithm.

    Bubble sort is a simple sorting algorithm that repeatedly steps through the list,
    compares adjacent elements and swaps them if they are in the wrong order. The pass
    through the list is repeated until the list is sorted.

    Args:
    w (list): A list of elements to be sorted.

    Returns:
    list: The sorted list in ascending order.

    Example:
    > bubble_sort([3, 2, 1])
    [1, 2, 3]

    > bubble_sort([1, 2, 3])
    [1, 2, 3]

    > bubble_sort([5, 1, 4, 2, 8])
    [1, 2, 4, 5, 8]
    """
    for n in range(len(w) - 1, 1, -1):
        for i in range(0, len(w) - 1):
            if w[i] > w[i + 1]:
                w[i], w[i + 1] = w[i + 1], w[i]
    return w


def get_val(json_data, key, do_xmlcharrefreplace=True):
    # type : (dict, str, bool) -> any
    """
    Retrieve the value associated with the given key from a JSON dictionary.

    Args:
        json_data (dict): The JSON dictionary to search.
        key (str): The key whose value is to be retrieved.
        do_xmlcharrefreplace (bool): Whether to replace XML character references.

    Returns:
        any: The value associated with the key, with optional XML character reference replacement.
    """
    # Initialize an empty string as the default value
    val = ""

    # Check if the input is a dictionary
    if not isinstance(json_data, dict):
        return val

    # Retrieve the value associated with the key if it exists
    val = json_data.get(key, "")

    # Check if the value is a string or unicode, and replace XML character references if needed
    if isinstance(val, (str, unicode)) and do_xmlcharrefreplace:
        val = val.encode("ascii", "xmlcharrefreplace")

    return val
