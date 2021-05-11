Youtube sentiment analysis
melakukan analisis sentiment terhadap 5 komentar pada video di youtube

try : https://youtubecommensentimentanalysis.herokuapp.com/

cara penggunaan :
1. copy video url youtube
2. masukan url video pada input form
3. klik 'scan'

hasil :
1. reaction positive bila polarity > 0
2. reaction negative bila polarity < 0
3. reaction neutral bila polarity = 0

cara kerja :
1. mengambil 5 komentar menggunakan youtube data api v3
2. menghapus tanda baca pada setiap komentar
3. melakukan analisis sentiment pada setiap komentar
4. menampilkan hasil analisis pada index.html




