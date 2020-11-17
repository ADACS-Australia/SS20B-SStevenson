import unittest
import numpy as np
import h5py
from compas_hexbinplot import (
    get_groups,
    get_keys_from_groups,
    create_dictionary,
    update_dropdown,
    file_text_name,
    reformat_data,
    change_nan_inf,
    layout_and_filters,
)

from bokeh.models.widgets import Select


test_file = "testing.h5"


class TestLoad(unittest.TestCase):
    def test_if_h5_file(self):
        # Test if its an .h5 file
        self.assertTrue(get_groups(test_file), h5py.is_hdf5(test_file))

    def test_if_groups_are_list(self):
        # Test if its a list
        self.assertIsInstance(get_groups(test_file), list)

    def test_if_return_all_groups(self):
        self.assertEqual(get_groups(test_file), ["Group_1", "Group_2", "Group_3"])

    def test_if_keys_are_in_nested_list(self):
        # Test if its a nested list
        any(self.assertIsInstance(i, list) for i in get_keys_from_groups(test_file))

    def test_if_returns_all_sub_keys(self):
        self.assertEqual(
            get_keys_from_groups(test_file),
            [["Key_a", "Key_b", "Key_c", "Key_d"], ["Key_x", "Key_y", "Key_z"], ["Key_1", "Key_2", "Key_3"]],
        )

    def test_if_h5_structure_is_nested_dictionary(self):
        # Test if its a nested dict
        self.assertIsInstance(create_dictionary(get_groups(test_file), get_keys_from_groups(test_file)), dict)

    def test_if_returns_entire_dictionary(self):
        # Test if dictionary is well created
        self.assertEqual(
            create_dictionary(get_groups(test_file), get_keys_from_groups(test_file)),
            {
                "Group_1": ["Key_a", "Key_b", "Key_c", "Key_d"],
                "Group_2": ["Key_x", "Key_y", "Key_z"],
                "Group_3": ["Key_1", "Key_2", "Key_3"],
            },
        )

    def test_update_dropdown(self):

        # Groups in a list
        group_list = get_groups(test_file)

        group = Select(title="Groups", value=f"{group_list[0]}", options=group_list)

        self.assertEqual(update_dropdown(None, None, "Key_a"), (None, "Key_a"))

        self.assertEqual(update_dropdown(None, "Key_a", "Key_b"), ("Key_a", "Key_b"))

        self.assertEqual(group.value, "Group_1")

        self.assertEqual(group.options, ["Group_1", "Group_2", "Group_3"])

    def test_file_text_name(self):

        codefeedback = file_text_name(test_file)

        self.assertEqual(codefeedback.text, f"{test_file} file is loaded")

    def test_change_nan_inf(self):

        with h5py.File(test_file, "r") as f:

            x = change_nan_inf(f["Group_3"]["Key_3"][:])
            y = change_nan_inf(f["Group_3"]["Key_1"][:])
            z = change_nan_inf(f["Group_3"]["Key_2"][:])

            # test finding position of the nan/inf/boolean values
            x_inf = np.argwhere(np.isinf(f["Group_3"]["Key_3"][:]))
            y_nan = np.argwhere(np.isnan(f["Group_3"]["Key_3"][:]))

        self.assertEqual(list(x), list([1.125, 0, 2, 3, 0, 1, 1, 1, 1.125, 1]))
        self.assertEqual(list(y), list([0, 0, 1, 0, 0, 1, 1, 1, 1, 1]))
        self.assertEqual(list(z), list([0, 0, 1, 0, 0, 0, 1, 1, 0, 1]))

        self.assertEqual(x_inf, 8)
        self.assertEqual(y_nan, 0)

    def test_reformat_data(self):

        with h5py.File(test_file, "r") as f:

            x = reformat_data(f["Group_1"]["Key_a"][:] * 1)
            y = reformat_data(f["Group_2"]["Key_y"][:] * 1)
            z = reformat_data(f["Group_3"]["Key_2"][:] * 1)

            # test finding position of the nan/inf/boolean values
            # there should not be any
            x_inf = np.argwhere(np.isinf(x))
            y_nan = np.argwhere(np.isnan(z))

        self.assertEqual(max(x), 1)
        self.assertEqual(max(y), 1)
        self.assertEqual(max(z), 1)

        self.assertEqual(min(x), 0)
        self.assertEqual(min(y), 0)
        self.assertEqual(min(z), 0)

        self.assertEqual(len(x_inf), 0)
        self.assertEqual(len(y_nan), 0)

    def test_layout_and_filters(self):

        if get_groups(test_file)[0] == "Group_1":
            self.assertEqual(len(layout_and_filters()), 10)
            self.assertNotEqual(len(layout_and_filters()), 4)


if __name__ == "__main__":
    unittest.main()
