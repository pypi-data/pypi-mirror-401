import subprocess
import re
import glob
import shutil
import os
from setuptools import setup
from setuptools.command.build_py import build_py

TOP_LEVEL_PACKAGE_NAME = "python_avro_generator"

setup(
  name="python_avro_generator",
  setuptools_git_versioning={
    "enabled": True,
    "template": "{tag}",
    "dirty_template": "{tag}.post{ccount}+git.{sha}",
  },
  install_requires=[
    'lcdp-avro-to-python==0.3.3.post8',
    "lcdp-api"
  ],
  setup_requires=['setuptools-git-versioning==1.9.2'],
  packages=[TOP_LEVEL_PACKAGE_NAME],
  package_dir={TOP_LEVEL_PACKAGE_NAME: "src"},
  license='Apache-2.0',
  description='Python Avro codegen for Le Comptoir Des Pharmacies',
  long_description='Python Avro generator for Le Comptoir Des Pharmacies',
  author='Le Comptoir Des Pharmacies',
  author_email='g.thrasibule@lecomptoirdespharmacies.fr',
  url='https://bitbucket.org/lecomptoirdespharmacies/lcdp-openapi-codegen',
  keywords=['openapi', 'python-avro-generator', 'openapi3'],
)
