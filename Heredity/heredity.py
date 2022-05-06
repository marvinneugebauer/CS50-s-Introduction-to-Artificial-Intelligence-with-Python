import csv
import itertools
import sys
from math import prod

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():
    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):
                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    person_probabilities = dict()

    for q in people:
        if (people[q]["mother"] and people[q]["father"]) is not None:
            person_probabilities[q] = parents_check(people, one_gene, two_genes, have_trait, q)[q]
        elif q in one_gene:
            person_prob = PROBS["gene"][1]
            person_probabilities[q] = traits(person_prob, one_gene, two_genes, have_trait, q)[q]
        elif q in two_genes:
            person_prob = PROBS["gene"][2]
            person_probabilities[q] = traits(person_prob, one_gene, two_genes, have_trait, q)[q]
        elif q not in one_gene and q not in two_genes:
            person_prob = PROBS["gene"][0]
            person_probabilities[q] = traits(person_prob, one_gene, two_genes, have_trait, q)[q]

    joint_prob = prod(person_probabilities.values())

    return joint_prob


def parents_check(people, one_gene, two_genes, have_trait, person):
    if person in one_gene:

        # Case: mother: 0, father: 2
        if (people[person]["mother"] not in one_gene) and (people[person]["mother"] not in two_genes) and (
                people[person]["father"] in two_genes) \
                or (people[person]["father"] not in one_gene) and (people[person]["father"] not in two_genes) and (
                people[person]["mother"] in two_genes):
            person_prob = (PROBS["mutation"] * PROBS["mutation"]) + ((1 - PROBS["mutation"]) * (1 - PROBS["mutation"]))
            return traits(person_prob, one_gene, two_genes, have_trait, person)

        # Case: mother: 0, father: 0
        elif ((people[person]["mother"] not in one_gene) and (people[person]["mother"] not in two_genes) and (
                people[person]["father"] not in one_gene)
              and (people[person]["father"] not in two_genes)):
            person_prob = 2 * (PROBS["mutation"] * (1 - PROBS["mutation"]))
            return traits(person_prob, one_gene, two_genes, have_trait, person)

        # Case: mother: 2, father: 2
        elif (people[person]["mother"] in two_genes) and (people[person]["father"] in two_genes):
            person_prob = 2 * (PROBS["mutation"] * (1 - PROBS["mutation"]))
            return traits(person_prob, one_gene, two_genes, have_trait, person)

        # Case: mother: 1, father: 1
        elif (people[person]["mother"] in one_gene) and (people[person]["father"] in one_gene):
            person_prob = (0.5 * 0.5) + (0.5 * 0.5)
            return traits(person_prob, one_gene, two_genes, have_trait, person)

        # Case: mother: 1, father: 0 or mother: 0, father: 1
        elif ((people[person]["mother"] in one_gene) and (people[person]["father"] not in one_gene) and (
                people[person]["father"] not in two_genes)) \
                or ((people[person]["father"] in one_gene) and (people[person]["mother"] not in one_gene) and (
                people[person]["mother"] not in two_genes)):
            person_prob = (0.5 * (1 - PROBS["mutation"])) + (0.5 * PROBS["mutation"])
            return traits(person_prob, one_gene, two_genes, have_trait, person)

        # Case: mother: 2 father: 1 or mother: 1, father: 2
        elif ((people[person]["mother"] in two_genes) and (people[person]["father"] in one_gene)) or \
                ((people[person]["father"] in two_genes) and (people[person]["mother"] in one_gene)):
            person_prob = ((1 - PROBS["mutation"]) * 0.5) + (PROBS["mutation"] * 0.5)
            return traits(person_prob, one_gene, two_genes, have_trait, person)

    elif person in two_genes:

        # Case: mother: 0, father: 2
        if (people[person]["mother"] not in one_gene) and (people[person]["mother"] not in two_genes) and (
                people[person]["father"] in two_genes) \
                or (people[person]["father"] not in one_gene) and (people[person]["father"] not in two_genes) and (
                people[person]["mother"] in two_genes):
            person_prob = (PROBS["mutation"] * (1 - PROBS["mutation"]))
            return traits(person_prob, one_gene, two_genes, have_trait, person)

        # Case: mother: 0, father: 0
        elif ((people[person]["mother"] not in one_gene) and (people[person]["mother"] not in two_genes) and (
                people[person]["father"] not in one_gene) and (people[person]["father"] not in two_genes)):
            person_prob = PROBS["mutation"] * PROBS["mutation"]
            return traits(person_prob, one_gene, two_genes, have_trait, person)

        # Case: mother: 2, father: 2
        elif (people[person]["mother"] in two_genes) and (people[person]["father"] in two_genes):
            person_prob = (1 - PROBS["mutation"]) * (1 - PROBS["mutation"])
            return traits(person_prob, one_gene, two_genes, have_trait, person)

        # Case: mother: 1, father: 1
        elif (people[person]["mother"] in one_gene) and (people[person]["father"] in one_gene):
            person_prob = 0.5 * 0.5
            return traits(person_prob, one_gene, two_genes, have_trait, person)

        # Case: mother: 1, father: 0 or mother: 0, father: 1
        elif ((people[person]["mother"] in one_gene) and (people[person]["father"] not in one_gene) and (
                people[person]["father"] not in two_genes)) \
                or ((people[person]["father"] in one_gene) and (people[person]["mother"] not in one_gene) and (
                people[person]["mother"] not in two_genes)):
            person_prob = 0.5 * PROBS["mutation"]
            return traits(person_prob, one_gene, two_genes, have_trait, person)

        # Case: mother: 2 father: 1 or mother: 1, father: 2
        elif ((people[person]["mother"] in two_genes) and (people[person]["father"] in one_gene)) or \
                ((people[person]["father"] in two_genes) and (people[person]["mother"] in one_gene)):
            person_prob = (1 - PROBS["mutation"]) * 0.5
            return traits(person_prob, one_gene, two_genes, have_trait, person)

    elif person not in (one_gene and two_genes):

        # Case: mother: 0, father: 2 or mother: 0, father: 2
        if (people[person]["mother"] not in one_gene) and (people[person]["mother"] not in two_genes) and (
                people[person]["father"] in two_genes) \
                or (people[person]["father"] not in one_gene) and (people[person]["father"] not in two_genes) and (
                people[person]["mother"] in two_genes):
            person_prob = (PROBS["mutation"] * (1 - PROBS["mutation"]))
            return traits(person_prob, one_gene, two_genes, have_trait, person)

        # Case: mother: 0, father: 0
        elif ((people[person]["mother"] not in one_gene) and (people[person]["mother"] not in two_genes) and (
                people[person]["father"] not in one_gene) and (people[person]["father"] not in two_genes)):
            person_prob = (1 - PROBS["mutation"]) * (1 - PROBS["mutation"])
            return traits(person_prob, one_gene, two_genes, have_trait, person)

        # Case: mother: 2, father: 2
        elif (people[person]["mother"] in two_genes) and (
                people[person]["father"] in two_genes):
            person_prob = PROBS["mutation"] * PROBS["mutation"]
            return traits(person_prob, one_gene, two_genes, have_trait, person)

        # Case: mother: 1, father: 1
        elif (people[person]["mother"] in one_gene) and (people[person]["father"] in one_gene):
            person_prob = 0.5 * 0.5
            return traits(person_prob, one_gene, two_genes, have_trait, person)

        # Case: mother: 1, father: 0 or mother: 0, father: 1
        elif ((people[person]["mother"] in one_gene) and (people[person]["father"] not in one_gene) and (
                people[person]["father"] not in two_genes)) \
                or ((people[person]["father"] in one_gene) and (people[person]["mother"] not in one_gene) and (
                people[person]["mother"] not in two_genes)):
            person_prob = 0.5 * (1 - PROBS["mutation"])
            return traits(person_prob, one_gene, two_genes, have_trait, person)

        # Case: mother: 2 father: 1 or mother: 1, father: 2
        elif ((people[person]["mother"] in two_genes) and (people[person]["father"] in one_gene)) or \
                ((people[person]["father"] in two_genes) and (people[person]["mother"] in one_gene)):
            person_prob = PROBS["mutation"] * 0.5
            return traits(person_prob, one_gene, two_genes, have_trait, person)


