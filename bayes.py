#!/usr/bin/python2.7 -tt
# -*- coding: utf-8 -*-
###############################################################################
# Main InternistI Bayes implementation file
###############################################################################

import sys
import re
import os
import pandas as pd
import argparse
import logging
import numpy as np
from termcolor import colored # https://pypi.python.org/pypi/termcolor

class BayesInternsist:

  title="Bayes' Internist"
  # @todo replace with acutual instructions
  instructions=""

  symptoms = None  # holds signs/symtpom input
  logger   = None  # logging

  diseases_txt_path = 'data/Diseases_for_2015_decision_support_exercise_v03.txt'
  findings_txt_path = 'data/Findings_for_2015_decision_support_exercise_v03.txt'

  diseases_dat_path = 'data/diseases.dat'
  findings_dat_path = 'data/findings.dat'

  diseases = None
  findings = None

  kb = None

  ####
  # constructor
  ####
  def __init__(self):

    self.setup_logging()
    self.logger.debug('started logger')

    self.symptoms = pd.DataFrame(columns=['negation_status_human','negation_status_int', 'finding_id'])
    self.open_kb()
    self.findings = pd.DataFrame()

  ####
  # open knowledge base
  ####
  def open_kb(self):

    self.logger.debug('attempting to open knowledge base')
    self.kb = BayesKB()

  ####
  # setup_logging
  ####
  def setup_logging(self):
    # create logging framework
    # @see http://victorlin.me/posts/2012/08/26/good-logging-practice-in-python
    self.logger = logging.getLogger(__name__)
    self.logger.setLevel(logging.DEBUG)

    # create a file handler
    handler = logging.FileHandler('bayes.log')

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # add the handlers to the logger
    self.logger.addHandler(handler)

  ####
  # display the help dialog when a user presses '?'
  ####
  def print_help(self):
    self.logger.debug('displayed help')
    string = ""
    s = [
      "command help",
      "+/- symptom",
      "?  - display this message",
      "q  - quit",
      ]
    string = ""
    for str in s:
      string += str + "\n"
    print string

  ####
  # show prompt
  ####
  def get_user_choice(self,prompt):
    self.logger.debug('soliciting user choice')

    # Let users know what they can do.
    sys.stdout.write(prompt)
    return raw_input("")

  ####
  # validate input
  ####
  def validate(self,string):
    self.logger.debug('validating user input of ' + string)
    p = re.compile('^\s*(\+|\-)\s+(.*)')
    match = p.match(string)
    if match:
      self.logger.debug('matched ' + string)
      negation_status = match.group(1)
      finding = match.group(2).upper()
      t = self.kb.findings[self.kb.findings['mx'].str.contains(finding)]

      if len(t) == 0:
        self.logger.debug('could not find ' + finding + ' in knowledge base')
        print 'I couldn\'t find the finding, please try again'
        return False

      # creating choices
      self.logger.debug('creating choices table')
      choices = pd.DataFrame()
      choices['choice'] = np.array(range(1,len(t)+1))
      choices['id'] = t['id'].values
      choices['finding'] = t['mx'].values

      self.logger.debug('printing user choices')

      i=0
      for index, row in choices.iterrows():
        text = str(row['choice']) + '\t' + row['finding'].lower()
        if i % 2:
          print colored(text,'cyan',attrs=['reverse'])
        else:
          print colored(text,'white',attrs=['reverse'])
        i += 1

      self.logger.debug('waiting for user response')
      print
      number = self.get_user_choice('choose number of finding: ')

      # @todo ensure numeric input and of reasonable range

      t = choices[choices['choice'] == int(number)]
      id = t['id'].values[0]

      negation_status_int = None
      if negation_status == '+':
        negation_status_int = 1
      elif negation_status == '-':
        negation_status_int = 0
      else:
        self.logger.error('expected +/-, got ' + negation_status)
        sys.exit(1)

      self.symptoms = self.symptoms.append([{'negation_status_human':negation_status,'negation_status_int':negation_status_int,'finding_id':id}])

      # print findings
      self.print_findings()

      # print kb_findings
      return True
    else:
      self.logger.debug('unmatched ' + string)
      print 'I can\'t seem to find that finding, please try again.  Did you omit the +/-?'
      return False


  def print_findings(self):

    self.logger.debug('printing findings')
    print '#################\nFindings so far\n#################\n'
    if len(self.symptoms) == 0:
      print '\tnone'
      return

    joined = pd.DataFrame.merge(self.symptoms,self.kb.findings,left_on='finding_id',right_on='id')[['negation_status_human','mx']]

    self.logger.debug('creating patterns')
    p1 = re.compile('^\s*\+')
    p2 = re.compile('^\s*\-')
    self.logger.debug('patterns created')

    for index, row in joined.iterrows():

      text = '\t' + row['negation_status_human'] + ' ' + row['mx'].lower()
      self.logger.debug('testing ' + text)

      if p1.search(text):
        print colored(text,'green')
      elif p2.search(text):
        print colored(text,'red')
      else:
        self.logger.debug('unexpected string ' + text)
        sys.exit(1)
    print

  ####
  # add a finding to the symptoms frame
  ####
  def add_finding(self,string):
    self.logger.debug('adding finding')
    # at this point everything should be validated
    # @todo divide string into +/- and finding
    # @todo add to dataframe
    pass

  ####
  # tests
  ####
  def run_tests(self):
    self.logger.debug('running unit tests')
    # @todo add tests to test the following functionality
    #   1. constructor creates empty symtpom frame with two-columns
    #   2. constructor creates kb frame
    #   3. if pickled file exists, kb uses that
    #   4. if pickled file does not exist, kb parses text file
    #   5. graceful handling of kb text file not existing
    #   6. saving kb as pickle file
    #   7. validating user input (validate())
    #   8. suite of findings and for diseases
    #
    pass


  ####
  # interactive
  ####
  def interactive(self):
    self.logger.debug('beginning interactive mode')
    # Clear the screen.
    os.system('clear')

    print self.title
    self.print_findings()
    print self.instructions
    quit = False

    while not quit:
      self.logger.debug('getting additional finding')
      command = self.get_user_choice('enter symptom (? for help) # ')

      if command == 'q':
        self.logger.debug('received quit command')
        quit = True
      elif command == '?':
        self.print_help()
      elif command == '':
        self.process()
        quit = True
      else:
        if not self.validate(command):
          # if illegal input
          # @todo decide whether to get error message and/or suggestions
          pass
        else:
          # if legal input
          self.add_finding(command)
          pass

  def datastructures(self):
    self.kb.pprint()

  def process(self):
    # at this point, findings dataframe should be filled
    print "processing logic"
    print self.symptoms

