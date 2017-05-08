import sys
import math
from collections import defaultdict
import random


def read_initial_state():
    factory_count = int(raw_input())  # the number of factories

    factories = defaultdict(list)
    link_count = int(raw_input())  # the number of links between factories
    for i in xrange(link_count):
        factory_1, factory_2, distance = [int(j) for j in raw_input().split()]
        factories[factory_1].append((factory_2, distance))
        factories[factory_2].append((factory_1, distance))

    return factories, factory_count


def read_move_state():
    factory_state = {}
    troops_state = []
    entity_count = int(raw_input())  # the number of entities (e.g. factories and troops)

    for i in xrange(entity_count):
        entity_id, entity_type, arg_1, arg_2, arg_3, arg_4, arg_5 = raw_input().split()
        entity_id = int(entity_id)
        arg_1 = int(arg_1)
        arg_2 = int(arg_2)
        arg_3 = int(arg_3)
        arg_4 = int(arg_4)
        arg_5 = int(arg_5)

        if entity_type == 'FACTORY':
            owner = arg_1
            cyborgs = arg_2
            production = arg_3
            factory_state[entity_id] = owner, cyborgs, production
            # print >>sys.stderr, 'FACTORY %d: (%d, %d, %d)' % (entity_id, owner, cyborgs, production)
        elif entity_type == 'TROOP':
            owner = arg_1
            source = arg_2
            target = arg_3
            cyborgs = arg_4
            distance = arg_5
            troops_state.append((owner, source, target, cyborgs, distance))
    return factory_state, troops_state


def format_moves(moves):
    """Output in the form of m_1;m_2;m_3, where m_i is:
        MOVE source_id destination_id count
        BOMB source_id destination_id
        INC factory_id"""
    if moves:
        return ";".join(moves)
    else:
        return "WAIT"


minimal_base_troops = 10
bombs_count = 2

factories, factory_count = read_initial_state()

# game loop
while True:
    factory_state, troops_state = read_move_state()

    moves = []
    for factory_id, (owner, cyborgs, production) in factory_state.iteritems():
        if owner == 1:
            options = []
            for other_factory_id, other_distance in factories[factory_id]:
                other_owner, other_cyborgs, other_production = factory_state[other_factory_id]

                if other_owner == 1:
                    continue

                how_good = (
                    other_production > 0,
                    -other_distance + random.random()
                )

                options.append((how_good, other_factory_id))

            if cyborgs >= 10 and production < 3:
                moves.append("INC %d" % factory_id)
                continue
            elif options:
                _, target_id = max(options)
                target_owner, target_cyborgs, target_production = factory_state[target_id]

                if bombs_count > 0 and target_owner == -1 and target_cyborgs + target_production * 2 >= 10:
                    moves.append(
                        "BOMB %d %d" % (factory_id, target_id)
                    )
                    bombs_count -= 1
                else:
                    moves.append(
                        "MOVE %d %d %d" % (factory_id, target_id, max(0, (production)))
                    )
                    # To our next factory
                continue

    print format_moves(moves)