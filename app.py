import streamlit as st
from streamlit_option_menu import option_menu
import pickle 
import pandas as pd
from textpreprocesing import DataPreprocessing
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
from nltk.tokenize import WordPunctTokenizer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import itertools
import warnings
warnings.filterwarnings("ignore")

labels = ['Neutral', 'Positif','SARA','Sindiran','Diskriminasi']
data_pilih = ['data_train_anis', 'data_train_prabowo','data_train_ganjar']

# Data training
#Anis Baswedan
data_train_anis = pd.read_csv('Data_Train/Train_Anis.csv')
data_train_anis.rename(columns={'Pornografi': 'SARA'}, inplace=True)
df = pd.read_csv("Data_Train/Tain_Anis.csv")
data_train_anis = df[['Neutral', 'Positif']].join(data_train_anis)
ambil = ['full_text','username','created_at','clean','english', 'sentimen','Neutral', 'Positif','SARA','Ancaman','Sindiran','Diskriminasi']

data_train_anis = data_train_anis[ambil]

#Ganjar Pranowo
data_train_ganjar = pd.read_csv('Data_Train/Train_Ganjar.csv')
data_train_ganjar.rename(columns={'Pornografi': 'SARA'}, inplace=True)
df = pd.read_csv("Data_Train/Tain_Ganjar.csv")
data_train_ganjar = df[['Neutral', 'Positif']].join(data_train_ganjar)
ambil = ['full_text','username','created_at','clean','english', 'sentimen','Neutral', 'Positif','SARA','Ancaman','Sindiran','Diskriminasi']

data_train_ganjar = data_train_ganjar[ambil]

#Prabowo Subianto
data_train_prabowo = pd.read_csv('Data_Train/Train_Prabowo.csv')
data_train_prabowo.rename(columns={'Pornografi': 'SARA'}, inplace=True)
df = pd.read_csv("Data_Train/Tain_Prabowo.csv")
data_train_prabowo = df[['Neutral', 'Positif']].join(data_train_prabowo)
ambil = ['full_text','username','created_at','clean','english', 'sentimen','Neutral', 'Positif','SARA','Ancaman','Sindiran','Diskriminasi']

data_train_prabowo = data_train_prabowo[ambil]



#fungsi

# Fungsi untuk menghasilkan wordcloud dari teks
def generate_wordcloud(data_train):
    selected_label = st.selectbox("Pilih Label:", labels)
    
    # Filter teks yang sesuai dengan label
    label_text = " ".join(data_train[data_train[selected_label] == 1]['clean'])

    # Membuat WordCloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(label_text)

    # Menampilkan WordCloud dengan Streamlit
    st.image(wordcloud.to_array(), use_column_width=True, caption=f'WordCloud untuk label {selected_label}.')

def display_sentiment_analysis_chart(data_train,nama):
    # Count the number of occurrences for each label
    label_counts = data_train.iloc[:, 7:].sum()

    # Create a pie chart
    plt.figure(figsize=(16, 8))
    plt.pie(label_counts, labels=label_counts.index, autopct='%1.1f%%')
    plt.title(nama)
    
    # Display the pie chart in Streamlit
    st.pyplot(plt)

    
 # Translate emoticon
emoticon_data_path = 'emoticon.txt'
emoticon_df = pd.read_csv(emoticon_data_path, sep='\t', header=None)
emoticon_dict = dict(zip(emoticon_df[0], emoticon_df[1]))

def translate_emoticon(t):
    for w, v in emoticon_dict.items():
        pattern = re.compile(re.escape(w))
        match = re.search(pattern,t)
        if match:
            t = re.sub(pattern,v,t)
    return t

def remove_newline(text):
    return re.sub('\n', ' ',text)

def remove_kaskus_formatting(text):
    text = re.sub('\[', ' [', text)
    text = re.sub('\]', '] ', text)
    text = re.sub('\[quote[^ ]*\].*?\[\/quote\]', ' ', text)
    text = re.sub('\[[^ ]*\]', ' ', text)
    text = re.sub('&quot;', ' ', text)
    return text

