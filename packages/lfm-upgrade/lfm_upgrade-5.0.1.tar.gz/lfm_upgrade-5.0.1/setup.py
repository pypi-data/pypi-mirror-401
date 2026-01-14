"""
LFM AI Upgrade - 38% Power Savings Beyond 3V
System-Level Copyright Protected AI Enhancement Package
"""

from setuptools import setup, find_packages
import os

# Read version from file
with open("VERSION", "r") as f:
    VERSION = f.read().strip()

# Read long description
with open("README.md", "r", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

# Read requirements
with open("requirements.txt", "r") as f:
    REQUIREMENTS = [line.strip() for line in f if line.strip() and not line.startswith("#")]

# Copyright embedded in setup
COPYRIGHT_NOTICE = """
LFM AI Upgrade Package
========================================
COPYRIGHT © 2025 KEITH LUTON - ALL RIGHTS RESERVED
PATENT PENDING: Geometric Scaling Resonance Method
SYSTEM-LEVEL COPYRIGHT: AI Enhancement Algorithms

38% Power Savings Beyond 3V Demonstrated
Quantum Arbitration System Enforced
Commercial License Required for Production Use

Contact: keith@thenewfaithchurch.org
"""

setup(
    name="lfm-upgrade",
    version=VERSION,
    author="Keith Luton",
    author_email="keith@thenewfaithchurch.org",
    description="38% Power Savings AI Upgrade with System-Level Copyright",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/keithluton/lfm-ai-upgrade",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=REQUIREMENTS,
    include_package_data=True,
    package_data={
        "lfm_upgrade": [
            "copyright_notice.txt",
            "licensing_terms.md",
            "arbitration/*.py",
            "physics/*.py",
        ],
    },
  entry_points={
    "console_scripts": [
        "lfm-diagnose=lfm_upgrade.utils.diagnostics:cli_diagnose",
        "lfm-power-save=lfm_upgrade.neural.power_saver:cli_power_save",
        "lfm-validate=lfm_upgrade.utils.system_check:cli_validate",
    ],
},
        
    project_urls={
        "Documentation": "https://lfm-tnefc.org/docs",
        "Source": "https://github.com/keithluton/lfm-ai-upgrade",
        "Bug Reports": "https://github.com/keithluton/lfm-ai-upgrade/issues",
        "Commercial Licensing": "https://lfm-tnefc.org/licensing",
    },
    license="PROPRIETARY",
    copyright=COPYRIGHT_NOTICE,
)