def traits(person_prob, one_gene, two_genes, have_trait, person):
    person_probabilities = dict()
    if person in one_gene:
        if person in have_trait:
            person_prob = person_prob * PROBS["trait"][1][True]
            person_probabilities[person] = person_prob
            return person_probabilities
        else:
            person_prob = person_prob * PROBS["trait"][1][False]
            person_probabilities[person] = person_prob
            return person_probabilities
    if person in two_genes:
        if person in two_genes:
            if person in have_trait:
                person_prob = person_prob * PROBS["trait"][2][True]
                person_probabilities[person] = person_prob
                return person_probabilities
            else:
                person_prob = person_prob * PROBS["trait"][2][False]
                person_probabilities[person] = person_prob
                return person_probabilities
    if person not in (one_gene and two_genes):
        if person in have_trait:
            person_prob = person_prob * PROBS["trait"][0][True]
            person_probabilities[person] = person_prob
            return person_probabilities
        else:
            person_prob = person_prob * PROBS["trait"][0][False]
            person_probabilities[person] = person_prob
            return person_probabilities


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        if person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        elif person not in (one_gene and two_genes):
            probabilities[person]["gene"][0] += p

    for person in probabilities:
        if person in have_trait:
            probabilities[person]["trait"][True] += p
        elif person not in have_trait:
            probabilities[person]["trait"][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    # print("Person Probabiltes: ", person_probabilities)

    for person in probabilities:
        if probabilities[person]["gene"][0] == 0 and probabilities[person]["gene"][1] == 0 and \
                probabilities[person]["gene"][2] == 0:
            probabilities[person]["gene"][2] = 1 / 3
            probabilities[person]["gene"][1] = 1 / 3
            probabilities[person]["gene"][0] = 1 / 3
        else:
            sum_1 = (probabilities[person]["gene"][0] + probabilities[person]["gene"][1] +
                     probabilities[person]["gene"][2])
            probabilities[person]["gene"][2] = probabilities[person]["gene"][2] / sum_1
            probabilities[person]["gene"][1] = probabilities[person]["gene"][1] / sum_1
            probabilities[person]["gene"][0] = probabilities[person]["gene"][0] / sum_1

        if probabilities[person]["trait"][True] == 0 and probabilities[person]["trait"][False] == 0:
            probabilities[person]["trait"][True] == 1 / 2
            probabilities[person]["trait"][False] == 1 / 2
        else:
            sum_2 = (probabilities[person]["trait"][True] + probabilities[person]["trait"][False])
            probabilities[person]["trait"][True] = probabilities[person]["trait"][True] / sum_2
            probabilities[person]["trait"][False] = probabilities[person]["trait"][False] / sum_2


if __name__ == "__main__":
    main()
