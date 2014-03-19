#!usr/bin/env python
"""
Retrieve NeXus files from a server
"""
import paramiko
import os
import os.path
import re
import getpass
import sys
import argparse
import h5py
from stat import S_ISDIR

URL = 'scp.nbi.ansto.gov.au'
port = 22

cycle_directory = '/experiments/%s/data/cycle'
current_directory = '/experiments/%s/data/current'
hsdata_directory = '/experiment_hsdata/%s/hsdata'

animals = {'platypus': 'PLP',
           'quokka': 'QKK',
           'echidna': 'ECH',
           'wombat': 'WBT',
           'kookaburra': 'KKB',
           'kowari': 'KWW',
           'bilby': 'BBY',
           'emu': 'EMU',
           'pelican': 'PLN',
           'taipan': 'TPN'}


def _expand_range(file_numbers):
    '''Expand string of file numbers into integer list
    e.g.
    >>>_expand_range('112-114, 222, 223, 1223-1225')
    [112, 113, 114, 222, 223, 1223, 1224, 1225]
    '''
    individuals = list()
    entries = file_numbers.split(',')
    for entry in entries:
        #see if you have a range
        file_range = entry.split('-')
        if len(file_range) > 1:
            individuals.append(list(range(int(file_range[0]),
                                          int(file_range[1]) + 1)))
        else:
            individuals.append([int(entry)])

    return set([item for sublist in individuals for item in sublist])


def isdir(path, sftp):
    """See if a path is a directory on an SFTP server"""
    try:
        return S_ISDIR(sftp.stat(path).st_mode)
    except IOError:
        #Path does not exist, so by definition not a directory
        return False


def sftp_get_recursive(source, dest, sftp):
    """A recursive FTP downloader"""
    original_dir = os.getcwd()

    if not os.path.isdir(dest):
        os.mkdir(os.path.normpath(dest))
        os.chdir(os.path.normpath(dest))

    items = sftp.listdir(source)
    for item in items:
        if isdir(os.path.join(source, item),
                 sftp):
            sftp_get_recursive(os.path.join(source, item),
                               os.path.join(dest, item),
                               sftp)
        else:
            sftp.get(os.path.join(source, item),
                     os.path.join(dest, item))

    os.chdir(original_dir)


class NXGet():
    """
        A class for retrieving NeXus files from an instrument.
    """
    def __init__(self, username, password, animal=None):
        """
        Parameters
        ----------

        username: str
            Your username
        password: str
            Your password
        animal: str, optional
            The instrument you wish to retrieve data for
        """

        self.t = paramiko.Transport((URL, port))
        self.t.connect(username=username, password=password)
        self.sftp = paramiko.SFTPClient.from_transport(self.t)

        self.animal = animal or 'platypus'

        #let's get the cycle map, so we can locate files
        cycle_URL = (cycle_directory % self.animal) + '/data_map.txt'
        data_map_filename = os.path.join(os.getcwd(), 'data_map.txt')
        self._get(cycle_URL, data_map_filename)

        self.mapped_files = {}

        with open(data_map_filename) as f:
            self.data_map = self._parse_data_map(f)

    def __del__(self):
        self.t.close()

    def _get(self, source, dest):
        """
            Perform the paramiko SFTP request
        """
        self.sftp.get(source, dest)

    def _parse_data_map(self, f):
        """
        look through the data map to see if the file number is in
        the cycles directory
        """
        regex_str = '%s([0-9]{7}).nx.hdf' % animals[self.animal]
        regex = re.compile(regex_str)

        for line in f:
            match = regex.search(line)
            if match:
                try:
                    temp, stamp, size, path = line.split(' ')
                    path = path.split('\n')[0]
                    filename = os.path.basename(path)
                    number = int(match.group(1))
                    self.mapped_files[number] = {'filename': filename,
                                                 'path': path,
                                                 'timestamp': stamp,
                                                 'size': size}
                except (ValueError):
                    #some files have space in path, but these wont be
                    #nx.hdf
                    continue

    def _get_event_file(self, nexusnumber):
        """
            Get an event file corresponding to a nexus file, referred to
            by nexusnumber
        """
        fname = ('%s%07d.nx.hdf') % (animals[self.animal],
                                     nexusnumber)
        entry = '/entry1/instrument/detector/daq_dirname'
        try:
            with h5py.File(fname, 'r') as f:
                DAQ_dirname = f[entry].value[0]
        except (IOError, AttributeError):
            return

        try:
            hsdata_dir = (hsdata_directory) % self.animal
            self.sftp.lstat(os.path.join(hsdata_dir, DAQ_dirname))
            sftp_get_recursive(os.path.join(hsdata_dir, DAQ_dirname),
                               os.path.join(os.getcwd(), DAQ_dirname),
                               self.sftp)
        except (OSError, IOError):
            pass

        return

    def get_files(self, file_numbers, get_event_files=False):
        """
            Retrieves nexus files from the server, for a given
            animal. Specify file numbers as:
            '123, 125, 130-150'
        """
        numbers = _expand_range(file_numbers)
        for number in numbers:
            if number in self.mapped_files:
                info = self.mapped_files[number]
                print((info['filename']))
                self._get(info['path'],
                          os.path.join(os.getcwd(),
                                       info['filename']))
            else:
            #if may be in the current data directory
                current_dir = current_directory % self.animal
                fname = ('%s%07d.nx.hdf') % (animals[self.animal],
                                             number)
                try:
                    self.sftp.lstat(os.path.join(current_dir, fname))
                    self._get(os.path.join(current_dir, fname),
                              os.path.join(os.getcwd(), fname))
                    print(fname)
                except (OSError, IOError):
                    continue

            #retrieve eventfiles
            if get_event_files:
                self._get_event_file(number)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download NeXus files.')
    parser.add_argument('-u', help='username')
    parser.add_argument('-p', help='password')
    parser.add_argument('-e', action='store_true', help='retrieve event files')

    parser.add_argument('-a',
                        choices=list(animals.keys()),
                        help='instrument animal')

    parser.add_argument('filelist',
                        help=("Enter filenumbers to retrieve. "
                              "e.g. '1,2,3,4,5-10, 20-30'"))
    namespace = parser.parse_args()

    try:
        user = namespace.u or raw_input('Username: ')
    except NameError:
        user = namespace.u or input('Username: ')

    password = namespace.p or getpass.getpass()
    animal = namespace.a or 'platypus'

    getter = NXGet(user, password, animal=animal)
    getter.get_files(namespace.filelist,
                     get_event_files=namespace.e)
