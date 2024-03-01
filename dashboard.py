import streamlit as st 
import pandas as pd
import plotly.express as px
import numpy as np
from scipy.spatial import distance

hitung_jarak=pd.read_excel(r"data_pengukuran_jarak(2).xlsx",index_col=0)
visualisasi_data=pd.read_excel(r"data_visualisasi(4).xlsx",index_col=0)


#UPDATE LABEL GRAPH
def update_graph(tahun_terpilih):
   dff=visualisasi_data[(visualisasi_data["Tahun"]>=tahun_terpilih[0])&(visualisasi_data["Tahun"]<=tahun_terpilih[1])]
   plot=px.scatter(
   data_frame=dff,
   x="xaxis",
   y="yaxis",
   color="Label",
   hover_data=["Tahun"],
   hover_name="Kabkot",
   labels="Tahun",
   marginal_x="histogram"
   )
   plot.update_layout(coloraxis_showscale=False)
    
   return (plot)

# UPDATE KETIMPANGAN GRAPH
def perhitungan(kota_acuan,kota_terhitung,tahun):
    if kota_terhitung==[]:
        kota_terhitung=["KABUPATEN BANDUNG"]
    full=[]
    jarak=[]
    for kabkot in kota_terhitung:
        full.append(hitung_jarak[(hitung_jarak.kabkot==kabkot)&(hitung_jarak.tahun==tahun)])
    full=pd.concat(full).reset_index(drop=True).set_index("kabkot")
    for i in range(len(full)):
        kota1=np.squeeze(np.array(full.loc[full.index[i],"halase":"uhahi"]))
        kota2=np.squeeze(np.array(hitung_jarak[(hitung_jarak.kabkot==kota_acuan)&(hitung_jarak.tahun==tahun)].loc[:,"halase":"uhahi"]))
        jrk=distance.euclidean(kota1,kota2)
        jarak.append(jrk)
    jarak=pd.DataFrame(jarak,columns=[kota_acuan],index=full.index)
    jarak=pd.concat([jarak,full.label],axis=1)
    label=np.array(hitung_jarak[(hitung_jarak.kabkot==kota_acuan)&(hitung_jarak.tahun==tahun)].loc[:,"label"])[0]
    plot=px.bar(
        jarak
        ,color=jarak.index
        ,title=f"Perbandingan Jarak Ketimpangan dengan {kota_acuan} ({label})"
        ,hover_data=["label"]
    )
    # plot.update_traces(width = 0.5)
    return (plot)


# =============================================================================
# CONTAINER UNTUK TITLE HINGGA ABSTRAK
# =============================================================================
with st.container():
    st.title("Ketimpangan Wilayah Kabupaten di Jawa Barat")
    st.markdown(
        '''
        **Bintang Abelian Mahardika Wijonarko**
        
        *bintangabelianmahardikaw@gmail.com*
       ''' )
    st.header("Pendahuluan")
    st.markdown("""
            <div style="text-align: justify;">Jawa Barat merupakan salah satu provinsi di Indonesia yang terletak di sebelah barat pulau Jawa. Provinsi tersebut terletak bersebelahan dengan ibu kota negara yaitu Jakarta. 
            Lokasi geografis dari provinsi yang dekat dengan ibu kota menimbulkan pertanyaan apakah terdapat ketimpangan wilayah yang terjadi di provinsi tersebut karena ketimpangan dapat 
            terjadi dalam skala nasional atau pun lokal. Penelitian ini menilai ketimpangan wilayah dari 4 aspek antara lain Infrastruktur (Banyak Titik WiFi), Kependudukan (Usia Harapan Hidup), 
            Kemiskinan (Indeks Keparahan Kemiskinan), dan Pendidikan (Harapan Lama Sekolah). Ketimpangan tersebut dinlai melalui analisis AHP yang diklaster melalui K-Means. 
            Label yang didapatkan dari klasterisasi terdapat 8 jenis ketimpangan.</div>
            
            """,unsafe_allow_html=True)

# =============================================================================
# CONTAINER UNTUK PEMBAHASAN AHP
# =============================================================================

with st.container():
   st.header("Analisis Aspek Prioritas")
   st.markdown("""
            <div style="text-align: justify;">
            Analisis AHP dilakukan pada setiap aspek yang dianalisis antara lain Infrastruktur, Kependudukan, Kemiskinan, dan Pendidikan. Berdasarkan beberapa jurnal yang dibaca 
            dapat disimpulkan bahwa urutan aspek prioritas antara lain:
            
            1. Usia Harapan Hidup (Kependudukan)
            2. Indeks Keparahan Kemiskinan (Kemiskinan)
            3. Harapan Lama Sekolah (Pendidikan)
            4. Banyak Titik WiFi (Infrastruktur)
            
            </div>
            
            """,unsafe_allow_html=True)

