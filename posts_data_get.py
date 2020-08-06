import requests
import datetime
import time
import csv
from ac_tk import tokenPers as tokenVlp
from ac_tk import group_id as group_id

def postsDataGet (group_id):
    count = 100  # количество постов, получаемых за 1 запрос
    offset = 0  # начальное смещение
    r = requests.get('https://api.vk.com/method/wall.get', params={'owner_id': group_id,
                                                                   'count': 0,
                                                                   'v': '5.103',
                                                                   'access_token': tokenVlp})
    response = r.json()
    post_count = response['response']['count']  # количество постов в группе или профиле
    print('Количество постов в сообществе:',response['response']['count'])
    print('Дата публикации', ',', 'Ссылка', ',', 'Просмотров', ',', 'Количество лайков',
          ',', 'Количество репостов', ',', 'Количество комментариев')
    while offset < post_count:
        r = requests.get('https://api.vk.com/method/wall.get',
                         params={'owner_id': group_id, 'count': count, 'v': '5.103',
                                 'access_token': tokenVlp, 'offset': offset})
        response = r.json()
        print('офсет!')
        # запускаем цикл для обработки ответа
        for i in range(100):
            post_date = datetime.datetime.fromtimestamp(  # функция преобразования
                int(response['response']['items'][i]['date'])
            ).strftime('%Y-%m-%d')  # фортма преобразования Год-Месяц Час-Минута-Секунда
            post_date_h = datetime.datetime.fromtimestamp(  # функция преобразования
                int(response['response']['items'][i]['date'])
            ).strftime('%H:%M:%S')  # фортма преобразования Год-Месяц Час-Минута-Секунда
            post_id = response['response']['items'][i]['id']  # id поста в сообществе
            group_id = response['response']['items'][i][
                'owner_id']  # id сообщества . В версиях API ниже 5.7 вместо поля owner_id приходит to_id.
            views_count = response['response']['items'][i]['views']['count']  # количество просмотров
            likes_count = response['response']['items'][i]['likes']['count']  # количество лайков
            repost_count = response['response']['items'][i]['reposts']['count']  # количество репостов
            comments_count = response['response']['items'][i]['comments']['count']  # количество комментариев
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
