# VerseVault
VerseVault is a flask web app that displays poems found in the 
<a href = https://github.com/thundercomb/poetrydb/blob/master/README.md>PoetryDB API </a>

My main goal for this project was to get more exprience with using APIs and web app libraries as opposed to a static webpage. 

Local storage for favorite poems has been integrated using an sqlite database, the contents of which can be accessed through the favorites menu on the main page or the button in the navbar on the other pages of the app.

A search bar has also been added for poems that returns the top five (or fewer) results for a given query. Due to how PoetryDB handles searches, not every entry is perfect, but navigation to a given poem can also be handled by searching for that particular poet and finding the link to the specified poem in the list of their works, which is organized by line length in ascending order. 