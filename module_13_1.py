import asyncio

async def start_strongman(name: str, power: int):
    print(f'Силач {name} начал соревнования')
    for i in range(5):
        await asyncio.sleep(1 / power)
        print(f'Силач {name} поднял {i + 1} шар')
    print(f'Силач {name} закончил соревнования.')

async def start_tournament():
    tasks1 = asyncio.create_task(start_strongman('Pasha', 3))
    tasks2 = asyncio.create_task(start_strongman('Denis', 4))
    tasks3 = asyncio.create_task(start_strongman('Apollon', 5))

    await tasks1
    await tasks2
    await tasks3

if __name__ == '__main__':
    asyncio.run(start_tournament())

