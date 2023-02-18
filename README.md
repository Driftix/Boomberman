# Boomberman Guilhem Schira

## Notes de versions
- V1 : Expérimentation Websocket  :negative_squared_cross_mark:
- V2 : Mise à jour de la V1 avec rework de classes : :negative_squared_cross_mark:
- V3 : Mise à jour de la V2 avec amélioration instance client / serveur (le serveur gère beaucoup plus de trucs) :white_check_mark:
- V4 : Rework fonctionnel a 80% de la V3 suite à certaines limitations observées dans la V3 (Voir bug logs):white_check_mark:
- Version en ligne : http://guilhem-schira.fr/ <= Version en ligne mise à jour de la V3 vers la V4 

## A savoir avant de lancer :O
- La V1 ne se lancera pas correctement, cependant vous pouvez essayer la V2, V3, et V4 => à noter que la V3 est LARGEMENT recommandée car stable

## Installation des modules automatiquement :
- Lancez module.cmd pour importer les modules utilisés

## Si vous voulez installer les modules vous même :

```shell
pip install bs4
```
```shell
pip install threading
```
```shell
pip install asyncio
```
```shell
pip install bs4
```
```shell
pip install time
```
```shell
pip install random
```
```shell
pip install websockets
```
```shell
pip install secrets
```

## Une fois les dépendance ajoutées, lancez le jeu !
- D'abord le serveur web client
```shell
python -m http.server
```
- Puis le serveur python
```shell
python .\Serveur.py
```

## Les bugs qui seront surement corrigés & pense-bête
- Collision entre les joueurs qui fait qu'ils se "mangent entre eux"
- Bug d'animation concernant les explosions (Il faut que je modifie pour que ça fonctionne côté serveur cet affichage)
- Lorsqu'on récupère une nouvelle bombe via bonus, le compteur ne se met à jour qu'au moment de l'utilisation de celle-ci
- Correction des taux de spawn des bonus



