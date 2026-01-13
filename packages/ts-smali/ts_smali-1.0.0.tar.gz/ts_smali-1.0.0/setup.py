from os.path import isdir, join
from platform import system

from setuptools import Extension, find_packages, setup
from setuptools.command.build import build
from setuptools.command.develop import develop
from wheel.bdist_wheel import bdist_wheel


def copy_queries_to_package(package_dir):
    """Copy queries directory to the package directory."""
    from shutil import copytree, rmtree
    from os.path import exists
    
    queries_source = "queries"
    queries_dest = join(package_dir, "tree_sitter_smali", "queries")
    
    if isdir(queries_source):
        if exists(queries_dest):
            rmtree(queries_dest)
        copytree(queries_source, queries_dest)


class Build(build):
    def run(self):
        if isdir("queries"):
            dest = join(self.build_lib, "tree_sitter_smali", "queries")
            self.copy_tree("queries", dest)
        super().run()


class Develop(develop):
    def run(self):
        # Copy queries to the package directory for editable installs BEFORE super().run()
        # This ensures queries are available when the package is linked
        import os
        package_dir = os.path.abspath("bindings/python")
        copy_queries_to_package(package_dir)
        super().run()


class BdistWheel(bdist_wheel):
    def get_tag(self):
        python, abi, platform = super().get_tag()
        if python.startswith("cp"):
            python, abi = "cp38", "abi3"
        return python, abi, platform


setup(
    name="ts-smali",
    packages=find_packages("bindings/python"),
    package_dir={"": "bindings/python"},
    package_data={
        "tree_sitter_smali": ["*.pyi", "py.typed", "queries/*.scm"],
    },
    ext_package="tree_sitter_smali",
    ext_modules=[
        Extension(
            name="_binding",
            sources=[
                "bindings/python/tree_sitter_smali/binding.c",
                "src/parser.c",
                "src/scanner.c",
            ],
            extra_compile_args=[
                "-std=c11",
            ] if system() != "Windows" else [
                "/std:c11",
                "/utf-8",
            ],
            define_macros=[
                ("Py_LIMITED_API", "0x03080000"),
                ("PY_SSIZE_T_CLEAN", None)
            ],
            include_dirs=["src"],
            py_limited_api=True,
        )
    ],
    cmdclass={
        "build": Build,
        "develop": Develop,
        "bdist_wheel": BdistWheel
    },
    entry_points={
        "console_scripts": [
            "ts-smali-highlights=tree_sitter_smali.cli:print_highlights",
        ],
    },
    zip_safe=False
)
