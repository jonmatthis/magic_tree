from pprint import pprint

from magic_tree.magic_tree_dict import MagicTreeDict


def create_sample_magic_tree():
    magic_tree = MagicTreeDict()
    magic_tree['a']['b']['c']['woo'] = [1, 2, 13]
    magic_tree['a']['b']['c']['woo2'] = '✨'
    magic_tree['a']['b']['bang'] = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    magic_tree['a']['c']['pow'] = [4, 51, 6]
    magic_tree['a']['b']['c']['hey'] = [71, 8, 9]

    return magic_tree


def magic_tree_demo():

    tree = create_sample_magic_tree()
    print(f"Print as regular dict:\n")
    pprint(tree.dict(), indent=4)

    # TODO - this still includes the defaultdicts, will need to override __iter__ or items or soemthing to fix this ish
    # print(dict(tree))

    print(f"Original MagicTreeDict:\n{tree}\n\n")
    print(f"Print Table:\n")
    tree.print_table(['woo', 'bang', 'hey'])

    print(f"Filter tree on `c`:\n")
    c_tree = tree.filter_tree('c')
    print(c_tree)
    #
    # stats = tree.map_function(function=lambda x: sum(x) / len(x),
    #                           map_to='leaves', )
    # print(f"Calculate Tree Stats:\n{stats}\n\n")


if __name__ == "__main__":
    tree = magic_tree_demo()
    f = 9
