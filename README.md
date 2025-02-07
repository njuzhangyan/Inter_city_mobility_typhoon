## Inter city human mobility analysis during Typhoon Bebinca of the Yangtze River Delta (YRD), China

This is a dataset for inter-city human mobility research of the 41 cities in YRD during extreme weather typhoon Bebinca. The dataset consists of cleaned and processed original data, the main analytical code, some of the results, and so on.

Author: Yan Zhang (yan_zhang@smail.nju.edu.cn), Yuwen Lu (luyw@nju.edu.cn)

## Data Description
### Inter_city_typhoon
The inter-city mobility data used in this study is drawn from the Amap platform (https://report.amap.com/migrate/page.do), which provides daily travel index of will and real at city level based on its Location Based Services (LBS). Within the YRD, China, a total of 41 cities and 1640 links are covered from 8 September to 18 September 2024. Additionally, the data of 2018 to 2023 are also collected for comparision research.

Besides, the daily weather information from CMA, daily search index of key-word 'typhoon' from Baidu, hourly typhoon Bebinca path, and yearly publicly available social-economical data from government are also collected. All the datasets are summarized in a table with city name as row name for regression analysis.

## Files
### datasets
* `migation_index_Amap_2024.csv`: Raw migration index data obtained from Amap starting from 41 cities in the YRD from 18 August to 18 September 2024, including data, startcity_code, startcity_name, endcity_code, endcity_name, willIdx, realIdx, start_X, start_Y, end_X, end_Y. 

* `real_links_2024.csv`: Daily real inter-city mobility index among 41 cities in the YRD, from 18 August to 18 September 2024, including StartID, StartCity, EndID, EndCity, typhoon, base, start_lon, start_lat, end_lon, end_lat, and day-by-day data. 

* `will_links_2024.csv`: Daily will inter-city mobility index among 41 cities in the YRD from 18 August to 18 September 2024, including StartID, StartCity, EndID, EndCity, typhoon, base, start_lon, start_lat, end_lon, end_lat, and day-by-day data.

* `real_inter_city_links_2018_2023.csv`: Real inter-city mobility index that before and after the Mid-autumn Festival among 41 cities in the YRD from 2018 to 2023. (Since the Mid-Autumn Festival is calculated according to the Chinese Lunar Calendar, the dates vary from year to year.)

* `typhoon_Bebinca_path.csv`: Hourly movement information of typhoon Bebinca with date, time, direction, typhoon level, wind speed, longitude and latitude of typhoon center point.

* `search_index.csv`: Daily search index of 'typhoon' from 41 cities with date, city, and equipments from Baidu platform. (Search Index used in this study is the search volume data published by Baidu https://index.baidu.com/v2/index.html#/ , the world's largest Chinese search engine, which allows users to customize search keywords and search source cities.)

* `weather.csv`: Daily weather with atmospheric condition, rainfall, wind speed, and temperature of 41 cities.

* `social_economic_infomation.csv`: Social and economic information that collected from year books 2023 of 41 cities. 

* `YRD_boundary.shp`: The SHP file of city boundary based on WGS_84 coordinate system. 

* `YRD_citycenter.shp`: The SHP file of city center point based on WGS_84 coordinate system. 

### codes
* `Amap_data.py`: Code for batch querying and exporting day-by-day migration indexes from the Amap platform in JSON format, the date range and cities can be set as desired.

* `resilience_degree.py`: Resilience indicators calculation process of the 'weighted degree centrality' and 'weighted clustering coefficient' of city nodes. (Other indicators such as link intensity, Modularity Index are calcalated in the Excel and the Gephi software without coding)

* `Link_plot.py`:  Ploting the figures that indicated how link-based resilience indicators changed during the typhoon event. 

* `Node_plot.py`:  Ploting the figures that indicated how node-based resilience indicators changed during the typhoon event. 

* `mul-regression.py`: Traditional regerssion and machine learning based regression with Squared R value for the choosing of models.  

* `catboost-regression.py`: Cat-Boost model based regression with parameter adjustment process, k-fold cross-validation process, shap value calculation, and shap summary plot. 

* `shap.py`: For the further visualization of shap summary diagrams, dependency diagrams, spatial distribution diagrams, etc.

##
More updates will be posed in the near future! 

Thank you for your interest. Feel free to contact us via email with any questions about data and code.
