# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

# Testing 'load_file.py' file

import unittest
import h5py
from load_file import get_groups, get_keys_from_groups, create_dictionary, create_group_map


# filename = 'COMPAS_CHE_30xZ_3000000.h5'
filename = 'test.h5'


class TestLoad(unittest.TestCase):
    def test_if_h5_file(self):
        # Test if its an .h5 file
        self.assertTrue(get_groups(filename), h5py.is_hdf5(filename))

    def test_if_groups_are_list(self):
        # Test if its a list
        self.assertIsInstance(get_groups(filename), list)

    def test_if_return_all_groups(self):
        self.assertEqual(get_groups(filename), ['Group_A', 'Group_B'])

    def test_if_keys_are_in_nested_list(self):
        # Test if its a nested list
        any(self.assertIsInstance(i, list) for i in get_keys_from_groups(filename))

    def test_if_returns_all_sub_keys(self):
        self.assertEqual(get_keys_from_groups(filename), [['Key_a', 'Key_b', 'Key_c'], ['Key_x', 'Key_y', 'Key_z']])

    def test_if_h5_structure_is_nested_dictionary(self):
        # Test if its a nested dict
        self.assertIsInstance(create_dictionary(get_groups(filename), get_keys_from_groups(filename)), dict)

    def test_if_returns_entire_dictionary(self):
        # Test if dictionary is well created
        self.assertEqual(
            create_dictionary(get_groups(filename), get_keys_from_groups(filename)),
            {'Group_A': ['Key_a', 'Key_b', 'Key_c'], 'Group_B': ['Key_x', 'Key_y', 'Key_z']},
        )


# =============================================================================
#     def test_group_map(self):
#         #Test if group_map is well created
#         self.assertEqual(create_group_map(filename),
#                          {'Group_A': 'Group_A', 'Group_B': 'Group_B'})
#
#
# =============================================================================

if __name__ == '__main__':
    unittest.main()
