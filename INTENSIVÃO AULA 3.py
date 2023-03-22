#!/usr/bin/env python
# coding: utf-8

# # Automação Web e Busca de Informações com Python
# 
# #### Desafio: 
# 
# Trabalhamos em uma importadora e o preço dos nossos produtos é vinculado a cotação de:
# - Dólar
# - Euro
# - Ouro
# 
# Precisamos pegar na internet, de forma automática, a cotação atual desses 3 itens e saber quanto devemos cobrar pelos nossos produtos, considerando uma margem de contribuição que temos na nossa base de dados.
# 
# Base de Dados: https://drive.google.com/drive/folders/1KmAdo593nD8J9QBaZxPOG1yxHZua4Rtv?usp=sharing
# 
# Para isso, vamos criar uma automação web/web scrapping:
# 
# - Usaremos o selenium
# - Importante: baixar o webdriver

# In[ ]:


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
servico = Service(ChromeDriverManager().install())    

#cotação do dólar
web = webdriver.Chrome(service=servico)     #abrir navegador
web.get('https://www.google.com.br/')     #digitar e acessar o site google (~pyautogui.click, .write, .press)
web.find_element('xpath', '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys('cotação dólar', Keys.ENTER)     #encontrar a caixa de texto (botão direito no local, inspecionar (F12), clicar no canto superior esquerdo, clicar no local, botão direito no campo selecionado em azul, copy, copy xpath); digitar; apertar Enter   
cot_dolar = web.find_element('xpath', '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value')     #pegar a cotação: 'data-value' é a informação que preciso dentro da cotação > inspecionar (F12)
cot_dolar = float(cot_dolar)
print(f'Dólar: R$ {cot_dolar:.2f}')

#cotação do euro (repetem-se todos os códigos acima, já que são os mesmos xpaths)
web.get('https://www.google.com.br/') 
web.find_element('xpath', '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys('cotação euro')
web.find_element('xpath', '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)
cot_euro = web.find_element('xpath', '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value')
cot_euro = float(cot_euro)
print(f'Euro: R$ {cot_euro:.2f}')

#cotação do ouro (outro site)
web.get('https://www.melhorcambio.com/ouro-hoje')
cot_ouro = web.find_element('xpath', '//*[@id="comercial"]').get_attribute('value')
cot_ouro = cot_ouro.replace(',', '.')
cot_ouro = float(cot_ouro)
print(f'Ouro: R$ {cot_ouro:.2f}')

web.quit() 


# In[4]:


#2 - atualizar os preços dos produtos na base de dados
    #importar e tratar a base de dados
import pandas as pd

df = pd.read_excel('Produtos.xlsx')
display(df)
print(df.info())


# In[7]:


#atualizar a coluna Cotação
df.loc[df['Moeda'] == 'Dólar', 'Cotação'] = cot_dolar
df.loc[df['Moeda'] == 'Euro', 'Cotação'] = cot_euro
df.loc[df['Moeda'] == 'Ouro', 'Cotação'] = cot_ouro

#atualizar o preço de compra
df['Preço de Compra'] = df['Preço Original'] * df['Cotação']

#atualizar o preço de venda
df['Preço de Venda'] = df['Preço de Compra'] * df['Margem']

#tratar os valores
pd.options.display.float_format = '{:,.2f}'.format

display(df)
df.info()


# In[ ]:


#3 - exportar a base de dados atualizada
df.to_excel('Produtos.xlsx')

