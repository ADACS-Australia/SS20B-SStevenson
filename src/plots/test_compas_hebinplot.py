import unittest
import h5py
from compas_hex_no_update import(get_groups, get_keys_from_groups, 
                                 create_dictionary, update_dropdown,
                                 update_x, update_y, update_plot)

from bokeh.models.widgets import Select

#filename = 'COMPAS_CHE_30xZ_3000000.h5'
filename = 'testing.h5'

class TestLoad(unittest.TestCase):
    
    def test_if_h5_file(self):
        #Test if its an .h5 file
        self.assertTrue(get_groups(filename), h5py.is_hdf5(filename))
        
        
    def test_if_groups_are_list(self):
        #Test if its a list
        self.assertIsInstance(get_groups(filename), list)
        
        
    def test_if_return_all_groups(self):
        self.assertEqual(get_groups(filename), 
                         ['Group_1', 'Group_2', 'Group_3'])
        
        
    def test_if_keys_are_in_nested_list(self):
        #Test if its a nested list
        any(self.assertIsInstance(i, list) for i in 
            get_keys_from_groups(filename))
        
    def test_if_returns_all_sub_keys(self):
        self.assertEqual(get_keys_from_groups(filename),
                    [['Key_a', 'Key_b', 'Key_c', 'Key_d'], 
                     ['Key_x', 'Key_y', 'Key_z'],
                     ['Key_1', 'Key_2', 'Key_3']])
    
    def test_if_h5_structure_is_nested_dictionary(self):
        #Test if its a nested dict
        self.assertIsInstance(
            create_dictionary(get_groups(filename),
                get_keys_from_groups(filename)), dict)
        
    def test_if_returns_entire_dictionary(self):
        #Test if dictionary is well created
        self.assertEqual(create_dictionary(get_groups(filename),
                                           get_keys_from_groups(filename)),
                         {'Group_1': ['Key_a', 'Key_b', 'Key_c', 'Key_d'],
                          'Group_2': ['Key_x', 'Key_y', 'Key_z'],
                          'Group_3': ['Key_1', 'Key_2', 'Key_3']})
        
    def test_update_dropdown(self):
        
        # Groups in a list
        group_list = get_groups(filename)

        group = Select(title="Groups", value=f"{group_list[0]}",
                       options=group_list)

        self.assertEqual(update_dropdown(None, None, 'Key_a'), 
                         (None, "Key_a"))
        
        self.assertEqual(update_dropdown(None, 'Key_a', 'Key_b'), 
                         ('Key_a', 'Key_b'))
        
        self.assertEqual(group.value, 'Group_1')
        
        self.assertEqual(group.options, ['Group_1', 'Group_2', 'Group_3'])

    def test_update_x(self):

        group_list = get_groups(filename)

        env_dict = create_dictionary(get_groups(filename),
                             get_keys_from_groups(filename))
        
        group = Select(title="Groups", value=f"{group_list[0]}",
                       options=group_list)

        y = Select(title="Y-axis",
                   value=f"{env_dict[group.value][0]}", 
                   options=env_dict[group.value])
        
        
        self.assertEqual(update_x(None, None, 'Key_a'), 
                         (None, "Key_a"))
        
        self.assertEqual(update_x(None, 'Key_a', 'Key_b'), 
                         ('Key_a', 'Key_b'))
        
        self.assertEqual(y.value, 'Key_a')
        
        self.assertEqual(y.options, ['Key_a', 'Key_b', 'Key_c', 'Key_d'])
        
        
    def test_update_plot(self):
        # Check are they getting correct values from the file
        with h5py.File(filename, 'r') as f:
            data = dict(
                x = f['Group_1']['Key_a'][:],
                y = f['Group_2']['Key_y'][:],
                ) 
            print(data['x'][0])
                
        self.assertEqual(data['x'][0], 0)
        
        self.assertEqual(data['y'][0], 45898 )
        
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