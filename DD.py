import re
import requests
import os
import sys
import time

out_dir = ''    #out dir to write files to

def main():
    global out_dir

    base_url = 'http://www.iskconkolkata.com/media/picture-gallery/deity-darshan/'
    print('[*]Hare Krishna. PAMHO. Deity Darshan @',base_url,'\n')

    if len(sys.argv) == 2:
        arg1 = sys.argv[1]
        
        if arg1 == '--all':
            allURLs = getDarshanPage(base_url, True)       #True to download all recent Darshans
            print('[*]Requesting for all recent Darshans...')

            for url_x in allURLs:
                print('\n[*]Attempting:',url_x)
                try:
                    out_dir =  re.findall('([\d]+-[\d\w]+-[\d]+)',url_x)[0]
                except:
                    if url_x.split('/')[-1]:
                        out_dir = url_x.split('/')[-1]
                    else:
                        out_dir = url_x.split('/')[-2]
                
                #print('[]TESTING if exsits ',out_dir)
                if not os.path.isdir(out_dir):
                    os.mkdir(out_dir)
                    img_urls = get_imgURL(url_x)
                    saveImg(img_urls)
                else:
                    print('[*]Skipping: ',out_dir)

        else:
            date_in_arg = re.findall('([\d]+-[\d]+-[\d]+)',arg1)
            if date_in_arg:
                out_dir = date_in_arg[0]
                if not os.path.isdir(out_dir):
                    os.mkdir(out_dir)
                date = date_in_arg[0]
                datewiseURL = findDateWiseURL(date)
                #datewiseURL = useGoogleDork(date)

                print('[*]Trying to get Special Darshna of ',date)
                imgURLs = get_imgURL(datewiseURL)
                saveImg(imgURLs)
            else:
                print('[*]USAGE:python3 DD.py <specific_date>\n         python3 DD.py --all #to download all in page\n         python3 DD.py    #for Last update')

    else:    
        imgURLs = getDarshanPage(base_url)
        if not os.path.isdir(out_dir):
            os.mkdir(out_dir)
        saveImg(imgURLs)
    
    print('\nYS. Hari Bol! :) ')
   

def findDateWiseURL(date):
    #current format: 'http://www.iskconkolkata.com/todayss-darshan-12-06-2018/'
    from datetime import date as datedate
    dateS = date.split('-')
    datef1 = datedate(int(dateS[2]),int(dateS[1]),int(dateS[0])).strftime("%d-%B-%Y")
    
    if(len(dateS[0]) == 1):
        date2 = date
        date = '0' + date
        datef2 = datef1[1:]
    elif(date[0] == '0'):
        date2 = date[1:]
        datef2 = datef1[1:]
    else:
        date2 = date
        datef2 = datef1


    url_list = list(set(['http://www.iskconkolkata.com/todayss-darshan-'+date,\
                'http://www.iskconkolkata.com/todayss-darshan-'+date2,\
                'http://www.iskconkolkata.com/todays-darshan-'+datef1,\
                'http://www.iskconkolkata.com/todays-darshan-'+datef2]))

    for url in url_list:
        temp_res = requests.head(url)
        if temp_res.status_code == 404:
            print('[-]Failed: ',url)
        else:
            print('[+]Success: ',url)
            return url
    
    print('[-]Either PAge not found or different format Darshan Page` URL')
    quit()


def getDarshanPage(base_url, getAllDarshan=False):

    r1 = requests.get(base_url)
    t1 = r1.text
    darshanURL = re.findall('<a title="Today.*?".*href="(.*)"',t1) 
    #print(set(darshanURL))
    if not getAllDarshan:                   
        return get_imgURL(darshanURL[0])        #1st element recent Darshan
    else:
        return list(set(darshanURL))                       #so that all Darshan URLs in page can be retreived


def get_imgURL(darshanURL):
    
    global out_dir
    #folderName = re.findall('([\d]+-[\d]+-[\d]+)',darshanURL.split('/')[-2])[0]  #safer but -2 position can be dynamic
    #if not folderName:
    #   folderName = re.findall('([\d]+-[\d]+-[\d]+)',darshanURL.split('/')[-1])[0]
    if not out_dir:
        try:
            out_dir = re.findall('([\d]+-[\d\w]+-[\d]+)',darshanURL)[0]  #date format in URL may change
        except:
            print('[-]Uncommon Format: ',darshanURL)
            out_dir = '??__' + darshanURL.split('/')[-2]

    today = time.strftime("%d-%m-%Y")  #change format so that it matches out_dir 
    if out_dir == today: 
        print('[+]Hari Bol! We are getting LAtest Darshan!\n')
    else:
        print('[*]Requesting: ',out_dir,'\'s Darshan (Today:', today,')')
    
    print('[*]Praying Sri Sri Radha-Govinda Ji for Darshan....')
    r2 = requests.get(darshanURL)
    if r2.status_code == 404:
        print('[-]Darshan Page NOT FOUND! Try another date...')
        quit()

    t2 = r2.text
    imgURLs = list(set(re.findall('<img.*?(https://.*?\.jpg)',t2,re.IGNORECASE))) #include other extensions based on statistics

    return imgURLs


def saveImg(imgURLs):
    #print('[+]Trying to download:\n',imgURLs)
    print('[*]It looks like our Prayer has been granted!')

    for url in imgURLs:
        r = requests.get(url)
        try:
            with open(out_dir + '/' + url.split('/')[-1],'wb') as f:
                f.write(r.content)
            print('[+]Downloaded: ',url)
        except:
            print('[-]Failed to write file.\n')

    print('\n')


if __name__ == '__main__':
    main()
