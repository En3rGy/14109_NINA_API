# coding: UTF-8

import unittest
import time

# functional import

import json
import urllib2
import ssl
import urlparse
import threading


#########################################################

class hsl20_4:
    LOGGING_NONE = 0

    def __init__(self):
        pass

    class BaseModule:
        debug_output_value = {}  # type: {}
        debug_set_remanent = {}  # type: {}
        debug_input_value = {}  # type: {}

        def __init__(self, a, b):
            pass

        def _get_framework(self):
            f = hsl20_4.Framework()
            return f

        def _get_logger(self, a, b):
            return 0

        def _get_remanent(self, key):
            return 0

        def _set_remanent(self, key, val):
            self.debug_set_remanent = val

        def _set_output_value(self, pin, value):
            """

            :type pin: int
            """
            self.debug_output_value[int(pin)] = value
            print "# Out: pin " + str(pin) + " <- " + str(value)

        def _get_input_value(self, pin):
            if pin in self.debug_input_value:
                return self.debug_input_value[pin]
            else:
                return 0

        def _get_module_id(self):
            return 123

    class Framework:
        def __init__(self):
            pass

        def _run_in_context_thread(self, a):
            pass

        def create_debug_section(self):
            d = hsl20_4.DebugHelper()
            return d

        def get_homeserver_private_ip(self):
            return "127.0.0.1"

        def get_instance_by_id(self, id):
            return ""

        def resolve_dns(self, a):
            import socket
            data = socket.gethostbyname_ex(a)
            ips = data[2]
            print(a + " -> " + str(ips[0]))
            return str(ips[0])

    class DebugHelper:
        def __init__(self):
            pass

        def set_value(self, cap, text):
            print("DEBUG value\t'" + str(cap) + "': " + str(text))

        def add_message(self, msg):
            print("Debug Msg\t" + str(msg))

        def add_exception(self, msg):
            print("EXCEPTION Msg\t" + str(msg))


#########################################################

##!!!!##################################################################################################
#### Own written code can be placed above this commentblock . Do not change or delete commentblock! ####
########################################################################################################
##** Code created by generator - DO NOT CHANGE! **##

