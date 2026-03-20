import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def minerar_aliexpress_v7(termo_busca):
    try:
        url = f"https://pt.aliexpress.com/wholesale?SearchText={termo_busca}"
        driver.get(url)
        print("Aguardando carregamento (12s)...")
        time.sleep(12)

        # Rolagem para carregar imagens (Lazy Load)
        for i in range(3):
            driver.execute_script(f"window.scrollTo(0, {i * 1000 + 500});")
            time.sleep(2)

        produtos = []
        # Localiza os links que contêm a palavra 'item' (padrão de produto do Ali)
        cards = driver.find_elements(By.XPATH, "//a[contains(@href, 'item/')]")

        for card in cards:
            try:
                texto = card.text
                if not texto or "R$" not in texto: continue # Garante que pegamos itens com preço

                link = card.get_attribute('href')
                
                # Captura de Imagem: tenta o src ou data-src
                img_tag = card.find_element(By.TAG_NAME, "img")
                img_url = img_tag.get_attribute('src') or img_tag.get_attribute('data-src')
                
                if not img_url or "blank.gif" in img_url: continue

                linhas = texto.split('\n')
                produtos.append({
                    'Título': linhas[0][:60],
                    'Preço': next((l for l in linhas if "R$" in l), "Consultar"),
                    'Imagem': img_url,
                    'Link': link
                })
            except: continue
            if len(produtos) >= 12: break
        return produtos
    finally:
        driver.quit()

# Executar e salvar
dados = minerar_aliexpress_v7("teclado mecanico gamer")
if dados:
    df = pd.DataFrame(dados)
    
    # Limpeza de Link de Imagem para garantir que funcione na Vitrine
    df['Imagem'] = df['Imagem'].str.replace('.avif', '', regex=False)
    
    # Salva com cabeçalhos claros que o gerador vai entender
    df.to_csv('produtos_minerados.csv', index=False, encoding='utf-8-sig')
    print(f"✅ SUCESSO! {len(df)} produtos prontos para a vitrine.")