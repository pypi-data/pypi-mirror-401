from lukedrew_bird_feeder import hello as hello_bird_feeder
from lukedrew_bird_feeder_2 import hello as hello_bird_feeder_2
from lukedrew_mahjong import hello as hello_mahjong
from lukedrew_mahjong_2 import hello as hello_mahjong_2
from lukedrew_seeds import hello as hello_seeds
from lukedrew_seeds_2 import hello as hello_seeds_2

from lukedrew_uvw_demo import hello as hello_uvw_demo
from lukedrew_uvw_demo_2 import hello as hello_uvw_demo_2


def main():
    hello_functions = [
        hello_uvw_demo,
        hello_uvw_demo_2,
        hello_bird_feeder,
        hello_bird_feeder_2,
        hello_mahjong,
        hello_mahjong_2,
        hello_seeds,
        hello_seeds_2,
    ]

    for func in hello_functions:
        print(func())


if __name__ == "__main__":
    main()