class NINAAPI_14109_14109(hsl20_4.BaseModule):

    def __init__(self, homeserver_context):
        hsl20_4.BaseModule.__init__(self, homeserver_context, "hsl20_4_NINA_API")
        self.FRAMEWORK = self._get_framework()
        self.LOGGER = self._get_logger(hsl20_4.LOGGING_NONE, ())
        self.PIN_I_SAGS = 1
        self.PIN_I_NUPDATERATE = 2
        self.PIN_I_NON = 3
        self.PIN_O_SALLWARNINGS = 1
        self.PIN_O_SHEADLINE = 2
        self.PIN_O_NSEVERITY = 3
        self.PIN_O_SURGENCY = 4
        self.PIN_O_SCERTAINTY = 5
        self.PIN_O_SDESCR = 6
        self.PIN_O_SINSTR = 7
        self.PIN_O_NEVENTID = 8
        self.PIN_O_SEVENTSYMBOLURL = 9
        self.PIN_O_SJSON = 10

    ########################################################################################################
    #### Own written code can be placed after this commentblock . Do not change or delete commentblock! ####
    ###################################################################################################!!!##

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
                       "event_id:    " + str(self.event_id))

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

        def get_val(self, json_data, key, do_xmlcharrefreplace=True):
            # type : (json, str, bool) -> any
            val = str()

            if type(json_data) != dict:
                return val

            if key in json_data:
                val = json_data[key]
            if (type(val) == str or type(val) == unicode) and do_xmlcharrefreplace:
                val = val.encode("ascii", "xmlcharrefreplace")
            return val

        def set_detailed_warning(self, detailed_warning_json):
            # type: ({}) -> bool

            if type(detailed_warning_json) == str:
                try:
                    detailed_warning_json = json.loads(detailed_warning_json)
                except Exception as e:
                    return False

            self.status = self.get_val(detailed_warning_json, "status")
            info = self.get_val(detailed_warning_json, "info")  # type: any

            if type(info) == list and len(info) == 1:
                info = info[0]

            if type(info) != dict:
                return False

            if "eventCode" in info:
                if len(info["eventCode"]) == 1:
                    self.event_code = self.get_val(info["eventCode"][0], "value")
                    self.symbol_url = "https://nina.api.proxy.bund.dev/api31/appdata/gsb/eventCodes/" + \
                                      self.event_code + ".png"

                    if "EVC" in self.event_code:
                        self.event_id = int(self.event_code[len(self.event_code) - 3:])
                    else:
                        self.event_id = 1

            self.description = self.get_val(info, "description")
            self.instruction = self.get_val(info, "instruction")

            return True

        def set_warning(self, warning_json):
            # type: (json) -> str

            if type(warning_json) == str:
                try:
                    warning_json = json.loads(warning_json)
                except Exception as e:
                    return str()

            self.warning_json = warning_json

            self.id = self.get_val(warning_json, "id")
            self.expires = self.get_val(warning_json, "expires")
            self.effective = self.get_val(warning_json, "effective")

            if "payload" not in warning_json:
                return str()

            payload = warning_json["payload"]
            if "data" in payload:
                data = payload["data"]

                self.headline = self.get_val(data, "headline")
                self.severity = self.get_val(data, "severity")
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

    def get_data(self, warning_id=str()):
        # type: (str) -> str

        if warning_id:
            url_parsed = urlparse.urlparse("https://nina.api.proxy.bund.dev/api31/warnings/")
        else:
            url_parsed = urlparse.urlparse("https://nina.api.proxy.bund.dev/api31/dashboard")
        # Use Framework to resolve the host ip address.
        host_ip = self.FRAMEWORK.resolve_dns(url_parsed.hostname)
        # Append port if provided.
        netloc = host_ip
        if url_parsed.port is not None:
            netloc += ':%s' % url_parsed.port
        # Build URL with the host replaced by the resolved ip address.
        url_resolved = urlparse.urlunparse((url_parsed[0], netloc) + url_parsed[2:])  # type : str
        # Build a SSL Context to disable certificate verification.
        response_data = ""
        ags = self._get_input_value(self.PIN_I_SAGS)  # type : str
        try:
            if warning_id:
                url_resolved = url_resolved + "/" + warning_id + ".json"
            else:
                url_resolved = url_resolved + "/" + str(ags) + ".json"
            ctx = ssl._create_unverified_context()

            request = urllib2.Request(url_resolved, headers={'Host': url_parsed.hostname, "accept": "application/json"})
            response = urllib2.urlopen(request, context=ctx)
            response_data = response.read()

        except Exception as e:
            self.DEBUG.add_message("14109 " + str(ags) + ": In 'get_data', " + str(e) + " for '" + url_resolved + "'")

        finally:
            return response_data

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
        if not bool(self._get_input_value(self.PIN_I_NON)):
            self.log_msg("in 'update' stopping timer due to on = False.")
            self.t.cancel()
            return

        interval = self._get_input_value(self.PIN_I_NUPDATERATE)
        if interval <= 0:
            self.log_msg("in 'update' stopping timer due to interval <= 0.")
            self.t.cancel()
            return

        warnings = []  # type: [Warning]

        self.log_msg("Requesting NINA data.")
        data = self.get_data()
        if not data:
            self.reset_outputs()
        else:
            try:
                data = json.loads(data)
            except Exception as e:
                self.log_msg("In 'update' " + str(e))
                return

            for warning in data:
                w = self.Warning()
                warning_id = w.set_warning(warning)
                if warning_id:
                    detailed_data = self.get_data(warning_id)
                    w.set_detailed_warning(detailed_data)
                warnings.append(w)

            res = []  # type: [Warning]
            for i in warnings:
                if i not in res:
                    res.append(i)

            warnings = res

            warnings = self.bubble_sort(warnings)
            worst_warning = warnings[-1]

            # remove duplicates from headlines
            all_warnings = []
            for i in warnings:
                if i.headline not in all_warnings:
                    all_warnings.append(i.headline)

            all_warnings_text = str()
            for i in all_warnings:
                all_warnings_text = str(i) + all_warnings_text
                all_warnings_text = ", " + all_warnings_text

            all_warnings_text = all_warnings_text[2:]

            # self.id = str()  # type: str
            # self.effective = str()  # type: str
            # self.expires = str()  # type: str
            # self.status = str()  # type: str

            self.set_output_value_sbc(self.PIN_O_SJSON, worst_warning.warning_json)
            self.set_output_value_sbc(self.PIN_O_SDESCR, worst_warning.description)
            self.set_output_value_sbc(self.PIN_O_SINSTR, worst_warning.instruction)
            self.set_output_value_sbc(self.PIN_O_NEVENTID, worst_warning.event_id)
            self.set_output_value_sbc(self.PIN_O_NSEVERITY, worst_warning.severity)
            self.set_output_value_sbc(self.PIN_O_SURGENCY, worst_warning.severity_id)
            self.set_output_value_sbc(self.PIN_O_SHEADLINE, worst_warning.headline)
            self.set_output_value_sbc(self.PIN_O_SEVENTSYMBOLURL, worst_warning.symbol_url)
            self.set_output_value_sbc(self.PIN_O_SALLWARNINGS, all_warnings_text)

        self.t = threading.Timer(interval, self.update)
        self.t.start()

    def bubble_sort(self, w):
        # type: ([]) -> []
        for n in range(len(w) - 1, 1, -1):
            for i in range(0, len(w) - 1):
                if w[i] > w[i + 1]:
                    w[i], w[i + 1] = w[i + 1], w[i]
        return w

    def on_init(self):
        self.DEBUG = self.FRAMEWORK.create_debug_section()
        self.g_out_sbc = {}  # type: dict
        self.t = threading.Timer(100, self.update)  # type: threading.Timer

        self.update()

    def on_input_value(self, index, value):
        self.update()


