import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdktn-provider-random",
    "version": "12.1.0",
    "description": "Prebuilt random Provider for Terraform CDK (cdktf)",
    "license": "MPL-2.0",
    "url": "https://github.com/cdktn-io/cdktn-provider-random.git",
    "long_description_content_type": "text/markdown",
    "author": "CDK Terrain Maintainers",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdktn-io/cdktn-provider-random.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdktn_provider_random",
        "cdktn_provider_random._jsii",
        "cdktn_provider_random.bytes",
        "cdktn_provider_random.id",
        "cdktn_provider_random.integer",
        "cdktn_provider_random.password",
        "cdktn_provider_random.pet",
        "cdktn_provider_random.provider",
        "cdktn_provider_random.shuffle",
        "cdktn_provider_random.string_resource",
        "cdktn_provider_random.uuid"
    ],
    "package_data": {
        "cdktn_provider_random._jsii": [
            "provider-random@12.1.0.jsii.tgz"
        ],
        "cdktn_provider_random": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.9",
    "install_requires": [
        "cdktf>=0.21.0, <0.22.0",
        "constructs>=10.4.2, <11.0.0",
        "jsii>=1.119.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard>=2.13.3,<4.3.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
