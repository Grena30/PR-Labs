# Lab 3: Web crawling/Parsing

## Task:

### Create a function that will perform the following actions:	

*  Extract all urls from a product listing page of 999.md like this one: https://999.md/ru/list/real-estate/apartments-and-rooms

* After extracting all links from the page it should filter out the boosters.

* All extracted urls should be absolute urls.

* After extracting all urls, the function should check if there are more pages to extract urls from. Here we have 2 cases:
* 1. Case 1: If there are more pages, the function should call itself recursively for the new pagination url and pass the parsed url to the function as an argument.
* 2. Case 2: If there is no more pages to parse then return the list of parsed urls.

* Optional: To not wait for the parser to parse all pagination pages you can an additional int argument - max_page_num - it will limit the number of paged parsed by the function.

## Homework:

Create a function that takes as an argument one of urls parsed by the function above and extract the product details (for example for an apartament it would be the number of rooms, area, location etc.)
