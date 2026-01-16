#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""RINEX parser module for reading and analyzing RINEX observation files.

This file is part of rinexparser.
https://github.com/dach.pos/rinexparser

Licensed under the Apache 2.0 license:
http://opensource.org/licenses/apache2.0
Copyright (c) 2018, jiargei <juergen.fredriksson@bev.gv.at>
"""

import os
import argparse
from typing import Optional

from rinex_parser.logger import logger
from rinex_parser.obs_factory import RinexObsFactory, RinexObsReader


def run():
    parser = argparse.ArgumentParser(description="Analyse your Rinex files.")
    parser.add_argument("file", type=str, help="rinex file including full path")
    parser.add_argument("version", type=int, help="rinex version (2 or 3)")
    args = parser.parse_args()
    rinex_parser = RinexParser(rinex_version=args.version, rinex_file=args.file)
    rinex_parser.run()


class RinexParser:
    """Parser for RINEX observation files (versions 2 and 3).
    
    Handles reading, processing, and manipulation of RINEX observation data.
    """

    def __init__(
        self,
        rinex_file: str,
        rinex_version: int,
        **kwargs,
    ) -> None:
        """Initialize the RINEX parser.
        
        Args:
            rinex_file: Path to the RINEX observation file.
            rinex_version: RINEX format version (2 or 3).
            **kwargs: Additional keyword arguments.
            
        Raises:
            ValueError: If rinex_version is not 2 or 3.
            FileNotFoundError: If rinex_file does not exist.
        """
        if rinex_version not in [2, 3]:
            raise ValueError(
                f"Unknown RINEX version {rinex_version} (must be 2 or 3)"
            )
        if not os.path.isfile(rinex_file):
            raise FileNotFoundError(f"RINEX file not found: {rinex_file}")
            
        self.rinex_version = rinex_version
        self.rinex_file = rinex_file
        self.rinex_reader_factory = RinexObsFactory()
        self.rinex_reader: Optional[RinexObsReader] = None
        self._create_reader(self.rinex_version)

    def _create_reader(self, rinex_version: int, **reader_kwargs) -> None:
        """Create a RINEX reader instance for the specified version.
        
        Args:
            rinex_version: RINEX format version (2 or 3).
            **reader_kwargs: Additional arguments passed to reader constructor.
        """
        self.rinex_reader = self.rinex_reader_factory.create_obs_reader_by_version(
            rinex_version
        )(**reader_kwargs)

    def set_rinex_file(self, rinex_file: str) -> None:
        """Set or validate the RINEX file path.
        
        Args:
            rinex_file: Path to the RINEX observation file.
        """
        if os.path.isfile(rinex_file):
            self.rinex_file = rinex_file
        else:
            logger.warning(f"Could not find file: {rinex_file}")
            self.rinex_file = ""

    def get_rinex_file(self) -> str:
        """Get the current RINEX file path.
        
        Returns:
            str: Path to the RINEX file or empty string if not set.
        """
        return self.rinex_file

    def set_reader_options(self, **options) -> None:
        """Recreate reader with new options for optimization.
        
        Args:
            **options: Options to pass to reader (e.g., skip_datadict=True).
        """
        self._create_reader(self.rinex_version, **options)
    
    def do_create_datadict(self) -> None:
        """Read RINEX file and create data dictionary.
        
        Raises:
            ValueError: If rinex_file is not set.
            FileNotFoundError: If rinex_file does not exist.
        """
        if not self.rinex_file:
            raise ValueError("RINEX file not specified")
        if not os.path.exists(self.rinex_file):
            raise FileNotFoundError(f"Could not find file {self.rinex_file}")
            
        self.rinex_reader.set_rinex_obs_file(self.rinex_file)
        self.rinex_reader.read_header()
        self.rinex_reader.read_data_to_dict()

    def do_clear_datadict(self) -> None:
        """Clear unused observation types from header data.
        
        Reads all epochs to find observation types that don't have data,
        then removes them from the header.
        """
        found_obs_types = {}
        for sat_sys in self.rinex_reader.header.sys_obs_types.keys():
            found_obs_types[sat_sys] = set()

        # Iterate through all epochs and satellites to find used obs types
        for rinex_epoch in self.rinex_reader.rinex_epochs:
            for item in rinex_epoch.satellites:
                sat_sys = item["id"][0]  # Satellite system (G, R, E, C, J, S)
                for sat_obs in item["observations"].keys():
                    if sat_obs.endswith("_value"):
                        obs_type = sat_obs.split("_")[0]
                        found_obs_types[sat_sys].add(obs_type)

        # Remove obs types from header that weren't found in any epoch
        for sat_sys in self.rinex_reader.header.sys_obs_types:
            input_obs_types = set(
                self.rinex_reader.header.sys_obs_types[sat_sys]["obs_types"]
            )
            for obs_type in input_obs_types - found_obs_types[sat_sys]:
                logger.info(f"Remove unused OBS TYPE {obs_type}")
                self.rinex_reader.header.sys_obs_types[sat_sys][
                    "obs_types"
                ].remove(obs_type)

    def run(self) -> None:
        """Run the parser on the configured RINEX file.
        
        Raises:
            FileNotFoundError: If the RINEX file does not exist.
        """
        if not os.path.isfile(self.rinex_file):
            raise FileNotFoundError(f"Not a file: {self.rinex_file}")
        self.do_create_datadict()
