import os
import requests
import json
import time

class DataFetcher:
    def __init__(self, base_dir='./data'):
        self.base_dir = base_dir
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def fetch_data(self, url, category):
        data = []
        max_retries = 5
        while url and max_retries > 0:
            try:
                response = requests.get(url)
                data.extend(response.json()['results'])
                url = response.json()['next']
                max_retries = 5  # reset the retry count after a successful request
            except requests.exceptions.RequestException as e:
                print(f"Erro ao buscar dados: {e}. Tentando novamente...")
                max_retries -= 1
                time.sleep(5)
        with open(os.path.join(self.base_dir, f'{category}.json'), 'w') as f:
            json.dump(data, f)

    def read_data(self, category):
        with open(os.path.join(self.base_dir, f'{category}.json')) as f:
            return json.load(f)

    def write_data(self, category, data):
        with open(os.path.join(self.base_dir, f'{category}.json'), 'w') as f:
            json.dump(data, f)

class Main:
    def __init__(self):
        self.fetcher = DataFetcher()
        self.base_dir = self.fetcher.base_dir

    def people_with_more_than_two_starships(self, people):
        return [person for person in people if len(person['starships']) > 2]

    def most_populated_planet(self, planets):
        return max(planets, key=lambda planet: float(planet['population']) if planet['population'].isdigit() else -1)

    def people_data(self, people, starships, planets):
        people_data = []
        for person in people:
            person_data = person.copy()
            person_data['starships'] = [starship for starship in starships if starship['url'] in person['starships']]
            person_data['homeworld'] = next(planet for planet in planets if planet['url'] == person['homeworld'])
            people_data.append(person_data)
        self.fetcher.write_data('peopleData', people_data)
        return people_data

    def find_people_data(self, url):
        people_data = self.fetcher.read_data('peopleData')
        return next((people for people in people_data if people['url'] == url), None)

    def run(self):
        for category in ['people', 'planets', 'starships']:
            self.fetcher.fetch_data(f'https://swapi.dev/api/{category}/', category)

        people = self.fetcher.read_data('people')
        starships = self.fetcher.read_data('starships')
        planets = self.fetcher.read_data('planets')

        print(f'Existem {len(starships)} naves.')

        people_with_more_than_two_starships = self.people_with_more_than_two_starships(people)
        print(f'Existem {len(people_with_more_than_two_starships)} pessoas com mais de 2 naves.')

        most_populated_planet = self.most_populated_planet(planets)
        print(f'O planeta com mais população é {most_populated_planet["name"]} com {most_populated_planet["population"]} habitantes.')

        people_data = self.people_data(people, starships, planets)

        # print('Os dados de Luke Skywalker é', self.find_people_data('https://swapi.dev/api/people/1/'))

if __name__ == "__main__":
    main = Main()
    main.run()
