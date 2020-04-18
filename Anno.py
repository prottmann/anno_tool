#!/usr/bin/env python3

import numpy as np
import os


class AnnoDataset(object):
    """docstring for AnnoDataset"""
    def __init__(self,
                 buildings_path="data/buildings.txt",
                 chain_path="data/product_chains.txt",
                 productivity_path="custom_productivity.txt"):
        self.buildings_path = buildings_path
        self.chain_path = chain_path
        self.productivity_path = productivity_path
        self.time = {}
        self.chain = {}
        self.productivity = {}
        if self.paths_valid:
            self.readData()

    def paths_valid(self):
        return os.path.exists(self.buildings_path) and os.path.exists(
            self.chain_path)

    def readData(self):
        assert (self.paths_valid)
        with open(self.buildings_path, "r") as f:
            next(f)
            for line in f:
                comps = line.rstrip().split(",")
                self.time[comps[0]] = float(comps[1])

        with open(self.chain_path, "r") as f:
            next(f)
            for line in f:
                comps = line.rstrip().split(",")
                if comps[2] is "":
                    self.chain[comps[0]] = comps[1:2]
                else:
                    self.chain[comps[0]] = comps[1:]
        if os.path.exists(self.productivity_path):
            with open(self.productivity_path, "r") as f:
                next(f)
                for line in f:
                    comps = line.rstrip().split(",")
                    assert (float(comps[1]) < 100)
                    self.productivity[comps[0]] = float(comps[1])

    def get_chain(self, product):
        sources = []
        sources.append(product)
        if product in self.chain:
            for s in self.chain[product]:
                sources.extend(self.get_chain(s))
        return sources

    def scaleChain(self, chain, number):
        self.initialize_chain_productivity(chain)

        target = chain[0]
        print("Target product is: {} with productivity of {:1.2f}.".format(
            target, self.productivity[target]))
        faktor = self.time[target] / self.productivity[target] / number

        max_length = get_max_stringlenth_of_sources(chain)
        for source in chain[1:]:
            source_number = self.time[source] / self.productivity[
                source] / faktor
            self.print_source(source, source_number, max_length)

    def initialize_chain_productivity(self, chain):
        for p in chain:
            if p not in self.productivity:
                self.productivity[p] = 1

    def print_source(self, source, source_number, max_length=10):
        print(
            "Source: {:{max_length}} with productivity of {:1.2f} needs {:1.2f} buildings."
            .format(source,
                    self.productivity[source],
                    source_number,
                    max_length=max_length))


def get_max_stringlenth_of_sources(chain):
    max_length = 0
    for source in chain[1:]:
        if len(source) > max_length:
            max_length = len(source)
    return max_length


if __name__ == '__main__':
    d = AnnoDataset()
    d.readData()
    chain = d.get_chain(product="naehmaschinen")
    d.scaleChain(chain=chain, number=3)