import streamlit as st 
import pandas as pd
import plotly.express as px
import numpy as np

hitung_jarak=pd.read_excel(r"data_pengukuran_jarak(2).xlsx",index_col=0)
visualisasi_data=pd.read_excel(r"data_visualisasi(4).xlsx",index_col=0)
ranktrix=pd.read_csv(r"rank_matrix.csv",index_col=0)
halase=pd.read_csv(r"bps-od_17052_harapan_lama_sekolah_berdasarkan_kabupatenkota_data.csv",index_col=0)
wifi=pd.read_csv(r"diskominfo-od_17306_jml_titik_layanan_akses_internet_publik_wifi__kabupate_data.csv",index_col=0)
uhahi=pd.read_csv(r"bps-od_15038_usia_harapan_hidup_berdasarkan_kabupatenkota_data.csv",index_col=0)
kemiskinan=pd.read_csv(r"bps-od_19998_indeks_keparahan_kemiskinan_berdasarkan_kabupatenkota_data.csv",index_col=0)
database=pd.read_csv(r"_select_data2019_kabupaten_data2019_wifi_as_wifi2019_data2020_wi_202402051507.csv",index_col=0)

# =============================================================================
# KUMPULAN DARI FUNGSI UNTUK KEBUTUHAN TAMPILAN DAN LAIN LAIN
# =============================================================================

def ketimpangan_kab(kabupaten,tahun):
    selected=[]
    if kabupaten==[]:
        kabupaten=["KABUPATEN BANDUNG"]
    for kab in kabupaten:
        index=ranktrix[(ranktrix.tahun==tahun)&(ranktrix.kabkot==kab)].index[0]
        df=pd.DataFrame(ranktrix[ranktrix.tahun==tahun].loc[index]).T
        selected.append(df)
    df=pd.concat(selected)
    df.rename(columns={"sum":"Nilai Wilayah","kabkot":"Kabupaten/Kota"},inplace=True)
    plot=px.bar(df,x="Kabupaten/Kota",y="Nilai Wilayah",text="Nilai Wilayah")
    plot.update_traces(textposition='inside')
    plot.update_layout(yaxis={'visible': False, 'showticklabels': False})
    return plot,df

def show_tabel(df):
    if df=="Harapan Lama Sekolah":
        st.dataframe(halase)
    elif df=="Banyak Titik WiFi":
        st.dataframe(wifi)
    elif df=="Usia Harapan Hidup":
        st.dataframe(uhahi)
    else:
        st.dataframe(kemiskinan)

