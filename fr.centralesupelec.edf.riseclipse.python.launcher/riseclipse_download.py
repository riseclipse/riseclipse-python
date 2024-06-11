# *************************************************************************
# **  Copyright (c) 2024 CentraleSupélec & EDF.
# **  All rights reserved. This program and the accompanying materials
# **  are made available under the terms of the Eclipse Public License v2.0
# **  which accompanies this distribution, and is available at
# **  https://www.eclipse.org/legal/epl-v20.html
# ** 
# **  This file is part of the RiseClipse tool
# **  
# **  Contributors:
# **      Computer Science Department, CentraleSupélec
# **      EDF R&D
# **  Contacts:
# **      dominique.marcadet@centralesupelec.fr
# **      aurelie.dehouck-neveu@edf.fr
# **  Web site:
# **      https://riseclipse.github.io
# *************************************************************************

from urllib.request import urlopen, urlretrieve
from urllib.error import URLError, HTTPError

class RiseClipseDownload:

    def __init__(self):
        pass

    def get_latest_version(self, repository):
        url = 'https://github.com/riseclipse/' + repository + '/releases/latest'
        page = None
        try:
            page = urlopen(url)
        except HTTPError as e:
            print('Getting ', url, ' failed, error code: ', e.code)
            return None
        except URLError as e:
            print('Getting ', url, ' failed, reason: ', e.reason)
            return None
        
        title = None
        for line in page:
            line = line.lstrip().decode("utf-8")
            if line.startswith('<title>'):
                title = line
                break
        
        if title == None:
            return None
        
        start = '<title>Release ' + repository + ' v'
        if not title.startswith(start):
            return None
        version = title[len(start):]
        version = version.split()[0]
        version = version.split('.')
        for i in range(len(version)):
            version[i] = int(version[i])
        return version

    def download_version(self, repository, name, version, output):
        version = '%d.%d.%d' % (version[0], version[1], version[2])
        url = 'https://github.com/riseclipse/' + repository + '/releases/download/'
        url = url + repository + '-' + version + '/' + name + '-' + version + '.jar'
        try:
            urlretrieve(url, output)
        except HTTPError as e:
            print('Downloading ', url, ' failed, error code: ', e.code)
        except URLError as e:
            print('Downloading ', url, ' failed, reason: ', e.reason)
    

#r = RiseClipseDownload()
#r.get_latest_version('riseclipse-validator-scl2003')
#r.get_latest_version('riseclipse-validator-cgmes-3-0-0')

#r.download_version('riseclipse-validator-scl2003', 'RiseClipseValidatorSCL', [1, 2, 7], 'validator.jar')
#r.download_version('riseclipse-validator-cgmes-3-0-0', 'RiseClipseValidatorCGMES3', [1, 0, 3], 'validator.jar')