################################################################################


class TestSequenceFunctions(unittest.TestCase):
    test = NINAAPI_14109_14109(0)

    def setUp(self):
        print("\n###setUp")
        with open("credentials.txt") as f:
            self.cred = json.load(f)

        self.test = NINAAPI_14109_14109(0)
        self.test.debug_input_value[self.test.PIN_I_SAGS] = self.cred["PIN_I_SAGS"]
        self.test.debug_input_value[self.test.PIN_I_NUPDATERATE] = 10

        self.test.debug_input_value[self.test.PIN_I_NON] = False
        self.test.on_init()
        self.test.debug_input_value[self.test.PIN_I_NON] = True

    def test_operators(self):
        print("\n### test_operators")
        self.test.debug_input_value[self.test.PIN_I_NON] = False
        self.test.on_input_value(self.test.PIN_I_NON, False)
        w1 = Warning()
        w2 = Warning()
        w3 = Warning()
        w4 = Warning()

        w1.severity_id = 4
        w2.severity_id = 5
        w3.severity_id = 2
        w4.severity_id = 8

        self.assertTrue(w1 == w1)
        self.assertFalse(w1 == w2)
        self.assertTrue(w1 != w2)
        self.assertFalse(w1 != w1)
        self.assertTrue(w1 < w4)
        self.assertFalse(w4 < w1)
        self.assertTrue(w4 > w1)
        self.assertFalse(w1 > w4)

    def test_bubble_sort(self):
        print("\n### test_bubble_sort")
        w1 = 4
        w2 = 5
        w3 = 2
        w4 = 8

        w = [w1, w2, w3, w4]
        w_res = self.test.bubble_sort(w)

        w_solution = [w3, w1, w2, w4]

        self.assertEqual(w_res, w_solution)

    def test_update(self):
        print("\n### test_update (! combines several other testcases !)")
        self.test.debug_input_value[self.test.PIN_I_NUPDATERATE] = 60
        self.test.update()
        self.test.debug_input_value[self.test.PIN_I_NUPDATERATE] = 0

    def test_mult_update(self):
        print("\n### test_mult_update (! combines several other testcases !)")
        self.test.debug_input_value[self.test.PIN_I_NON] = 1
        self.test.debug_input_value[self.test.PIN_I_NUPDATERATE] = 3
        self.test.on_init()
        res = self.test.debug_output_value[self.test.PIN_O_SALLWARNINGS]
        self.assertTrue(res)
        self.test.reset_outputs()
        time.sleep(8)
        res = self.test.debug_output_value[self.test.PIN_O_SALLWARNINGS]
        self.assertTrue(res)

    def test_stop(self):
        print("\n### test_stop (! combines several other testcases !)")
        self.test.debug_input_value[self.test.PIN_I_NON] = 1
        self.test.debug_input_value[self.test.PIN_I_NUPDATERATE] = 3
        self.test.on_init()
        self.test.reset_outputs()
        self.test.debug_input_value[self.test.PIN_I_NON] = 0
        time.sleep(5)
        res = self.test.debug_output_value[self.test.PIN_O_SALLWARNINGS]
        self.assertFalse(res)

    def test_get_json(self):
        print("\n### test_get_json")
        ret = self.test.get_data()
        print(ret)
        self.assertTrue(ret)

    def test_error_ags(self):
        print("\n### test_error_ags")
        self.test.debug_input_value[self.test.PIN_I_SAGS] = "125"
        self.test.on_input_value(self.test.PIN_I_SAGS, "123")
        symbol_url = self.test.debug_output_value[self.test.PIN_O_SEVENTSYMBOLURL]
        print(symbol_url)
        self.assertTrue(symbol_url == "0")

    def test_error_json(self):
        print("\n### test_error_json")
        ret = self.test.Warning()
        res = ret.set_warning("Not a valid json")
        self.assertFalse(res)

        res = ret.set_detailed_warning("Not a valid json")
        self.assertFalse(res)

    def tearDown(self):
        print("\n### tearDown")
        self.test.debug_input_value[self.test.PIN_I_NON] = False
        self.test.on_input_value(self.test.PIN_I_NON, False)


if __name__ == '__main__':
    unittest.main()
