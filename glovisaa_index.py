from glovisa_async import GlovisaAsync
import asyncio
g = GlovisaAsync()

def main():
    all_links = g.get_all_links()
    #print(all_links)
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(g.get_data(all_links))
    except Exception as e:
        print('main function ERROR %s' % e)
if __name__ == '__main__':
    main()