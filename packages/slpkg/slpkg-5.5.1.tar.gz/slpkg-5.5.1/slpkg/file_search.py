#!/usr/bin/python3
# -*- coding: utf-8 -*-

import gzip
import json
import logging
import os
from typing import Dict, List

from slpkg.config import config_load
from slpkg.repositories import Repositories
from slpkg.utilities import Utilities
from slpkg.views.view_process import ViewProcess

logger = logging.getLogger(__name__)


class FileSearch:  # # pylint: disable=[R0902]
    """Search for files within the gzipped repository indexes."""

    def __init__(self, options: dict[str, bool], search_terms: list[str], repository: str) -> None:
        """
        Initialize the FileSearch module.

        Args:
            options (dict): Command line options (e.g., 'quiet').
            search_terms (list): List of strings to search for.
        """
        logger.debug("Initializing FileSearch with terms: %s, options: %s", search_terms, options)
        self.options = options
        self.search_terms = search_terms
        self.repository = repository

        # Load colors for consistent UI
        self.grey = config_load.grey
        self.green = config_load.green
        self.red = config_load.red
        self.yellow = config_load.yellow
        self.endc = config_load.endc

        self.log_packages = config_load.log_packages

        self.repos = Repositories()
        self.utils = Utilities()
        self.view_process = ViewProcess()

        self.matching_count = 0
        # Results structure: {repository: {package: [matching_files]}}
        self.results: Dict[str, Dict[str, List[str]]] = {}

        self.option_for_no_case: bool = options.get('option_no_case', False)
        self.option_quiet: bool = options.get('option_quiet', False)
        self.option_local: bool = options.get('option_local', False)
        self.option_repository: bool = options.get('option_repository', False)

    def search(self) -> None:
        """Execute the file search across all enabled repositories."""
        logger.info("Starting file search for terms: %s", self.search_terms)

        for repo_name, repo_config in self.repos.repositories.items():
            if self.option_repository and self.repository != repo_name:
                continue

            repo_path = repo_config['path']
            index_file = os.path.join(repo_path, "filelist.json.gz")

            if not os.path.exists(index_file):
                continue

            try:
                with gzip.open(index_file, mode='rt', encoding='utf-8') as f:
                    repo_data = json.load(f)

                    for pkg_name, files in repo_data.items():
                        for term in self.search_terms:
                            # Logic for Case-Insensitive vs Case-Sensitive search
                            if self.option_for_no_case:
                                # Compare lowercased versions
                                term_lower = term.lower()
                                matches = [f for f in files if term_lower in f.lower()]
                            else:
                                # Standard case-sensitive search
                                matches = [f for f in files if term in f]

                            if matches:
                                if repo_name not in self.results:
                                    self.results[repo_name] = {}
                                if pkg_name not in self.results[repo_name]:
                                    self.results[repo_name][pkg_name] = []

                                self.results[repo_name][pkg_name].extend(matches)
                                self.matching_count += len(set(matches))

            except Exception as e:  # pylint: disable=[W0718]
                logger.error("Error reading index for %s: %s", repo_name, e)

    def search_local(self) -> None:
        """Search for terms within locally installed packages via /var/log/packages/."""
        logger.info("Starting local file search for terms: %s", self.search_terms)

        if not os.path.exists(self.log_packages):
            return

        # We read all the files in /var/log/packages/.
        for pkg_log in os.listdir(self.log_packages):
            log_path = os.path.join(self.log_packages, pkg_log)

            try:
                with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                    # Slackware archives have the files after the line "FILE LIST:"
                    lines = f.readlines()
                    try:
                        file_list_index = lines.index("FILE LIST:\n")
                        files = [line.strip() for line in lines[file_list_index + 1:]]
                    except ValueError:
                        continue   # If it doesn't find the FILE LIST line, skip it.

                    for term in self.search_terms:
                        if self.option_for_no_case:
                            term_lower = term.lower()
                            matches = [f for f in files if term_lower in f.lower()]
                        else:
                            matches = [f for f in files if term in f]

                        if matches:
                            repo_name = "Installed (Local)"
                            if repo_name not in self.results:
                                self.results[repo_name] = {}

                            if pkg_log not in self.results[repo_name]:
                                self.results[repo_name][pkg_log] = []

                            self.results[repo_name][pkg_log].extend(matches)
                            self.matching_count += len(set(matches))
            except Exception as e:  # pylint: disable=[W0718]
                logger.error("Error reading local package log %s: %s", pkg_log, e)

    def display_results(self) -> None:
        """Format and print the results. Respects the 'quiet' option."""
        print()
        if not self.results:
            print("Does not match any file.\n")
            return

        for repo, packages in sorted(self.results.items()):
            print(f"{self.yellow}[ Repository: {repo} ]{self.endc}")

            for pkg, files in sorted(packages.items()):
                pkg_name: str = self.utils.split_package(pkg)['name']
                # Check if the package is currently installed.
                if self.utils.is_package_installed(pkg_name):
                    status = f"[{self.green} installed {self.endc}]"
                else:
                    status = f"[{self.red} uninstalled {self.endc}]"

                print(f"  {status} - {pkg}")

                # Display paths if not in quiet mode.
                if not self.option_quiet:
                    for file_path in sorted(set(files)):
                        display_path = file_path
                        for term in self.search_terms:
                            display_path = display_path.replace(term, f"{self.yellow}{term}{self.endc}")
                        print(f"      {display_path}")
            print()

        print(f"{self.grey}Total found {self.matching_count} matches.{self.endc}")

    def run(self) -> None:
        """
        Main execution method.
        Check if the 'local' option is provided to perform a local search.
        """
        # Start the progress spinner once for the entire process.
        self.view_process.message('Searching for files, please wait')

        if self.option_local:
            self.search_local()
        else:
            self.search()

        # Finish progress spinner and Done.
        self.view_process.done()

        # Format and print the consolidated results.
        self.display_results()
