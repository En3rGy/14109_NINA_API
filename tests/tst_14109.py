# coding: UTF-8
import unittest
import time
import logging
# functional import

import json

################################
# get the code
with open('../tests/framework_helper.py', 'r') as f1, open('../src/14109_NINA API (14109).py', 'r') as f2:
    framework_code = f1.read()
    debug_code = f2.read()

exec (framework_code + debug_code)

################################################################################


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        print("\n###setUp")
        with open("../tests/credentials.txt") as f:
            self.cred = json.load(f)

        self.test = NINAAPI_14109_14109(0)
        self.test.debug_input_value[self.test.PIN_I_SAGS] = self.cred["PIN_I_SAGS"]
        self.test.debug_input_value[self.test.PIN_I_NUPDATERATE] = 10

        self.test.debug_input_value[self.test.PIN_I_NON] = False
        self.test.on_init()
        self.test.debug_input_value[self.test.PIN_I_NON] = True
        # self.test.debug_input_value[self.test.PIN_I_PROCESS_DWD] = True

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
