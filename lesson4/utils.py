import numpy as np

def get_popularity(data):
    popularity = data.groupby('item_id')['user_id'].nunique().reset_index() / data['user_id'].nunique()
    popularity.rename(columns={'user_id': 'share_unique_users'}, inplace=True)
    

def prefilter_items(data, features, take_n_popular=None):
    # Уберем самые популярные товары (их и так купят)
    popularity = get_popularity(data)

    top_popular = popularity[popularity['share_unique_users'] > 0.5].item_id.tolist()
    data = data[~data['item_id'].isin(top_popular)]

    # Уберем самые НЕ популярные товары (их и так НЕ купят)
    top_unpopular = popularity[popularity['share_unique_users'] < 0.01].item_id.tolist()
    data = data[~data['item_id'].isin(top_unpopular)]

    # Уберем товары, которые не продавались за последние 12 месяцев
    unsale = data[data['week_no'] > 52].item_id.tolist()
    data = data[~data['item_id'].isin(unsale)]

    # Уберем не интересные для рекоммендаций категории (department)

    # Уберем слишком дешевые товары (на них не заработаем). 1 покупка из рассылок стоит 60 руб.

    # Уберем слишком дорогие товары
    if take_n_popular:
        popularity = get_popularity(data)
        top_n_popular = popularity.sort_values('share_unique_users')[:take_n_popular].item_id.tolist()
        data = data[data['item_id'].isin(top_n_popular)]

    return data


def postfilter_items(user_id, recommednations):
    pass