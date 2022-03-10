# Tewiki Asteroids and Comers
Tewiki Asteroid Bot is a Wikipedia bot that aims to generate wiki articles primarily in the celestial objects (asteroids, comets, trans-neptunian objects) domain. The bot currently focuses on articles in the Telugu language, however the system architecture is language-agnostic and can be easily extended to other languages such as Tamil, Hindi, etc. 

## Architecture
The overall system architecture is divided into three steps : 
1. **KB creation**  : An enriched domain-specific knowledge base is created as the base for the bot. The KB design and enrichment process might involve domain expertise, human annotation, crowd sourcing and/or focused crawling.
2. **KB translation** : Translation and/or transliteration of the enriched KB to required language.
3. **Template creation** : The bot depends on human-written templates to generate meaningful and grammatically correct  articles in each domain. These templates are created for every domain-language pair and integrated with the domain-specific knowledge base to generate articles. 
4. **Wiki Article Generation** : The articles are then rendered in a human-consumable format, including support for  wiki references, infoboxes,  images, tables and other domain-specific features.

## References
1. [wiki-ragas](https://github.com/nikhilpriyatam/wiki_ragas)

#tewiki #indicwiki #documentation
