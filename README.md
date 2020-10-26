# Webscraper
Outputs an Excel file (.xls) with current book discounts from the store https://www.medimops.de/buecher-fachbuecher-informatik-praktische-informatik-software-entwicklung-C0655742/ (incl. title, price, discount)

## Content of the repository

1. __Webscraper.py__: python script file 
    * using the modules `urllib` , the URL of the shop is accessed
    * the html is parsed using the module `BeautifulSoup`
    * price numbers and titles are extracted from the gained strings
    * the results are saved in an .xls file using the module `xlwt`, file naming is done using the module `datetime`
         
  
  
2. __Bücher-Discount   26_10_2020 13-29-07.xls__:  
    * exemplary output file (file name is date-dependant)
            
        
***


Contact m.bachmaier@posteo.de for further information.  
