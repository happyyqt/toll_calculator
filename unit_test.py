import unittest
import json
import tkinter as tk
from tkinter import messagebox
import sys
from unittest.mock import patch
from main import calculate_cost, get_route, find_next

class TestCalculator(unittest.TestCase):
    
    def setUp(self):
        # load interchanges data from JSON file
        with open('interchanges.json') as f:
            self.interchanges = json.load(f)['locations']
        
        # create GUI window
        self.window = tk.Tk()
        self.window.withdraw()
        
        self.from_entry = tk.Entry(self.window, width=30)
        self.to_entry = tk.Entry(self.window, width=30)
        self.result_label = tk.Label(self.window, text='')

        self.calculate_button = tk.Button(self.window, text='Calculate', command=self.calculate)
        self.clear_button = tk.Button(self.window, text='Clear', command=self.clear)
        self.quit_button = tk.Button(self.window, text='Quit', command=self.quit)

    def calculate(self):
        from_interchange = self.from_entry.get()
        to_interchange = self.to_entry.get()
        result = calculate_cost(from_interchange, to_interchange)
        if result is None:
            messagebox.showerror('Error', 'Invalid interchange names')
        else:
            distance = result['distance']
            cost = result['cost']
            self.result_label.config(text=f'Total distance: {distance} km\nTotal cost: ${cost}')
    
    def clear(self):
        self.from_entry.delete(0, 'end')
        self.to_entry.delete(0, 'end')
        self.result_label.config(text='')

    def quit(self):
        self.window.destroy()
        sys.exit()
    
    # test get_route method with valid input
    def test_get_route_with_valid_input(self):
        from_id = 1
        to_id = 2
        expected_result = 6.062
        result = get_route(from_id, to_id)
        self.assertEqual(result, expected_result)

    # test get_route method with invalid input
    def test_get_route_with_invalid_input(self):
        from_id = 1
        to_id = 3
        expected_result = None
        result = get_route(from_id, to_id)
        self.assertEqual(result, expected_result)

    # test find_next method with valid input
    def test_find_next_with_valid_input(self):
        id = 1
        direction = True
        self.assertEqual(find_next(id, direction), 2)

        id = 22
        direction = False
        self.assertEqual(find_next(id, direction), 20)

    # test find_next method with invalid input
    def test_find_next_with_invalid_input(self):
        id = 1
        direction = False
        self.assertIsNone(find_next(id, direction))

    # test calculate_cost method with valid input
    def test_calculate_cost_valid_inputs(self):
        message = "Distance or Cost are not almost equal"
        result = calculate_cost('QEW', 'Highway 400')
        expected_result = {'distance': 67.748, 'cost': 16.94}
        self.assertEqual(result, expected_result, message)

        result = calculate_cost('Salem Road', 'QEW')
        expected_result = {'distance': 107.964, 'cost': 26.99}
        self.assertEqual(result, expected_result, message)

        result = calculate_cost('QEW', 'Salem Road')
        expected_result = {'distance': 115.277, 'cost': 28.82}
        self.assertEqual(result, expected_result, message)

    # test calculate_cost method with invalid input
    def test_calculate_cost_invalid_inputs(self):
        result = calculate_cost('Invalid Interchange', 'Pizza Plaza')
        self.assertIsNone(result)
        
        result = calculate_cost('Pizza Plaza', 'Invalid Interchange')
        self.assertIsNone(result)
    
    # test clear button
    def test_clear_button(self):
        self.from_entry.insert(0, 'ABC')
        self.to_entry.insert(0, 'Damansara Plaza')
        self.result_label.config(text='some result')
        
        self.clear_button.invoke()
        
        self.assertEqual(self.from_entry.get(), '')
        self.assertEqual(self.to_entry.get(), '')
        self.assertEqual(self.result_label['text'], '')

    # test quit button   
    def test_quit_button(self):
        with patch('sys.exit') as mock_exit:
            self.quit_button.invoke()
            mock_exit.assert_called_once()

    # test calculate button with valid inputs        
    def test_calculate_button_valid_inputs(self):
        self.from_entry.insert(0, 'QEW')
        self.to_entry.insert(0, 'Highway 400')
        result_text = f'Total distance: 67.748 km\nTotal cost: $16.94'
        self.calculate_button.invoke()
        self.assertEqual(self.result_label['text'], result_text)

    # test calculate button with invalid inputs       
    def test_calculate_button_invalid_inputs(self):
        self.from_entry.insert(0, 'Invalid Interchange')
        self.to_entry.insert(0, 'Pizza Plaza')
        with patch('tkinter.messagebox.showerror') as mock_showerror:
            self.calculate_button.invoke()
            mock_showerror.assert_called_once_with('Error', 'Invalid interchange names')
        
if __name__ == '__main__':
    unittest.main(verbosity=2)
