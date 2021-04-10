from faker import Faker
import random


class Product:
    def __init__(self, shared_data):
        self.producer = shared_data['company']
        self.name = shared_data['name']
        self.type = shared_data['type']

    def introduce(self, unique: dict):
        print("_"*50 + f'\nAbout {self.name}\n'
              f'{self.type}\n'
              f'All rights belong to {self.producer}\n' + "_"*50
              )
        print(f'Licence number: {unique["license"][:10]}...')
        print(f'Licence owner: {unique["owner"]}')

    def __str__(self):
        return f"{self.name}.{self.producer}.All rights reserved"


class ProductDataBase:
    _flyweights = {}

    def __init__(self, states: list, uniques: dict):
        self.licenses = uniques
        for state in states:
            self._flyweights[state['name']] = Product(state)

    def get_flyweight(self, shared_state: dict):

        if shared_state['name'] not in self._flyweights:
            self._flyweights[shared_state['name']] = Product(shared_state)

        return self._flyweights[shared_state['name']]

    def list_of_products(self):
        print(f'We have {len(self._flyweights.keys())}')
        for prod in self._flyweights:
            try:
                self._flyweights[prod].introduce(unique=self.licenses[prod])
            except KeyError:
                print(f'You have no license for {prod}')


if __name__ == '__main__':
    f = Faker()

    olga = {
        'company': 'slb',
        'name': 'Olga',
        'type': 'Simulation of unsteady processes'
    }

    pipesim = {
        'company': 'slb',
        'name': 'Pipesim',
        'type': 'Simulation of steady processes'
    }

    eclipse = {
        'company': 'slb',
        'name': 'Eclipse',
        'type': 'Simulation of reservoir processes'
    }

    saphir = {
        'company': 'kappa',
        'name': 'saphir',
        'type': 'Reservoir simulation'
    }

    licenses = {
        olga['name']: {
            'owner': f.name(),
            'license': "".join([str(random.randint(0, 9)) for _ in range(100000)])
        },
        pipesim['name']: {
            'owner': f.name(),
            'license': "".join([str(random.randint(0, 9)) for _ in range(100000)])
        },
        saphir['name']: {
            'owner': f.name(),
            'license': "".join([str(random.randint(0, 9)) for _ in range(100000)])
        }
    }

    prods = ProductDataBase(states=[pipesim, olga, saphir], uniques=licenses)
    prods.list_of_products()
    print(prods.get_flyweight(eclipse))
    prods.list_of_products()
