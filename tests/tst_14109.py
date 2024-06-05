# coding: UTF-8
import unittest
import time
import matplotlib.pyplot as plt

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
        self.test.debug = True
        self.test.debug_input_value[self.test.PIN_I_SAGS] = self.cred["PIN_I_SAGS"]
        self.test.debug_input_value[self.test.PIN_I_LONGITUDE] = self.cred["LON"]
        self.test.debug_input_value[self.test.PIN_I_LATITUDE] = self.cred["LAT"]

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
        w_res = bubble_sort(w)
        w_solution = [w3, w1, w2, w4]
        self.assertEqual(w_res, w_solution)

    def test_in_out(self):
        print("\n### test_in_out")

        polygon = [[10, 0], [4, 3], [3, 10], [-2, 5], [-8, 6], [-6, 0], [-8, -6], [-2, -5], [3, -10], [4, -3]]
        point_in = [7, 1]
        point_out = [5, 5]

        # draw_polygon_and_point(polygon, point_in)
        # draw_polygon_and_point(polygon, point_out)

        self.assertTrue(is_point_in_polygon(point_in, polygon))
        self.assertFalse(is_point_in_polygon(point_out, polygon))

    def test_update(self):
        print("\n### test_update (! combines several other testcases !)")
        self.test.debug_input_value[self.test.PIN_I_NUPDATERATE] = 60
        self.test.update()
        self.test.debug_input_value[self.test.PIN_I_NUPDATERATE] = 0

    def test_no_data(self):
        print("\n### test_update (! combines several other testcases !)")
        self.test.debug_input_value[self.test.PIN_I_SAGS] = "00000000"
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
        ret = self.test.get_nina_data()
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

def draw_polygon_and_point(polygon_points, point, title=""):
    """
    Draws a polygon defined by polygon_points and a single point on the same plot.

    :param polygon_points: List of lists, where each inner list is a [x, y] coordinate of the polygon vertices.
    :param point: List [x, y] coordinate of the single point to plot.
    """
    # Unzip the polygon points into separate x and y lists
    x_polygon, y_polygon = zip(*polygon_points)

    # Append the first point to close the polygon
    x_polygon += (x_polygon[0],)
    y_polygon += (y_polygon[0],)

    # Create the plot
    plt.figure()

    # Plot the polygon
    plt.plot(x_polygon, y_polygon, marker='o', linestyle='-')

    # Plot the single point
    plt.plot(point[0], point[1], 'ro')  # 'ro' means red color and 'o' as marker

    # Set plot limits to ensure all points are visible
    plt.xlim(min(x_polygon + (point[0],)) - 0.01, max(x_polygon + (point[0],)) + 0.01)
    plt.ylim(min(y_polygon + (point[1],)) - 0.01, max(y_polygon + (point[1],)) + 0.01)

    # Show the plot
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title(title)
    plt.grid(True)
    plt.show()