###############################################################################
# BayesKB
# @author Ivo Violich
# migrated from baye_import.py
#
###############################################################################
class BayesKB:

  # dataframe
  # [id]  [finding_text]
  findings = None

  # dataframe
  # [id]  [dx_text]
  diseases = None

  # dataframe
  # [id]  [IM]  [TY]
  frequencies = None

  # dataframe
  # [DX id]  [LINK ID]  [LINK ??] [NPV] [PPV]
  disease_linkage = None

  # dataframe
  # [DX id]  [MX ID]  [NPV] [PPV]
  disease_finding_linkage = None

  logger = None

  ####
  # constructor
  ####
  def __init__(self):
    # @todo allow logging level and file to be passed to constructor
    self.setup_logging()
    self.logger.debug('KB started logger')
    self.parse()

  ####
  # setup_logging
  ####
  def setup_logging(self):
    # create logging framework
    # @see http://victorlin.me/posts/2012/08/26/good-logging-practice-in-python
    self.logger = logging.getLogger(__name__)
    self.logger.setLevel(logging.DEBUG)

    # create a file handler
    handler = logging.FileHandler('bayes.log')

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # add the handlers to the logger
    self.logger.addHandler(handler)

  def parse(self):
    # @todo ensure directory data is present
    # @todo ensure files are present and if not prompt to dl from Oak
    # @todo move text name to constructor
    # @todo add logging to text file
    # @todo pickle and cache to provide (marginal) speed up

    self.logger.debug('started KB.parse')

    self.logger.debug('opening files')
    findings = open('data/Findings_for_2015_decision_support_exercise_v03.txt')
    diseases = open('data/Diseases_for_2015_decision_support_exercise_v03.txt')

    sx_map = {}
    IM_TY = {}

    self.logger.debug('started parsing findings file')
    for line in findings:
      line = line.rstrip('\r\n')
      if (re.match('MX', line)):
        line_list = line.split(None, 2)
        sx_map[line_list[1]] = line_list[2]
      else:
        line_list = line.split(None, 4)
        IM_TY[line_list[0]] = {line_list[1]:line_list[2],
          line_list[3]:line_list[4]}

    dz_map = {}
    dz_mx = []
    dz_lk = []

    self.logger.debug('started parsing diseases')
    for line in diseases:
      line = line.rstrip('\r\n')
      if (re.match('DX', line)):
        line_list = line.split(None, 2)
        dz_map[line_list[1]] = line_list[2]
        dz_set = line_list[1]
      elif (re.match('MX', line)):
        line_list = line.split(None, 3)
        dz_mx.append(
                {
                'DX':dz_set,
                'MX':line_list[2],
                'PPV':list(line_list[1])[0],
                'NPV':list(line_list[1])[1]
                }
                )
      elif (re.match('LINK', line)):
        line_list = line.split(None, 4)
        dz_lk.append(
                {
                'DX':dz_set,
                'LINK':line_list[3],
                'LINK_t':line_list[1],
                'PPV':list(line_list[2])[0],
                'NPV':list(line_list[2])[1]
                }
                )
        dz_map[line_list[3]] = line_list[4]

    findings.close()
    diseases.close()

    self.logger.debug('formatting high level data structures')

    # create findings
    self.findings = pd.DataFrame()
    self.findings['id'] = sx_map.keys()
    self.findings['mx'] = sx_map.values()
    self.findings = self.findings.convert_objects(convert_numeric=True).sort(['mx','id'])

    # create diseases
    self.diseases = pd.DataFrame()
    self.diseases['id'] = dz_map.keys()
    self.diseases['dx'] = dz_map.values()
    self.diseases= self.diseases.convert_objects(convert_numeric=True).sort(['dx','id'])

    # frequency mapping
    self.frequencies = pd.DataFrame.from_dict(IM_TY).transpose()
    self.frequencies['id'] = self.frequencies.index
    self.frequencies = self.frequencies[['id','IM','TY']].convert_objects(convert_numeric=True).sort(['id'])

    # disease linkage
    self.disease_linkage = pd.DataFrame.from_dict(dz_lk).convert_objects(convert_numeric=True).sort('DX')

    # disease-finding linkage
    self.disease_finding_linkage = pd.DataFrame.from_dict(dz_mx).convert_objects(convert_numeric=True).sort(['DX','MX'])

  def pprint(self,n=10):
    self.logger.debug('printing data structures')
    print '\n\n## FINDINGS ##\n',self.findings.head(n)
    print '\n\n## DISEASES ##\n',self.diseases.head(n)
    print '\n\n## FREQUENCIES ##\n',self.frequencies.head(n)
    print '\n\n## DISEASE LINKAGES ##\n',self.disease_linkage.head(n)
    print '\n\n## DISEASE LINKAGES ##\n',self.disease_finding_linkage.head(n)

