import pandas as pd
import os
import webbrowser

def gerar_vitrine_blindada(csv_file):
    try:
        pasta_destino = 'site_drop'
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)

        df = pd.read_csv(csv_file)
        
        # 1. HTML TOPO: CSS com Pulse e Estilo do Botão de Topo
        html_topo = """
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <script src="https://cdn.tailwindcss.com"></script>
            <style>
                body { background-color: #000; margin: 0; font-family: sans-serif; padding-top: 60px; scroll-behavior: smooth; }
                
                .countdown-bar {
                    position: fixed; top: 0; left: 0; width: 100%; background: #ff0000;
                    color: #fff; text-align: center; padding: 12px; font-weight: 900;
                    z-index: 1000; text-transform: uppercase; font-style: italic;
                    animation: pulse-red 2s infinite;
                }
                @keyframes pulse-red {
                    0% { background-color: #cc0000; box-shadow: 0 0 0px rgba(255,0,0,0); }
                    50% { background-color: #ff0000; box-shadow: 0 0 20px rgba(255,0,0,0.6); }
                    100% { background-color: #cc0000; box-shadow: 0 0 0px rgba(255,0,0,0); }
                }

                .product-card { background: #080808; border: 1px solid #1a1a1a; transition: 0.3s; position: relative; }
                .product-card:hover { border-color: #ff0000; transform: translateY(-5px); }
                .img-box { background: #fff; aspect-ratio: 1/1; display: flex; align-items: center; justify-content: center; overflow: hidden; }
                
                .btn-buy { 
                    transition: all 0.2s; width: 100px; height: 35px; 
                    display: flex; align-items: center; justify-content: center; border: 1px solid #fff; cursor: pointer;
                }
                .btn-buy:hover { background: #f00 !important; border-color: #f00 !important; color: #fff !important; transform: scale(1.1); }

                /* BOTÃO VOLTAR AO TOPO */
                #backToTop {
                    position: fixed; bottom: 30px; right: 30px; background: #ff0000;
                    color: white; border: none; border-radius: 50%; width: 50px; height: 50px;
                    font-weight: bold; cursor: pointer; display: none; z-index: 1000;
                    box-shadow: 0 0 15px rgba(255,0,0,0.5); transition: 0.3s;
                }
                #backToTop:hover { transform: scale(1.2); background: #fff; color: #f00; }

                .spark { position: fixed; width: 4px; height: 4px; background: #f00; border-radius: 50%; pointer-events: none; z-index: 999; animation: fly 0.6s ease-out forwards; }
                @keyframes fly { 0% { transform: translate(0,0) scale(1); opacity: 1; } 100% { transform: translate(var(--x), var(--y)) scale(0); opacity: 0; } }
            </style>
        </head>
        <body class="text-white p-6 md:p-12">
            <button id="backToTop" onclick="window.scrollTo(0,0)">↑</button>
            <div class="countdown-bar">A OFERTA EXPIRA EM: <span id="timer">00:00:00</span></div>
            
            <header class="text-center mb-16 mt-8">
                <h1 class="text-6xl font-black italic uppercase">TECH<span style="color:#f00">DROP</span></h1>
                <div class="h-1 w-24 bg-red-600 mx-auto mt-4"></div>
            </header>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        """

        html_cards = ""

        # 2. LOOP DE PRODUTOS
        for index, row in df.iterrows():
            titulo = str(row['Título'])[:45] + "..."
            preco = str(row['Preço']).replace('R$', '').strip()
            
            card = f"""
            <div class="product-card overflow-hidden flex flex-col group">
                <div class="img-box">
                    <img class="w-full h-full object-cover transition-transform group-hover:scale-105" src="{row['Imagem']}" onerror="this.src='https://via.placeholder.com/400';">
                </div>
                <div class="p-6 flex flex-col flex-grow">
                    <h5 class="text-sm font-bold uppercase mb-4 h-10 overflow-hidden text-zinc-100">{titulo}</h5>
                    <div class="mt-auto flex items-center justify-between border-t border-zinc-900 pt-5">
                        <span class="text-2xl font-black italic text-white">R$ {preco}</span>
                        <button onclick="createSparks(event); setTimeout(() => window.open('{row['Link']}', '_blank'), 180)" 
                                class="btn-buy bg-white text-black font-black text-[10px] uppercase italic">BUY NOW</button>
                    </div>
                </div>
            </div>
            """
            html_cards += card

        # 3. HTML RODAPÉ: Lógica JS para Scroll e Timer
        html_rodape = """
            </div>
            <script>
                function startTimer(duration, display) {
                    var timer = duration, hours, minutes, seconds;
                    setInterval(function () {
                        hours = Math.floor(timer / 3600);
                        minutes = Math.floor((timer % 3600) / 60);
                        seconds = Math.floor(timer % 60);
                        display.textContent = (hours < 10 ? "0" + hours : hours) + ":" + 
                                            (minutes < 10 ? "0" + minutes : minutes) + ":" + 
                                            (seconds < 10 ? "0" + seconds : seconds);
                        if (--timer < 0) timer = duration;
                    }, 1000);
                }

                window.onscroll = function() {
                    var btn = document.getElementById("backToTop");
                    if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
                        btn.style.display = "block";
                    } else {
                        btn.style.display = "none";
                    }
                };

                window.onload = function () { startTimer(24 * 60 * 60, document.querySelector('#timer')); };
                
                function createSparks(e) {
                    for (let i = 0; i < 20; i++) {
                        const s = document.createElement('div');
                        s.className = 'spark';
                        s.style.left = e.clientX + 'px';
                        s.style.top = e.clientY + 'px';
                        s.style.setProperty('--x', (Math.random() - 0.5) * 250 + 'px');
                        s.style.setProperty('--y', (Math.random() - 0.5) * 250 + 'px');
                        document.body.appendChild(s);
                        setTimeout(() => s.remove(), 600);
                    }
                }
            </script>
        </body>
        </html>
        """

        # Escrita final
        with open(os.path.join(pasta_destino, "index.html"), "w", encoding="utf-8") as f:
            f.write(html_topo + html_cards + html_rodape)
        
        print("✅ SUCESSO: Tudo rodando!")
        webbrowser.open('file://' + os.path.realpath(os.path.join(pasta_destino, "index.html")))

    except Exception as e:
        print(f"❌ ERRO: {e}")

gerar_vitrine_blindada('produtos_minerados.csv')