# =============================================================================
# CONTAINER UNTUK GRAPH LABEL
# =============================================================================
with st.container():
    st.header("Persebaran Label Ketimpangan Wilayah Kabupaten di Jawa Barat")
    st.markdown("""
                <div style="text-align: justify;">
                Label ketimpangan yang didapatkan diurutkan berdasarkan berat matriks verbal judgment
                dan dijadikan ordinal. Label tersebut antara lain:
                    
                1. Sempurna
                2. Luar Biasa
                3. Sangat Baik
                4. Baik
                5. Cukup Baik
                6. Kurang Baik
                7. Buruk
                8. Sangat Buruk</div>
                """,unsafe_allow_html=True)
    value=st.slider("Pilih Rentang Tahun",min_value=2019,max_value=2023,value=[2019,2023],label_visibility="visible")
    plot=update_graph(value)
    st.plotly_chart(plot)
    
    
# =============================================================================
# CONTAINER UNTUK BAR CHART (JARAK PER KABUPATEN SETIAP TAHUN)
# =============================================================================
with st.container(): 
   st.header("Jarak Ketimpangan Wilayah per Kabupaten/Kota setiap Tahun")
   st.markdown("""
            <div style="text-align: justify;">Jarak ketimpangan merupakan pengukuran seberapa jauh atau dekat suatu kabupaten terukur 
            terhadap kabupaten acuan. Semakin dekat kabupaten terukur dengan kabupaten acuan maka jarak akan semakin kecil dan 
            semakin tidak timpang. Jarak ketimpangan dapat dilihat pada diagram blok di bawah.
            </div>
            """,unsafe_allow_html=True)
   tahun=st.radio("Pilih Tahun",hitung_jarak.sort_values("tahun")["tahun"].unique(),horizontal=True)
   kota_acuan=st.selectbox("Pilih Kabupaten Acuan",hitung_jarak.sort_values("kabkot")["kabkot"].unique(),placeholder="Kabupaten/Kota")
   kota_terhitung=st.multiselect("Pilih Kabupaten Terukur",hitung_jarak.sort_values("kabkot")["kabkot"].unique(),placeholder="Kabupaten/Kota")
   barchart=perhitungan(kota_acuan, kota_terhitung, tahun)
   st.plotly_chart(barchart)
   
# =============================================================================
# CONTAINER UNTUK REFERENCE
# =============================================================================
with st.container():
    st.header("Referensi")
    st.markdown("""
                1. Aprianoor, P., & Muktiali, M. (2015). KAJIAN KETIMPANGAN WILAYAH DI PROVINSI JAWA BARAT. Teknik PWK (Perencanaan Wilayah Kota), 4(4), 484-498. https://doi.org/10.14710/tpwk.2015.9809
                2. Goczek, Ł., Witkowska, E., & Witkowski, B. (2021). How Does Education Quality Affect Economic Growth?. Sustainability, 13, 6437. https://doi.org/10.3390/SU13116437.
                3. Silva-Laya, M., D’Angelo, N., Garcia, E., Zúñiga, L., & Fernández, T. (2020). Urban poverty and education. A systematic literature review. Educational Research Review, 29, 100280. https://doi.org/10.1016/J.EDUREV.2019.05.002.
                4. Mihaela Mihai, Emilia Ţiţan, Daniela Manea. (2015). Education and Poverty. Procedia Economics and Finance. https://doi.org/10.1016/S2212-5671(15)01532-4.
                5. Hegelund, E., Grønkjær, M., Osler, M., Dammeyer, J., Flensborg-Madsen, T., & Mortensen, E. (2020). The influence of educational attainment on intelligence. Intelligence, 78, 101419. https://doi.org/10.1016/j.intell.2019.101419.
                6. Oonagh O'Brien, Dr. Alexander Sumich, Dr. Eiman Kanjo, Dr. Daria Kuss. (2022). WiFi at University: A Better Balance between Education Activity and Distraction Activity Needed. Computers and Education Open. https://doi.org/10.1016/j.caeo.2021.100071.
                7. Mora-Rivera, J., & García-Mora, F. (2021). Internet access and poverty reduction: Evidence from rural and urban Mexico. Telecommunications Policy, 45, 102076. https://doi.org/10.1016/j.telpol.2020.102076.
                8. Bellmann, L., & Hübler, O. (2020). Working from home, job satisfaction and work–life balance – robust or heterogeneous links?. International Journal of Manpower. https://doi.org/10.1108/ijm-10-2019-0458.
                9. Gragnano, A., Simbula, S., & Miglioretti, M. (2020). Work–Life Balance: Weighing the Importance of Work–Family and Work–Health Balance. International Journal of Environmental Research and Public Health, 17. https://doi.org/10.3390/ijerph17030907.
                """)























