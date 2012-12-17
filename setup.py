from distutils.core import setup

setup(name="algolab",
        version="0.1",
        description="Algorithm Lab",
        packages=["algolab"],
        scripts=[
            "bin/filter",
            "bin/visualize",
            "bin/create_testgraph"],
        install_requires=[
            "numpy",
        ]
        )
