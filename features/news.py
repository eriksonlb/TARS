from GoogleNews import GoogleNews


def get_news(assunto):
    news = GoogleNews(period='d')
    news.setlang('pt')
    news.set_encode('utf-8')
    news.set_time_range('12/02/2021','13/02/2021')
    news.get_news(assunto)
    results = news.get_texts()
    result = results[3:8] if len(results) > 0 else "Sem notícias recentes"
    return result
    