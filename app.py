import feedparser
from datetime import datetime

# URL kanału RSS z wiadomościami o sztucznej inteligencji / technologii
RSS_URL = "https://www.theverge.com/rss/index.xml"

def pobierz_newsy():
    print("Pobieranie najnowszych wiadomości...")
    feed = feedparser.parse(RSS_URL)
    artykuly = []
    
    # Pobieramy maksymalnie 10 najnowszych wpisów
    for entry in feed.entries[:10]:
        artykuly.append({
            "tytul": entry.title,
            "link": entry.link,
            "zrodlo": "The Verge"
        })
    return artykuly

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

    # Cały szablon strony dopasowany do stylu dzis.ai
    szablon = f'''<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>dzis.ai - Minimalistyczny Agregator AI</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
</head>
<body class="bg-[#fcfcfc] text-[#1a1a1a] font-sans antialiased selection:bg-black selection:text-white">

    <div class="max-w-2xl mx-auto px-6 py-16">
        
        <!-- Nagłówek strony -->
        <header class="mb-12 border-b border-gray-200 pb-6">
            <div class="flex justify-between items-baseline">
                <h1 class="text-3xl font-black tracking-tight text-black">dzis<span class="text-gray-400">.ai</span></h1>
                <span class="text-xs font-mono text-gray-400 bg-gray-100 px-2 py-1 rounded">{dzisiejsza_data}</span>
            </div>
            <p class="text-sm text-gray-500 mt-2 font-mono">Najważniejsze wydarzenia ze świata sztucznej inteligencji i technologii.</p>
        </header>

        <!-- Główna sekcja z treściami -->
        <main>
            <section>
                <h2 class="text-xs font-mono uppercase tracking-wider text-gray-400 mb-4 flex items-center">
                    <span class="inline-block w-2 h-2 rounded-full bg-green-500 mr-2 animate-pulse"></span>
                    Najnowsze doniesienia
                </h2>
                <ul class="space-y-1">
                    {lista_html}
                </ul>
            </section>
        </main>

        <!-- Stopka -->
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
