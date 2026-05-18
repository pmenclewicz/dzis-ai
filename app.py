import feedparser
from datetime import datetime
import time

# Lista wielu polskich źródeł RSS
ZRODLA_RSS = [
    {"nazwa": "AntyWeb", "url": "https://antyweb.pl/feed"},
    {"nazwa": "Benchmark", "url": "https://www.benchmark.pl/rss/aktualnosci.xml"},
    {"nazwa": "Chip.pl", "url": "https://www.chip.pl/feed"}
]

def pobierz_newsy():
    wszystkie_artykuly = []
    
    for zrodlo in ZRODLA_RSS:
        print(f"Pobieranie z: {zrodlo['nazwa']}...")
        try:
            feed = feedparser.parse(zrodlo['url'])
            for entry in feed.entries:
                # Próbujemy pobrać datę publikacji (w bezpieczny sposób)
                data_struktura = getattr(entry, 'published_parsed', None) or getattr(entry, 'updated_parsed', None)
                znacznik_czasu = time.mktime(data_struktura) if data_struktura else 0
                
                wszystkie_artykuly.append({
                    "tytul": entry.title,
                    "link": entry.link,
                    "zrodlo": zrodlo['nazwa'],
                    "czas": znacznik_czasu
                })
        except Exception as e:
            print(f"Błąd podczas pobierania z {zrodlo['nazwa']}: {e}")
            
    # Sortujemy wszystkie artykuły od najnowszych do najstarszych
    wszystkie_artykuly.sort(key=lambda x: x['czas'], reverse=True)
    
    # Zwracamy tylko top 12 najnowszych newsów ze wszystkich portali
    return wszystkie_artykuly[:12]

def generuj_strone(newsy):
    print("Generowanie pliku HTML...")
    lista_html = ""
    for i, item in enumerate(newsy, start=1):
        lista_html += f'''
            <li>
                <a href="{item['link']}" target="_blank" class="block group py-3 border-b border-gray-100 last:border-0">
                    <div class="flex items-start">
                        <span class="text-gray-400 font-mono text-xs mr-3 mt-1">{i:02d}.</span>
                        <div>
                            <span class="group-hover:text-black text-[#1a1a1a] text-base font-medium transition-colors duration-200">{item['tytul']}</span>
                            <span class="block text-xs text-gray-400 mt-1">źródło: {item['zrodlo']}</span>
                        </div>
                    </div>
                </a>
            </li>
        '''

    dzisiejsza_data = datetime.now().strftime("%d.%m.%Y")

    szablon = f'''<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>dzis.ai - Polski Agregator Tech</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
</head>
<body class="bg-[#fcfcfc] text-[#1a1a1a] font-sans antialiased selection:bg-black selection:text-white">
    <div class="max-w-2xl mx-auto px-6 py-16">
        <header class="mb-12 border-b border-gray-200 pb-6">
            <div class="flex justify-between items-baseline">
                <h1 class="text-3xl font-black tracking-tight text-black">dzis<span class="text-gray-400">.ai</span></h1>
                <span class="text-xs font-mono text-gray-400 bg-gray-100 px-2 py-1 rounded">{dzisiejsza_data}</span>
            </div>
            <p class="text-sm text-gray-500 mt-2 font-mono">Najważniejsze wydarzenia ze świata polskiej technologii i AI.</p>
        </header>
        <main>
            <section>
                <h2 class="text-xs font-mono uppercase tracking-wider text-gray-400 mb-4 flex items-center">
                    <span class="inline-block w-2 h-2 rounded-full bg-green-500 mr-2 animate-pulse"></span>
                    Najnowsze doniesienia po polsku
                </h2>
                <ul class="space-y-1">
                    {lista_html}
                </ul>
            </section>
        </main>
        <footer class="mt-20 pt-6 border-t border-gray-100 flex justify-between items-center text-xs text-gray-400 font-mono">
            <p>&copy; {datetime.now().year} dzis.ai</p>
            <p>Aktualizowane automatycznie</p>
        </footer>
    </div>
</body>
</html>'''

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(szablon)
    print("Strona została pomyślnie zaktualizowana (index.html)!")

if __name__ == "__main__":
    dane = pobierz_newsy()
    generuj_strone(dane)