def remove_url(text):
    return re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))', '', text)

def remove_excessive_whitespace(text):
    return re.sub('  +', ' ', text)

def tokenize_text(text, punct=False):
    text = WordPunctTokenizer().tokenize(text)
    text = [word for word in text if punct or word.isalnum()]
    text = ' '.join(text)
    text = text.strip()
    return text

slang_words = pd.read_csv('slangword.csv')
slang_dict = dict(zip(slang_words['original'],slang_words['translated']))

def transform_slang_words(text):
    word_list = text.split()
    word_list_len = len(word_list)
    transformed_word_list = []
    i = 0
    while i < word_list_len:
        if (i + 1) < word_list_len:
            two_words = ' '.join(word_list[i:i+2])
            if two_words in slang_dict:
                transformed_word_list.append(slang_dict[two_words])
                i += 2
                continue
        transformed_word_list.append(slang_dict.get(word_list[i], word_list[i]))
        i += 1
    return ' '.join(transformed_word_list)

def remove_non_alphabet(text):
    output = re.sub('[^a-zA-Z ]+', ' ', text)
    return output

def remove_twitter_ig_formatting(text):
    text = re.sub(r'@[A-Za-z0-9]+', '', text)
    text = re.sub(r'\brt\b', '', text)
    return text

def remove_repeating_characters(text):
    return ''.join(''.join(s)[:1] for _, s in itertools.groupby(text))

stopword = pd.read_csv('stopwordbahasa.csv', header=None)
id_stopword_dict = stopword.rename(columns={0: 'stopword'})

def remove_stopword(text):
    text = ' '.join(['' if word in id_stopword_dict.stopword.values else word for word in text.split(' ')])
    text = re.sub('  +', ' ', text)
    text = text.strip()
    return text

# Buat objek stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

def preprocess_text(text):
    transformed_text = text.lower()
    transformed_text = remove_newline(text)
    transformed_text = remove_url(transformed_text)
    transformed_text = remove_twitter_ig_formatting(transformed_text)
    transformed_text = remove_kaskus_formatting(transformed_text)
    transformed_text = translate_emoticon(transformed_text)
    transformed_text = transformed_text.lower()
    transformed_text = remove_non_alphabet(transformed_text)
    transformed_text = remove_repeating_characters(transformed_text)
    transformed_text = remove_excessive_whitespace(transformed_text)
    transformed_text = tokenize_text(transformed_text)
    transformed_text = transform_slang_words(transformed_text)
    transformed_text = stemmer.stem(transformed_text)
    transformed_text = remove_stopword(transformed_text)
    transformed_text = transformed_text.lower().strip()
    return transformed_text   


