import os
import requests
import datetime
import time

def get_date_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def files_list(path_to_files):
    directory_with_files = {}

    for root, dirs, files in os.walk(path_to_files):
        for name in files:
            directory_with_files[name] = { 'directory' : path_to_files,
                                'status' : '',
                                'checked_time' : '',
                                'scan_id' : '' }
    return directory_with_files

def sent_to_virus_total(file_name, path_to_file):
    url = 'https://www.virustotal.com/vtapi/v2/file/scan'
    params = {'apikey': '36b0af7b758614ac306afbbc3ae0c08a1a853bbc4d7b4b8b9cb89e17652fe551'}
    files = {'file': (file_name, open(path_to_file, 'rb'))}

    try:
        response = requests.post(url, files=files, params=params)
    except Exception as content:
        print(f' [EXCEPTION]   {content}')
    if response.status_code == 200:
        print(get_date_time() + ' [OK] Udało się połączyć z serwerem Virus Total')
        print(get_date_time() + ' [INFO] Do skanowania został przesłany plik: ' + str(file_name))
        return response.json()
    else:
        print(get_date_time() + ' [ERROR] Nie udało się połączyć z serwerem, kod HTTP: ' + str(response.status_code))
    return False


##################################

directory_with_files = files_list(str(os.getcwd()) + '\\File_to_check\\')

for file_name in directory_with_files:
    path_to_file = str(directory_with_files[file_name]['directory']+ file_name)
    #print(path_to_file)

    response = sent_to_virus_total(file_name, path_to_file)
    directory_with_files[file_name]['checked_time'] = get_date_time()

    if response != False:
        print(get_date_time() + ' [INFO] ' + response['verbose_msg'])
        directory_with_files[file_name]['scan_id'] = response['scan_id']
    else:
        print(get_date_time() + ' [ERROR] Błąd wysyłania pliku!' )