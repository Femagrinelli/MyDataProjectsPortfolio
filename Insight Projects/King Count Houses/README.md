# Insight Project - KC House Insights

> Status: Developing by cicles. In continuos updates  ⚠️

Esse Projeto de Insights foi desenvolvido por mim, ministrado pela Comunidade DS.

## **1.0 Business Problem**
Esse projeto busca encontrar as melhores oportunidades de adquirir (dentro do portfólio disponível) imóveis para a maximização do lucro da empresa House Rocket, através da análise de dados.
### **1.1 Business Questions**
O projeto tenta responder da melhor maneira, duas questões de negócio: 

**1)** Quais são os imóveis que a House Rocket deveria comprar ?

**2)** Uma vez a casa comprada, qual o melhor momento para vendê-las e por qual preço ?

**3)** Esse projeto também busca validar 8 hipóteses através da análise exploratória de dados:
* **H1:** Imóveis que possuem boa vista para água, são 30% mais caros, na média, dos que não possuem;
* **H2:** Imóveis com data de construção anterior a 1955, são 50% mais baratos, na média, dos que com data de contrução posterior a 1955;
* **H3:** Imóveis sem porão possuem sqrt_lot 50% maiores do que com porão;
* **H4:** O crescimento do preço dos imóveis YoY (Year over Year) é de 10%;
* **H5:** Imóveis com 3 banheiros tem um crescimento médio MoM (Month over Month) de 15%;
* **H6:** Imóveis renovados são 15% ou mais caros em relação a média total;
* **H7:** Imóveis com mais de 3 quarto são 20% ou mais caros em relação a média total;
* **H8:** Imóveis com boas condições correspondem a 30% ou mais do preço total de imóveis;

## **2.0 Solution Strategy**
Meus passos estratégicos para solucionar os problemas de negócio em questão foram:

**Step 1: Business Understanding**

**Step 2: Solution Planning**

**Step 3: Data Collect**

**Step 4: Data Description**

**Step 5: Data Cleaning and Data Transformation**

**Step 6: Exploratory Data Analysis**

A abordagem dos dados do projeto está contida no notebook.

## **3.0 Business Results**
**1 e 2) Business Questions:**
Os resultados das questões de negócio estão explícitos em dois dataframes, (1) properties_to_be_purchased.csv e (2) gain_from_sale_of_properties.csv. Nesses dataframes possuem todos os imóveis que são ideais para serem adquiridos e por quais valores poderiam ser vendidos, com o lucro disponível.

**3) Validação de Hipóteses:**

**H1: False** 
> Imóveis que possuem boa vista para água são mais 200% na média, mais caros do que os que não possuem vista para água.

**H2: False** 
> Imóveis com data de construção anterior a 1955, são menos de 1% mais baratos, na média, dos que com data de contrução posterior;

**H3: False** 
> Imóveis sem porão possuem sqrt_lot 21,75% maiores do que com porão;

**H4: False** 
> O crescimento do preço dos imóveis YoY (Year over Year) é de 0,7%;

**H5: False** 
> Imóveis com 3 banheiros tem um crescimento médio MoM (Month over Month) de 9,66%;

**H6: False** 
> Imóveis renovados são 40,92% ou mais caros em relação a média total;

**H7: True** 
> Imóveis com mais de 3 quarto são 20% ou mais caros em relação a média total;

**H8: False** 
> Imóveis com boas condições correspondem a 30% ou mais do preço total de imóveis;
### **4.0 Lessons Learned**
 * Planejamento da Solução;
 * Análise Exploratória de Dados com pandas_profiling;
 * Tratamento de Outliers;
 * Validação de Hipóteses;
 
### **5.0 Next Steps to Improve**
**Para 2º Ciclo:**
 - Integração dos Dados (ETL);
 - Criação e validação de mais hipóteses;
 - Visualização de Dados usando Streamlit;
