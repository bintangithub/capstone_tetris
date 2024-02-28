import streamlit as st 
import pandas as pd
import plotly.express as px
import numpy as np
from scipy.spatial import distance

hitung_jarak=pd.read_excel(r"D:\Kuliah\S8\DQ Lab\Capstone\data_pengukuran_jarak(2).xlsx",index_col=0)
visualisasi_data=pd.read_excel(r"D:\Kuliah\S8\DQ Lab\Capstone\data_visualisasi(4).xlsx",index_col=0)


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
# CONTAINER UNTUK GRAPH LABEL
# =============================================================================
with st.container():
    st.title("Ketimpangan Kesejahteraan Kabupaten di Jawa Barat")
    st.header("Persebaran Label Kesejahteraan Kabupaten di Jawa Barat")
    value=st.slider("Pilih Rentang Tahun",min_value=2019,max_value=2023,value=[2019,2023],label_visibility="visible")
    plot=update_graph(value)
    st.plotly_chart(plot)
    
    
# =============================================================================
# CONTAINER UNTUK BAR CHART (JARAK PER KABUPATEN SETIAP TAHUN)
# =============================================================================
with st.container(): 
   st.header("Jarak Ketimpangan per Kabupaten/Kota setiap Tahun")
   tahun=st.radio("Pilih Tahun",hitung_jarak.sort_values("tahun")["tahun"].unique(),horizontal=True)
   kota_acuan=st.selectbox("Pilih Kabupaten Acuan",hitung_jarak.sort_values("kabkot")["kabkot"].unique(),placeholder="Kabupaten/Kota")
   kota_terhitung=st.multiselect("Pilih Kabupaten Terukur",hitung_jarak.sort_values("kabkot")["kabkot"].unique(),placeholder="Kabupaten/Kota")
   barchart=perhitungan(kota_acuan, kota_terhitung, tahun)
   st.plotly_chart(barchart)




