#!/usr/bin/env python

import random

class Matchbox(object):

    candidates = [1, 2, 3]

    def __init__(self, answer=False):
        if answer:
            self.answer = answer
        else:
            self.answer = random.choice(Matchbox.candidates)

    def answer(self):
        return self.answer

    def mutate(self):
        self.answer = {1: 2, 2: 3, 3: 1}[self.answer]

class Gene(object):

    counter = 0

    def __init__(self, answers=False):
        self.id = Gene.counter
        Gene.counter += 1
        self.matchboxes = []
        if answers:
            for i in range(10):
                self.matchboxes.append(Matchbox(answers[i]))
        else:
            for i in range(10):
                self.matchboxes.append(Matchbox())

    def __getitem__(self, i):
        return self.matchboxes[i]

    def answers(self):
        return [m.answer for m in self.matchboxes]

    def evaluate(self, answers):
        score = 0
        for i in range(len(self.matchboxes)):
            if self.answers()[i] == answers[i]:
                score += 1
        return score

    def whois(self):
        return self.id

class Genes(object):

    def __init__(self):
        self.num_selections = 0
        self.genes = []
        for i in range(10):
            self.genes.append(Gene())

    def select(self, right_answers):
        while True:
            print 'Round %d' % self.num_selections

            self.genes = sorted(self.genes, key=lambda gene: gene.evaluate(right_answers))
            for gene in self.genes:
                print '(g%03d)' % gene.whois(), gene.answers(), gene.evaluate(right_answers)
            for i in range(2):
                self.genes.pop(0)
            for baby in breed(self.genes[-1], self.genes[-2]):
                self.genes.append(baby)

            quit = raw_input('Enter q to quit: ')
            if quit == 'q':
                break

            self.num_selections += 1

            print

def breed(g1, g2):
    # g1, g2: Gene objects
    # Returns: Baby Gene objects

    a1, a2 = g1.answers(), g2.answers()

    # crossover
    s = random.randint(1, 6) + random.randint(1, 6) - 1
    if s < 10:
        baby1, baby2 = Gene(a1[:s] + a2[s:]), Gene(a2[:s] + a1[s:])
    else:
        baby1, baby2 = Gene(a1), Gene(a2)

    # mutation
    s = random.randint(1, 6) + random.randint(1, 6) - 1
    if s < 11:
        baby1[s % 10].mutate()
        baby2[s % 10].mutate()

    return baby1, baby2


if __name__ == '__main__':
    right_answers = [3, 1, 2, 2, 2, 3, 1, 3, 3, 1]
    genes = Genes()
    genes.select(right_answers)
