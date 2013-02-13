from distutils.core import setup

setup(name="algolab",
        version="0.1",
        description="Algorithm Lab",
        packages=["algolab"],
        scripts=[
            "bin/al_filter",
            "bin/al_visualize",
            "bin/al_create_testgraph"],
        install_requires=[
            "numpy",
            "scipy",
        ]
        )
