import csv
import os
import webbrowser

def creeaza_si_deschide_grafic(fisier_csv):
    nume_algoritmi = []
    valori_n = []
    date_grafic = {}

    if not os.path.exists(fisier_csv):
        print(f"Eroare: Nu gasesc fisierul {fisier_csv}. Ruleaza intai testele!")
        return

    
    with open(fisier_csv, mode='r') as f:
        lines = f.readlines()
        for line in lines[1:]: # Sarim peste header
            parts = line.strip().split(',')
            if len(parts) < 4 or parts[2] == "SKIP":
                continue
            
            
            try:
                n = int(parts[0].replace('random_', '').replace('.txt', ''))
                alg = parts[1]
                timp = float(parts[2])

                if n not in valori_n: valori_n.append(n)
                if alg not in nume_algoritmi: nume_algoritmi.append(alg)
                if alg not in date_grafic: date_grafic[alg] = {}
                date_grafic[alg][n] = timp
            except ValueError:
                continue

    valori_n.sort()
    
    
    datasets = []
    culori = ["#FF3D67", "#059BFF", "#FFC233", "#22CECE", "#9966FF", "#FB9E40"]
    
    for i, alg in enumerate(nume_algoritmi):
        puncte = [f"{{x: {n}, y: {date_grafic[alg][n]}}}" for n in valori_n if n in date_grafic[alg]]
        dataset_js = f"""{{
            label: '{alg}',
            data: [{", ".join(puncte)}],
            borderColor: '{culori[i % len(culori)]}',
            backgroundColor: '{culori[i % len(culori)]}',
            fill: false,
            borderWidth: 3
        }}"""
        datasets.append(dataset_js)

    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Grafic Performanta Sortare</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f0f2f5; padding: 40px; }}
            .container {{ background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); max-width: 1000px; margin: auto; }}
            h2 {{ text-align: center; color: #333; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Analiza Algoritmi de Sortare</h2>
            <canvas id="canvas"></canvas>
        </div>
        <script>
            new Chart(document.getElementById('canvas'), {{
                type: 'line',
                data: {{ datasets: [{", ".join(datasets)}] }},
                options: {{
                    responsive: true,
                    scales: {{
                        x: {{ 
                            type: 'logarithmic', 
                            title: {{ display: true, text: 'Numar Elemente (N) - Scara Logaritmica', font: {{ weight: 'bold' }} }} 
                        }},
                        y: {{ 
                            type: 'logarithmic', 
                            title: {{ display: true, text: 'Timp Executie (Secunde) - Scara Logaritmica', font: {{ weight: 'bold' }} }} 
                        }}
                    }},
                    plugins: {{ 
                        legend: {{ position: 'bottom' }}
                    }}
                }}
            }});
        </script>
    </body>
    </html>
    """

    
    fisier_html = os.path.abspath("grafic_final.html")
    with open(fisier_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"Succes! Graficul a fost creat.")
    print(f"Deschid automat: {fisier_html}")
    webbrowser.open(f"file://{fisier_html}")

if __name__ == "__main__":
    creeaza_si_deschide_grafic("raport_final.csv")