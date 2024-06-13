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

    """
    This class is used to download RiseClipse validator ``jar`` files.
    """

    def get_latest_version(self, repository: str) -> list[int]:
        """
        Get the latest version of the tool in the given repository of `RiseClipse organisation`_
        on GitHub.
        
        .. _RiseClipse organisation:
            https://github.com/riseclipse
        
        Example:
            Get the latest version of RiseClipseValidatorSCL tool::
            
                download = RiseClipseDownload()
                download.get_latest_version('risceclipse_validator_scl2003')
        
        Args:
            repository: The repository of `RiseClipse organisation`_ dedicated to the wanted tool.
                
        Returns:
            A list of three integers giving the latest version.
        """
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

    def download_version(self, repository : str, name: str, version: list[int], output: str) -> None:
        """
        Download the ``jar`` of the tool in the given repository of `RiseClipse organisation`_
        on GitHub, with the given name and version, put it in the file with the given path.
        
        .. _RiseClipse organisation:
            https://github.com/riseclipse
        
        Example:
            Get the latest version of RiseClipseValidatorSCL tool::
            
                download = RiseClipseDownload()
                download.download_version('risceclipse_validator_scl2003', 'RiseClipseValidatorSCL', [1, 2, 7], 'RiseClipseValidatorSCL.jar')
        
        Args:
            repository: The repository of `RiseClipse organisation`_ dedicated to the wanted tool.
            name: the name of the ``jar`` file without the version number.
            version: the requested version.
            output: the path where the ``jar`` will be saved.
        """
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