# Main
def main():
    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'>Dashboard Menu</h2>", unsafe_allow_html=True)
        selected = option_menu(
            menu_title=None,  # required
            options=["Home", "Sentiment Analysis", "Sentiment Comment Detector", "About"],  # required
            icons=["house", "blockquote-left", "chat-left-text", "info-circle"],  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            styles={
                "nav-link": {
                    "font-family": "calibri",
                    "font-size": "18px" 
                },
            },
        )
    if selected == "Home":
        st.title("Sentimen Analysis Calon Presiden Indonesia 2024")
        st.image("https://akcdn.detik.net.id/community/media/visual/2023/11/24/anis-cak-imin-prabowo-gibran-ganjar-mafud-1_169.jpeg?w=700&q=90", use_column_width=True)
        st.subheader("Analisis Sentimen Calon Presiden 2024 Menggunakan Algoritma SVM Pada Media Sosial Twitter")
        st.info("Penelitian ini menggunakan data Twitter dengan kata kunci Ganjar, Anies, Prabowo, Gibran, Muhaimin, dan Mahfud. Diharapkan bahwa penelitian ini dapat memberikan wawasan yang berharga dalam memahami persepsi dan sentimen masyarakat terhadap calon presiden, serta memberikan kontribusi pada pengembangan algoritma klasifikasi sentimen yang lebih akurat. Melalui analisis ini, diharapkan kampanye dapat merespons umpan balik dari warganet untuk memperbaiki atau meningkatkan citra calon presiden.")
        st.write("Pada menu anda dapat melakukan:")
        st.write(""" 
                    - Melihat Hasil Analisis Sentimen Netizen Twiter Hasil Model SVM Pasca debat pamungkas Pilpres 2024.
                    - Memasukan kalimat kepada semua Capres dan akan diberikan apakah kalimat tersebut positif, negatif, atau netral.
                    - Mengunggah file CSV berisi komentar untuk prediksi banyak komentar sekaligus.
                """)
        st.write('Selamat menjelajahi!')

    elif selected == "Sentiment Comment Detector":
            st.title("Sentiment Comment Detector Dashboard")

            tab1, tab2 = st.tabs(["With Comment", "With CSV File"])

            with tab1:
                st.subheader("Prediksi Sentimentasi Komentar Bahasa Indonesia")
            
                # Input Komentar
                input_text = st.text_area("Silahkan Masukkan Komentar:")
                
                # Tombol prediksi
                if st.button("Prediksi Komentar"):
                    def prediksi_sentimen(df_content):
                        
                        vectorizer = pickle.load(open("vectorizer_tfidf_prabowo.pkl", "rb"))  
                        df_content = vectorizer.transform(df_content)
                        
                        svc = pickle.load(open("model_prabowo_svm.pkl", "rb"))
                        pred_sentimen = svc.predict(df_content)
                        
                        return pred_sentimen
                    # Lakukan prediksi
                    text = preprocess_text(input_text)
                    result = prediksi_sentimen([text])
                    output_sentence_neg = "Komentar tersebut <span style='font-weight:bold;color:red'>Negatif</span> "
                    output_sentence_pos = "Komentar tersebut <span style='font-weight:bold;color:green'>Positif</span> "
                    output_sentence_neu = "Komentar tersebut <span style='font-weight:bold;color:blue'>Netral</span> "
                    # Print the result
                    if result == 0:
                        st.markdown(output_sentence_neg + '.', unsafe_allow_html=True)
                    elif result == 1:
                        st.markdown(output_sentence_neu + '.', unsafe_allow_html=True)
      
                    elif result == 2:
                        st.markdown(output_sentence_pos + '.', unsafe_allow_html=True)
                

            with tab2:
                st.subheader("Prediksi Komentar Toxic Bahasa Indonesia dari File CSV")
                st.markdown('''
                        <strong>Panduan Penggunaan:</strong>
                        Silahkan masukkan komentar dalam satu kolom saja. Setiap baris akan merepresentasikan satu komentar.
                ''', unsafe_allow_html=True)

                # Upload file CSV
                uploaded_file = st.file_uploader("Upload file CSV:", type=["csv"])

                if uploaded_file is not None:
                    try:
                        # Membaca data dari file CSV dengan kolom default "Komentar"
                        df = pd.read_csv(uploaded_file)
                        # Preprocess comments
                        comment_preprocessing = DataPreprocessing(df)
                        comment_preprocessing.text_preprocessing(df.columns[0], 'output')

                        # Tombol prediksi
                        if st.button("Prediksi File CSV"):
                            # Lakukan prediksi
                            def prediksi_sentimen(df_content):
                        
                                vectorizer = pickle.load(open("vectorizer_tfidf_prabowo.pkl", "rb"))  
                                df_content = vectorizer.transform(df_content)
                                
                                svc = pickle.load(open("model_prabowo_svm.pkl", "rb"))
                                pred_sentimen = svc.predict(df_content)
                                
                                return pred_sentimen
                            # Lakukan prediksi
                            hasil_prediksi = prediksi_sentimen(df["output"])
                            df['Sentiment'] = ['Komentar Negatif' if pred == 0 else 'Komentar Neutral' if pred == 1 else 'Komentar Positif' for pred in hasil_prediksi]
                            # Tampilkan hasil prediksi pada streamlit
                            st.dataframe(pd.DataFrame({"Komentar": df["output"], "Sentiment": df['Sentiment']}))

                            

                    except Exception as e:
                        st.error(f"Terjadi kesalahan: {str(e)}")

   
    elif selected == "Sentiment Analysis":
        st.title("Toxic Comment Detector Dashboard")
        st.markdown("<h2 style='text-align: center;'>Dashboard Menu</h2>", unsafe_allow_html=True)
        selected_sentimen = option_menu(
            menu_title=None,  # required
            options=["Anis Baswedan", "Prabowo Subianto", "Ganjar Pranowo"],  # required
            icons=["house", "blockquote-left", "chat-left-text", "info-circle"],
            orientation="horizontal",# optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            styles={
                "nav-link": {
                    "font-family": "calibri",
                    "font-size": "18px" 
                },
            },
        )
        
        

        # Tampilkan wordcloud
        if selected_sentimen == "Anis Baswedan":
            
                    # Membuat kolom dengan layout 1:2
            col1, col2 = st.columns([1, 2])

            # Menampilkan foto di kolom 1
            col1.image("https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Anies_Baswedan%2C_Candidate_for_Indonesia%27s_President_in_2024.jpg/220px-Anies_Baswedan%2C_Candidate_for_Indonesia%27s_President_in_2024.jpg", use_column_width=True, output_format="JPEG", caption="Anis Baswedan")

            # Menampilkan deskripsi tentang diri di kolom 2
            col2.markdown('''<div style="text-align: justify;">Anies Rasyid Baswedan dikenal sebagai sosok yang memiliki integritas, amanah, cerdas, dan berani. Anies memiliki kemampuan membuat perubahan, inovatif, memimpin di saat krisis, dan bisa membuat kebijakan yang tepat serta cepat. Kini, Anies telah mendapatkan banyak penghargaan individu dan penghargaan saat menjabat menjadi Gubernur DKI Jakarta. Berasal dari keluarga akademisi, Anies menjadi pribadi yang sangat tekun dan semangat dalam menjalani pendidikannya. Tak hanya menuntut ilmu di negeri tercinta, Anies juga berusaha mendapatkan beasiswa agar bisa menuntut ilmu hingga ke luar negeri.\n “Mewujudkan keadilan dan kesejahteraan bagi seluruh rakyat Indonesia.”</div>''', unsafe_allow_html=True)
            
            pilih = ['Pilih','Word World', 'Pie Chart']
            selected_pilih = st.selectbox("Pilih Visualisasi Sentiment Analysis:", pilih)
            if selected_pilih == "Word World":
                st.subheader("Wordcloud Sentiment Analysis")
                generate_wordcloud(data_train_anis)
            elif selected_pilih == "Pie Chart":
                st.subheader("Bar Chart Sentiment Analysis")
                display_sentiment_analysis_chart(data_train_anis,"Sentiment Analysis Anies Baswedan")
                
                
        elif selected_sentimen  == "Prabowo Subianto":
                    # Membuat kolom dengan layout 1:2
            col1, col2 = st.columns([1, 2])

            # Menampilkan foto di kolom 1
            col1.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Prabowo_Subianto%2C_Candidate_for_Indonesia%27s_President_in_2024.jpg/220px-Prabowo_Subianto%2C_Candidate_for_Indonesia%27s_President_in_2024.jpg", use_column_width=True, output_format="JPEG", caption="Anis Baswedan")

            # Menampilkan deskripsi tentang diri di kolom 2
            col2.markdown('''<div style="text-align: justify;">Prabowo Subianto adalah politikus Indonesia yang sebelumnya berkarier sebagai prajurit TNI dan pengusaha. Saat ini, dia menduduki jabatan publik sebagai Menteri Pertahanan periode 2019-2024. Sejak didirikannya pada 2008, Prabowo juga menjabat sebagai Ketua Umum Partai Gerindra. Dirinya sempat maju sebagai calon wakil presiden pada Pilpres 2009 dan calon presiden pada Pilpres 2014 serta Pilpres 2019. Semangat patriotik dan militernya tak kunjung padam. Prabowo Subianto  seorang jenderal yang memiliki kecerdasan di atas rata-rata jenderal lainnya. Tak hanya menguasai dunia militer, tapi juga memahami dunia pergerakan, politik, dan ekonomi. Anak begawan ekonomi Soemitro dan menantu Presiden Soeharto ini, setelah pensiun dari tentara, membangun bisnis dan partai politik.”</div>''', unsafe_allow_html=True)
            
            pilih = ['Pilih','Word World', 'Pie Chart']
            selected_pilih = st.selectbox("Pilih Visualisasi Sentiment Analysis:", pilih)
            if selected_pilih == "Word World":
                st.subheader("Wordcloud Sentiment Analysis")
                generate_wordcloud(data_train_prabowo)
            elif selected_pilih == "Pie Chart":
                st.subheader("Bar Chart Sentiment Analysis")
                display_sentiment_analysis_chart(data_train_prabowo,"Sentiment Analysis Prabowo Subianto")
                
        elif selected_sentimen  == "Ganjar Pranowo":
                    # Membuat kolom dengan layout 1:2
            col1, col2 = st.columns([1, 2])

            # Menampilkan foto di kolom 1
            col1.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/Ganjar_Pranowo_Candidate_for_Indonesia%27s_President_in_2024.jpg/220px-Ganjar_Pranowo_Candidate_for_Indonesia%27s_President_in_2024.jpg", use_column_width=True, output_format="JPEG", caption="Ganjar Pranowo")

            # Menampilkan deskripsi tentang diri di kolom 2
            col2.markdown('''<div style="text-align: justify;">Ganjar Pranowo merupakan anak kelima dari pasangan Parmudji Pramudi Wiryo dan Sri Suparni, yang dikenal sebagai keluarga yang sederhana. Ayahnya seorang polisi dengan pangkat terakhir Letnan Satu, sedangkan ibunya adalah seorang ibu rumah tangga yang membantu keluarga dengan membuka warung kelontong.
                          Dengan latar belakang tersebut, Ganjar Pranowo dibesarkan dengan nilai-nilai disiplin, kebangsaan, berbagi, hidup sederhana, tidak menyerah, serta bekerja keras untuk mencapai cita citanya. Sedari kecil, Ganjar Pranowo terbiasa dengan tugas dan tanggung jawab yang diberikan oleh ayahnya dalam keluarga. Misalnya membersihkan rumah, menemani ibunya berbelanja ke pasar, hingga membantu berjualan bensin di warung.”</div>''', unsafe_allow_html=True)
            
            pilih = ['Pilih','Word World', 'Pie Chart']
            selected_pilih = st.selectbox("Pilih Visualisasi Sentiment Analysis:", pilih)
            if selected_pilih == "Word World":
                st.subheader("Wordcloud Sentiment Analysis")
                generate_wordcloud(data_train_ganjar)
            elif selected_pilih == "Pie Chart":
                st.subheader("Bar Chart Sentiment Analysis")
                display_sentiment_analysis_chart(data_train_ganjar,"Ganjar Pranowo")
                
        else:
            st.write("Data tidak tersedia")

        
        
        
        
        
        

    elif selected == "About":
        
        
        selected = option_menu(
        menu_title = None,
        options = ['About',"Education", "Skills", "Experience", "Projects"],
        icons = ['person','book-half','person-up','clipboard-data-fill','bricks'],
        orientation="horizontal"
    )
        if selected == 'About':
            
            st.title("About")
            st.write("")

            # Membuat kolom dengan layout 1:2
            col1, col2 = st.columns([1, 2])

            # Menampilkan foto di kolom 1
            col1.image("assets/foto.png", use_column_width=True)

            # Menampilkan deskripsi tentang diri di kolom 2
            col2.markdown('''<div style="text-align: justify;">I'm I Putu Ferry Wistika, a final-year Meteorology Study Program Class of 2020 at Institute Technology of Bandung who is very excited to learn. I'm passionate about technology, especially artificial intelligence, and data science. I have a strong grasp of machine learning and deep learning tools, including Python, TensorFlow, Pytorch. I'm passionate about data science with strong analytical skills, excelling in critical thinking and decision-making based on data insights.</div>''', unsafe_allow_html=True)
            col2.write("")
            col2.markdown('''
                <style>
                    .icon {
                        margin-right: 30px; /* Atur jarak kanan antara gambar */
                    }
                </style>

                <a href="https://www.linkedin.com/in/putuwistika/" class="icon">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" width="20" height="20" />
                </a>

                <a href="https://github.com/putuwistika/" class="icon">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" width="20" height="20" />
                </a>
                
                <a href="mailto:putuferrywistika@gmail.com?" class="icon">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Gmail_icon_%282020%29.svg/150px-Gmail_icon_%282020%29.svg.png" width="20" height="20" />
                </a>
                ''',
                unsafe_allow_html=True
            )
        def txt(a, b):
            col1, col2 = st.columns([4,1])
            with col1:
                st.info(a)
            with col2:
                st.info(b)
        
    if selected == 'Education':
        st.subheader("Education",divider='rainbow')
        txt('🏆 **Undergraduate of Meteorology**, *Bandung Institute Of Technology*, Jawa Barat, Indonesia ','2020 - Now')
        st.info(''' 
                :white_check_mark: The most outstanding student Institute Technology of Bandung (Mahasiswa Berprestasi Meteorlogi ITB 2022)\n
                :white_check_mark: Awards : 1st Winner of National Dharma Discourse, Awarde Ganesha Award “Ganesha Rasa”\n
                :white_check_mark: Institute Technology of Bandung Ambassador ( Duta Kampus Institut Teknologi Bandung)
                ''')
        st.divider()
        st.subheader("Courses",divider='rainbow')
        txt('🏆 **Data Science Series Fundamental Python and Algorithm**, *Bandung Institute Of Technology Career Center*, Jawa Barat, Indonesia ','10 Oct - 11 Nov 2023')
        st.info(''' 
                :white_check_mark: Basic Python training in the context of Data Science involves understanding variables, data types, control structures, and so on. The ability to manipulate and analyze data using libraries in Python is crucial. In addition to Python, a strong understanding of algorithms is also a primary focus. Algorithm training includes an understanding of time and space complexity, data structures, data analysis, and designing solutions\n
            
                ''')
        st.divider()
        st.subheader("Achievement",divider='rainbow')
        st.info(''' 
                🏆 Awarde Ganesha Award as The most outstanding student Institute Technology of Bandung (Mahasiswa Berprestasi Meteorlogi ITB 2022)\n
                🏆 Institute Technology of Bandung Ambassador ( Duta Kampus Institut Teknologi Bandung)\n
                🏆 Ambassador Of Bali Environments ( Duta Lingkungan Provinsi Bali)\n
                🏆 Bali Tabanan Tourism and Culture Ambassador ( Jegeg Bagus Tabanan)
            
                ''')
        st.divider()
    
    if selected == 'Skills':
        st.subheader("Skills",divider='rainbow')
        with st.container():
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/121px-Python-logo-notext.svg.png',width=100)
            with col2:
                st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/Adobe_Premiere_Pro_CC_icon.svg/64px-Adobe_Premiere_Pro_CC_icon.svg.png',width=100)
            with col3:
                st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/SQLite370.svg/440px-SQLite370.svg.png',width=200)
            with col3:
                st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Matlab_Logo.png/100px-Matlab_Logo.png',width=100)
            with col1:
                st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/RStudio_logo_flat.svg/183px-RStudio_logo_flat.svg.png')
            with col1:    
                st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/ArcGIS_logo.png/120px-ArcGIS_logo.png',width=130)
            with col2:
                st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Adobe_After_Effects_CC_icon.svg/64px-Adobe_After_Effects_CC_icon.svg.png',width=100)        
            
    
    if selected == 'Experience':
        st.subheader("Experience",divider='rainbow')
        txt('🏆 **CEO & Event Director** | Tirai Prada Event Organizer ','Jan 2022 - Now')
        st.info(''' 
                :white_check_mark: Motivated events coordinator with excellent interpersonal and communication skills and over 5 years of experience in the recreation industry.\n
                :white_check_mark: Articulate and talented in ensuring social interactions and events run smoothly for client satisfaction.\n
                :white_check_mark: Created engaging and thought-provoking speeches relevant to specific events
                ''')
        st.divider()
        txt('🏆 **Chief of the Bali Arts Festival, Maha Gotra Ganesha.** ','Mar 2021 - Nov 2021')
        st.info(''' 
                :white_check_mark: Maha Gotra Ganesha is a Balinese arts unit at the Bandung Institute of Technology. One of its major annual events is the National Bali Dance Festival, providing a platform for Bali dance enthusiasts to showcase their skills. 
                Beyond being a showcase of talent, this event is also intended to bring together Balinese dance artists from across Indonesia at the Technology of Arts and Sciences Campus in Bandung.
                ''')
        st.divider()
        txt('🏆 **Content Creator, Master Of Ceremony & Host** Biro Komunikasi dan Hubungan Masyarakat Institut Teknologi Bandung ','Jan 2022 - Now')
        st.info(''' 
                :white_check_mark: Become a content creator for promoting ITB campus activities\n
                :white_check_mark: Host events on campus
                ''')
        st.divider()
        txt('🏆 **Radio Announcer** *Radio Republic Of Indonesia Denpasar*','Dec 2018 - May 2021')
        st.info(''' 
                :white_check_mark: Communicated valuable information to listeners in case of emergencies and/or other matters of public interest.\n
                :white_check_mark: Interviewed theatrical personalities and created original content to deliver at scheduled intervals weeks\n 
                :white_check_mark: Collaborated with all departments to solve problems and formulate ideas to improve the company\n 
                :white_check_mark: Made sure that callers were dealt with courteously and efficiently\n 
                :white_check_mark: Appeared at local community/university/professional events representing the radio station\n 
                :white_check_mark: Producing advertising audio Voice
                ''')
        st.divider()

    if selected == 'Projects':
        st.subheader("Projects",divider='rainbow')
        txt('🏆 **Meteorological Information System Project** ','Jan 2022 - Mei 2022')
        st.info(''' 
                :white_check_mark: Succeeded in creating a meteorological information website **SIBAPA – Sistem Informasi Meteorologi Pertanian Bali Dwipa**”\n
                :white_check_mark: Developing an interactive web application using Streamlit in Python results in a responsive and dynamic interface for seamless data display. 
                This application can be employed for data visualization, statistical analysis, or even building interactive dashboards.
                ''')
        st.divider()
        txt('🏆 **Kegiatan IGT Peringatan Dini Banjir Tahun 2023** ','Agu 2023 - Dec 2023')
        st.info(''' 
                :white_check_mark: This project utilizes the Rain Perturbation Database 100 Member Ensemble, where an ensemble of 100 mathematical models is applied to the same data to generate diverse rainfall predictions. 
                The use of ensemble provides a better understanding of patterns, trends, and uncertainties associated with global rainfall forecasts.
                ''')
        st.divider()
        txt('🏆 **Climate Policy Course Assistant** ','Jan 2023 - Mei 2023')
        st.info(''' 
                :white_check_mark: Moderator in discussions on climate policy in Indonesia, the IPCC and the Paris Agreement
                :white_check_mark: Project on climate change
                ''')
        st.divider()
        txt('🏆 **Prediction of Flood Discharge in the Sub-Watershed Area of Citarik Citarum River Basin.** ','Jan 2023 - Mei 2023')
        st.info(''' 
                :white_check_mark: This report is compiled as a Collaborative Major Assignment. The task focuses on the analysis of data related to weather and climate, the implementation of numerical weather prediction methods, as well as hydrometeorological modeling. 
                It involves the use of Python and the ArcGIS hydrology model.
                ''')
        st.divider()
        txt('🏆 **"Numerical Extreme Weather Prediction"** ','Jan 2023 - Mei 2023')
        st.info(''' 
                :white_check_mark: Numerical models like WRF utilize atmospheric observational data, including air temperature, humidity, wind speed, and air pressure, to generate future weather forecasts. 
                This is achieved through the use of Python and Fortran programming languages.
                ''')
        st.divider()        
   

        

if __name__ == "__main__":
    main()

