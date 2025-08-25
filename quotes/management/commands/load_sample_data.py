from django.core.management.base import BaseCommand
from quotes.models import Source, Quote


class Command(BaseCommand):
    help = 'Загружает примеры цитат в базу данных'

    def handle(self, *args, **options):
        self.stdout.write('Загрузка примеров цитат...')
        
        sources_data = [
            {'name': 'Мастер и Маргарита', 'type': 'book'},
            {'name': 'Война и мир', 'type': 'book'},
            {'name': 'Преступление и наказание', 'type': 'book'},
            {'name': 'Матрица', 'type': 'movie'},
            {'name': 'Титаник', 'type': 'movie'},
            {'name': 'Форрест Гамп', 'type': 'movie'},
            {'name': 'Игра престолов', 'type': 'series'},
            {'name': 'Во все тяжкие', 'type': 'series'},
            {'name': 'Гарри Поттер', 'type': 'book'},
            {'name': 'Властелин колец', 'type': 'book'},
            {'name': 'Звездные войны', 'type': 'movie'},
            {'name': 'Назад в будущее', 'type': 'movie'},
            {'name': 'Друзья', 'type': 'series'},
            {'name': 'Теория большого взрыва', 'type': 'series'},
            {'name': 'Другое', 'type': 'other'},
        ]
        
        sources = {}
        for source_data in sources_data:
            source, created = Source.objects.get_or_create(
                name=source_data['name'],
                type=source_data['type']
            )
            sources[source_data['name']] = source
            if created:
                self.stdout.write(f'Создан источник: {source}')
        
        quotes_data = [
            {
                'text': 'Человек смертен, но это было бы еще полбеды. Плохо то, что он иногда внезапно смертен, вот в чем фокус!',
                'author': 'Воланд',
                'source_name': 'Мастер и Маргарита',
                'weight': 8
            },
            {
                'text': 'Рукописи не горят.',
                'author': 'Воланд',
                'source_name': 'Мастер и Маргарита',
                'weight': 9
            },
            {
                'text': 'Все счастливые семьи похожи друг на друга, каждая несчастливая семья несчастлива по-своему.',
                'author': 'Лев Толстой',
                'source_name': 'Война и мир',
                'weight': 7
            },
            {
                'text': 'Человек есть тайна. Ее надо разгадать, и ежели будешь ее разгадывать всю жизнь, то не говори, что потерял время.',
                'author': 'Федор Достоевский',
                'source_name': 'Преступление и наказание',
                'weight': 8
            },
            {
                'text': 'Выбирай красную таблетку или синюю таблетку.',
                'author': 'Морфеус',
                'source_name': 'Матрица',
                'weight': 9
            },
            {
                'text': 'К сожалению, никто не может сказать, что такое Матрица. Ты должен увидеть это сам.',
                'author': 'Морфеус',
                'source_name': 'Матрица',
                'weight': 7
            },
            {
                'text': 'Я никогда не сдамся, Джек!',
                'author': 'Роза',
                'source_name': 'Титаник',
                'weight': 6
            },
            {
                'text': 'Жизнь как коробка шоколадных конфет. Никогда не знаешь, что тебе попадется.',
                'author': 'Форрест Гамп',
                'source_name': 'Форрест Гамп',
                'weight': 10
            },
            {
                'text': 'Когда играешь в игру престолов, ты либо побеждаешь, либо умираешь.',
                'author': 'Серсея Ланнистер',
                'source_name': 'Игра престолов',
                'weight': 8
            },
            {
                'text': 'Я не в опасности, Скайлер. Я сам опасность.',
                'author': 'Уолтер Уайт',
                'source_name': 'Во все тяжкие',
                'weight': 9
            },
            {
                'text': 'Счастье можно найти даже в темные времена, если не забывать включать свет.',
                'author': 'Альбус Дамблдор',
                'source_name': 'Гарри Поттер',
                'weight': 9
            },
            {
                'text': 'Не все те, кто бродят, потерялись.',
                'author': 'Дж. Р. Р. Толкин',
                'source_name': 'Властелин колец',
                'weight': 8
            },
            {
                'text': 'Да пребудет с тобой Сила.',
                'author': 'Оби-Ван Кеноби',
                'source_name': 'Звездные войны',
                'weight': 10
            },
            {
                'text': 'Дороги? Куда мы идем, дороги не нужны.',
                'author': 'Доктор Эмметт Браун',
                'source_name': 'Назад в будущее',
                'weight': 7
            },
            {
                'text': 'Как дела?',
                'author': 'Джоуи Триббиани',
                'source_name': 'Друзья',
                'weight': 6
            },
            {
                'text': 'Баззанг!',
                'author': 'Шелдон Купер',
                'source_name': 'Теория большого взрыва',
                'weight': 8
            },
            {
                'text': 'Любовь побеждает все, кроме бедности и зубной боли.',
                'author': 'Мэй Уэст',
                'source_name': 'Другое',
                'weight': 7
            },
            {
                'text': 'Лучше один раз увидеть, чем сто раз услышать.',
                'author': 'Русская пословица',
                'source_name': 'Другое',
                'weight': 6
            },
            {
                'text': 'Время - деньги.',
                'author': 'Бенджамин Франклин',
                'source_name': 'Другое',
                'weight': 5
            },
            {
                'text': 'Знание - сила.',
                'author': 'Фрэнсис Бэкон',
                'source_name': 'Другое',
                'weight': 8
            },
        ]
        
        for quote_data in quotes_data:
            quote, created = Quote.objects.get_or_create(
                text=quote_data['text'],
                source=sources[quote_data['source_name']],
                defaults={
                    'author': quote_data['author'],
                    'weight': quote_data['weight']
                }
            )
            if created:
                self.stdout.write(f'Создана цитата: {quote.text[:50]}...')
        
        self.stdout.write(
            self.style.SUCCESS('Успешно загружено примеров цитат!')
        )
