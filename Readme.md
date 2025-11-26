# Mtg Tournament Api

#### Description

````
> Public api to serve data

> Connected with potsgresql on supabasePython fastapi
> Technology: Python fastapi + swagger doc
> Can be tested on docker
````

#### Api Swagger - local urls
- [http://localhost:8000/docs](http://localhost:8000/docs)
- [http://localhost:8000/redoc](http://localhost:8000/redoc)

#### Container build
````
- docker-compose build
- docker-compose up -d
````

#### execute - no docker environment
````
- uvicorn app:app
````


## MTG Stats project

#### Description

````
> All repositories used to develop mtg stats website

> Public development React website + fastapi api    + postgresql (Supabase)
> CMS development    React website + expressjs api  + postgresql (Supabase)
> Actual Data from python scrapper (mtgtop8 website + scryfall website)
> Old data (before 2022) access old database data
````

#### Api
- [https://github.com/JorgeRico/MtgTop8Api](https://github.com/JorgeRico/MtgTop8Api)
#### Front
- [https://github.com/JorgeRico/MtgTop8React](https://github.com/JorgeRico/MtgTop8React)
#### BBDD
- [https://github.com/JorgeRico/MTGTop8Database](https://github.com/JorgeRico/MTGTop8Database)
#### Backoffice API 
- [https://github.com/JorgeRico/MtgTop8-Backoffice-api](https://github.com/JorgeRico/MtgTop8-Backoffice-api)
#### Backoffice Front
- [https://github.com/JorgeRico/MtgTop8-Backoffice-front](https://github.com/JorgeRico/MtgTop8-Backoffice-front)
#### Python scrapper
- Supabase [https://github.com/JorgeRico/MtgTop8Scrapper-Supabase](https://github.com/JorgeRico/MtgTop8Scrapper-Supabase)
- Mysql (previous version, not full updated) [https://github.com/JorgeRico/MtgTop8Scrapper](https://github.com/JorgeRico/MtgTop8Scrapper)
- Access data to mysql [https://github.com/JorgeRico/MtgTop8AccessData](https://github.com/JorgeRico/MtgTop8AccessData)

#### Websites
- [https://mtg-stats.vercel.app/](https://mtg-stats.vercel.app/)
- [https://mtg-top8-backoffice-front.vercel.app/](https://mtg-top8-backoffice-front.vercel.app/)


#### References

- <https://fastapi.tiangolo.com/>
- <https://hub.docker.com/>
