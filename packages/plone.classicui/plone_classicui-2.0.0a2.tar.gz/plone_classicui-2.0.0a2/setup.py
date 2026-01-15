from setuptools import setup


long_description = "\n\n".join(
    [
        open("README.md").read(),
        open("CHANGES.md").read(),
    ]
)


setup(
    name="plone.classicui",
    version="2.0.0a2",
    description="Plone Classic UI distribution",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Web Environment",
        "Framework :: Plone :: 6.2",
        "Framework :: Plone :: Distribution",
        "Framework :: Plone",
        "Framework :: Zope :: 5",
        "Framework :: Zope",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python",
    ],
    keywords="Python Plone CMS Distribution",
    author="Plone Foundation",
    author_email="releasemanager@plone.org",
    url="https://github.com/plone/plone.classicui",
    project_urls={
        "Source": "https://github.com/plone/plone.classicui",
        "Tracker": "https://github.com/plone/plone.classicui/issues",
    },
    license="GPL version 2",
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.10",
    install_requires=[
        "plone.distribution",
        "plone.base",
        "plone.app.layout",
        "Zope",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            "plone.testing",
            "pytest-cov",
            "pytest-plone>=0.5.0",
            "zest.releaser[recommended]",
            "zestreleaser.towncrier",
        ]
    },
    entry_points="""
    [plone.autoinclude.plugin]
    target = plone
    """,
)