def show_hist(aspek):
    col1,col2=st.columns(2)
    if aspek=="Harapan Lama Sekolah":
        hist=px.histogram(database.halase)
        st.plotly_chart(hist)
        col2.info("""
                Range dari Harapan Lama Sekolah:
                
                Range 1: 11.69 - 12.1275
                
                Range 2: 12.1276 - 12.565
                
                Range 3: 12.566 - 13.4275
                
                Range 4: 13.4276 - 14.29
                """)
        
    elif aspek=="Banyak Titik WiFi":
        hist=px.histogram(database.wifi)
        st.plotly_chart(hist)
        col2.info("""
                Range dari WiFi:
                
                Range 1: 0 - 2.5
                
                Range 2: 2.6 - 5.0
                
                Range 3: 5.1 - 11.5
                
                Range 4: 11.6 - 18.0
                """)
    elif aspek=="Usia Harapan Hidup":
        hist=px.histogram(database.uhahi)
        st.plotly_chart(hist)
        col2.info("""
                Range dari Usia Harapan Hidup:
                
                Range 1: 69.21 - 70.85
                
                Range 2: 70.86 - 72.49
                
                Range 3: 72.50 - 74.14
                
                Range 4: 74.15 - 75.79
                """)
    else:
        hist=px.histogram(database.kemiskinan)
        st.plotly_chart(hist)
        col2.info("""
                Range dari Kemiskinan:
                
                Range 1: 0.03 - 0.145
                
                Range 2: 0.146 - 0.26
                
                Range 3: 0.27 - 0.515
                
                Range 4: 0.516 - 0.77
                """)
    col1.markdown("""
                  <div style="text-align: justify;">
                  Analisis deskriptif melalui histogram menghasilkan range/rentang dari data setiap tabel
                  yang masing-masing rentang tersebut akan dinilai bobotnya sesuai dengan karakteristik 
                  data
                  
                  </div>
                  """,unsafe_allow_html=True)
                  
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
            Kemiskinan (Indeks Keparahan Kemiskinan), dan Pendidikan (Harapan Lama Sekolah). Ketimpangan tersebut dinilai melalui analisis AHP</div>
            
            """,unsafe_allow_html=True)
            
# =============================================================================
# CONTAINER UNTUK PENJELASAN LENGKAP ANALISIS AHP
# =============================================================================
with st.container():
    st.header("Analisis Analytical Hierarchy Process (AHP)")
    st.markdown("""
            <div style="text-align: justify;">
            Analisis AHP merupakan metode pengambilan keputusan yang membandingkan alternatif dari pilihan. Metode ini diterapkan untuk analisis aspek apa saja yang merupakan prioritas penyebab ketimpangan wilayah kabupaten di Jawa Barat. 
            Pada analisis ketimpangan kabupaten di Jawa Barat dilakukan terhadap aspek antara lain Infrastruktur (Banyak Titik WiFi), Kependudukan (Usia Harapan Hidup), Kemiskinan (Indeks Keparahan Kemiskinan), 
            dan Pendidikan (Harapan Lama Sekolah). Analisis ini dapat disimak melalui tahapan seperti  di bawah.
            
            </div>
            
            """,unsafe_allow_html=True)
    st.subheader("Pengumpulan Tabel")
    st.markdown("""
            <div style="text-align: justify;">
            Pengumpulan tabel dilakukan untuk mendapatkan nilai-nilai dari setiap aspek yang dianalisis. Tabel tersebut didapatkan dari Open Data Jabar secara online. Pengumpulan tabel dilakukan juga dimaksud untuk mendapatkan insight
            dari berbagai nilai yang dianalisis melalui AHP. Tabel-tabel yang dikumpulkan dapat diakses melalui link di bawah.
            
            1. [Banyak Titik Wifi](https://opendata.jabarprov.go.id/id/dataset/jumlah-titik-layanan-akses-internet-publik-wifi-berdasarkan-kabupatenkota-di-jawa-barat)
            2. [Usia Harapan Hidup](https://opendata.jabarprov.go.id/id/dataset/usia-harapan-hidup-berdasarkan-kabupatenkota-di-jawa-barat)
            3. [Kemiskinan](https://opendata.jabarprov.go.id/id/dataset/indeks-keparahan-kemiskinan-berdasarkan-kabupatenkota-di-jawa-barat)
            4. [Harapan Lama Sekolah](https://opendata.jabarprov.go.id/id/dataset/harapan-lama-sekolah-berdasarkan-kabupatenkota-di-jawa-barat)
            
            
            </div>
            
            """,unsafe_allow_html=True)
    st.markdown("""
            <div style="text-align: center;">
            TAMPILKAN TABEL YANG ANDA MAU !!
            </div>
            """,unsafe_allow_html=True)
    df=st.selectbox("Pilih Tabel",["Harapan Lama Sekolah","Banyak Titik WiFi","Usia Harapan Hidup","Tingkat Keparahan Kemiskinan"],key=0)
    show_tabel(df)
    st.subheader("Analisis Deskriptif Tabel")
    st.markdown("""
            <div style="text-align: justify;">
            Analisis deskriptif merupakan sebuah tahap yang dilakukan untuk menentukan range dari aspek melalui penilaian verbal pada analisis AHP. Analisis deskriptif dapat dilakukan
            melalui menampilkan persebaran data dari sebuah tabel yang berisi nilai dari kumpulan tabel di atas dari tahun 2019 hingga tahun 2023.
            
            </div>
            """,unsafe_allow_html=True)
    st.markdown("""
            <div style="text-align: center;"><br/>
            TAMPILKAN DISTRIBUSI TABEL YANG ANDA MAU !!</br>
            </div>
            """,unsafe_allow_html=True)
    aspek=st.selectbox("Pilih Tabel",["Harapan Lama Sekolah","Banyak Titik WiFi","Usia Harapan Hidup","Tingkat Keparahan Kemiskinan"],key=1)
    show_hist(aspek)
    st.subheader("Studi Literatur")
    st.markdown(
            """
            <div style="text-align: justify;">
            Studi literatur merupakan metode yang sangat penting untuk menentukan penentuan bobot antara aspek. Studi literatur dilakukan melalui paper-paper
            yang mengandung aspek-aspek yang diteliti serta hubungannya. Contoh: Hubungan WiFi dengan Pendidikan. Literasi yang dipilih juga akan mengandung 
            kata kunci seperti ketimpangan wilayah, wifi, kemiskinan, pendidikan, kehidupan, dan jawa barat. Literasi atau jurnal yang dipilih dapat dilihat pada 
            bagian referensi.
            </div>
            """,unsafe_allow_html=True)
    st.subheader("Menentukan Beban per Kabupaten")
    st.markdown("""
                <div style="text-align: justify;">
                Terakhir untuk menentukan ketimpangan dari masing-masing kabupaten di Jawa Barat. Beban dari masing-masing kabupaten berdasarkan analisis verbal range/rentang dan analisis verbal aspek. 
                Dua nilai analisis tersebut akan dinormalisasi sehingga didapatkan nilai aspek prioritas dari masing-masing analisis. Kemudian nilai ketimpangan akan didapatkan ketika jumlah dari hasil kali analisis
                aspek prioritas dan range/rentang didapatkan. 
                
                """,unsafe_allow_html=True)
    st.markdown("""<b/>Analisis dapat dilihat pada file excel berikut :
                [Analisis AHP](https://github.com/bintangithub/capstone_tetris/blob/46a1ced457e86773846e7a28d37e001464e5d292/Analisis%20AHP%20by%20excel.xlsx)</b>""",unsafe_allow_html=True)


# =============================================================================
# CONTAINER UNTUK ANALISIS PERSEBARAN KETIMPANGAN
# =============================================================================
with st.container():
    st.header("Persebaran Ketimpangan Wilayah per Tahun")
    std=[]
    for i in range(2019,2024):
        std.append(ranktrix[ranktrix.tahun==i].loc[:,"sum"].std())
    persebaran_ketimpangan=pd.DataFrame({"Tahun":ranktrix.sort_values("tahun")["tahun"].unique(),"Persebaran Ketimpangan":std})
    ketimpangan=px.line(persebaran_ketimpangan,x="Tahun",y="Persebaran Ketimpangan")
    ketimpangan.update_xaxes(tickvals=persebaran_ketimpangan['Tahun'], ticktext=persebaran_ketimpangan['Tahun'].astype(str))
    st.plotly_chart(ketimpangan)

# =============================================================================
# CONTAINER UNTUK ANALISIS KETIMPANGAN PER KABUPATEN PER TAHUN
# =============================================================================
with st.container():
    st.header("Perbandingan Ketimpangan Wilayah per Kabupaten per Tahun")
    tahun=st.radio("Pilih Tahun",ranktrix.sort_values("tahun")["tahun"].unique(),horizontal=True)
    kotkab=st.multiselect("Pilih Kabupaten",ranktrix.sort_values("kabkot")["kabkot"].unique(),placeholder="Kabupaten/Kota",default=["KABUPATEN BANDUNG","KOTA BANDUNG","KABUPATEN TASIKMALAYA"])
    ketimpangankab,df=ketimpangan_kab(kotkab, tahun)
    s=""
    if len(df)==1:
        s=df[df.loc[:,"Nilai Wilayah"]==df.loc[:,"Nilai Wilayah"].max()]["Kabupaten/Kota"].values[0]
    else:
        for i in df[df.loc[:,"Nilai Wilayah"]==df.loc[:,"Nilai Wilayah"].max()]["Kabupaten/Kota"].values:
            if np.where(df[df.loc[:,"Nilai Wilayah"]==df.loc[:,"Nilai Wilayah"].max()]["Kabupaten/Kota"].values==i)[0][0]==(len(df[df.loc[:,"Nilai Wilayah"]==df.loc[:,"Nilai Wilayah"].max()]["Kabupaten/Kota"].values)-1):
                s+=" " + i + "."
            else:
                s+=" " + i + ","
    st.info(
        f"""
        **TERBAIK**
        
        KABUPATEN/KOTA : {s}
        
        Nilai Wilayah : {df.loc[:,"Nilai Wilayah"].max()}
        """
        
        )
    st.plotly_chart(ketimpangankab)
    
    
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
