import os
import sys
import datetime
import csv
import collections

films_dict = {}
shows_dict = {}
shows_cnt = collections.Counter()
shows_list = []
watched_dict = {}
watched_list = []


def process_results(prog_list):
    # -----------------------------------------------------------------------------------------------
    # Created: 20200103 by Jason Braid
    # Strip out season, episode name if applicable
    # -----------------------------------------------------------------------------------------------

    for item in prog_list:

        if item.type == 'Film':
            films_dict[item.title] = item.watched

        if item.type == 'Show':
            shows_list.append(item.title)

        watched_list.append(item.watched)


def parse_show(show, watched):
    # -----------------------------------------------------------------------------------------------
    # Created: 20200103 by Jason Braid
    # Strip out season, episode name if applicable
    # -----------------------------------------------------------------------------------------------

    NetflixShow = collections.namedtuple(
        'NetflixShow', 'type title season episode watched')

    title = 'not defined'
    type = 'not defined'
    season = 'n/a'
    episode = 'n/a'

    if show.count(':') == 0:
        #print('Film: %s' % show)
        type = 'Film'
        title = show
    elif show.count(':') == 2:
        title, season, episode = show.split(':')
        type = 'Show'
       # print(f'SERIES: {title} - {season} - {episode}')
    elif show.count(':') == 1:
        #print('Film series ?: %s' % show)
        title, episode = show.split(':')
        type = 'Film Series'
    else:
        #print('Investigate: %s' % show)
        title = show
        type = 'Other'

    return NetflixShow(type, title, season, episode, watched)


if __name__ == "__main__":

    results = []

    rowie_data = r"RowieNetflixViewingHistory.csv"
    rosie_data = r"RosieNetflixViewingHistory.csv"

    with open(rosie_data) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0

        for row in csv_reader:

            if line_count == 0:
                #print(f'Columns names are {", ".join(row)}')
                line_count += 1
            else:
                show, day = row
                results.append(parse_show(show, day))

                line_count += 1

    print(f'processed {len(results)} items.\n')
    process_results(results)

    print(f"You have watched {len(films_dict)} films")
    print(f"You have watched {len(shows_list)} shows")

    cnt = collections.Counter(shows_list)

    print("\nYour ten most popular shows are")
    for k, v in cnt.most_common(10):
        print(k, v)

    cnt = collections.Counter(watched_list)

    print("\nYour ten most viewed days were")
    for k, v in cnt.most_common(10):
        print(k, v)

    #print(datetime.datetime.now())

    sys.exit(0)
