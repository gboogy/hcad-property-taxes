<!-- SHIELDS -->
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- LOGO -->
<br />
<p align="center">
  <a href="https://en.wikipedia.org/wiki/Harris_County,_Texas">
    <img src="images/hctx-logo.png" alt="Logo" width="200" height="200">
  </a>

  <h3 align="center">Harris County Property Tax Bot</h3>

  <p align="center">
    A Web Scraping Bot for Harris County, TX property taxes.
    <br />
    <a href="https://www.hctax.net/Property/Overview"><strong>Visit Harris County Tax Website »</strong></a>
    <br />
    <br />
  </p>
</p>


## Use Case
Find out how much everyone who lives on your street pays in property taxes.

## Overview
User is prompted to enter a year and street name to lookup all of the Harris County Appraisal Distirct (HCAD) account numbers from https://hcad.org.

The account numbers are then used to find property tax data from https://www.hctax.net.

The output is then saved to property_taxes.csv

### Built With
* Python
* [Selenium](https://selenium-python.readthedocs.io/)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/gilbert-hopkins
[product-screenshot]: images/screenshot.png
