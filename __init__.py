#!/usr/bin/python2.7 -tt
# -*- coding: utf-8 -*-
###############################################################################
# Main InternistI Bayes implementation file
###############################################################################

import sys
import os
import pandas as pd

class BayesInternsist:

  title="Bayes' Internist"
  # @todo replace with acutual instructions
  instructions=""

  symptoms = None  # holds signs/symtpom input

  #
  # constructor
  #
  def __init__(self):
    symptoms = pd.DataFrame(columns=['pos_neg','symptom'])
    self.run()

  #
  # display the help dialog when a user presses '?'
  #
  def print_help(self):
    string = ""
    s = [
      "command help",
      "? - display this message",
      ]
    string = ""
    for str in s:
      string += str + "\n"
    print string

  #
  # show prompt
  #
  def get_user_choice(self):
    # Let users know what they can do.
    sys.stdout.write('enter symptom (? for help) # ')
    return raw_input("")

  #
  # validate input
  #
  def validate(self,string):
    # @todo insert validation logic
    return True

  #
  # run the program
  #
  def run(self):

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
          pass


###############################################################################
# This will be called from the command line if no arguments are given
###############################################################################
if __name__ == '__main__':
  bi = BayesInternsist()