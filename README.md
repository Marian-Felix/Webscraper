# Webscraper
Outputs an Excel file with current book discounts from medimops.de (incl. title, price, discount)

## Content of the repository

1. __Webscraper.py__: python script file 
    * using the modules `urllib` , the URL of the shop is accessed
    * the html is parsed using the module `BeautifulSoup`
    * price numbers and titles are extracted from the gained strings
    * the results are saved in an .xls file using the module `xlwt`, file naming is done using the module `datetime`
         
  
  
2. __Bücher-Discount   07_10_2020 11-39-05.xls__:  
    * exemplary output file (file name is date-dependant)
            
        
***


Contact m.bachmaier@posteo.de for further information.  
