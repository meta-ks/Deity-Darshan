# Hare Krishna

This script automates the downloading of daily Darshan uploaded at http://www.iskconkolkata.com/media/picture-gallery/deity-darshan/ 

Currently it relies on extracting dates from the URLs in the subsequent pages, so the regular expression definitions may need an update.

Currently it supports-- 
  1. Last update download:
        python3 DD.py
  2. Custom date: 
        python3 DD.py 11-11-2018
  3. Recent all (use --all): 
        python DD.py --all
        
        
  It will create folders according to dates.
  
  TODO: 
    > Using google dorks for finding Custom Date Darshan (present method is unreliable as the URL format for older years may not be covered.)
    > Extending to other similar Darshan Pages like http://darshan.iskcondesiretree.com/
  
  PS: You can MEET HIM at 
            Sri Sri Radha Govinda Mandir
            3C Albert Road, Near Birla High School,
            Minto Park, Kolkata – 700017
            
  YS
