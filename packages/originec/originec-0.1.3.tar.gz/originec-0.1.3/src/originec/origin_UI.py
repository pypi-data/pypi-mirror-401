import FreeSimpleGUI as sg
import os
from .CV.cvorigin import CVMakerGamry, CVMakerBiologic
from .Biologic.chdis_bio import ECLabChDisMaker


def main():
    # create a dictionary mapping function names to functions
    functions = {
        'CV_Gamry': CVMakerGamry,
        'CV_Biologic': CVMakerBiologic,
        'ChDis_ECLab': ECLabChDisMaker,
    }

    layout = [
        [sg.Text('File Browser')],
        [sg.Input(), sg.FilesBrowse()],
        [sg.Text('Select Processing Method')],
        # add a drop-down for functions
        [sg.Combo(list(functions.keys()), key='-FUNCTION-', size=(15, 1))],
        [sg.OK(), sg.Cancel()]
    ]

    window = sg.Window('File Browser', layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Cancel':
            break
        elif event == 'OK':
            file_list = values[0].split(';')
            file_list = [f for f in file_list if f]
            function_name = values['-FUNCTION-']
            # get the selected function from the dictionary
            function = functions.get(function_name)
            if function_name == 'CV_Gamry':
                # show additional input fields for CV_Gamry
                layout2 = [
                    [sg.Text('Diameter (mm)')],
                    [sg.Input()],
                    [sg.Text('Scan Rate (mV/s): optional')],
                    [sg.Input()],
                    [sg.Text('Split Value (V): optional')],
                    [sg.Input()],
                    [sg.OK(), sg.Cancel()]
                ]
                window2 = sg.Window('CV_Gamry', layout2)
                while True:
                    event2, values2 = window2.read()
                    if event2 == sg.WINDOW_CLOSED or event2 == 'Cancel':
                        break
                    elif event2 == 'OK':
                        try:
                            diameter = float(values2[0])
                        except ValueError:
                            diameter = None
                        try:
                            scan_rate = float(values2[1])
                        except ValueError:
                            scan_rate = None
                        try:
                            split_val = float(values2[2])
                        except ValueError:
                            split_val = None
                        break
                window2.close()
                maker = CVMakerGamry(
                    file_list, diameter=diameter, scan_rate=scan_rate, split_val=split_val)
                maker.plot()
                break
            elif function_name == 'CV_Biologic':
                # show additional input fields for CV_Biologic
                layout2 = [
                    [sg.Text('Sample Name (optional)')],
                    [sg.Input()],
                    [sg.Text('Diameter (mm)')],
                    [sg.Input()],
                    [sg.Text('Scan Rate (mV/s): optional')],
                    [sg.Input()],
                    [sg.Text('Split Value (V): optional')],
                    [sg.Input()],
                    [sg.OK(), sg.Cancel()]
                ]
                window2 = sg.Window('CV_Biologic', layout2)
                while True:
                    event2, values2 = window2.read()
                    if event2 == sg.WINDOW_CLOSED or event2 == 'Cancel':
                        break
                    elif event2 == 'OK':
                        name = values2[0] if values2[0] else None
                        try:
                            diameter = float(values2[1])
                        except ValueError:
                            diameter = None
                        try:
                            scan_rate = float(values2[2])
                        except ValueError:
                            scan_rate = None
                        try:
                            split_val = float(values2[3])
                        except ValueError:
                            split_val = None
                        break
                window2.close()
                maker = CVMakerBiologic(
                    diameter=diameter, scan_rate=scan_rate, split_val=split_val, name=name)
                maker.plot()
                break
            elif function_name == 'ChDis_ECLab':
                # show additional input fields for ChDis_ECLab
                # layout2 = [
                #     [sg.Text('Cell Name')],
                #     [sg.Input()],
                #     [sg.OK(), sg.Cancel()]
                # ]
                # window2 = sg.Window('ChDis_ECLab', layout2)
                # while True:
                #     event2, values2 = window2.read()
                #     if event2 == sg.WINDOW_CLOSED or event2 == 'Cancel':
                #         break
                #     elif event2 == 'OK':
                #         cellname = values2[0]
                #         break
                # window2.close()
                maker = ECLabChDisMaker()
                maker.split_data()
                maker.plot()
                break
            elif function:
                maker = function(file_list)
                maker.plot()
                break

            else:
                sg.popup('Please select a processing method!')

    window.close()


if __name__ == '__main__':
    main()
