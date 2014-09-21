#!/usr/bin/python
#coding=utf8
#author:Richard Liu
#email:richardxxx0x@gmail.com

import os
import sys
from optparse import OptionParser
import bencode

"""
exit status
0 ==> ok
1 ==> path not found
2 ==> torrent list filename not exist
"""

'''
获取此脚本所在目录中的所有torrent文件名
'''
class FindTorrent(object):
  def __init__(self, path_name=''):
    self.path_name = path_name
    
  def find_torrent(self):
    if not os.path.isdir(self.path_name):
      print '\033[91m'+'path not found.'+'\033[0m'
      sys.exit(1)
    with open('torrent_lists.txt','w') as f:
      for root, dirs, files in os.walk(self.path_name):
        for file in files:
          if file.endswith('.torrent'):
            f.write(os.path.join(root, file)+'\n')
    print '\033[92m'+'torrents file lists in torrent_lists.txt'+'\033[0m'

'''
读取种子，获取种子信息中文件名
'''
class GetTorrentFileName(object):
  def __init__(self, file_name=''):
    self.file_name = file_name
    self.lines = []
    
  def load_file(self):
    if not os.path.exists(self.file_name):
      print '\033[91m'+'not found torrent_lists.txt file in current directory,run python GetTorrentName.py -p first.'+'\033[0m'
      sys.exit(2)
    with open(self.file_name) as f:
      self.lines.append(f.readlines())
      self.process_torrent()
      
  def process_torrent(self):
    file_list = self.lines[0]
    length = len(file_list)
    out = open('result.txt','w')
    for line in range(0,length):
      file_name = file_list[line].rstrip()
      with open(file_name,'r') as f:
        raw_data = f.read()
	try:
          torrent_dic = bencode.bdecode(raw_data)
          torrent_name = torrent_dic['info']['name']
          torrent_info = file_name+'\t'+torrent_name+'\n'
          out.write(torrent_info)
        except:
	  pass	
    out.close()
        
  def run(self):
    self.load_file()
    
if __name__ == '__main__':
  parser = OptionParser()
  parser.add_option('-p', '--path', dest='path',
                    help='path you want to find torrent')
  parser.add_option('-r', '--read', dest='read',
                    help='get information of files(torrent) in list')
  (options, args) = parser.parse_args()
  
  if options.path:
    torrent_lists = FindTorrent(options.path).find_torrent()
  elif options.read:
    torrent_names = GetTorrentFileName(options.read).run()
  else:
    parser.error('use -h or --help for help information')
    
  
  