###############################################################################
#
# This will be called from the command line if no arguments are given
# run from the command line with --help for options
# @see https://docs.python.org/2/howto/argparse.html
#
###############################################################################
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  group = parser.add_mutually_exclusive_group()
  group.add_argument("-i","--interactive", help="launch interactive mode",action="store_true")
  group.add_argument("-d","--datastructures", help="show data structures",action="store_true")
  group.add_argument("-t","--test", help="perform unit testing",action="store_true")
  parser.add_argument("-v","--verbose", help="increase output verbosity",action="store_true")
  args = parser.parse_args()

  # @todo add log level to commandline

  # set defaults
  (verbose,test,interactive,datastructures) = (False,False,True,False)
  if args.verbose:
    verbose = True
  if args.test:
    test = True
    interactive = False
  if args.interactive:
    test = False
    interactive = True
  if args.datastructures:
    test = False
    interactive = False
    datastructures = True

  # create object
  bi = BayesInternsist()
  bi.logger.debug('BayesInternsist called from command-line')

  if test:
    # perform unit tests
    bi.run_tests()
  elif interactive:
    # run in interactive mode
    bi.interactive()
  elif datastructures:
    # show data structures
    bi.datastructures()
  else:
    bi.logger.error('illegal argument sent')
    raise Exception('illegal argument sent, terminating')

  bi.logger.debug('application finished without error')
  sys.exit(0)