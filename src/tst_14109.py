# coding: UTF-8

import unittest

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
            if a == 'nina.api.proxy.bund.dev':
                return "52.59.159.124"
            else:
                print("Warning! resolve_dns: No IP for hoste reuqest " + a)
                return "127.0.0.1"

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
        self.LOGGER = self._get_logger(hsl20_4.LOGGING_NONE,())
        self.PIN_I_SAGS=1
        self.PIN_I_NUPDATERATE=2
        self.PIN_I_NON=3
        self.PIN_O_SALLWARNINGS=1
        self.PIN_O_SHEADLINE=2
        self.PIN_O_NSEVERITY=3
        self.PIN_O_SURGENCY=4
        self.PIN_O_SCERTAINTY=5
        self.PIN_O_SDESCR=6
        self.PIN_O_SINSTR=7
        self.PIN_O_NEVENTID=8
        self.PIN_O_SJSON=9


########################################################################################################
#### Own written code can be placed after this commentblock . Do not change or delete commentblock! ####
###################################################################################################!!!##

    # Warnungen vor extremem Unwetter (Stufe 4) - lila
    # Unwetterwarnungen (Stufe 3) -> rot
    # Warnungen vor markantem Wetter (Stufe 2) -> orange
    # Wetterwarnungen (Stufe 1) -> gelb
    # Vorabinformation Unwetter -> rot gestreift
    # Hitzewarnung (extrem) -> dunkles flieder -> LEvel +20
    # Hitzewarnung -> helles flieder -> Level +20
    # UV - Warnung -> rosa -> Level 20
    # Keine Warnungen -> ---

    severity = {"Vorwarnung": 1, "Minor": 2, "Moderate": 3, "Severe": 4, "Extreme": 5}

    def set_output_value_sbc(self, pin, val):
        if pin in self.g_out_sbc:
            if self.g_out_sbc[pin] == val:
                print ("# SBC: pin " + str(pin) + " <- data not send / " + str(val))
                return

        self._set_output_value(pin, val)
        self.g_out_sbc[pin] = val

    def get_data(self, warning_id=str()):
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
            # self.set_output_value_sbc(self.PIN_O_BERROR, True)
            self.DEBUG.add_message("14109 " + str(ags) + ": " + str(e) + " for '" + url_resolved + "'")

        return response_data

    def read_json(self, json_data):
        warnings_data = json.loads(json_data)
        self.set_output_value_sbc(self.PIN_O_SJSON, json_data)
        warnings_cnt = len(warnings_data)
        self.DEBUG.set_value("Warnings for " + str(self._get_input_value(self.PIN_I_SAGS)), warnings_cnt)

        if warnings_cnt == 0:
            self.DEBUG.add_message("14109 " + str(self._get_input_value(self.PIN_I_SAGS)) + ": No warn data available.")
            self.reset_outputs()
            return

        all_warnings = self.get_all_warnings(warnings_data)
        if all_warnings:
            self.set_output_value_sbc(self.PIN_O_SALLWARNINGS, all_warnings.encode("ascii", "xmlcharrefreplace"))
        else:
            self.DEBUG.add_message("14109 " + str(self._get_input_value(self.PIN_I_SAGS)) + ": No warn data available.")
            self.valid_data = False
            self.reset_outputs()
            return

        # find worst warning
        worst_data = {}
        max_level = 0
        for i in range(0, warnings_cnt):
            try:
                if "payload" in warnings_data[i]:
                    payload = warnings_data[i]["payload"]
                    if "data" in payload:
                        data = payload["data"]
                        severity = self.get_val(data, "severity")
                        level = 0

                        if severity in self.severity:
                            level = self.severity[severity]
                        else:
                            level = -100

                        if level > max_level:
                            max_level = level
                            worst_data = payload["data"]
                            worst_data["warning_id"] = self.get_val(payload, "id")

                        worst_data["LEVEL"] = max_level

            finally:
                pass

        headline = worst_data["headline"]  # type : str
        level = worst_data["LEVEL"]
        if headline:
            self.set_output_value_sbc(self.PIN_O_SHEADLINE, headline.encode("ascii", "xmlcharrefreplace"))
        if level:
            self.set_output_value_sbc(self.PIN_O_NSEVERITY, level)

        return worst_data

    def complete_worst_warning_data(self, worst_data):
        warning_id = worst_data["warning_id"]
        if warning_id:
            full_warning = self.get_data(warning_id)
            return full_warning

    def read_detailed_json(self, full_warning):
        full_warning = json.loads(full_warning)
        if not full_warning:
            self.valid_data = False
            return

        if "info" not in full_warning:
            self.valid_data = False
            return

        info = full_warning["info"]
        if len(info) == 1:
            info = info[0]
        else:
            self.valid_data = False
            print("Something went wrong")
            return

        # "category": [ "Fire", "Infra" ]
        # "event"

        urgency = self.get_val(info, "urgency")
        certainty = self.get_val(info, "certainty")
        description = self.get_val(info, "description")
        instruction = self.get_val(info, "instruction")

        if urgency:
            self.set_output_value_sbc(self.PIN_O_SURGENCY, urgency.encode("ascii", "xmlcharrefreplace"))
        if certainty:
            self.set_output_value_sbc(self.PIN_O_SCERTAINTY, certainty.encode("ascii", "xmlcharrefreplace"))
        if description:
            self.set_output_value_sbc(self.PIN_O_SDESCR, description.encode("ascii", "xmlcharrefreplace"))
        if instruction:
            self.set_output_value_sbc(self.PIN_O_SINSTR, instruction.encode("ascii", "xmlcharrefreplace"))

        if "eventCode" in info:
            if len(info["eventCode"]) > 0:
                event_code = self.get_val(info["eventCode"][0], "value")
                print(event_code)
                if "EVC" in event_code:
                    event_id = int(event_code[len(event_code)-3:])
                else:
                    event_id = 1

                # event_url = "https://nina.api.proxy.bund.dev/api31/appdata/gsb/eventCodes/" + event_code + ".png"
                self.set_output_value_sbc(self.PIN_O_NEVENTID, event_id)

        self.valid_data = True

    def get_val(self, json_data, key):  # type : str
        val = ""
        if key in json_data:
            val = json_data[key]
        return val

    def get_all_warnings(self, warnings_data):  # type : str
        msg = ""

        for i in range(0, len(warnings_data)):
            warning = warnings_data[i]
            if "payload" in warning:
                if "data" in warning["payload"]:
                    payload = warning["payload"]["data"]
                    msg += self.get_val(payload, "headline")
                    if i < len(warnings_data) - 1:
                        msg += ", "

        return msg

    def reset_outputs(self):
        self.DEBUG.add_message("14109 " + str(self._get_input_value(self.PIN_I_SAGS)) + ": Delete warn data.")
        self.valid_data = False
        self.set_output_value_sbc(self.PIN_O_SALLWARNINGS, "")
        self.set_output_value_sbc(self.PIN_O_SHEADLINE, "")
        self.set_output_value_sbc(self.PIN_O_NSEVERITY, 0)
        self.set_output_value_sbc(self.PIN_O_SJSON, "")
        self.set_output_value_sbc(self.PIN_O_SINSTR, "")
        self.set_output_value_sbc(self.PIN_O_SDESCR, "")
        self.set_output_value_sbc(self.PIN_O_SCERTAINTY, "")
        self.set_output_value_sbc(self.PIN_O_SURGENCY, "")
        self.set_output_value_sbc(self.PIN_O_NEVENTID, "")

    def update(self):
        if not bool(self._get_input_value(self.PIN_I_NON)):
            return

        interval = self._get_input_value(self.PIN_I_NUPDATERATE)
        if interval <= 0:
            return

        try:
            self.DEBUG.add_message("14109 " + str(self._get_input_value(self.PIN_I_SAGS)) + ": Requesting NINA data.")
            data = self.get_data()
            worst_data = self.read_json(data)
            full_warning = self.complete_worst_warning_data(worst_data)
            self.read_detailed_json(full_warning)
        finally:
            threading.Timer(interval, self.update).start()

    def on_init(self):
        self.DEBUG = self.FRAMEWORK.create_debug_section()
        self.g_out_sbc = {}
        self.valid_data = False

        self.update()

    def on_input_value(self, index, value):
        if not bool(self._get_input_value(self.PIN_I_NON)):
            return

        # get json date if triggered
        if (index == self.PIN_I_NUPDATERATE) and value == 0:
            return

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
        self.test.on_init()

    def test_update(self):
        print("\n### test_update (! combines several other testcases !)")
        self.test.debug_input_value[self.test.PIN_I_NON] = 1
        self.test.debug_input_value[self.test.PIN_I_NUPDATERATE] = 60
        self.test.update()
        self.test.debug_input_value[self.test.PIN_I_NUPDATERATE] = 0

    def test_get_json(self):
        print("\n### test_get_json")
        ret = self.test.get_data()
        print(ret)
        self.assertTrue(ret)

    def test_read_json(self):
        print("\n### test_read_json")
        with open("sample1.txt") as f:
            json_data = f.read()

        ret = self.test.read_json(json_data)
        self.assertTrue(ret)

    def test_read_detailed_json(self):
        print("\n### test_read_detailed_json")
        with open("sample2.txt") as f:
            json_data = f.read()

        self.test.read_detailed_json(json_data)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
