import json
import tkinter as tk
import sys

# load interchanges data from JSON file
with open('interchanges.json') as f:
    interchanges = json.load(f)['locations']

# get the distance between two interchanges
def get_route(from_id, to_id):
    for route in interchanges[str(from_id)]['routes']:
        if route['toId'] == to_id:
            return route['distance']
        
# get next interchange id
def find_next(id, direction):
    for route in interchanges[str(id)]['routes']:
        if route["toId"] > id and direction or route["toId"] < id and not direction:
            return route["toId"]
                
# calculate toll cost and distance for given route
def calculate_cost(from_interchange, to_interchange):
    # find the interchange IDs for the given names
    from_id = next((int(i) for i in interchanges if interchanges[i]['name'] == from_interchange), None)
    to_id = next((int(i) for i in interchanges if interchanges[i]['name'] == to_interchange), None)
    if from_id is None or to_id is None:
        return None
    # direction = True if from_id < to_id else False
    direction = from_id <= to_id
    distance = 0
    if direction:
        for id in range(from_id, to_id+1):
            if id == to_id:
                break
            # No.21 and No.27 interchange is not listed in data
            if id == 21 or id == 27:
                continue
            next_id = find_next(id, direction)
            distance += get_route(id, next_id)
    else:
        for id in range(from_id, to_id-1, -1):
            if id == to_id:
                break
            # No.21 and No.27 interchange is not listed in data
            if id == 21 or id == 27:
                continue
            next_id = find_next(id, direction)
            distance += get_route(id, next_id)

    cost = distance * 0.25
    return {'distance': round(distance, 3), 'cost': round(cost, 2)}

# main program
if __name__ == '__main__':
    # create GUI window
    window = tk.Tk()
    window.title('Toll Calculator')
    window.geometry('400x250')
    
    # create UI elements
    from_label = tk.Label(window, text='From interchange:')
    from_label.pack()
    from_entry = tk.Entry(window, width=30)
    from_entry.pack()
    
    to_label = tk.Label(window, text='To interchange:')
    to_label.pack()
    to_entry = tk.Entry(window, width=30)
    to_entry.pack()
    
    result_label = tk.Label(window, text='')
    result_label.pack()
    
    ## add functions and the buttons
    def calculate():
        from_interchange = from_entry.get()
        to_interchange = to_entry.get()
        result = calculate_cost(from_interchange, to_interchange)
        if result is None:
            result_label.config(text='Error: Invalid interchange names')
        else:
            distance = result['distance']
            cost = result['cost']
            result_label.config(text=f'Total distance: {distance} km\nTotal cost: ${cost}')

    def quit():
        window.destroy()
        sys.exit()

    def clear():
        from_entry.delete(0, 'end')
        to_entry.delete(0, 'end')
        result_label.config(text='')
    
    calculate_button = tk.Button(window, text='Calculate', command=calculate)
    calculate_button.pack(pady=5)

    clear_button = tk.Button(window, text='Clear', command=clear)
    clear_button.pack(pady=5)

    quit_button = tk.Button(window, text='Quit', command=quit)
    quit_button.pack(pady=5)

    # start the GUI event loop
    window.mainloop()
