import requests
import datetime
import time
import csv
from ac_tk import tokenPers as tokenVlp
from ac_tk import group_id as group_id

def postsDataGet (group_id):
    count = 100  # number of Posts got through one request
    offset = 0  # first offset (there is no offset at the beginnning)
    r = requests.get('https://api.vk.com/method/wall.get', params={'owner_id': group_id,
                                                                   'count': 0,
                                                                   'v': '5.103',
                                                                   'access_token': tokenVlp})
    response = r.json()
    post_count = response['response']['count']  # number of Posts in Business group or Profile
    print('Количество постов в сообществе:',response['response']['count'])
    print('Дата публикации', ',', 'Ссылка', ',', 'Просмотров', ',', 'Количество лайков',
          ',', 'Количество репостов', ',', 'Количество комментариев')
    while offset < post_count:
        r = requests.get('https://api.vk.com/method/wall.get',
                         params={'owner_id': group_id, 'count': count, 'v': '5.103',
                                 'access_token': tokenVlp, 'offset': offset})
        response = r.json()
        print('офсет!')
        # cycle begins
        for i in range(100):
            post_date = datetime.datetime.fromtimestamp(  # time converting function
                int(response['response']['items'][i]['date'])
            ).strftime('%Y-%m-%d')  # converting in Year-Month-Day
            post_date_h = datetime.datetime.fromtimestamp(  # time converting function
                int(response['response']['items'][i]['date'])
            ).strftime('%H:%M:%S')  # converting in Hours-Minutes-Seconds
            post_id = response['response']['items'][i]['id']  # post id in community's group
            group_id = response['response']['items'][i][
                'owner_id']  # group id . If use API verion below 5.7 instead of owner_id you will receive to_id.
            views_count = response['response']['items'][i]['views']['count']  # Views numbers
            likes_count = response['response']['items'][i]['likes']['count']  # Likes numbers
            repost_count = response['response']['items'][i]['reposts']['count']  # Shares numbers
            comments_count = response['response']['items'][i]['comments']['count']  # Comments numbers
            postLink = 'https://vk.com/wall' + str(group_id) + '_' + str(post_id)
            print(post_date, ',', post_date_h, ',', postLink, ',', likes_count, ',', repost_count, ',', comments_count)

            # пишем в csv \ заменить на запись в БД
            with open('stats_posts.csv', 'a', newline='') as csvfile:
                datawriter = csv.writer(csvfile, delimiter=',',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                datawriter.writerow(
                    [post_date + ' ' + post_date_h] +
                    [postLink] + [views_count] + [likes_count] + [repost_count] + [comments_count])

        offset = offset + 100
        # time.sleep(.33)

postsDataGet (group_id)
