#!/bin/bash
set -e

cd ./evo-sim/
gnome-terminal -e "python3 ./evo-sim.py"

cd ../command_parser/
gnome-terminal -e "python3 ./parse_server.py"

cd ../command_synthesiser/
gnome-terminal -e "python3 ./command_synthesiser.py"
