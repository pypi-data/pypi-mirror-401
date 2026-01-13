import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdktn-provider-docker",
    "version": "12.1.0",
    "description": "Prebuilt docker Provider for Terraform CDK (cdktf)",
    "license": "MPL-2.0",
    "url": "https://github.com/cdktn-io/cdktn-provider-docker.git",
    "long_description_content_type": "text/markdown",
    "author": "CDK Terrain Maintainers",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdktn-io/cdktn-provider-docker.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdktn_provider_docker",
        "cdktn_provider_docker._jsii",
        "cdktn_provider_docker.buildx_builder",
        "cdktn_provider_docker.config",
        "cdktn_provider_docker.container",
        "cdktn_provider_docker.data_docker_image",
        "cdktn_provider_docker.data_docker_logs",
        "cdktn_provider_docker.data_docker_network",
        "cdktn_provider_docker.data_docker_plugin",
        "cdktn_provider_docker.data_docker_registry_image",
        "cdktn_provider_docker.data_docker_registry_image_manifests",
        "cdktn_provider_docker.image",
        "cdktn_provider_docker.network",
        "cdktn_provider_docker.plugin",
        "cdktn_provider_docker.provider",
        "cdktn_provider_docker.registry_image",
        "cdktn_provider_docker.secret",
        "cdktn_provider_docker.service",
        "cdktn_provider_docker.tag",
        "cdktn_provider_docker.volume"
    ],
    "package_data": {
        "cdktn_provider_docker._jsii": [
            "provider-docker@12.1.0.jsii.tgz"
        ],
        "cdktn_provider_docker": [
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
