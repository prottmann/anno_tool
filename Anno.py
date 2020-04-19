#!/usr/bin/env python3
import os


class AnnoDataset(object):
    """docstring for AnnoDataset"""
    def __init__(self,
                 buildings_path="data/buildings.txt",
                 chain_path="data/product_chains.txt",
                 productivity_path="data/custom_productivity.txt"):
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

    def write_data(self):
        self.write_productivities()

        with open(self.buildings_path, "w") as f:
            f.write("product,time\n")
            for k in sorted([*self.time.keys()]):
                f.write("{},{:1.2f}\n".format(k, self.time[k]))

        with open(self.chain_path, "w") as f:
            f.write("product,s1,s2\n")
            for k in sorted([*self.chain.keys()]):
                if len(self.chain[k]) is 1:
                    f.write("{},{},\n".format(k, self.chain[k][0]))
                else:
                    f.write("{},{},{}\n".format(k, self.chain[k][0],
                                                self.chain[k][1]))

    def write_productivities(self):
        with open(self.productivity_path, "w") as f:
            f.write("name,productivity\n")
            for k in sorted([*self.productivity.keys()]):
                f.write("{},{:1.2f}\n".format(k, self.productivity[k]))

    def get_names(self):
        return sorted([*self.time.keys()])

    def get_chain(self, product):
        sources = []
        sources.append(product)
        if product in self.chain:
            for s in self.chain[product]:
                sources.extend(self.get_chain(s))
        return sources

    #TODO: Endproduct != scale product
    def scaleChain(self, chain, number, scale_product=None):
        result = {}
        self.initialize_chain_productivity(chain)
        if scale_product is None:
            scale_product = chain[0]

        s = "Target product is: {} of {} with productivity of {:1.2f}.".format(
            number, scale_product, self.productivity[scale_product])
        print(s)
        faktor = self.time[scale_product] / self.productivity[
            scale_product] / number

        result[scale_product, "number"] = number
        result[scale_product,
               "productivity"] = self.productivity[scale_product]
        result[scale_product, "string"] = s

        max_length = get_max_stringlenth_of_sources(chain)
        for source in chain:
            if source is scale_product:
                continue
            source_number = self.time[source] / self.productivity[
                source] / faktor
            s = self.print_source(source, source_number, max_length)
            print(s)

            result[source, "number"] = source_number
            result[source, "productivity"] = self.productivity[source]
            result[source, "string"] = s
        return result

    def initialize_chain_productivity(self, chain):
        for p in chain:
            if p not in self.productivity:
                self.productivity[p] = 1.

    def get_chain_productivity(self, chain):
        self.initialize_chain_productivity(chain)
        result = []
        for c in chain:
            result.append(self.productivity[c])
        return result

    def print_source(self, source, source_number, max_length=10):
        return "Source: {:{max_length}} with productivity of {:1.2f} needs {:1.2f} buildings.".format(
            source,
            self.productivity[source],
            source_number,
            max_length=max_length)


def get_max_stringlenth_of_sources(chain):
    max_length = 0
    for source in chain[1:]:
        if len(source) > max_length:
            max_length = len(source)
    return max_length


if __name__ == '__main__':
    d = AnnoDataset()
    chain = d.get_chain(product="naehmaschinen")
    d.scaleChain(chain=chain, number=3)
