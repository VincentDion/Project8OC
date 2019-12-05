# Project8OC

Project number 8 of the program : Python Web Developper of OpenClassrooms. Goal of this project is to create a website where users can find products of better nutritive quality. Database used is a fraction of the French Open Food Facts one (https://fr.openfoodfacts.org/)

Python version 3.5.0
Django version 2.2.5

The application can be found at the following adress : https://purbeurre-p8vd.herokuapp.com

Web ressources used in this project are listed in the legal_notice.html file in bestproduct/templates. 

To test the application, clone the repository and change the settings file with your own private key.

# Versions log

Version 0.1 (29/07/2019) :
- Creation of env
- Creation of project
- Settings add in gitignore while figuring how to hide password
- DB is created and connected
- Setting up Debug Toolbar

Version 0.2 (03/08):
- first views
- Search function added with a simple set of data (no sql yet)

Version 0.3 (05/08):
- Integration of PostGres Model (30ish products, 2 categories)
- Modification of view.detail in accordance
- Modification of view.search in accordance (search based on product name)
=> Still a little problem on list display, a list bullet appears between each item (PROBLEM SOLVED - 06/08)

Version 0.4 (06/08):
- View of replacement of product (named replace instead of search to avoid confusion)
- Ground work set for front dev initiation

Version 0.5 (11/08):
- Front dev begun, homepage, detail and replacement page are made (fex adjustments still needed)
- Back and front linked for simple queries on the limited database, working as intended when query are accepted (bad queries not handled yet)
- Change in url paths to correct a bug when filling form from homepage
- Replacement page working as intended, graphic not on point, may skip that.

Version 0.6 (27/08):
- Premice for User usage, add of register and login page and correct interface
- Add of User in database to handle inscription and favorites
- Updates of some links
- Add of 404 and 500 error page but tests are needed under production state
- Add of admin interface from where database had been filled with around 5000 products

Version 0.7 (03/09):
- User interface completed
- Pages 404 and 500 completed
- Links corrected
- Legal Notice page added and completed
- Pagination of products added (not working yet for replace view but working for favorites)
- Test suite of around 20 tests covering all the pages of the site, since it is a school project, test suite is upload to github
- Navbar is updated for when the user is connected and when he is not

=> At this point, the website is almost complete, only a few minor adjustments to make before upload on Heroku.

Version 0.8 (04/09)
- Preparation for upload
- To do list : add the settings.py file to github with os.environ + add pagination to replace functionnality + minor adjustments here and there

Version 1.0 (19/09)
- Website is now live at the following adress : https://purbeurre-p8vd.herokuapp.com
- To not overload the database nd to not copy the whole database of OpenFoodFacts, only products for few categories can be found for a total of 5000 products approx. (category : fromage à tartiner, jus d'orange, jus de pamplemousse, jus de raisin, jus de pomme, jus multifruits, cremes fraiches, biscuits apéritifs, confitures d'abricot, confitures de fruits rouges, pâte à tartiner au chocolat, beurres, huiles d'olive).

Version 1.1 (06/11)
- Preparation for the 11th project of OpenClassrooms
- DB has been changed to sqlite3 because of troubles with psycopg2 module

Version 1.2 (06/11)
- To try the application, you must fill a secret Django key in the settings.py file, as well as using the commands migrate & fill_db.
- Small fix on Login and Logout function

Version 1.3 (05/12)
- Add of new functionnality : registered user can now delete favorite products. Tests comming soon.