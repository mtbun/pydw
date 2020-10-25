#!/usr/bin/python3
import math
import os
import sys
import time
import requests


def generate_filename(url):
    if '?' in url.split('/')[-1]:
        url = url.split('?')
        url.pop(-1)
        url = ''.join(url)
    if url[-1] == '/':
        url = list(url)
        url.pop(-1)
        url = ''.join(url)
    filename = url.split('/')[-1]
    return filename


def download(url, filename, directory):
    try:
        response = requests.get(url).content
        with open(os.path.join(directory, filename), 'wb') as file:
            file.write(response)
        return True
    except:
        return False

def file_exists(file, directory):
    files = os.listdir(directory)
    if file in files:
        return True
    else:
        return False

args = sys.argv
if '--help' in args or '-h' in args:
    print('\nKullanım:            Açıklama:')
    print('    -l <dosya>             İndirilecek dosyaların listesi')
    print('    -d <klasör> [optional] İndirilecek konum')
    print('    --delay [optional]     Gecikme')
    print('\nversion: 0.0.4\n')
    sys.exit()

txt_file = args[args.index('-l') + 1]
url_list = open(txt_file, 'r').read().split('\n')

if '-d' in args:
	save_directory = args[args.index('-d') + 1]
else:
	save_directory = './'

if '--delay' in args:
    delay = args[args.index('--delay') + 1]
    delay = float(delay)
else:
    delay = None

dw, fail, passed, msg = 0, 0, 0, ''
for url in url_list:
    try:
        filename = generate_filename(url)
        if (filename) and (not file_exists(filename, save_directory)):
            status = download(url, filename, save_directory)

            if delay != None:
                time.sleep(delay) 

            if status:
                sys.stdout.write('\b' * len(msg))
                dw += 1
                bar = (dw + fail + passed) / len(url_list)
                rate = bar
                bar = math.ceil(bar * 20)
                msg = '%' + str(round(rate * 100)) + '  |' + (bar * '█') + ((20 - bar) * ' ') + '|   ' + 'İndirilen dosya sayısı: ' + str(dw) + '/' + str(len(url_list)) + ', ' + str(fail) + ' başarısız.'
                sys.stdout.write(msg)
                sys.stdout.flush()
            else:
                fail += 1
        else:
            passed += 1        
    except Exception as e:
        open('error.txt', 'a').write(url + '\n')
        fail += 1

print('\n')
