import setuptools


setuptools.setup(
    # info
    name="cogload",
    description="Pre-loading for discord.py cog files",
    license="MIT",
    url="https://github.com/TychoTeam/cogload",
    # README
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    # SCM versioning (git tags)
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    # author
    author="Tycho",
    author_email="mail@tycho.team",
    # find and add packages
    packages=setuptools.find_packages(),
    include_package_data=True,
    # requirements and search
    python_requires=">=3.8",
    install_requires=["discord.py"],
    classifiers=[],
    keywords=[
        "discord.py",
        "discord bot",
        "cogs",
        "discord cogs",
        "discord.py cogs",
        "dpy cogs",
    ],
)
