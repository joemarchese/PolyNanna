import data
import os
from random import choice


class Polyanna:
    '''This class contains stats, the drawing logic, and all data.'''

    def __init__(self, participants=None):
        self.participants = []
        self.failcount = 0


    def build_participants(self):
        '''Builds a list of Participant objects from Data.py'''
        for key, restricted in data.data.items():
            self.participants.append(Participant(key, set(restricted)))


    def build_all_history(self):
        '''Iterates over participants and removes prior years' selections.'''
        for participant in self.participants:
            participant.build_history()


    def run_drawing_until_completed(self):
        '''Build a Hat and make selections until a valid result is achieved.

        The try/except block works by iterating over hat contents and making
        selections. If no selection is available (No valid gift recipient for a
        participant), it will raise an IndexError add to the failcount, and
        restart the while loop.
        '''
        completed = False
        while not completed:
            hat = Hat(self.participants)
            try:
                for participant in self.participants:
                    participant.giving_to = hat.select(participant)
                    hat.contents.remove(participant.giving_to)
                completed = True
            except IndexError:
                completed = False
                self.failcount += 1
        return completed


class Participant:
    '''The class for individual participants that contains their attributes.'''

    def __init__(self, name, restricted_set=None, giving_to=None):
        self.name = name
        self.restricted_set = restricted_set
        self.giving_to = giving_to

    def build_history(self):
        '''Adds previous gift recipients to a Participant's restricted_set.'''
        for year in data.history[self.name]:
            self.restricted_set.add(year[1])


class Hat:
    '''This class represents the valid participants still in the drawing.'''

    def __init__(self, contents=None):
        self.contents = contents
        self.contents = set([participant.name for participant in self.contents])


    def select(self, participant):
        '''takes a participant and returns a valid selection out of the hat.'''
        return choice(list(self.contents - participant.restricted_set))


class Results:
    '''This class handles the I/O file operations and offers console output.'''

    def __init__(self, polyanna, results_directory=os.getcwd() + '\Results'):
        self.polyanna = polyanna
        self.results_directory = results_directory
        if not os.path.exists(results_directory):
            os.mkdir(results_directory)
        if not os.path.exists(results_directory + '\Individual_Results'):
            os.mkdir(results_directory + '\Individual_Results')

    def print_results(self):
        '''Print results to the console.'''
        for participant in self.polyanna.participants:
            print(participant.name, ' --> ', participant.giving_to)


    def write_full_results(self):
        '''Write results to a .txt file.'''
        os.chdir(self.results_directory)
        with open('full_results.txt', 'w') as f:
            for participant in self.polyanna.participants:
                f.write(participant.name + ' --> ' + participant.giving_to + '\n')


    def write_individual_results(self):
        '''Write individual results to separate files.

        Note:
            This is to keep the program's selections confidential from the
            program's operator. Participants can be instructed to open the .txt
            file with their name, it will provide their intended recipient.
        '''
        os.chdir(self.results_directory + '\Individual_Results')
        for participant in self.polyanna.participants:
            filename = '{}.txt'.format(participant.name)
            with open(filename, 'w') as file:
                file.write(participant.giving_to)


def main():
    polyanna = Polyanna()
    polyanna.build_participants()
    polyanna.build_all_history()
    if polyanna.run_drawing_until_completed():
        print('Success. You are awesome.')
        results = Results(polyanna)
        results.print_results()
        # results.write_full_results()
        # results.write_individual_results()
    print('Fail Count: ', polyanna.failcount)

if __name__ == '__main__': main()
