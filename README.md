# Digital Asset Blacklist Detector ⚠️

A lightweight **Python tool** that detects whether a digital asset (e.g., IP address, domain, or other digital identifier) is listed in any public blacklists via the **MultiRBL** service (aggregating multiple blacklist sources).  
Ideal for OSINT, cybersecurity screening, and asset‐risk assessment.

---

## 🔍 Overview

This repository contains a script `Blacklist_detector.py` which:
- Queries the **MultiRBL** website/API for blacklist status of a given digital asset.  
- Parses and returns whether the asset appears in one or more blacklists.  
- Enables quick automation or manual checks of asset reputation.

Original description: “This code detects if a digital active is in a blacklist using the web site “MultiRBL” that add data of several Blacklists.”  

---

## 🧰 Features

- ✅ Written in **Python** (100% of the codebase) :contentReference[oaicite:1]{index=1}  
- 🔎 Checks digital assets (e.g., domains, IPs) against aggregated blacklist sources  
- 🧩 Suitable for integration into larger cybersecurity or OSINT pipelines  
- 🚀 Easy to run and modify for custom use cases  

---

## ⚙️ Usage

1. Clone the repository  
   ```bash
   git clone https://github.com/axm1/Detector_of_digital_actives_in_blacklist.git
   cd Detector_of_digital_actives_in_blacklist
Ensure you have Python installed (e.g., Python 3.8+)

Run the script with your target asset

bash
Copiar código
python Blacklist_detector.py <asset_identifier>
Example:

bash
Copiar código
python Blacklist_detector.py example.com
The script will output whether the asset is listed in one or more blacklists and provide basic summary information.

📚 Technologies & Dependencies
Language: Python

No external dependencies listed in the repo (ensure any required modules are installed)

Simple, standalone script demonstrating asset‐reputation checking

🎯 Intended Use & Audience
This tool is aimed at:

Cybersecurity professionals performing asset-risk assessments

OSINT analysts needing quick blacklist checks

Developers who want an example of Python script integration with external blacklist services

Recruiters and hiring managers evaluating backend scripting, Python skills and cybersecurity awareness
