from hspf.parser import graph
from pathlib import Path

from hspf.uci import UCI




uci = UCI(Path(__file__).parent.joinpath('data\Clearwater.uci'))
G = uci.network.G

def test_lakes():
    assert uci.network._lakes() == [12,
                                    32,
                                    52,
                                    112,
                                    114,
                                    140,
                                    152,
                                    172,
                                    214,
                                    272,
                                    434,
                                    442,
                                    446,
                                    502,
                                    504,
                                    512,
                                    522,
                                    532,
                                    542,
                                    592,
                                    594,
                                    596,
                                    636]

def test_calibration_order():
    orders = graph.calibration_order(graph.make_watershed(G,[90]))
    test_orders = [[52,53,10,12,32,71],
                    [55,13],
                    [30],
                    [50],
                    [70],
                    [90]]
    assert(len(orders) == len(test_orders))
    for order,test_order in zip(orders,test_orders):
        assert set(order) == set(test_order)
                                           
def test_get_opnids():
    reach_ids = graph.get_opnids(G,'RCHRES',[90])
    expected_reach_ids = [10,12,13,30,32,50,52,53,55,70,71,90]
    assert set(reach_ids) == set(expected_reach_ids)

    perlnd_ids = graph.get_opnids(G,'PERLND',[90])
    expected_perlnd_ids = [30, 31, 32, 33, 35, 36, 37, 38, 39, 40, 41, 42, 43, 45, 46, 47, 49, 48]
    assert set(perlnd_ids) == set(expected_perlnd_ids)

    implnd_ids = graph.get_opnids(G,'IMPLND',[90])
    expected_implnd_ids = [31,41]
    assert set(implnd_ids) == set(expected_implnd_ids)

    gener_ids = graph.get_opnids(G,'GGENER',[90])
    expected_gener_ids = [3]
    assert set(gener_ids) == set(expected_gener_ids)





'''
Methods of the Network class:
_downstream',
 '_lakes',
 '_routing_reaches',
 '_upstream',
 'calibration_order',
 'catchment_ids',
 'downstream',
 'drainage',
 'drainage_area',
 'drainage_area_landcover',
 'get_node_type_ids',
 'get_opnids',
 'lake_area',
 'lakes',
 'operation_area',
 'outlets',
 'paths',
 'reach_contributions',
 'routing_reaches',
 'schematic',
 'station_order',
 'subwatershed',
 'subwatershed_area',
 'subwatersheds',
 'uci',
 'upstream'
'''




