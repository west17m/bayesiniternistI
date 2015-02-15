#!/usr/bin/python2.7 -tt
# -*- coding: utf-8 -*-
###############################################################################
# Main InternistI Bayes implementation file
###############################################################################

import sys
import os
import pandas as pd
import argparse
import logging

class BayesInternsist:

  title="Bayes' Internist"
  # @todo replace with acutual instructions
  instructions=""

  symptoms = None  # holds signs/symtpom input
  logger   = None  # logging

  ####
  # constructor
  ####
  def __init__(self):

    self.setup_logging()

    self.logger.debug('started logger')

    symptoms = pd.DataFrame(columns=['pos_neg','symptom'])

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
    string = ""
    s = [
      "command help",
      "? - display this message",
      "q - quit",
      ]
    string = ""
    for str in s:
      string += str + "\n"
    print string

  ####
  # show prompt
  ####
  def get_user_choice(self):
    # Let users know what they can do.
    sys.stdout.write('enter symptom (? for help) # ')
    return raw_input("")

  ####
  # validate input
  ####
  def validate(self,string):
    # @todo insert validation logic
    return True

  ####
  # add a finding to the symptoms frame
  ####
  def add_finding(self,string):
    # at this point everything should be validated
    # @todo divide string into +/- and finding
    # @todo add to dataframe
    pass

  ####
  # tests
  ####
  def run_tests(self):
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
    # Clear the screen.
    os.system('clear')

    print self.title
    print self.instructions
    quit = False

    while not quit:
      command = self.get_user_choice()

      if command == 'q':
        quit = True
      elif command == '?':
        self.print_help()
      else:
        if not self.validate(command):
          # if illegal input
          # @todo decide whether to get error message and/or suggestions
          pass
        else:
          # if legal input
          self.add_finding(command)
          pass


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
  group.add_argument("-t","--test", help="perform unit testing",action="store_true")
  parser.add_argument("-v","--verbose", help="increase output verbosity",action="store_true")
  args = parser.parse_args()

  # @todo add log level to commandline

  # set defaults
  (verbose,test,interactive) = (False,False,True)
  if args.verbose:
    verbose = True
  if args.test:
    test = True
    interactive = False
  if args.interactive:
    test = False
    interactive = True

  # create object
  bi = BayesInternsist()

  if test:
    # perform unit tests
    bi.run_tests()
  elif interactive:
    # run in interactive mode
    bi.interactive()
  else:
    raise Exception('illegal argument sent, terminating')