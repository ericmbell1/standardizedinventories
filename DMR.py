#!/usr/bin/env python


import requests
import pandas as pd
import json
import os


# appends form object to be used in query to sic code
def app_sic(form_obj, SIC):
    result = [form_obj + s for s in SIC]
    return result


# sets the output directory
def set_output_dir(directory):
    outputdir = directory
    if not os.path.exists(outputdir): os.makedirs(outputdir)
    return outputdir


# creates urls from various search parameters and outputs as a list
def create_urls(main_api, service_parameter, year, l, output_type):
    urls = []
    for s in l:
        url = main_api + service_parameter + year + s + '&output=' + output_type
        urls.append(url)
    return urls


# creates file path for json output. irterates through url list, requests data, and writes to json file in output directory.
def get_write_json_file(urls, path, file):
    final_path = path + file + '.json'
    for url in urls:
        json_data = requests.get(url).json()
        df = pd.DataFrame(json_data)
        if 'Error' in df.index:
            if df['Results'].astype(str).str.contains('Maximum').any():
                print("iterate through by region code " + url)
            # split url by & and append region code, import function debugging
            else:
                print("Error:" + url)
        elif 'NoDataMsg' in df.index:
            print('No data found for:' + url)
        else:
            with open(final_path, 'w') as fp:
                json.dump(json_data, fp, indent=2)


#def main():
DMR_year = '2015'  # year of data requested
main_api = 'https://ofmpub.epa.gov/echo/dmr_rest_services.get_custom_data_'  # base url
service_parameter = 'annual?'  # define which parameter is primary search criterion
year = 'p_year=' + DMR_year  # define year
form_obj = '&p_sic2='  # define any secondary search criteria
output_type = 'JSON'  # define output type

# two digit SIC codes from advanced search drop down stripped and formatted as a list
sic = ['01', '02', '07', '08', '09', '10']#, '12', '13', '14', '15',
#        '16', '17', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29'
#        , '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41',
#        '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53',
#        '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65'
#        , '67', '70', '72', '73', '75', '76', '78', '79', '80', '81', '82'
#        , '83', '84', '86', '87', '88', '89', '91', '92', '93', '95', '96', '97', '99']

sic_code_query = app_sic(form_obj, sic)
outputdir = set_output_dir('../LCI-Primer-Output/')
urls = create_urls(main_api, service_parameter, year, sic_code_query,
                   output_type)  # creates a list oof urls based on sic
print(urls)
json_output_file = get_write_json_file(urls, outputdir, 'DMR_data')  # saves json file to LCI-Prime_Output


#if __name__ == '__main__':
#    main()
