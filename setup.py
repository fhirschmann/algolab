from distutils.core import setup

setup(name="algolab",
        version="0.1",
        description="Algorithm Lab",
        packages=["algolab"],
        scripts=[
            "bin/al_cp",
            "bin/al_crop_stations",
            "bin/al_filter",
            "bin/al_inspect",
            "bin/al_mk_sg",
            "bin/al_rm",
            "bin/al_visualize_algo",
            "bin/al_visualize_data",
            "bin/al_visualize_report",
            "bin/al_visualize_rg"],
        install_requires=[
            "numpy",
            "scipy",
        ]
        )
