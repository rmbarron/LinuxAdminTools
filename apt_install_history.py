#!/usr/bin/python
"""Python script to parse dpkg logs and return timeline of installed packages.
"""

# Copyright 2017 Robert Barron

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import argparse
import glob
import gzip
import re


INSTALLED = re.compile(r'.*status installed.*')
NOT_INSTALLED = re.compile(r'.*status not-installed.*')
REMOVE = re.compile(r'.*remove .*')
INSTALL = re.compile(r'.*install .*')
PURGE = re.compile(r'.*purge .*')
FULL_LIST = [INSTALLED, NOT_INSTALLED, REMOVE, INSTALL, PURGE]
COMMANDS = [REMOVE, INSTALL, PURGE]
STATUS = [INSTALLED, NOT_INSTALLED]

# Use a dictionary instead of enum to prevent dependency on aenum pip package.
ENUM = {'all': FULL_LIST, 'command_code': COMMANDS, 'status_code': STATUS}


def SortList(log_list):
  """Sorts list of log files by integer instead of lexicographically.

  Args:
    log_list: List of log file names.

  Returns:
    List sorted by the integer in the name (with absence assumed at 0)
  """
  sort_list = []
  for path in log_list:
    split_file = path.split('.')
    if split_file[-1] == 'gz':
      log_num = int(split_file[-2])
    elif split_file[-1] == 'log':
      log_num = 0
    else:
      log_num = int(split_file[-1])
    sort_list.append((log_num, path))
  sorted_list = []
  for values in sorted(sort_list):
    sorted_list.append(values[1])
  return sorted_list


def ParseLogs(path_list):
  """Parse files in path_list for specific keys.

  Args:
    path_list: Pre-sorted list of paths to search.

  Returns:
    List of reversed file objects.
  """
  file_list = []
  for file_name in path_list:
    if file_name.endswith('.gz'):
      with gzip.open(file_name, 'r') as f:
        file_list.append(f.read().splitlines())
    else:
      with open(file_name, 'r') as f:
        file_list.append(f.read().splitlines())
  return reversed(file_list)


def MatchLines(file_list, matcher):
  """Matches lines in list of files against re object.

  Args:
    file_list: List of file objects to match against.
    matcher: list of re.compile() objects used to match lines.

  Returns:
    List of matched lines.
  """
  matched_lines = []
  for files in file_list:
    for line in files:
      for instance in matcher:
        if instance.match(line):
          matched_lines.append(line)
  return matched_lines


def ParseOptions():
  """Parse the command line options.

  Returns:
    Args that are specified by argparse.
  """
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '-a', '--all', help='Print status and command lines.',
      action='store_true')
  parser.add_argument(
      '-n', '--number', type=int, help='Number of lines to print.')
  parser.add_argument(
      '-s', '--status_code', help='Print only status lines from logs.',
      action='store_true')
  parser.add_argument(
      '-c', '--command_code', help='Print only command lines from logs.',
      action='store_true')

  return parser.parse_args()


def OutputLogs(line_num, mode):
  """Print logs based on provided flag(s).

  Args:
    line_num: number flag for how many lines to print.
    mode: Flag enum to affect how program executes.
  """
  log_list = glob.glob('/var/log/dpkg.*')
  log_list = SortList(log_list)
  file_list = ParseLogs(log_list)
  matched_lines = MatchLines(file_list, mode)
  if line_num:
    for i in range(-(line_num), 0, 1):
      print matched_lines[i]
  else:
    for line in matched_lines:
      print line


def main():
  args = ParseOptions()
  if args.all:
    OutputLogs(args.number, ENUM['all'])
    return
  elif args.status_code:
    OutputLogs(args.number, ENUM['status_code'])
    return
  elif args.command_code:
    OutputLogs(args.number, ENUM['command_code'])
    return
  else:
    OutputLogs(args.number, ENUM['all'])
    return

if __name__ == '__main__':
  main()
